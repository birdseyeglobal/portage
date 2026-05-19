/* Reusable primitives — exported to window for other Babel scripts */
const { useState, useEffect, useRef } = React;

function Icon({ name, size = 16, className = '', style = {} }) {
  const ref = useRef(null);
  useEffect(() => {
    if (ref.current && window.lucide) {
      ref.current.innerHTML = '';
      const i = document.createElement('i');
      i.setAttribute('data-lucide', name);
      ref.current.appendChild(i);
      window.lucide.createIcons({ nameAttr: 'data-lucide' });
    }
  }, [name]);
  return <span ref={ref} className={className} style={{ display: 'inline-flex', width: size, height: size, ...style }}>
    <i data-lucide={name} style={{ width: size, height: size }}></i>
  </span>;
}

function Btn({ variant = 'primary', size, icon, iconRight, children, ...rest }) {
  const cls = `btn btn-${variant}${size === 'sm' ? ' btn-sm' : ''}`;
  return <button className={cls} {...rest}>
    {icon && <Icon name={icon} size={size === 'sm' ? 14 : 16} />}
    {children}
    {iconRight && <Icon name={iconRight} size={size === 'sm' ? 14 : 16} />}
  </button>;
}

function Chip({ children, selected, platform, dot, onClick }) {
  return <button
    className={`chip${selected ? ' selected' : ''}`}
    onClick={onClick}
    style={{ cursor: onClick ? 'pointer' : 'default' }}
  >
    {platform && <span className="platform-dot" style={{ background: platform.color }}>{platform.code}</span>}
    {dot && <span className="platform-dot" style={{ background: dot }} />}
    {children}
  </button>;
}

function Badge({ variant = 'muted', children, icon }) {
  return <span className={`badge ${variant}`}>
    {icon && <Icon name={icon} size={11} />}
    {children}
  </span>;
}

// LLM platform palette
const PLATFORMS = {
  chatgpt:    { code: 'CG', color: '#10A37F', name: 'ChatGPT'    },
  claude:     { code: 'CL', color: '#D77655', name: 'Claude'     },
  gemini:     { code: 'GM', color: '#4285F4', name: 'Gemini'     },
  perplexity: { code: 'PX', color: '#20808D', name: 'Perplexity' },
  grok:       { code: 'GR', color: '#161518', name: 'Grok'       },
};

// Sparkline — simple SVG path
function Sparkline({ data, width = 100, height = 28, color = 'var(--color-purple-300)' }) {
  const max = Math.max(...data), min = Math.min(...data);
  const span = max - min || 1;
  const pts = data.map((v, i) => {
    const x = (i / (data.length - 1)) * width;
    const y = height - ((v - min) / span) * height;
    return `${x.toFixed(1)},${y.toFixed(1)}`;
  }).join(' ');
  return <svg width={width} height={height} style={{ display: 'block' }}>
    <polyline points={pts} fill="none" stroke={color} strokeWidth="1.5" strokeLinejoin="round" strokeLinecap="round" />
  </svg>;
}

// Stacked bar segment — platform share of voice
function ShareBar({ segments, height = 20 }) {
  const total = segments.reduce((s, seg) => s + seg.value, 0);
  return <div style={{ display: 'flex', height, borderRadius: 6, overflow: 'hidden', background: 'var(--bg-bolder)', width: '100%' }}>
    {segments.map((seg, i) => (
      <div key={i} style={{
        background: seg.color, width: `${(seg.value / total) * 100}%`,
        display: 'flex', alignItems: 'center', justifyContent: 'center',
        color: '#fff', fontFamily: 'var(--font-mono)', fontSize: 10, fontWeight: 500, minWidth: 0
      }}>
        {(seg.value / total) > 0.08 && `${Math.round((seg.value/total)*100)}%`}
      </div>
    ))}
  </div>;
}

// Big line chart — simulated visibility over time
function AreaChart({ series, width = 760, height = 220 }) {
  const allValues = series.flatMap(s => s.data);
  const max = Math.max(...allValues), min = Math.min(...allValues);
  const pad = { t: 12, r: 8, b: 24, l: 32 };
  const w = width - pad.l - pad.r;
  const h = height - pad.t - pad.b;
  const span = max - min || 1;
  const n = series[0].data.length;
  const xAt = i => pad.l + (i / (n - 1)) * w;
  const yAt = v => pad.t + h - ((v - min) / span) * h;
  const gridY = [0, .25, .5, .75, 1].map(t => pad.t + h * t);

  return <svg width={width} height={height} style={{ display: 'block', maxWidth: '100%' }}>
    {gridY.map((y, i) => <line key={i} x1={pad.l} x2={pad.l + w} y1={y} y2={y} stroke="var(--border-subtle)" strokeDasharray="2,3" />)}
    {[0, .25, .5, .75, 1].map((t, i) => {
      const v = max - (max - min) * t;
      return <text key={i} x={pad.l - 6} y={pad.t + h * t + 4} fontSize="10" fill="var(--content-subtlest)" textAnchor="end" fontFamily="var(--font-mono)">{Math.round(v)}</text>;
    })}
    {series.map((s, si) => {
      const pts = s.data.map((v, i) => `${xAt(i)},${yAt(v)}`).join(' L');
      return <g key={s.label}>
        {s.fill && <path d={`M${pad.l},${pad.t + h} L${pts} L${pad.l + w},${pad.t + h} Z`} fill={s.color} opacity="0.1" />}
        <path d={`M${pts}`} fill="none" stroke={s.color} strokeWidth="2" strokeLinejoin="round" strokeLinecap="round" />
      </g>;
    })}
    {/* x-axis labels */}
    {['Mon','Tue','Wed','Thu','Fri','Sat','Sun'].map((lbl, i) => {
      const x = xAt((i / 6) * (n - 1));
      return <text key={lbl} x={x} y={height - 6} fontSize="10" fill="var(--content-subtlest)" textAnchor="middle" fontFamily="var(--fontFamily-body)">{lbl}</text>;
    })}
  </svg>;
}

Object.assign(window, { Icon, Btn, Chip, Badge, Sparkline, ShareBar, AreaChart, PLATFORMS });
