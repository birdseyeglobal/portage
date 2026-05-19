/* Citations — which sources LLMs pull from when talking about you */

function CitationsScreen() {
  const [mode, setMode] = React.useState('domains');

  const domains = [
    { domain: 'birdseyepost.com',         owner: 'owned',      cites: 148, share: 18.4, platforms: ['chatgpt','claude','gemini','perplexity'], trend: 'up' },
    { domain: 'reddit.com/r/marketing',   owner: 'earned',     cites: 94,  share: 11.7, platforms: ['claude','gemini'],                         trend: 'up' },
    { domain: 'g2.com',                   owner: 'earned',     cites: 72,  share: 9.0,  platforms: ['chatgpt','perplexity'],                    trend: 'flat' },
    { domain: 'surferseo.com/blog',       owner: 'competitor', cites: 64,  share: 8.0,  platforms: ['chatgpt','claude'],                        trend: 'up' },
    { domain: 'techcrunch.com',           owner: 'earned',     cites: 48,  share: 6.0,  platforms: ['gemini','perplexity'],                     trend: 'down' },
    { domain: 'x.com/birdseyeglobal',     owner: 'social',     cites: 40,  share: 5.0,  platforms: ['grok','claude'],                           trend: 'up' },
    { domain: 'searchengineland.com',     owner: 'earned',     cites: 36,  share: 4.5,  platforms: ['chatgpt','gemini'],                        trend: 'flat' },
    { domain: 'linkedin.com/company',     owner: 'owned',      cites: 30,  share: 3.7,  platforms: ['claude'],                                  trend: 'up' },
  ];

  const ownerBadge = o => ({
    owned:      <Badge variant="brand">Owned</Badge>,
    earned:     <Badge variant="info">Earned</Badge>,
    competitor: <Badge variant="warn">Competitor</Badge>,
    social:     <Badge variant="success">Social</Badge>,
  }[o]);

  return <div className="page">
    <div className="page-head">
      <div>
        <h1>Citations</h1>
        <p style={{ marginTop: 8 }}>804 citations this month. 18% of them point at your own domains. Reddit and G2 are doing heavy lifting — make them work harder.</p>
      </div>
      <div className="spacer" />
      <Btn variant="outline" size="sm" icon="calendar">Last 30 days</Btn>
      <Btn variant="outline" size="sm" icon="download">Export</Btn>
    </div>

    {/* Share of citations */}
    <div className="card">
      <div className="card-head">
        <div>
          <h3>Share of citations</h3>
          <p className="sub">How often the model pulls from each source category</p>
        </div>
      </div>
      <ShareBar segments={[
        { color: 'var(--color-purple-500)', value: 24 },
        { color: 'var(--color-blue-500)',   value: 38 },
        { color: 'var(--color-orange-500)', value: 22 },
        { color: 'var(--color-green-500)',  value: 16 },
      ]} height={28} />
      <div className="row-flex" style={{ gap: 16, marginTop: 4, fontSize: 12, color: 'var(--content-subtler)' }}>
        <span className="row-flex" style={{ gap: 6 }}><span style={{ width: 10, height: 10, background: 'var(--color-purple-500)', borderRadius: 2 }} /> Owned 24%</span>
        <span className="row-flex" style={{ gap: 6 }}><span style={{ width: 10, height: 10, background: 'var(--color-blue-500)', borderRadius: 2 }} /> Earned 38%</span>
        <span className="row-flex" style={{ gap: 6 }}><span style={{ width: 10, height: 10, background: 'var(--color-orange-500)', borderRadius: 2 }} /> Competitor 22%</span>
        <span className="row-flex" style={{ gap: 6 }}><span style={{ width: 10, height: 10, background: 'var(--color-green-500)', borderRadius: 2 }} /> Social 16%</span>
      </div>
    </div>

    {/* Drill-down tabs */}
    <div className="tabs">
      {[
        { id: 'domains', label: 'Domains', n: 42 },
        { id: 'pages',   label: 'Pages',   n: 188 },
        { id: 'prompts', label: 'Prompts', n: 74 },
        { id: 'topics',  label: 'Topics',  n: 24 },
      ].map(t => (
        <div key={t.id} className={`tab${mode === t.id ? ' active' : ''}`} onClick={() => setMode(t.id)}>
          {t.label} <span style={{ color: 'var(--content-subtlest)', fontFamily: 'var(--font-mono)', marginLeft: 4, fontSize: 11 }}>{t.n}</span>
        </div>
      ))}
    </div>

    <div className="card" style={{ padding: 0, overflow: 'hidden' }}>
      <table className="tbl">
        <thead>
          <tr>
            <th style={{ width: '34%' }}>Source</th>
            <th>Owner</th>
            <th>Citations</th>
            <th>Share</th>
            <th>Platforms</th>
            <th>Trend</th>
            <th style={{ width: 40 }}></th>
          </tr>
        </thead>
        <tbody>
          {domains.map((r, i) => (
            <tr key={i}>
              <td>
                <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
                  <div style={{ width: 28, height: 28, borderRadius: 6, background: 'var(--bg-bolder)', display: 'flex', alignItems: 'center', justifyContent: 'center', color: 'var(--content-subtler)' }}>
                    <Icon name="globe" size={14} />
                  </div>
                  <div>
                    <div style={{ fontFamily: 'var(--fontFamily-headings)', fontWeight: 500, fontSize: 13, letterSpacing: '-.14px' }}>{r.domain}</div>
                  </div>
                </div>
              </td>
              <td>{ownerBadge(r.owner)}</td>
              <td className="mono">{r.cites}</td>
              <td>
                <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                  <span style={{ fontFamily: 'var(--font-mono)', fontSize: 12, color: 'var(--content-default)' }}>{r.share}%</span>
                  <div style={{ width: 48, height: 6, background: 'var(--bg-bolder)', borderRadius: 3 }}>
                    <div style={{ width: `${Math.min(r.share * 4, 100)}%`, height: '100%', background: 'var(--color-purple-500)', borderRadius: 3 }} />
                  </div>
                </div>
              </td>
              <td>
                <div className="row-flex" style={{ gap: 3 }}>
                  {r.platforms.map(p => <span key={p} className="platform-dot" style={{ background: PLATFORMS[p].color, width: 16, height: 16, fontSize: 9 }}>{PLATFORMS[p].code}</span>)}
                </div>
              </td>
              <td>
                <span className="row-flex" style={{ gap: 4, fontFamily: 'var(--font-mono)', fontSize: 12, color: r.trend === 'up' ? 'var(--content-success)' : r.trend === 'down' ? 'var(--content-destructive)' : 'var(--content-subtler)' }}>
                  <Icon name={r.trend === 'up' ? 'trending-up' : r.trend === 'down' ? 'trending-down' : 'minus'} size={12} />
                  {r.trend}
                </span>
              </td>
              <td><button className="icon-btn"><Icon name="external-link" size={14} /></button></td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>

    {/* Recent citations feed */}
    <div className="card">
      <div className="card-head">
        <div>
          <h3>Recent citations</h3>
          <p className="sub">Live feed — last 24 hours</p>
        </div>
        <div className="spacer" />
        <Btn variant="ghost" size="sm" iconRight="arrow-right">See all</Btn>
      </div>
      {[
        { p: 'claude',  src: 'birdseyepost.com/geo-guide',        prompt: 'best AI SEO tools 2026',          ago: '2m'  },
        { p: 'chatgpt', src: 'reddit.com/r/marketing/…/ai-seo',    prompt: 'track brand mentions in AI search', ago: '8m' },
        { p: 'perplexity', src: 'g2.com/products/yolando',         prompt: 'AI visibility platform comparison', ago: '14m' },
        { p: 'gemini',  src: 'techcrunch.com/birdseye-raises…',    prompt: 'what is generative engine optimization', ago: '22m' },
      ].map((c, i) => (
        <div key={i} style={{
          display: 'grid', gridTemplateColumns: '24px 1fr auto auto', gap: 12, alignItems: 'center',
          padding: '10px 0', borderTop: i > 0 ? '1px solid var(--border-subtle)' : 0, fontSize: 13
        }}>
          <span className="platform-dot" style={{ background: PLATFORMS[c.p].color, width: 20, height: 20, fontSize: 9 }}>{PLATFORMS[c.p].code}</span>
          <div style={{ minWidth: 0 }}>
            <div style={{ fontFamily: 'var(--fontFamily-body)', fontSize: 13, color: 'var(--content-default)', lineHeight: 1.4 }}>
              <b style={{ fontWeight: 600 }}>{PLATFORMS[c.p].name}</b> cited <span style={{ color: 'var(--content-brand)', fontFamily: 'var(--fontFamily-headings)', fontWeight: 500 }}>{c.src}</span>
            </div>
            <div style={{ fontFamily: 'var(--fontFamily-body)', fontSize: 12, color: 'var(--content-subtler)', marginTop: 2 }}>
              in response to "<span style={{ fontStyle: 'italic' }}>{c.prompt}</span>"
            </div>
          </div>
          <span style={{ fontFamily: 'var(--font-mono)', fontSize: 11, color: 'var(--content-subtlest)' }}>{c.ago} ago</span>
          <button className="icon-btn"><Icon name="external-link" size={14} /></button>
        </div>
      ))}
    </div>
  </div>;
}

Object.assign(window, { CitationsScreen });
