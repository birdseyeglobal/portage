/* Prompts — topic/prompt explorer */

function PromptsScreen() {
  const [activeTab, setActiveTab] = React.useState('prompts');
  const [selPlatforms, setSelPlatforms] = React.useState(['chatgpt','claude','gemini','perplexity']);
  const togglePlat = id => setSelPlatforms(arr => arr.includes(id) ? arr.filter(p => p !== id) : [...arr, id]);

  const prompts = [
    { prompt: 'best AI SEO tools 2026',               topic: 'GEO tooling',    vis: 68, men: '14/20', cit: 11, trend: [40,42,48,55,60,62,65,68], platforms: ['chatgpt','claude','perplexity'] },
    { prompt: 'how to rank in ChatGPT answers',       topic: 'GEO tactics',    vis: 54, men: '11/20', cit: 7,  trend: [48,50,49,52,51,53,52,54], platforms: ['chatgpt','gemini'] },
    { prompt: 'AI visibility platform comparison',    topic: 'Competitor',     vis: 82, men: '18/20', cit: 15, trend: [60,65,70,72,75,78,80,82], platforms: ['chatgpt','claude','gemini','perplexity'] },
    { prompt: 'brand mentions in LLMs',               topic: 'GEO awareness',  vis: 41, men: '9/20',  cit: 4,  trend: [38,40,39,42,40,41,42,41], platforms: ['claude','gemini'] },
    { prompt: 'track brand in AI search',             topic: 'GEO tooling',    vis: 37, men: '8/20',  cit: 3,  trend: [22,25,30,31,34,35,36,37], platforms: ['chatgpt','perplexity'] },
    { prompt: 'generative engine optimization agency', topic: 'GEO services',  vis: 12, men: '3/20',  cit: 1,  trend: [8,9,10,11,10,11,12,12], platforms: ['claude'] },
    { prompt: 'answer engine optimization vs SEO',    topic: 'GEO education',  vis: 64, men: '13/20', cit: 9,  trend: [52,55,58,60,62,63,64,64], platforms: ['chatgpt','claude','gemini'] },
    { prompt: 'is Birdseye legit',                    topic: 'Brand',          vis: 88, men: '19/20', cit: 18, trend: [75,80,82,84,85,86,87,88], platforms: ['chatgpt','claude','gemini','perplexity','grok'] },
  ];

  return <div className="page">
    <div className="page-head">
      <div>
        <h1>Topics & prompts</h1>
        <p style={{ marginTop: 8 }}>1,248 prompts across 24 topics. You're winning on brand. Category prompts still have room.</p>
      </div>
      <div className="spacer" />
      <Btn variant="outline" size="sm" icon="upload">Import CSV</Btn>
      <Btn icon="plus" size="sm">Add prompt</Btn>
    </div>

    <div className="tabs">
      {['Prompts','Topics','Personas','Regions'].map(t => (
        <div key={t} className={`tab${activeTab === t.toLowerCase() ? ' active' : ''}`} onClick={() => setActiveTab(t.toLowerCase())}>{t}</div>
      ))}
    </div>

    {/* Filter bar */}
    <div className="card compact" style={{ gap: 10 }}>
      <div className="row-flex" style={{ gap: 8 }}>
        <span style={{ fontFamily: 'var(--fontFamily-headings)', fontWeight: 600, fontSize: 12, color: 'var(--content-subtlest)', textTransform: 'uppercase', letterSpacing: '.08em' }}>Platforms</span>
        {Object.entries(PLATFORMS).map(([id, p]) => (
          <Chip key={id} platform={p} selected={selPlatforms.includes(id)} onClick={() => togglePlat(id)}>{p.name}</Chip>
        ))}
        <div className="spacer" style={{ flex: 1 }} />
        <Btn variant="ghost" size="sm" icon="filter">More filters</Btn>
      </div>
    </div>

    <div className="card" style={{ padding: 0, overflow: 'hidden' }}>
      <table className="tbl">
        <thead>
          <tr>
            <th style={{ width: '32%' }}>Prompt</th>
            <th>Topic</th>
            <th>Visibility</th>
            <th>Mentions</th>
            <th>Citations</th>
            <th>Platforms</th>
            <th style={{ width: 100 }}>Trend</th>
            <th style={{ width: 40 }}></th>
          </tr>
        </thead>
        <tbody>
          {prompts.map((r, i) => (
            <tr key={i}>
              <td>
                <div style={{ fontFamily: 'var(--fontFamily-headings)', fontWeight: 500, fontSize: 13, letterSpacing: '-.14px' }}>"{r.prompt}"</div>
              </td>
              <td><Badge variant={r.topic === 'Brand' ? 'brand' : 'muted'}>{r.topic}</Badge></td>
              <td>
                <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                  <span style={{ fontFamily: 'var(--font-mono)', fontSize: 12, fontWeight: 500, color: 'var(--content-default)', minWidth: 24 }}>{r.vis}</span>
                  <div style={{ width: 56, height: 6, background: 'var(--bg-bolder)', borderRadius: 3, overflow: 'hidden' }}>
                    <div style={{ width: `${r.vis}%`, height: '100%', background: r.vis > 60 ? 'var(--color-green-500)' : r.vis > 40 ? 'var(--color-yellow-300)' : 'var(--color-orange-400)' }} />
                  </div>
                </div>
              </td>
              <td className="mono">{r.men}</td>
              <td className="mono">{r.cit}</td>
              <td>
                <div className="row-flex" style={{ gap: 3 }}>
                  {r.platforms.map(p => <span key={p} className="platform-dot" style={{ background: PLATFORMS[p].color, width: 16, height: 16, fontSize: 9 }}>{PLATFORMS[p].code}</span>)}
                </div>
              </td>
              <td><Sparkline data={r.trend} width={80} height={24} color={r.trend[r.trend.length-1] > r.trend[0] ? 'var(--color-green-400)' : 'var(--color-grey-400)'} /></td>
              <td><button className="icon-btn"><Icon name="more-horizontal" size={14} /></button></td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  </div>;
}

Object.assign(window, { PromptsScreen });
