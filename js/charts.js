/**
 * charts.js — Chart.js rendering helpers
 * All chart instances are tracked to allow destroy/re-render on filter change.
 */

const Charts = (() => {
  const instances = {};

  // ── Theme Palette ──────────────────────────────────────────────────────────
  const palette = {
    google:  { line: '#4285f4', fill: 'rgba(66,133,244,0.10)' },
    meta:    { line: '#5b92f5', fill: 'rgba(91,146,245,0.10)' },
    tiktok:  { line: '#ff6699', fill: 'rgba(255,102,153,0.10)' },
    spend:   { line: '#4f8ef7', fill: 'rgba(79,142,247,0.12)' },
    conv:    { line: '#34d399', fill: 'rgba(52,211,153,0.12)'  },
    rev:     { line: '#fbbf24', fill: 'rgba(251,191,36,0.12)'  },
    roas:    { line: '#a78bfa', fill: 'rgba(167,139,250,0.12)' },
  };

  const gridColor  = 'rgba(255,255,255,0.05)';
  const tickColor  = '#4f6680';
  const legendFont = { family: 'Inter', size: 11, weight: '500' };

  const baseLineDataset = (label, data, colorKey, yAxisID = 'y') => ({
    label, data,
    borderColor: palette[colorKey]?.line || palette.spend.line,
    backgroundColor: palette[colorKey]?.fill || palette.spend.fill,
    borderWidth: 2,
    pointRadius: 0,
    pointHoverRadius: 5,
    pointHoverBackgroundColor: palette[colorKey]?.line || palette.spend.line,
    tension: 0.4,
    fill: colorKey !== 'roas',
    yAxisID,
  });

  const defaultScales = (suffix = '') => ({
    x: {
      grid: { color: gridColor },
      ticks: { color: tickColor, font: { family: 'Inter', size: 11 }, maxTicksLimit: 10 },
    },
    y: {
      grid: { color: gridColor },
      ticks: {
        color: tickColor, font: { family: 'Inter', size: 11 },
        callback: (v) => suffix === '$' ? '$' + v.toLocaleString() : v.toLocaleString(),
      },
      beginAtZero: true,
    }
  });

  const defaultOptions = (tooltip = null) => ({
    responsive: true,
    maintainAspectRatio: false,
    interaction: { mode: 'index', intersect: false },
    plugins: {
      legend: {
        display: false,
      },
      tooltip: tooltip || {
        backgroundColor: '#172040',
        borderColor: 'rgba(255,255,255,0.1)',
        borderWidth: 1,
        titleColor: '#f0f4ff',
        bodyColor: '#8899bb',
        padding: 10,
        callbacks: {},
      },
    },
  });

  const destroy = (id) => {
    if (instances[id]) { instances[id].destroy(); delete instances[id]; }
  };

  // ── Public Chart Renderers ────────────────────────────────────────────────

  /**
   * Trend line chart: Spend + Conversions on dual Y-axis
   */
  const renderTrendChart = (canvasId, trendData) => {
    destroy(canvasId);
    const ctx = document.getElementById(canvasId)?.getContext('2d');
    if (!ctx) return;

    const labels = trendData.combined.map(d => d.date);
    const spendVals = trendData.combined.map(d => d.spend);
    const convVals  = trendData.combined.map(d => d.conversions);
    const revVals   = trendData.combined.map(d => d.revenue);

    instances[canvasId] = new Chart(ctx, {
      type: 'line',
      data: {
        labels,
        datasets: [
          { ...baseLineDataset('Spend', spendVals, 'spend', 'y'),  yAxisID: 'y'  },
          { ...baseLineDataset('Revenue', revVals, 'rev', 'y2'),   yAxisID: 'y2', fill: false },
          { ...baseLineDataset('Conversions', convVals, 'conv', 'y3'), yAxisID: 'y2', fill: false },
        ]
      },
      options: {
        ...defaultOptions(),
        scales: {
          x: {
            grid: { color: gridColor },
            ticks: { color: tickColor, font: { family: 'Inter', size: 11 }, maxTicksLimit: 12 },
          },
          y: {
            position: 'left',
            grid: { color: gridColor },
            ticks: { color: tickColor, font: { family: 'Inter', size: 11 }, callback: v => '$' + v.toLocaleString() },
            beginAtZero: true,
          },
          y2: {
            position: 'right',
            grid: { drawOnChartArea: false },
            ticks: { color: tickColor, font: { family: 'Inter', size: 11 } },
            beginAtZero: true,
          },
          y3: { display: false },
        },
      }
    });
  };

  /**
   * ROAS trend line
   */
  const renderRoasChart = (canvasId, trendData) => {
    destroy(canvasId);
    const ctx = document.getElementById(canvasId)?.getContext('2d');
    if (!ctx) return;

    const labels = trendData.combined.map(d => d.date);
    const roasVals = trendData.combined.map(d => d.roas);

    instances[canvasId] = new Chart(ctx, {
      type: 'line',
      data: {
        labels,
        datasets: [
          { ...baseLineDataset('ROAS', roasVals, 'roas'), fill: true }
        ]
      },
      options: {
        ...defaultOptions(),
        scales: {
          ...defaultScales(''),
          y: {
            ...defaultScales('').y,
            ticks: {
              ...defaultScales('').y.ticks,
              callback: v => v.toFixed(2) + 'x',
            }
          }
        },
      }
    });
  };

  /**
   * Platform breakdown bar chart
   */
  const renderPlatformBar = (canvasId, platformData) => {
    destroy(canvasId);
    const ctx = document.getElementById(canvasId)?.getContext('2d');
    if (!ctx) return;

    const platforms = Object.keys(platformData);
    const labels = ['Spend', 'Revenue', 'Conversions × 10'];
    const colors = { google: '#4285f4', meta: '#5b92f5', tiktok: '#ff6699' };

    const datasets = platforms.map(p => ({
      label: DB.PLATFORM_LABELS[p],
      data: [
        platformData[p].spend,
        platformData[p].revenue,
        platformData[p].conversions * 10,
      ],
      backgroundColor: colors[p] + 'cc',
      borderColor: colors[p],
      borderWidth: 1,
      borderRadius: 4,
    }));

    instances[canvasId] = new Chart(ctx, {
      type: 'bar',
      data: { labels, datasets },
      options: {
        ...defaultOptions(),
        scales: {
          x: { grid: { color: gridColor }, ticks: { color: tickColor, font: { family: 'Inter', size: 11 } } },
          y: {
            grid: { color: gridColor },
            ticks: { color: tickColor, font: { family: 'Inter', size: 11 }, callback: v => '$' + v.toLocaleString() },
            beginAtZero: true,
          }
        },
        plugins: {
          ...defaultOptions().plugins,
          legend: { display: true, labels: { color: tickColor, font: legendFont, usePointStyle: true, pointStyleWidth: 8 } },
        }
      }
    });
  };

  /**
   * Donut chart for spend share by platform
   */
  const renderSpendDonut = (canvasId, platformData) => {
    destroy(canvasId);
    const ctx = document.getElementById(canvasId)?.getContext('2d');
    if (!ctx) return;

    const data = Object.entries(platformData).map(([k, v]) => v.spend);
    const labels = Object.keys(platformData).map(k => DB.PLATFORM_LABELS[k]);
    const colors = ['#4285f4', '#5b92f5', '#ff6699'];

    instances[canvasId] = new Chart(ctx, {
      type: 'doughnut',
      data: {
        labels,
        datasets: [{
          data,
          backgroundColor: colors.map(c => c + 'cc'),
          borderColor: colors,
          borderWidth: 2,
          hoverOffset: 6,
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        cutout: '72%',
        plugins: {
          legend: {
            display: true,
            position: 'bottom',
            labels: { color: tickColor, font: legendFont, usePointStyle: true, pointStyleWidth: 8, padding: 16 },
          },
          tooltip: { backgroundColor: '#172040', borderColor: 'rgba(255,255,255,0.1)', borderWidth: 1, titleColor: '#f0f4ff', bodyColor: '#8899bb', padding: 10 },
        }
      }
    });
  };

  /**
   * Comparison bar chart (current vs prior period)
   */
  const renderComparisonBar = (canvasId, labels, current, prior, metricLabel) => {
    destroy(canvasId);
    const ctx = document.getElementById(canvasId)?.getContext('2d');
    if (!ctx) return;

    instances[canvasId] = new Chart(ctx, {
      type: 'bar',
      data: {
        labels,
        datasets: [
          {
            label: 'Current Period',
            data: current,
            backgroundColor: 'rgba(79,142,247,0.75)',
            borderColor: '#4f8ef7',
            borderWidth: 1,
            borderRadius: 4,
          },
          {
            label: 'Prior Period',
            data: prior,
            backgroundColor: 'rgba(255,255,255,0.08)',
            borderColor: 'rgba(255,255,255,0.2)',
            borderWidth: 1,
            borderRadius: 4,
          },
        ]
      },
      options: {
        ...defaultOptions(),
        scales: {
          x: { grid: { color: gridColor }, ticks: { color: tickColor, font: { family: 'Inter', size: 11 } } },
          y: {
            grid: { color: gridColor },
            ticks: { color: tickColor, font: { family: 'Inter', size: 11 } },
            beginAtZero: true,
          }
        },
        plugins: {
          ...defaultOptions().plugins,
          legend: { display: true, labels: { color: tickColor, font: legendFont, usePointStyle: true, pointStyleWidth: 8 } }
        }
      }
    });
  };

  /**
   * Multi-platform line chart (one line per platform)
   */
  const renderMultiPlatformTrend = (canvasId, trendData, metric) => {
    destroy(canvasId);
    const ctx = document.getElementById(canvasId)?.getContext('2d');
    if (!ctx) return;

    const labels = trendData.combined.map(d => d.date);
    const pfColors = { google: 'google', meta: 'meta', tiktok: 'tiktok' };
    const datasets = trendData.platforms.map(p => ({
      ...baseLineDataset(DB.PLATFORM_LABELS[p], trendData.series[p].map(d => d[metric] || 0), pfColors[p]),
      fill: false,
    }));

    instances[canvasId] = new Chart(ctx, {
      type: 'line',
      data: { labels, datasets },
      options: {
        ...defaultOptions(),
        scales: {
          x: { grid: { color: gridColor }, ticks: { color: tickColor, font: { family: 'Inter', size: 11 }, maxTicksLimit: 10 } },
          y: {
            grid: { color: gridColor },
            ticks: { color: tickColor, font: { family: 'Inter', size: 11 }, callback: v => metric === 'spend' || metric === 'revenue' ? '$' + v.toLocaleString() : v.toLocaleString() },
            beginAtZero: true,
          }
        },
        plugins: {
          ...defaultOptions().plugins,
          legend: { display: true, labels: { color: tickColor, font: legendFont, usePointStyle: true, pointStyleWidth: 8 } }
        }
      }
    });
  };

  return { renderTrendChart, renderRoasChart, renderPlatformBar, renderSpendDonut, renderComparisonBar, renderMultiPlatformTrend, destroy, instances };
})();
