/* Home / Overview — matches the canonical screenshot */

function HomeScreen() {
  return <div className="page">
    <div className="page-head">
      <h1>Overview</h1>
      <p>A snapshot of your brand's discoverability and key metrics.</p>
    </div>

    <div className="toolbar">
      <button className="filter-chip">
        <Icon name="calendar" />
        <span>Last 7 days</span>
        <Icon name="chevron-down" className="chev" />
      </button>
      <button className="filter-chip">
        <Icon name="layers" />
        <span>Platform: All</span>
        <Icon name="chevron-down" className="chev" />
      </button>
      <button className="filter-chip">
        <Icon name="tag" />
        <span>Topics: All</span>
        <Icon name="chevron-down" className="chev" />
      </button>
      <div className="spacer" />
      <button className="viewing-chip">
        <span className="vc-av">B</span>
        <span>Viewing as: BirdseyePost</span>
        <Icon name="chevron-down" className="chev" />
      </button>
      <button className="icon-btn"><Icon name="more-horizontal" /></button>
      <button className="icon-btn"><Icon name="chevron-up" /></button>
    </div>

    <div className="hint">
      <Icon name="info" />
      <span>Metrics show the average for the selected date range, compared to the previous period.</span>
    </div>

    <div className="info-banner">
      <Icon name="info" size={16} />
      <div style={{ flex: 1 }}>
        <b>Thank you for being an early believer!</b>
        <span>You're seeing an early version of the app. We'll be improving it quickly based on your feedback, so expect it to look and feel better every time you log in.</span>
      </div>
      <button className="close"><Icon name="x" size={14} /></button>
    </div>

    {/* Two-column: trend + score */}
    <div style={{ display: 'grid', gridTemplateColumns: '1.5fr 1fr', gap: 16 }}>
      <TrendCard />
      <ScoreCard />
    </div>

    {/* 4 KPI row */}
    <div className="kpi-row">
      <KpiCard label="Citation rate" value="89%" delta="+17%" />
      <KpiCard label="Reputation score" value="72.1%" delta="+17%" />
      <KpiCard label="Average position" value={<>8<sup style={{ fontSize: '.5em', fontWeight: 500 }}>th</sup></>} delta="+17%" showInfo />
      <KpiCard label="Citation rate" value="89%" delta="+17%" />
    </div>

    {/* Bottom row: share of voice + leaderboard */}
    <div style={{ display: 'grid', gridTemplateColumns: '1fr 1.5fr', gap: 16 }}>
      <ShareOfVoiceCard />
      <LeaderboardCard />
    </div>
  </div>;
}

function TrendCard() {
  const [tab, setTab] = React.useState('overall');
  const series = [
    { label: 'Discoverability', color: 'var(--color-purple-300)', data: [32, 48, 58, 62, 60, 22, 42, 55, 58, 60] },
  ];
  return <div className="card">
    <div className="card-head">
      <div>
        <h3 className="title">Discoverability trend</h3>
        <p className="sub">How often your brand shows up in AI responses over time</p>
      </div>
    </div>
    <div className="seg-tabs">
      <button className={`seg-tab${tab === 'overall' ? ' active' : ''}`} onClick={() => setTab('overall')}>Overall</button>
      <button className={`seg-tab${tab === 'competitor' ? ' active' : ''}`} onClick={() => setTab('competitor')}>By Competitor</button>
      <button className={`seg-tab${tab === 'topic' ? ' active' : ''}`} onClick={() => setTab('topic')}>By Topic</button>
    </div>
    <TrendChart series={series} />
  </div>;
}

function TrendChart({ series }) {
  const width = 560, height = 220;
  const pad = { t: 12, r: 16, b: 32, l: 40 };
  const w = width - pad.l - pad.r;
  const h = height - pad.t - pad.b;
  const max = 80, min = 0;
  const yTicks = [0, 20, 40, 60, 80];
  const days = ['Mon','Tue','Wed','Thur','Fri','Sat'];
  const n = series[0].data.length;
  const xAt = i => pad.l + (i / (n - 1)) * w;
  const yAt = v => pad.t + h - ((v - min) / (max - min)) * h;

  // tooltip point
  const hiIdx = 2;
  const hiX = xAt(hiIdx), hiY = yAt(series[0].data[hiIdx]);

  return <div style={{ position: 'relative' }}>
    <svg viewBox={`0 0 ${width} ${height}`} width="100%" style={{ display: 'block' }}>
      {yTicks.map(v => (
        <g key={v}>
          <line x1={pad.l} x2={pad.l + w} y1={yAt(v)} y2={yAt(v)} stroke="currentColor" strokeOpacity=".08" strokeDasharray="3,4" />
          <text x={pad.l - 8} y={yAt(v) + 4} fontSize="11" fill="currentColor" opacity=".5" textAnchor="end" fontFamily="var(--fontFamily-body)">{v}%</text>
        </g>
      ))}
      {series.map(s => {
        const pts = s.data.map((v, i) => `${xAt(i)},${yAt(v)}`).join(' L');
        return <g key={s.label}>
          <path d={`M${pad.l},${pad.t + h} L${pts} L${pad.l + w},${pad.t + h} Z`} fill={s.color} opacity=".08" />
          <path d={`M${pts}`} fill="none" stroke={s.color} strokeWidth="2" strokeLinejoin="round" strokeLinecap="round" />
        </g>;
      })}
      {days.map((lbl, i) => {
        const x = xAt((i / (days.length - 1)) * (n - 1));
        return <text key={lbl} x={x} y={height - 10} fontSize="11" fill="currentColor" opacity=".5" textAnchor="middle" fontFamily="var(--fontFamily-body)">{lbl}</text>;
      })}
      {/* highlighted point */}
      <circle cx={hiX} cy={hiY} r="5" fill="var(--color-orange-500)" />
      <circle cx={hiX} cy={hiY} r="3" fill="#fff" />
    </svg>
    {/* tooltip */}
    <div style={{
      position: 'absolute',
      left: `${(hiX / width) * 100}%`,
      top: `${(hiY / height) * 100 - 18}%`,
      transform: 'translate(-50%, -100%)',
      background: 'var(--color-grey-1000)',
      color: '#fff',
      padding: '8px 12px',
      borderRadius: 8,
      fontFamily: 'var(--fontFamily-body)',
      fontSize: 12,
      boxShadow: '0 4px 12px rgba(0,0,0,.25)',
      whiteSpace: 'nowrap',
      border: '1px solid rgba(255,255,255,.08)',
    }}>
      <div style={{ fontWeight: 600, marginBottom: 2 }}>Sep 4, 2025 <span style={{ fontWeight: 400, color: 'var(--color-grey-300)' }}>(Moving average)</span></div>
      <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
        <span style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
          <span style={{ width: 8, height: 8, borderRadius: 2, background: 'var(--color-purple-300)' }} />
          Discoverability score
        </span>
        <span style={{ fontFamily: 'var(--font-mono)', fontWeight: 500 }}>60%</span>
      </div>
    </div>
  </div>;
}

function ScoreCard() {
  const value = 72.2;
  const pct = value / 100;
  const r = 80, cx = 100, cy = 100;
  const circ = Math.PI * r; // semicircle length
  const dash = circ * pct;

  return <div className="card" style={{ justifyContent: 'space-between' }}>
    <div className="card-head">
      <div>
        <h3 className="title">Discoverability score</h3>
      </div>
      <div className="spacer" />
      <span className="badge success">+12.5%</span>
    </div>

    <div style={{ display: 'grid', gridTemplateColumns: '180px 1fr', gap: 20, alignItems: 'center' }}>
      <div style={{ position: 'relative', width: 180, height: 110 }}>
        <svg viewBox="0 0 200 110" width="180" height="110" style={{ display: 'block' }}>
          {/* Background semicircle */}
          <path d={`M 20 100 A 80 80 0 0 1 180 100`} fill="none" stroke="currentColor" strokeOpacity=".1" strokeWidth="14" strokeLinecap="round" />
          {/* Value arc */}
          <path
            d={`M 20 100 A 80 80 0 0 1 180 100`}
            fill="none"
            stroke="var(--color-green-500)"
            strokeWidth="14"
            strokeLinecap="round"
            strokeDasharray={`${dash} ${circ}`}
          />
        </svg>
        <div style={{
          position: 'absolute', left: 0, right: 0, bottom: 0,
          textAlign: 'center',
          fontFamily: 'var(--fontFamily-headings)',
          fontWeight: 700,
          fontSize: 32,
          letterSpacing: '-1px',
          color: 'var(--content-default)',
        }}>{value}%</div>
      </div>
      <div>
        <div style={{ fontFamily: 'var(--fontFamily-headings)', fontWeight: 600, fontSize: 17, color: 'var(--content-default)', letterSpacing: '-.2px', marginBottom: 6 }}>Very good!</div>
        <div style={{ fontFamily: 'var(--fontFamily-body)', fontSize: 13, color: 'var(--content-subtler)', lineHeight: 1.5 }}>BirdseyePost appears in <b style={{ color: 'var(--content-default)', fontWeight: 600 }}>72.2%</b> of AI responses. You're outperforming <b style={{ color: 'var(--content-default)', fontWeight: 600 }}>36%</b> of competitors.</div>
      </div>
    </div>
  </div>;
}

function KpiCard({ label, value, delta, showInfo }) {
  return <div className="kpi">
    <div className="label">
      <span>{label}</span>
      <span className="chev-r"><Icon name="chevron-right" size={13} /></span>
      {showInfo && <Icon name="info" size={12} />}
    </div>
    <div className="val-row">
      <span className="val">{value}</span>
      <span className="delta up">{delta}</span>
    </div>
  </div>;
}

function ShareOfVoiceCard() {
  return <div className="card">
    <div className="card-head">
      <div>
        <h3 className="title">Brand share of voice</h3>
        <p className="sub">Total mentions of your brand vs. tracked</p>
      </div>
      <div className="spacer" />
      <span className="badge success">+12.5%</span>
    </div>
    {/* donut + legend */}
    <div style={{ display: 'grid', gridTemplateColumns: '130px 1fr', gap: 16, alignItems: 'center' }}>
      <Donut segments={[
        { value: 38, color: 'var(--color-purple-300)' },
        { value: 22, color: 'var(--color-cyan-500)' },
        { value: 18, color: 'var(--color-orange-400)' },
        { value: 14, color: 'var(--color-blue-500)' },
        { value: 8,  color: 'var(--color-grey-500)' },
      ]} />
      <div className="col-flex" style={{ gap: 8 }}>
        {[
          { n:'BirdseyePost',      v:'38%', c:'var(--color-purple-300)' },
          { n:'Surfer SEO',        v:'22%', c:'var(--color-cyan-500)' },
          { n:'Clearscope',        v:'18%', c:'var(--color-orange-400)' },
          { n:'Semrush',           v:'14%', c:'var(--color-blue-500)' },
          { n:'Others',            v:'8%',  c:'var(--color-grey-500)' },
        ].map(x => (
          <div key={x.n} style={{ display: 'flex', alignItems: 'center', gap: 8, fontFamily: 'var(--fontFamily-body)', fontSize: 12 }}>
            <span style={{ width: 8, height: 8, borderRadius: 2, background: x.c }} />
            <span style={{ flex: 1, color: 'var(--content-subtle)' }}>{x.n}</span>
            <span style={{ fontFamily: 'var(--font-mono)', color: 'var(--content-default)', fontWeight: 500 }}>{x.v}</span>
          </div>
        ))}
      </div>
    </div>
  </div>;
}

function Donut({ segments }) {
  const r = 46, cx = 60, cy = 60;
  const total = segments.reduce((s, x) => s + x.value, 0);
  let acc = 0;
  const ring = 2 * Math.PI * r;
  return <svg viewBox="0 0 120 120" width="120" height="120" style={{ display:'block' }}>
    <circle cx={cx} cy={cy} r={r} fill="none" stroke="currentColor" strokeOpacity=".08" strokeWidth="16" />
    {segments.map((s, i) => {
      const len = (s.value / total) * ring;
      const dash = `${len} ${ring}`;
      const offset = ring - acc;
      acc += len;
      return <circle
        key={i}
        cx={cx} cy={cy} r={r}
        fill="none"
        stroke={s.color}
        strokeWidth="16"
        strokeDasharray={dash}
        strokeDashoffset={offset}
        transform={`rotate(-90 ${cx} ${cy})`}
      />;
    })}
  </svg>;
}

function LeaderboardCard() {
  const rows = [
    { n: 'BirdseyePost',   score: 72.2, delta: +12.5, you: true },
    { n: 'Surfer SEO',     score: 68.5, delta: +3.2 },
    { n: 'Clearscope',     score: 61.0, delta: -1.8 },
    { n: 'Semrush',        score: 54.4, delta: +0.4 },
    { n: 'Ahrefs',         score: 49.7, delta: -4.2 },
  ];
  return <div className="card">
    <div className="card-head">
      <div>
        <h3 className="title">Competitive leaderboard</h3>
        <p className="sub">Ranking of your brand vs. tracked competitors by discoverability or share of voice</p>
      </div>
      <div className="spacer" />
      <button className="filter-chip" style={{ fontSize: 12, padding: '4px 8px' }}>
        Discoverability <Icon name="chevron-down" className="chev" />
      </button>
    </div>
    <div className="col-flex" style={{ gap: 0 }}>
      {rows.map((r, i) => (
        <div key={r.n} style={{
          display: 'grid',
          gridTemplateColumns: '24px 1fr 60px 48px',
          alignItems: 'center',
          gap: 12,
          padding: '10px 0',
          borderTop: i > 0 ? '1px solid var(--kit-card-border)' : 0,
        }}>
          <span style={{ fontFamily: 'var(--font-mono)', fontSize: 12, color: 'var(--content-subtler)' }}>{String(i + 1).padStart(2, '0')}</span>
          <span style={{ display: 'flex', alignItems: 'center', gap: 8, fontFamily: 'var(--fontFamily-body)', fontSize: 13, fontWeight: r.you ? 600 : 500, color: 'var(--content-default)' }}>
            {r.n}
            {r.you && <span className="badge brand" style={{ fontSize: 10, height: 18, padding: '0 6px' }}>You</span>}
          </span>
          <span style={{ fontFamily: 'var(--font-mono)', fontSize: 13, color: 'var(--content-default)', textAlign: 'right' }}>{r.score}%</span>
          <span className={`delta ${r.delta >= 0 ? 'up' : 'down'}`} style={{ justifySelf: 'end', fontSize: 12 }}>
            {r.delta >= 0 ? '+' : ''}{r.delta}%
          </span>
        </div>
      ))}
    </div>
  </div>;
}

Object.assign(window, { HomeScreen, TrendCard, ScoreCard, KpiCard, ShareOfVoiceCard, LeaderboardCard, Donut });
