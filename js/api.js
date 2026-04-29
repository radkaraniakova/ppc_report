/**
 * api.js — Mock Database API Layer
 * Simulates fetching aggregated PPC data from PostgreSQL/BigQuery.
 * In production: replace fetch calls here to your actual /api endpoints.
 */

const DB = (() => {

  // ── Helpers ──────────────────────────────────────────────────────────────
  const rand = (min, max) => +(Math.random() * (max - min) + min).toFixed(2);
  const randInt = (min, max) => Math.floor(Math.random() * (max - min + 1) + min);
  const currency = (val) => '$' + val.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
  const pct = (val) => val.toFixed(2) + '%';
  const fmtNum = (val) => val.toLocaleString('en-US');

  const PLATFORMS = ['google', 'meta', 'tiktok'];
  const PLATFORM_LABELS = { google: 'Google Ads', meta: 'Meta Ads', tiktok: 'TikTok Ads' };

  const CLIENTS = {
    acme:  { name: 'Acme Corp',         currency: 'USD', ecom: false },
    bloom: { name: 'Bloom Fashion',      currency: 'USD', ecom: true  },
    tekko: { name: 'Tekko Electronics',  currency: 'USD', ecom: true  },
  };

  const CAMPAIGNS = [
    { id:'c1', name:'Brand Awareness Q2',       platform:'google', status:'active',  adsets: 4 },
    { id:'c2', name:'Retargeting — Cart Abnd.',  platform:'meta',   status:'active',  adsets: 3 },
    { id:'c3', name:'New Customer Acquisition',  platform:'google', status:'active',  adsets: 6 },
    { id:'c4', name:'Summer Sale Push',          platform:'tiktok', status:'active',  adsets: 2 },
    { id:'c5', name:'Competitor Conquesting',    platform:'google', status:'paused',  adsets: 3 },
    { id:'c6', name:'Lookalike Expansion',       platform:'meta',   status:'active',  adsets: 5 },
    { id:'c7', name:'Video Views — Awareness',   platform:'tiktok', status:'active',  adsets: 2 },
    { id:'c8', name:'Dynamic Product Ads',       platform:'meta',   status:'paused',  adsets: 4 },
    { id:'c9', name:'Shopping — Top Products',   platform:'google', status:'active',  adsets: 7 },
    { id:'c10',name:'Reengagement —30d',         platform:'tiktok', status:'active',  adsets: 2 },
  ];

  const ADSETS = [
    { id:'as1', campaign:'c1', name:'Broad — Desktop',          platform:'google', budget: 500 },
    { id:'as2', campaign:'c1', name:'Broad — Mobile',           platform:'google', budget: 300 },
    { id:'as3', campaign:'c2', name:'Cart — 1-3 days',          platform:'meta',   budget: 400 },
    { id:'as4', campaign:'c2', name:'Cart — 4-7 days',          platform:'meta',   budget: 250 },
    { id:'as5', campaign:'c3', name:'In-Market — Tech',         platform:'google', budget: 600 },
    { id:'as6', campaign:'c3', name:'Custom Intent — Buyers',   platform:'google', budget: 800 },
    { id:'as7', campaign:'c4', name:'TikTok 18-34 Female',      platform:'tiktok', budget: 350 },
    { id:'as8', campaign:'c6', name:'LAL 1% — Purchasers',      platform:'meta',   budget: 700 },
    { id:'as9', campaign:'c9', name:'Shopping — Electronics',   platform:'google', budget: 900 },
    { id:'as10',campaign:'c10',name:'Re-engage — 30d App Open', platform:'tiktok', budget: 200 },
  ];

  const ADS = [
    { id:'ad1', adset:'as1', name:'Q2 Summer Hero — v1',       format:'Image',  platform:'google' },
    { id:'ad2', adset:'as1', name:'Q2 Summer Hero — v2',       format:'Image',  platform:'google' },
    { id:'ad3', adset:'as3', name:'Cart Reminder — Carousel',  format:'Carousel',platform:'meta'  },
    { id:'ad4', adset:'as3', name:'Flash Sale — Story',        format:'Story',  platform:'meta'   },
    { id:'ad5', adset:'as5', name:'Tech Benefits — Long',      format:'Video',  platform:'google' },
    { id:'ad6', adset:'as7', name:'Dance Challenge UGC',       format:'Video',  platform:'tiktok' },
    { id:'ad7', adset:'as8', name:'LAL — Featured Products',   format:'Carousel',platform:'meta'  },
    { id:'ad8', adset:'as8', name:'LAL — Testimonial',         format:'Image',  platform:'meta'   },
    { id:'ad9', adset:'as9', name:'Shopping — Electronics',    format:'Shopping',platform:'google' },
    { id:'ad10',adset:'as10',name:'Re-engage TikTok — 15s',   format:'Video',  platform:'tiktok' },
  ];

  const KEYWORDS = [
    { id:'kw1', campaign:'c1', keyword:'buy running shoes online',    matchType:'Exact',   platform:'google' },
    { id:'kw2', campaign:'c1', keyword:'best running shoes 2024',     matchType:'Phrase',  platform:'google' },
    { id:'kw3', campaign:'c3', keyword:'running shoes for men',       matchType:'Broad',   platform:'google' },
    { id:'kw4', campaign:'c3', keyword:'lightweight trail runners',   matchType:'Exact',   platform:'google' },
    { id:'kw5', campaign:'c5', keyword:'[competitor brand] shoes',    matchType:'Exact',   platform:'google' },
    { id:'kw6', campaign:'c9', keyword:'shoe sale',                   matchType:'Broad',   platform:'google' },
    { id:'kw7', campaign:'c9', keyword:'buy sneakers online',         matchType:'Phrase',  platform:'google' },
    { id:'kw8', campaign:'c1', keyword:'athletic shoes women',        matchType:'Phrase',  platform:'google' },
    { id:'kw9', campaign:'c3', keyword:'marathon running shoes',      matchType:'Exact',   platform:'google' },
    { id:'kw10',campaign:'c5', keyword:'sport shoe brand review',     matchType:'Phrase',  platform:'google' },
  ];

  const AUDIENCES = [
    { id:'au1', name:'Custom Intent — Competitor Visitors', platform:'google', type:'Custom Intent' },
    { id:'au2', name:'In-Market — Athletic Apparel',        platform:'google', type:'In-Market'     },
    { id:'au3', name:'Retargeting — Website Visitors 30d',  platform:'meta',   type:'Custom Audience'},
    { id:'au4', name:'Lookalike 1% — All Purchasers',       platform:'meta',   type:'Lookalike'     },
    { id:'au5', name:'Lookalike 2-3% — Purchasers',         platform:'meta',   type:'Lookalike'     },
    { id:'au6', name:'Interest — Fitness & Running',        platform:'meta',   type:'Interest'      },
    { id:'au7', name:'TikTok Creator Audience 18-34',       platform:'tiktok', type:'Interest'      },
    { id:'au8', name:'TikTok Re-engage — App Users',        platform:'tiktok', type:'Retargeting'   },
    { id:'au9', name:'RLSA — Past Purchasers',              platform:'google', type:'RLSA'          },
    { id:'au10',name:'Video Viewers — 75% Watch',           platform:'tiktok', type:'Custom'        },
  ];

  const PRODUCTS = [
    { id:'p1',  name:'ProRun X9 — Mens',         sku:'PRX9M', category:'Running Shoes',  price:129.99  },
    { id:'p2',  name:'ProRun X9 — Womens',        sku:'PRX9W', category:'Running Shoes',  price:129.99  },
    { id:'p3',  name:'TrailBlazer 500',            sku:'TB500', category:'Trail Running',  price:159.99  },
    { id:'p4',  name:'Urban Stride Sneaker',       sku:'USS01', category:'Lifestyle',      price:89.99   },
    { id:'p5',  name:'CloudWalk 3 — Unisex',       sku:'CW3U',  category:'Walking',        price:109.99  },
    { id:'p6',  name:'SpeedForce Elite',           sku:'SFE01', category:'Racing',         price:199.99  },
    { id:'p7',  name:'RecoverySlide Plus',         sku:'RS001', category:'Recovery',       price:49.99   },
    { id:'p8',  name:'AllTerrain Boot — Womens',   sku:'ATB01', category:'Outdoor',        price:149.99  },
    { id:'p9',  name:'KidsRun 2024',               sku:'KR24',  category:'Kids',           price:69.99   },
    { id:'p10', name:'HiSock Pro Compression',     sku:'HSP01', category:'Accessories',    price:29.99   },
    { id:'p11', name:'WinterSprint Ice',           sku:'WSI01', category:'Winter Running', price:179.99  },
    { id:'p12', name:'LightStep 70 — Mens',        sku:'LS70M', category:'Running Shoes',  price:119.99  },
  ];

  // ── Seeded metric generation ──────────────────────────────────────────────
  // Generates realistic-looking PPC metrics per item, consistent per platform.
  const platformBias = {
    google: { spendMult: 1.8, cpcMult: 1.4, ctrBase: 4.5, cpaBase: 28, roasBase: 4.2 },
    meta:   { spendMult: 1.2, cpcMult: 0.6, ctrBase: 1.8, cpaBase: 22, roasBase: 3.5 },
    tiktok: { spendMult: 0.8, cpcMult: 0.4, ctrBase: 2.4, cpaBase: 19, roasBase: 2.8 },
  };

  const genMetrics = (platform, spendRange = [200, 2000]) => {
    const b = platformBias[platform] || platformBias.google;
    const spend   = rand(spendRange[0], spendRange[1]) * b.spendMult;
    const cpc     = rand(0.30, 2.00) * b.cpcMult;
    const clicks  = Math.round(spend / cpc);
    const ctr     = rand(b.ctrBase * 0.6, b.ctrBase * 1.5);
    const impressions = Math.round(clicks / (ctr / 100));
    const cpa     = rand(b.cpaBase * 0.7, b.cpaBase * 1.4);
    const conversions = Math.round(spend / cpa);
    const revenue   = +(conversions * rand(40, 180)).toFixed(2);
    const roas      = +(revenue / spend).toFixed(2);
    return { spend, cpc, clicks, ctr, impressions, conversions, revenue, roas, cpa };
  };

  // Generate a time series of N days
  const genTimeSeries = (days, platform, baseSpend) => {
    return Array.from({ length: days }, (_, i) => {
      const b = platformBias[platform] || platformBias.google;
      const noise = 0.7 + Math.random() * 0.6;
      const spend = baseSpend * noise;
      const cpc   = rand(0.4, 1.8) * b.cpcMult;
      const clicks = Math.round(spend / cpc);
      const ctr   = rand(b.ctrBase * 0.6, b.ctrBase * 1.5);
      const cpa   = rand(b.cpaBase * 0.7, b.cpaBase * 1.4);
      const conversions = Math.round(spend / cpa);
      const revenue = +(conversions * rand(40, 160)).toFixed(2);
      const roas = +(revenue / spend).toFixed(2);
      const date = new Date();
      date.setDate(date.getDate() - (days - i));
      return {
        date: date.toISOString().slice(0, 10),
        spend: +spend.toFixed(2),
        clicks, ctr: +ctr.toFixed(2), conversions, revenue, roas: +roas.toFixed(2), cpa: +cpa.toFixed(2)
      };
    });
  };

  // ── Public API ────────────────────────────────────────────────────────────
  return {
    currency, pct, fmtNum, PLATFORMS, PLATFORM_LABELS, CLIENTS, CAMPAIGNS, ADSETS, ADS, KEYWORDS, AUDIENCES, PRODUCTS,

    /** Get summary totals for Overview scorecards */
    getOverviewTotals(client, dateRange, platform) {
      const m = { google: genMetrics('google', [1000, 4000]), meta: genMetrics('meta', [800, 3000]), tiktok: genMetrics('tiktok', [400, 2000]) };
      const platforms = platform === 'all' ? ['google', 'meta', 'tiktok'] : [platform];
      const totals = platforms.reduce((acc, p) => {
        acc.spend += m[p].spend; acc.clicks += m[p].clicks;
        acc.conversions += m[p].conversions; acc.revenue += m[p].revenue;
        return acc;
      }, { spend: 0, clicks: 0, conversions: 0, revenue: 0 });
      totals.roas = +(totals.revenue / totals.spend).toFixed(2);
      totals.cpc  = +(totals.spend / totals.clicks).toFixed(2);
      totals.cpa  = +(totals.spend / totals.conversions).toFixed(2);
      totals.ctr  = rand(1.2, 4.8);
      // mock deltas vs prior period
      totals.delta = {
        spend:       rand(-15, 12),
        conversions: rand(-8, 25),
        revenue:     rand(-5, 30),
        roas:        rand(-12, 18),
        cpc:         rand(-20, 10),
        ctr:         rand(-5, 15),
      };
      totals.platformBreakdown = { google: m.google, meta: m.meta, tiktok: m.tiktok };
      return totals;
    },

    /** Get trend time-series data */
    getTrend(client, dateRange, platform) {
      const days = { today: 1, yesterday: 1, '7d': 7, '14d': 14, '30d': 30, mom: 60, yoy: 365 }[dateRange] || 30;
      const chartDays = Math.min(days, 90);
      const platforms = platform === 'all' ? ['google', 'meta', 'tiktok'] : [platform];
      const series = {};
      platforms.forEach(p => {
        const base = { google: 250, meta: 180, tiktok: 100 }[p] || 150;
        series[p] = genTimeSeries(chartDays, p, base);
      });
      // Merge into combined dates
      const dateSet = series[platforms[0]].map(d => d.date);
      const combined = dateSet.map((date, i) => {
        const row = { date };
        platforms.forEach(p => {
          const d = series[p][i] || {};
          row[`${p}_spend`] = d.spend || 0;
          row[`${p}_conversions`] = d.conversions || 0;
          row[`${p}_revenue`] = d.revenue || 0;
          row[`${p}_roas`] = d.roas || 0;
        });
        row.spend = platforms.reduce((s, p) => s + (series[p][i]?.spend || 0), 0);
        row.conversions = platforms.reduce((s, p) => s + (series[p][i]?.conversions || 0), 0);
        row.revenue = platforms.reduce((s, p) => s + (series[p][i]?.revenue || 0), 0);
        row.roas = +(row.revenue / (row.spend || 1)).toFixed(2);
        return row;
      });
      return { combined, series, platforms };
    },

    /** Get campaigns with metrics */
    getCampaigns(client, dateRange, platform) {
      return CAMPAIGNS
        .filter(c => platform === 'all' || c.platform === platform)
        .map(c => ({ ...c, ...genMetrics(c.platform, [100, 2500]) }));
    },

    /** Ad sets */
    getAdSets(client, dateRange, platform) {
      return ADSETS
        .filter(a => platform === 'all' || a.platform === platform)
        .map(a => ({ ...a, ...genMetrics(a.platform, [50, 900]) }));
    },

    /** Ads */
    getAds(client, dateRange, platform) {
      return ADS
        .filter(a => platform === 'all' || a.platform === platform)
        .map(a => ({ ...a, ...genMetrics(a.platform, [20, 600]) }));
    },

    /** Keywords */
    getKeywords(client, dateRange) {
      return KEYWORDS.map(k => ({ ...k, ...genMetrics(k.platform, [30, 400]) }));
    },

    /** Audiences */
    getAudiences(client, dateRange, platform) {
      return AUDIENCES
        .filter(a => platform === 'all' || a.platform === platform)
        .map(a => ({ ...a, ...genMetrics(a.platform, [50, 800]) }));
    },

    /** Products (GA4 e-com) */
    getProducts(client, dateRange, platform) {
      return PRODUCTS.map(p => {
        const sessions = randInt(400, 5000);
        const convRate = rand(1.2, 8.5);
        const transactions = Math.round(sessions * convRate / 100);
        const revenue = +(transactions * p.price * rand(0.9, 1.1)).toFixed(2);
        const spend = +(revenue / rand(1.5, 6.0)).toFixed(2);
        const roas = +(revenue / spend).toFixed(2);
        return { ...p, sessions, convRate, transactions, revenue, spend, roas, avgOrderValue: +(revenue / (transactions || 1)).toFixed(2) };
      }).sort((a, b) => b.revenue - a.revenue);
    },

    /** Performance alerts */
    getAlerts(client, totals) {
      const alerts = [];
      if (totals.roas < 2.5) alerts.push({ type: 'danger', metric: 'ROAS', msg: `Account ROAS is ${totals.roas.toFixed(2)}x — below target of 2.5x.`, campaign: 'All campaigns' });
      if (totals.cpa > 45)   alerts.push({ type: 'warn',   metric: 'CPA',  msg: `CPA has risen to ${currency(totals.cpa)} — exceeds KPI threshold of $45.`, campaign: 'Multiple campaigns' });
      if (totals.delta?.spend < -10) alerts.push({ type: 'warn', metric: 'Spend', msg: `Spend is down ${Math.abs(totals.delta.spend).toFixed(1)}% vs prior period — check budget pacing.`, campaign: 'Overall' });
      return alerts;
    }
  };
})();
