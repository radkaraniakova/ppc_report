/**
 * tables.js — Data table rendering helpers
 */

const Tables = (() => {

  const fmt = {
    spend:   v => '$' + (+v).toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 }),
    num:     v => (+v).toLocaleString('en-US'),
    pct:     v => (+v).toFixed(2) + '%',
    roas:    v => (+v).toFixed(2) + 'x',
    cpc:     v => '$' + (+v).toFixed(2),
    cpa:     v => '$' + (+v).toFixed(2),
    revenue: v => '$' + (+v).toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 }),
  };

  const platformChip = (p) => `<span class="chip ${p}">${DB.PLATFORM_LABELS[p] || p}</span>`;
  const statusChip = (s) => `<span class="chip ${s === 'active' ? 'active' : 'paused'}">${s}</span>`;
  const deltaCell = (val, isLower = false) => {
    if (val === undefined || val === null) return '<td class="num">—</td>';
    const good = isLower ? val < 0 : val > 0;
    const cls = good ? 'delta-up' : 'delta-down';
    const sign = val > 0 ? '+' : '';
    return `<td class="num ${cls}">${sign}${val.toFixed(1)}%</td>`;
  };

  // ── Campaigns ─────────────────────────────────────────────────────────────
  const renderCampaigns = (data, container) => {
    const rows = data.map(c => `
      <tr>
        <td class="name">${c.name}</td>
        <td>${platformChip(c.platform)}</td>
        <td>${statusChip(c.status)}</td>
        <td class="num">${fmt.spend(c.spend)}</td>
        <td class="num">${fmt.num(c.impressions)}</td>
        <td class="num">${fmt.num(c.clicks)}</td>
        <td class="num">${fmt.pct(c.ctr)}</td>
        <td class="num">${fmt.cpc(c.cpc)}</td>
        <td class="num">${fmt.num(c.conversions)}</td>
        <td class="num">${fmt.cpa(c.cpa)}</td>
        <td class="num">${fmt.revenue(c.revenue)}</td>
        <td class="num">${fmt.roas(c.roas)}</td>
      </tr>`).join('');

    container.innerHTML = `
      <div class="table-card">
        <div class="table-card-header">
          <span class="table-card-title">Campaign Performance</span>
          <div class="table-card-actions">
            <div class="search-input-wrap">
              <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35"/></svg>
              <input type="text" class="search-input" placeholder="Search campaigns..." oninput="Tables.filterTable(this, 'campaign-table')" />
            </div>
          </div>
        </div>
        <div style="overflow-x:auto">
          <table class="data-table" id="campaign-table">
            <thead>
              <tr>
                <th onclick="Tables.sortTable('campaign-table',0)">Campaign <span class="sort-icon">↕</span></th>
                <th onclick="Tables.sortTable('campaign-table',1)">Platform <span class="sort-icon">↕</span></th>
                <th onclick="Tables.sortTable('campaign-table',2)">Status <span class="sort-icon">↕</span></th>
                <th class="num" onclick="Tables.sortTable('campaign-table',3)">Spend <span class="sort-icon">↕</span></th>
                <th class="num" onclick="Tables.sortTable('campaign-table',4)">Impressions <span class="sort-icon">↕</span></th>
                <th class="num" onclick="Tables.sortTable('campaign-table',5)">Clicks <span class="sort-icon">↕</span></th>
                <th class="num" onclick="Tables.sortTable('campaign-table',6)">CTR <span class="sort-icon">↕</span></th>
                <th class="num" onclick="Tables.sortTable('campaign-table',7)">CPC <span class="sort-icon">↕</span></th>
                <th class="num" onclick="Tables.sortTable('campaign-table',8)">Conv. <span class="sort-icon">↕</span></th>
                <th class="num" onclick="Tables.sortTable('campaign-table',9)">CPA <span class="sort-icon">↕</span></th>
                <th class="num" onclick="Tables.sortTable('campaign-table',10)">Revenue <span class="sort-icon">↕</span></th>
                <th class="num" onclick="Tables.sortTable('campaign-table',11)">ROAS <span class="sort-icon">↕</span></th>
              </tr>
            </thead>
            <tbody>${rows}</tbody>
          </table>
        </div>
      </div>`;
  };

  // ── Ad Sets ───────────────────────────────────────────────────────────────
  const renderAdSets = (data, container) => {
    const rows = data.map(a => `
      <tr>
        <td class="name">${a.name}</td>
        <td>${platformChip(a.platform)}</td>
        <td class="num">${fmt.spend(a.budget)}/day</td>
        <td class="num">${fmt.spend(a.spend)}</td>
        <td class="num">${fmt.num(a.impressions)}</td>
        <td class="num">${fmt.num(a.clicks)}</td>
        <td class="num">${fmt.pct(a.ctr)}</td>
        <td class="num">${fmt.num(a.conversions)}</td>
        <td class="num">${fmt.cpa(a.cpa)}</td>
        <td class="num">${fmt.roas(a.roas)}</td>
      </tr>`).join('');

    container.innerHTML = `
      <div class="table-card">
        <div class="table-card-header">
          <span class="table-card-title">Ad Sets / Ad Groups</span>
        </div>
        <div style="overflow-x:auto">
          <table class="data-table" id="adsets-table">
            <thead>
              <tr>
                <th onclick="Tables.sortTable('adsets-table',0)">Ad Set <span class="sort-icon">↕</span></th>
                <th onclick="Tables.sortTable('adsets-table',1)">Platform <span class="sort-icon">↕</span></th>
                <th class="num" onclick="Tables.sortTable('adsets-table',2)">Daily Budget <span class="sort-icon">↕</span></th>
                <th class="num" onclick="Tables.sortTable('adsets-table',3)">Spend <span class="sort-icon">↕</span></th>
                <th class="num" onclick="Tables.sortTable('adsets-table',4)">Impressions <span class="sort-icon">↕</span></th>
                <th class="num" onclick="Tables.sortTable('adsets-table',5)">Clicks <span class="sort-icon">↕</span></th>
                <th class="num" onclick="Tables.sortTable('adsets-table',6)">CTR <span class="sort-icon">↕</span></th>
                <th class="num" onclick="Tables.sortTable('adsets-table',7)">Conv. <span class="sort-icon">↕</span></th>
                <th class="num" onclick="Tables.sortTable('adsets-table',8)">CPA <span class="sort-icon">↕</span></th>
                <th class="num" onclick="Tables.sortTable('adsets-table',9)">ROAS <span class="sort-icon">↕</span></th>
              </tr>
            </thead>
            <tbody>${rows}</tbody>
          </table>
        </div>
      </div>`;
  };

  // ── Ads ───────────────────────────────────────────────────────────────────
  const renderAds = (data, container) => {
    const rows = data.map(a => `
      <tr>
        <td class="name">${a.name}</td>
        <td>${platformChip(a.platform)}</td>
        <td><span class="chip active">${a.format}</span></td>
        <td class="num">${fmt.spend(a.spend)}</td>
        <td class="num">${fmt.num(a.impressions)}</td>
        <td class="num">${fmt.num(a.clicks)}</td>
        <td class="num">${fmt.pct(a.ctr)}</td>
        <td class="num">${fmt.num(a.conversions)}</td>
        <td class="num">${fmt.cpa(a.cpa)}</td>
        <td class="num">${fmt.roas(a.roas)}</td>
      </tr>`).join('');

    container.innerHTML = `
      <div class="table-card">
        <div class="table-card-header">
          <span class="table-card-title">Ads Performance</span>
          <div class="table-card-actions">
            <div class="search-input-wrap">
              <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35"/></svg>
              <input type="text" class="search-input" placeholder="Search ads..." oninput="Tables.filterTable(this, 'ads-table')" />
            </div>
          </div>
        </div>
        <div style="overflow-x:auto">
          <table class="data-table" id="ads-table">
            <thead>
              <tr>
                <th onclick="Tables.sortTable('ads-table',0)">Ad Name <span class="sort-icon">↕</span></th>
                <th onclick="Tables.sortTable('ads-table',1)">Platform <span class="sort-icon">↕</span></th>
                <th onclick="Tables.sortTable('ads-table',2)">Format <span class="sort-icon">↕</span></th>
                <th class="num" onclick="Tables.sortTable('ads-table',3)">Spend <span class="sort-icon">↕</span></th>
                <th class="num" onclick="Tables.sortTable('ads-table',4)">Impressions <span class="sort-icon">↕</span></th>
                <th class="num" onclick="Tables.sortTable('ads-table',5)">Clicks <span class="sort-icon">↕</span></th>
                <th class="num" onclick="Tables.sortTable('ads-table',6)">CTR <span class="sort-icon">↕</span></th>
                <th class="num" onclick="Tables.sortTable('ads-table',7)">Conv. <span class="sort-icon">↕</span></th>
                <th class="num" onclick="Tables.sortTable('ads-table',8)">CPA <span class="sort-icon">↕</span></th>
                <th class="num" onclick="Tables.sortTable('ads-table',9)">ROAS <span class="sort-icon">↕</span></th>
              </tr>
            </thead>
            <tbody>${rows}</tbody>
          </table>
        </div>
      </div>`;
  };

  // ── Keywords ─────────────────────────────────────────────────────────────
  const renderKeywords = (data, container) => {
    const rows = data.map(k => `
      <tr>
        <td class="name">${k.keyword}</td>
        <td><span class="chip ${k.matchType === 'Exact' ? 'active' : k.matchType === 'Phrase' ? 'budget-warn' : 'budget-ok'}">${k.matchType}</span></td>
        <td class="num">${fmt.spend(k.spend)}</td>
        <td class="num">${fmt.num(k.impressions)}</td>
        <td class="num">${fmt.num(k.clicks)}</td>
        <td class="num">${fmt.pct(k.ctr)}</td>
        <td class="num">${fmt.cpc(k.cpc)}</td>
        <td class="num">${fmt.num(k.conversions)}</td>
        <td class="num">${fmt.cpa(k.cpa)}</td>
        <td class="num">${fmt.roas(k.roas)}</td>
      </tr>`).join('');

    container.innerHTML = `
      <div class="table-card">
        <div class="table-card-header">
          <span class="table-card-title">Keyword Performance</span>
          <div class="table-card-actions">
            <div class="search-input-wrap">
              <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35"/></svg>
              <input type="text" class="search-input" placeholder="Search keywords..." oninput="Tables.filterTable(this, 'kw-table')" />
            </div>
          </div>
        </div>
        <div style="overflow-x:auto">
          <table class="data-table" id="kw-table">
            <thead>
              <tr>
                <th onclick="Tables.sortTable('kw-table',0)">Keyword <span class="sort-icon">↕</span></th>
                <th onclick="Tables.sortTable('kw-table',1)">Match Type <span class="sort-icon">↕</span></th>
                <th class="num" onclick="Tables.sortTable('kw-table',2)">Spend <span class="sort-icon">↕</span></th>
                <th class="num" onclick="Tables.sortTable('kw-table',3)">Impressions <span class="sort-icon">↕</span></th>
                <th class="num" onclick="Tables.sortTable('kw-table',4)">Clicks <span class="sort-icon">↕</span></th>
                <th class="num" onclick="Tables.sortTable('kw-table',5)">CTR <span class="sort-icon">↕</span></th>
                <th class="num" onclick="Tables.sortTable('kw-table',6)">CPC <span class="sort-icon">↕</span></th>
                <th class="num" onclick="Tables.sortTable('kw-table',7)">Conv. <span class="sort-icon">↕</span></th>
                <th class="num" onclick="Tables.sortTable('kw-table',8)">CPA <span class="sort-icon">↕</span></th>
                <th class="num" onclick="Tables.sortTable('kw-table',9)">ROAS <span class="sort-icon">↕</span></th>
              </tr>
            </thead>
            <tbody>${rows}</tbody>
          </table>
        </div>
      </div>`;
  };

  // ── Audiences ─────────────────────────────────────────────────────────────
  const renderAudiences = (data, container) => {
    const rows = data.map(a => `
      <tr>
        <td class="name">${a.name}</td>
        <td>${platformChip(a.platform)}</td>
        <td><span class="chip budget-ok">${a.type}</span></td>
        <td class="num">${fmt.spend(a.spend)}</td>
        <td class="num">${fmt.num(a.impressions)}</td>
        <td class="num">${fmt.num(a.clicks)}</td>
        <td class="num">${fmt.pct(a.ctr)}</td>
        <td class="num">${fmt.num(a.conversions)}</td>
        <td class="num">${fmt.cpa(a.cpa)}</td>
        <td class="num">${fmt.roas(a.roas)}</td>
      </tr>`).join('');

    container.innerHTML = `
      <div class="table-card">
        <div class="table-card-header">
          <span class="table-card-title">Audience Performance</span>
        </div>
        <div style="overflow-x:auto">
          <table class="data-table" id="audience-table">
            <thead>
              <tr>
                <th onclick="Tables.sortTable('audience-table',0)">Audience <span class="sort-icon">↕</span></th>
                <th onclick="Tables.sortTable('audience-table',1)">Platform <span class="sort-icon">↕</span></th>
                <th onclick="Tables.sortTable('audience-table',2)">Type <span class="sort-icon">↕</span></th>
                <th class="num" onclick="Tables.sortTable('audience-table',3)">Spend <span class="sort-icon">↕</span></th>
                <th class="num" onclick="Tables.sortTable('audience-table',4)">Impressions <span class="sort-icon">↕</span></th>
                <th class="num" onclick="Tables.sortTable('audience-table',5)">Clicks <span class="sort-icon">↕</span></th>
                <th class="num" onclick="Tables.sortTable('audience-table',6)">CTR <span class="sort-icon">↕</span></th>
                <th class="num" onclick="Tables.sortTable('audience-table',7)">Conv. <span class="sort-icon">↕</span></th>
                <th class="num" onclick="Tables.sortTable('audience-table',8)">CPA <span class="sort-icon">↕</span></th>
                <th class="num" onclick="Tables.sortTable('audience-table',9)">ROAS <span class="sort-icon">↕</span></th>
              </tr>
            </thead>
            <tbody>${rows}</tbody>
          </table>
        </div>
      </div>`;
  };

  // ── Products ─────────────────────────────────────────────────────────────
  const renderProducts = (data, container) => {
    const sorted = [...data];
    const top5 = sorted.slice(0, 5);
    const worst5 = [...sorted].sort((a, b) => a.revenue - b.revenue).slice(0, 5);

    const topRows = top5.map((p, i) => `
      <tr>
        <td><span class="rank-badge top">${i + 1}</span></td>
        <td class="name">${p.name}</td>
        <td>${p.category}</td>
        <td class="num">${fmt.spend(p.price)}</td>
        <td class="num">${p.transactions.toLocaleString()}</td>
        <td class="num">${fmt.revenue(p.revenue)}</td>
        <td class="num">${fmt.spend(p.spend)}</td>
        <td class="num">${fmt.roas(p.roas)}</td>
        <td class="num">${p.convRate.toFixed(2)}%</td>
      </tr>`).join('');

    const worstRows = worst5.map((p, i) => `
      <tr>
        <td><span class="rank-badge worst">${i + 1}</span></td>
        <td class="name">${p.name}</td>
        <td>${p.category}</td>
        <td class="num">${fmt.spend(p.price)}</td>
        <td class="num">${p.transactions.toLocaleString()}</td>
        <td class="num">${fmt.revenue(p.revenue)}</td>
        <td class="num">${fmt.spend(p.spend)}</td>
        <td class="num">${fmt.roas(p.roas)}</td>
        <td class="num">${p.convRate.toFixed(2)}%</td>
      </tr>`).join('');

    const allRows = sorted.map(p => `
      <tr>
        <td class="name">${p.name}</td>
        <td>${p.sku}</td>
        <td>${p.category}</td>
        <td class="num">${p.sessions.toLocaleString()}</td>
        <td class="num">${p.convRate.toFixed(2)}%</td>
        <td class="num">${p.transactions.toLocaleString()}</td>
        <td class="num">${fmt.revenue(p.revenue)}</td>
        <td class="num">${fmt.spend(p.spend)}</td>
        <td class="num">${fmt.roas(p.roas)}</td>
        <td class="num">${fmt.spend(p.avgOrderValue)}</td>
      </tr>`).join('');

    container.innerHTML = `
      <div class="tabs">
        <button class="tab-btn active" onclick="Tables.switchProductTab(this,'tab-top')">🏆 Top Performers</button>
        <button class="tab-btn" onclick="Tables.switchProductTab(this,'tab-worst')">⚠️ Worst Performers</button>
        <button class="tab-btn" onclick="Tables.switchProductTab(this,'tab-all')">All Products</button>
      </div>

      <div id="tab-top">
        <div class="table-card">
          <div class="table-card-header"><span class="table-card-title">Top 5 Products by Revenue</span></div>
          <div style="overflow-x:auto">
            <table class="data-table">
              <thead><tr>
                <th>#</th><th>Product</th><th>Category</th>
                <th class="num">Price</th><th class="num">Orders</th>
                <th class="num">Revenue</th><th class="num">Ad Spend</th>
                <th class="num">ROAS</th><th class="num">Conv. Rate</th>
              </tr></thead>
              <tbody>${topRows}</tbody>
            </table>
          </div>
        </div>
      </div>

      <div id="tab-worst" style="display:none">
        <div class="table-card">
          <div class="table-card-header"><span class="table-card-title">Worst 5 Products by Revenue</span></div>
          <div style="overflow-x:auto">
            <table class="data-table">
              <thead><tr>
                <th>#</th><th>Product</th><th>Category</th>
                <th class="num">Price</th><th class="num">Orders</th>
                <th class="num">Revenue</th><th class="num">Ad Spend</th>
                <th class="num">ROAS</th><th class="num">Conv. Rate</th>
              </tr></thead>
              <tbody>${worstRows}</tbody>
            </table>
          </div>
        </div>
      </div>

      <div id="tab-all" style="display:none">
        <div class="table-card">
          <div class="table-card-header">
            <span class="table-card-title">All Products (GA4 E-commerce)</span>
            <div class="table-card-actions">
              <div class="search-input-wrap">
                <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35"/></svg>
                <input type="text" class="search-input" placeholder="Search products..." oninput="Tables.filterTable(this, 'products-all-table')" />
              </div>
            </div>
          </div>
          <div style="overflow-x:auto">
            <table class="data-table" id="products-all-table">
              <thead><tr>
                <th onclick="Tables.sortTable('products-all-table',0)">Product <span class="sort-icon">↕</span></th>
                <th onclick="Tables.sortTable('products-all-table',1)">SKU <span class="sort-icon">↕</span></th>
                <th onclick="Tables.sortTable('products-all-table',2)">Category <span class="sort-icon">↕</span></th>
                <th class="num" onclick="Tables.sortTable('products-all-table',3)">Sessions <span class="sort-icon">↕</span></th>
                <th class="num" onclick="Tables.sortTable('products-all-table',4)">Conv. Rate <span class="sort-icon">↕</span></th>
                <th class="num" onclick="Tables.sortTable('products-all-table',5)">Orders <span class="sort-icon">↕</span></th>
                <th class="num" onclick="Tables.sortTable('products-all-table',6)">Revenue <span class="sort-icon">↕</span></th>
                <th class="num" onclick="Tables.sortTable('products-all-table',7)">Ad Spend <span class="sort-icon">↕</span></th>
                <th class="num" onclick="Tables.sortTable('products-all-table',8)">ROAS <span class="sort-icon">↕</span></th>
                <th class="num" onclick="Tables.sortTable('products-all-table',9)">AOV <span class="sort-icon">↕</span></th>
              </tr></thead>
              <tbody>${allRows}</tbody>
            </table>
          </div>
        </div>
      </div>`;
  };

  // ── Utility: Sort Table ───────────────────────────────────────────────────
  const _sortState = {};
  const sortTable = (tableId, colIdx) => {
    const table = document.getElementById(tableId);
    if (!table) return;
    const key = `${tableId}_${colIdx}`;
    _sortState[key] = _sortState[key] === 'asc' ? 'desc' : 'asc';
    const dir = _sortState[key] === 'asc' ? 1 : -1;
    const tbody = table.querySelector('tbody');
    const rows = Array.from(tbody.querySelectorAll('tr'));
    rows.sort((a, b) => {
      const av = a.cells[colIdx]?.innerText.replace(/[$%x,+]/g, '') || '';
      const bv = b.cells[colIdx]?.innerText.replace(/[$%x,+]/g, '') || '';
      const an = parseFloat(av), bn = parseFloat(bv);
      if (!isNaN(an) && !isNaN(bn)) return (an - bn) * dir;
      return av.localeCompare(bv) * dir;
    });
    rows.forEach(r => tbody.appendChild(r));
    // Update header indicator
    table.querySelectorAll('th').forEach((th, i) => {
      th.classList.toggle('sorted', i === colIdx);
      const icon = th.querySelector('.sort-icon');
      if (icon) icon.textContent = i === colIdx ? (_sortState[key] === 'asc' ? '↑' : '↓') : '↕';
    });
  };

  // ── Utility: Filter Table ─────────────────────────────────────────────────
  const filterTable = (input, tableId) => {
    const q = input.value.toLowerCase();
    const table = document.getElementById(tableId);
    if (!table) return;
    Array.from(table.querySelectorAll('tbody tr')).forEach(row => {
      row.style.display = row.innerText.toLowerCase().includes(q) ? '' : 'none';
    });
  };

  // ── Product Tab Switch ────────────────────────────────────────────────────
  const switchProductTab = (btn, tabId) => {
    ['tab-top','tab-worst','tab-all'].forEach(id => {
      const el = document.getElementById(id);
      if (el) el.style.display = 'none';
    });
    document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
    const el = document.getElementById(tabId);
    if (el) el.style.display = '';
    btn.classList.add('active');
  };

  return { renderCampaigns, renderAdSets, renderAds, renderKeywords, renderAudiences, renderProducts, sortTable, filterTable, switchProductTab };
})();
