/* Root — wires shell + screens + persists route & theme */
const { useState: useStateA, useEffect: useEffectA } = React;

function App() {
  const [route, setRoute]       = useStateA(() => localStorage.getItem('yolando-kit-route') || 'home');
  const [theme, setTheme]       = useStateA(() => localStorage.getItem('yolando-kit-theme') || 'dark');
  const [showHelp, setShowHelp] = useStateA(() => localStorage.getItem('yolando-kit-help') !== '0');

  useEffectA(() => localStorage.setItem('yolando-kit-route', route), [route]);
  useEffectA(() => localStorage.setItem('yolando-kit-help', showHelp ? '1' : '0'), [showHelp]);
  useEffectA(() => {
    localStorage.setItem('yolando-kit-theme', theme);
    document.documentElement.classList.toggle('dark',  theme === 'dark');
    document.documentElement.classList.toggle('light', theme === 'light');
  }, [theme]);

  const SCREEN = {
    home:      HomeScreen,
    prompts:   PromptsScreen,
    citations: CitationsScreen,
    content:   ContentScreen,
  };
  const Screen = SCREEN[route] || (() => <Placeholder route={route} setRoute={setRoute} />);

  return <div className="app-shell">
    <Sidebar
      route={route} setRoute={setRoute}
      theme={theme} setTheme={setTheme}
      showHelp={showHelp} setShowHelp={setShowHelp}
    />
    <div className="main">
      <div className="canvas">
        <Screen />
      </div>
    </div>
  </div>;
}

function Placeholder({ route, setRoute }) {
  const LABELS = { home:'Overview', prompts:'Topics & prompts', citations:'Citations', content:'Content hub' };
  return <div className="page">
    <div className="page-head">
      <h1 style={{ textTransform: 'capitalize' }}>{route.replace(/-/g,' ')}</h1>
      <p>This surface is available in the live app. The kit ships four canonical screens below.</p>
    </div>
    <div className="card" style={{ alignItems:'flex-start', padding: '32px' }}>
      <div style={{ fontFamily:'var(--fontFamily-body)', fontSize: 13, color:'var(--content-subtler)' }}>Jump to a built screen:</div>
      <div className="row-flex" style={{ gap: 8, marginTop: 12 }}>
        {Object.keys(LABELS).map(r => (
          <button key={r} className="btn btn-outline btn-sm" onClick={() => setRoute(r)}>
            {LABELS[r]}
          </button>
        ))}
      </div>
    </div>
  </div>;
}

ReactDOM.createRoot(document.getElementById('root')).render(<App />);
