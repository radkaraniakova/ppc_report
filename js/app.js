/**
 * app.js — PulseMetrics SPA Controller
 * Wires together DB, Charts, Tables and handles navigation/filters/export.
 */

const app = (() => {

  // ── State ──────────────────────────────────────────────────────────────────
  let state = {
    client:    'acme',
    section:   'overview',
    platform:  'all',
    dateRange: '7d',
    annotations: [],
  };

  let _fpInstance = null;

  // ── Helpers ────────────────────────────────────────────────────────────────
  const content    = () => document.getElementById('content');
  const pageTitle  = () => document.getElementById('page-title');
  const alertsBar  = () => document.getElementById('alerts-bar');
  const alertText  = () => document.getElementById('alert-text');

  const setActive = (navSection) => {
    document.querySelectorAll('.nav-item').forEach(el => {
      el.classList.toggle('active', el.dataset.section === navSection);
    });
  };

  // ── Public: setClient ──────────────────────────────────────────────────────
  const setClient = (val) => {
    state.client = val;
    render();
  };

  // ── Public: setFilter ──────────────────────────────────────────────────────
  const setFilter = (key, val) => {
    state[key] = val;
    render();
  };

  // ── Public: setDateRange ───────────────────────────────────────────────────
  const setDateRange = (range) => {
    state.dateRange = range;
    // Hide custom picker if not custom
    document.getElementById('custom-date-wrapper').classList.toggle('hidden', range !== 'custom');
    // Highlight active quick btn
    document.querySelectorAll('.dq-btn').forEach(b =>
      b.classList.toggle('active', b.dataset.range === range)
    );
    render();
  };

  // ── Public: openCustomDatePicker ───────────────────────────────────────────
  const openCustomDatePicker = () => {
    document.getElementById('custom-date-wrapper').classList.remove('hidden');
    document.querySelectorAll('.dq-btn').forEach(b =>
      b.classList.toggle('active', b.dataset.range === 'custom')
    );
    if (!_fpInstance) {
      _fpInstance = flatpickr('#custom-date-range', {
        mode: 'range',
        dateFormat: 'Y-m-d',
        onChange: (dates) => {
          if (dates.length === 2) {
            state.dateRange = 'custom';
            render();
          }
        },
      });
    }
    _fpInstance.open();
  };

  // ── Public: navigate ──────────────────────────────────────────────────────
  const navigate = (section) => {
    state.section = section;
    render();
  };

  // ── Public: exportCSV ─────────────────────────────────────────────────────
  const exportCSV = () => {
    let rows = [];
    const { client, dateRange, platform, section } = state;

    if (section === 'campaigns') {
      const data = DB.getCampaigns(client, dateRange, platform);
      rows = [['Campaign','Platform','Status','Spend','Impressions','Clicks','CTR','CPC','Conversions','CPA','Revenue','ROAS']];
      data.forEach(c => rows.push([c.name, c.platform, c.status,
        c.spend.toFixed(2), c.impressions, c.clicks, c.ctr.toFixed(2),
        c.cpc.toFixed(2), c.conversions, c.cpa.toFixed(2), c.revenue.toFixed(2), c.roas.toFixed(2)]));
    } else if (section === 'keywords') {
      const data = DB.getKeywords(client, dateRange);
      rows = [['Keyword','Match Type','Spend','Impressions','Clicks','CTR','CPC','Conv.','CPA','ROAS']];
      data.forEach(k => rows.push([k.keyword, k.matchType,
        k.spend.toFixed(2), k.impressions, k.clicks, k.ctr.toFixed(2),
        k.cpc.toFixed(2), k.conversions, k.cpa.toFixed(2), k.roas.toFixed(2)]));
    } else {
      const totals = DB.getOverviewTotals(client, dateRange, platform);
      rows = [['Metric','Value'],
        ['Spend', totals.spend.toFixed(2)],
        ['Clicks', totals.clicks],
        ['Conversions', totals.conversions],
        ['Revenue', totals.revenue.toFixed(2)],
        ['ROAS', totals.roas.toFixed(2)],
        ['CPC', totals.cpc.toFixed(2)],
        ['CPA', totals.cpa.toFixed(2)],
        ['CTR', totals.ctr.toFixed(2)],
      ];
    }

    const csv = rows.map(r => r.map(v => `"${v}"`).join(',')).join('\n');
    const blob = new Blob([csv], { type: 'text/csv' });
    const url  = URL.createObjectURL(blob);
    const a    = document.createElement('a');
    a.href = url;
    a.download = `pulsemetrics_${section}_${dateRange}.csv`;
    a.click();
    URL.revokeObjectURL(url);
  };

  // ── Alerts ─────────────────────────────────────────────────────────────────
  const showAlerts = (totals) => {
    const alerts = DB.getAlerts(state.client, totals);
    if (alerts.length === 0) {
      alertsBar().classList.add('hidden');
      return;
    }
    alertText().textContent = alerts.map(a => a.msg).join('  ·  ');
    alertsBar().classList.remove('hidden');
  };

  // ── Annotation Modal ───────────────────────────────────────────────────────
  const openAnnotationModal = () => {
    document.getElementById('annotation-modal').classList.remove('hidden');
  };

  const closeAnnotationModal = () => {
    document.getElementById('annotation-modal').classList.add('hidden');
  };

  const saveAnnotation = () => {
    const date = document.getElementById('annotation-date').value.trim();
    const note = document.getElementById('annotation-note').value.trim();
    if (!date || !note) return;
    state.annotations.push({ date, note });
    closeAnnotationModal();
  };

  // ── Section Renderers ──────────────────────────────────────────────────────

  // ─ Overview ─
  const renderOverview = () => {
    const { client, dateRange, platform } = state;
    const totals   = DB.getOverviewTotals(client, dateRange, platform);
    const trend    = DB.getTrend(client, dateRange, platform);
    showAlerts(totals);

    const delta = (val, lowerIsBetter = false) => {
      if (val === undefined) return '';
      const good = lowerIsBetter ? val < 0 : val > 0;
      const cls  = good ? 'delta-up' : 'delta-down';
      const sign = val > 0 ? '+' : '';
      return `<span class="${cls}">${sign}${val.toFixed(1)}%</span>`;
    };

    const scorecards = [
      { label: 'Total Spend',       val: DB.currency(totals.spend),       deltaKey: 'spend',       lowerIsBetter: false },
      { label: 'Conversions',       val: DB.fmtNum(totals.conversions),   deltaKey: 'conversions', lowerIsBetter: false },
      { label: 'Revenue',           val: DB.currency(totals.revenue),     deltaKey: 'revenue',     lowerIsBetter: false },
      { label: 'ROAS',              val: totals.roas.toFixed(2) + 'x',   deltaKey: 'roas',        lowerIsBetter: false },
      { label: 'Avg CPC',           val: DB.currency(totals.cpc),         deltaKey: 'cpc',         lowerIsBetter: true  },
      { label: 'CTR',               val: totals.ctr.toFixed(2) + '%',    deltaKey: 'ctr',         lowerIsBetter: false },
    ];

    const scoreHTML = scorecards.map(s => `
      <div class="scorecard">
        <div class="scorecard-label">${s.label}</div>
        <div class="scorecard-value">${s.val}</div>
        <div class="scorecard-delta">${delta(totals.delta?.[s.deltaKey], s.lowerIsBetter)} vs prior period</div>
      </div>`).join('');

    content().innerHTML = `
      <div class="scorecards">${scoreHTML}</div>

      <div class="chart-row">
        <div class="chart-card chart-card--lg">
          <div class="chart-card-header">
            <span class="chart-title">Spend · Revenue · Conversions Trend</span>
            <div class="chart-legend">
              <span class="legend-dot" style="background:#4f8ef7"></span>Spend
              <span class="legend-dot" style="background:#fbbf24"></span>Revenue
              <span class="legend-dot" style="background:#34d399"></span>Conv.
            </div>
          </div>
          <div class="chart-wrap"><canvas id="chart-trend"></canvas></div>
        </div>
        <div class="chart-card">
          <div class="chart-card-header"><span class="chart-title">ROAS Trend</span></div>
          <div class="chart-wrap"><canvas id="chart-roas"></canvas></div>
        </div>
      </div>

      <div class="chart-row">
        <div class="chart-card">
          <div class="chart-card-header"><span class="chart-title">Platform Comparison</span></div>
          <div class="chart-wrap"><canvas id="chart-platform-bar"></canvas></div>
        </div>
        <div class="chart-card">
          <div class="chart-card-header"><span class="chart-title">Spend Share by Platform</span></div>
          <div class="chart-wrap chart-wrap--donut"><canvas id="chart-spend-donut"></canvas></div>
        </div>
      </div>

      <div class="annotation-bar">
        <button class="btn-annotate" onclick="app.openAnnotationModal()">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 5v14M5 12h14"/></svg>
          Add Annotation
        </button>
        ${state.annotations.length > 0 ? `
          <div class="annotations-list">
            ${state.annotations.map(a => `<span class="annotation-chip"><strong>${a.date}:</strong> ${a.note}</span>`).join('')}
          </div>` : ''}
      </div>
    `;

    // Render charts after DOM is ready
    requestAnimationFrame(() => {
      Charts.renderTrendChart('chart-trend', trend);
      Charts.renderRoasChart('chart-roas', trend);
      Charts.renderPlatformBar('chart-platform-bar', totals.platformBreakdown);
      Charts.renderSpendDonut('chart-spend-donut', totals.platformBreakdown);
    });
  };

  // ─ Campaigns ─
  const renderCampaigns = () => {
    const { client, dateRange, platform } = state;
    const data = DB.getCampaigns(client, dateRange, platform);
    const trend = DB.getTrend(client, dateRange, platform);
    content().innerHTML = `
      <div class="chart-row">
        <div class="chart-card chart-card--lg">
          <div class="chart-card-header">
            <span class="chart-title">Spend by Platform — Trend</span>
            <div class="chart-legend">
              <span class="legend-dot" style="background:#4285f4"></span>Google
              <span class="legend-dot" style="background:#5b92f5"></span>Meta
              <span class="legend-dot" style="background:#ff6699"></span>TikTok
            </div>
          </div>
          <div class="chart-wrap"><canvas id="chart-campaigns-trend"></canvas></div>
        </div>
      </div>
      <div id="campaigns-table-container"></div>
    `;
    requestAnimationFrame(() => {
      Charts.renderMultiPlatformTrend('chart-campaigns-trend', trend, 'spend');
      Tables.renderCampaigns(data, document.getElementById('campaigns-table-container'));
    });
  };

  // ─ Ad Sets ─
  const renderAdSets = () => {
    const { client, dateRange, platform } = state;
    const data = DB.getAdSets(client, dateRange, platform);
    content().innerHTML = `<div id="adsets-table-container"></div>`;
    requestAnimationFrame(() => {
      Tables.renderAdSets(data, document.getElementById('adsets-table-container'));
    });
  };

  // ─ Ads ─
  const renderAds = () => {
    const { client, dateRange, platform } = state;
    const data = DB.getAds(client, dateRange, platform);
    content().innerHTML = `<div id="ads-table-container"></div>`;
    requestAnimationFrame(() => {
      Tables.renderAds(data, document.getElementById('ads-table-container'));
    });
  };

  // ─ Keywords ─
  const renderKeywords = () => {
    const { client, dateRange } = state;
    const data = DB.getKeywords(client, dateRange);
    const trend = DB.getTrend(client, dateRange, 'google');
    content().innerHTML = `
      <div class="chart-row">
        <div class="chart-card chart-card--lg">
          <div class="chart-card-header"><span class="chart-title">Google Ads — Clicks &amp; Conversions Trend</span></div>
          <div class="chart-wrap"><canvas id="chart-kw-trend"></canvas></div>
        </div>
      </div>
      <div id="kw-table-container"></div>
    `;
    requestAnimationFrame(() => {
      Charts.renderMultiPlatformTrend('chart-kw-trend', trend, 'spend');
      Tables.renderKeywords(data, document.getElementById('kw-table-container'));
    });
  };

  // ─ Audiences ─
  const renderAudiences = () => {
    const { client, dateRange, platform } = state;
    const data = DB.getAudiences(client, dateRange, platform);
    content().innerHTML = `<div id="audiences-table-container"></div>`;
    requestAnimationFrame(() => {
      Tables.renderAudiences(data, document.getElementById('audiences-table-container'));
    });
  };

  // ─ Products ─
  const renderProducts = () => {
    const { client, dateRange, platform } = state;
    const data = DB.getProducts(client, dateRange, platform);
    content().innerHTML = `<div id="products-table-container"></div>`;
    requestAnimationFrame(() => {
      Tables.renderProducts(data, document.getElementById('products-table-container'));
    });
  };

  // ── Master Render ──────────────────────────────────────────────────────────
  const render = () => {
    const { section } = state;
    setActive(section);

    const titles = {
      overview:  'Overview',
      campaigns: 'Campaigns',
      adsets:    'Ad Sets / Ad Groups',
      ads:       'Ads',
      keywords:  'Keywords',
      audiences: 'Audiences',
      products:  'Products',
    };
    pageTitle().textContent = titles[section] || 'Overview';

    switch (section) {
      case 'campaigns': renderCampaigns(); break;
      case 'adsets':    renderAdSets();    break;
      case 'ads':       renderAds();       break;
      case 'keywords':  renderKeywords();  break;
      case 'audiences': renderAudiences(); break;
      case 'products':  renderProducts();  break;
      default:          renderOverview();
    }
  };

  // ── Init ──────────────────────────────────────────────────────────────────
  document.addEventListener('DOMContentLoaded', () => {
    render();
  });

  return {
    setClient,
    setFilter,
    setDateRange,
    openCustomDatePicker,
    navigate,
    exportCSV,
    openAnnotationModal,
    closeAnnotationModal,
    saveAnnotation,
  };

})();
