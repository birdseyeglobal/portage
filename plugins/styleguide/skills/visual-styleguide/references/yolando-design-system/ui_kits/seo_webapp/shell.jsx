/* Sidebar shell — no topbar, title lives in the page */
const { useState: useStateShell } = React;

const NAV_STRUCTURE = [
  {
    id: 'insights', title: 'AI discoverability', icon: 'sparkles',
    items: [
      { id: 'overview',   title: 'Overview',         url: 'home'       },
      { id: 'prompts',    title: 'Topics & prompts', url: 'prompts'    },
      { id: 'platforms',  title: 'Platforms',        url: 'platforms'  },
      { id: 'citations',  title: 'Citations',        url: 'citations'  },
      { id: 'reputation', title: 'Reputation',       url: 'reputation' },
    ],
  },
  {
    id: 'actions', title: 'Marketing studio', icon: 'zap',
    items: [
      { id: 'recs',    title: 'Recommendations', url: 'recs',    badge: 17 },
      { id: 'content', title: 'Content hub',     url: 'content'             },
    ],
  },
];

function Sidebar({ route, setRoute, theme, setTheme, showHelp, setShowHelp }) {
  const [openGroups, setOpenGroups] = useStateShell({ insights: true, actions: false });
  const toggle = id => setOpenGroups(o => ({ ...o, [id]: !o[id] }));

  return <aside className="sidebar">
    <div className="sidebar-header">
      <button className="workspace-switcher">
        <span className="avatar">B</span>
        <div style={{ display: 'flex', flexDirection: 'column', minWidth: 0, flex: 1 }}>
          <span className="ws-name">BirdseyePost</span>
          <span className="ws-meta">birdseyepost.com</span>
        </div>
        <span className="switcher-icons">
          <Icon name="chevrons-up-down" size={14} />
        </span>
      </button>
      <button className="pin-btn" title="Collapse sidebar"><Icon name="panel-left-close" size={15} /></button>
    </div>

    <div className="sidebar-content">
      <div className="nav-group">
        <button
          className={`nav-item${route === 'home' ? ' active' : ''}`}
          onClick={() => setRoute('home')}
        >
          <Icon name="home" />
          <span>Home</span>
        </button>
      </div>

      {NAV_STRUCTURE.map(group => {
        const open = openGroups[group.id];
        const hasActive = group.items.some(it => it.url === route);
        return <div key={group.id} className="nav-group" data-open={open}>
          <button
            className={`nav-item${hasActive && !open ? ' active' : ''}`}
            onClick={() => toggle(group.id)}
          >
            <Icon name={group.icon} />
            <span>{group.title}</span>
            <Icon name="chevron-right" size={13} className="chev" />
          </button>
          {open && <div className="nav-sub">
            {group.items.map(it => (
              <button
                key={it.id}
                className={`nav-item${route === it.url ? ' active' : ''}`}
                onClick={() => setRoute(it.url)}
              >
                <span>{it.title}</span>
                {it.badge && <span className="nav-badge">{it.badge}</span>}
              </button>
            ))}
          </div>}
        </div>;
      })}

      <div className="nav-group">
        <button className="nav-item"><Icon name="radio" /><span>Competitor radar</span></button>
      </div>
    </div>

    {showHelp && <HelpCard onClose={() => setShowHelp(false)} />}

    <div className="sidebar-footer">
      <button className="nav-item quiet">
        <Icon name="message-square" />
        <span>Share feedback</span>
      </button>
      <button className="nav-item quiet">
        <Icon name="book-open" />
        <span>Knowledge base</span>
      </button>
      <button className="nav-item quiet" onClick={() => setTheme(theme === 'dark' ? 'light' : 'dark')} title="Toggle theme">
        <Icon name={theme === 'dark' ? 'sun' : 'moon'} />
        <span>{theme === 'dark' ? 'Light mode' : 'Dark mode'}</span>
      </button>
      <div className="user-card">
        <div className="user-avatar">C</div>
        <span className="name">Corey Tinianov</span>
        <Icon name="chevrons-up-down" size={14} className="chev-r" />
      </div>
    </div>
  </aside>;
}

function HelpCard({ onClose }) {
  return <div className="help-card">
    <button className="hc-close" onClick={onClose} title="Dismiss"><Icon name="x" size={12} /></button>
    <div className="faces">
      <span className="f"></span>
      <span className="f"></span>
    </div>
    <b>We're here to help</b>
    <p>Get personalized support for setup, strategy, and success.</p>
    <button className="hc-cta">Book a demo</button>
  </div>;
}

Object.assign(window, { Sidebar, HelpCard, NAV_STRUCTURE });
