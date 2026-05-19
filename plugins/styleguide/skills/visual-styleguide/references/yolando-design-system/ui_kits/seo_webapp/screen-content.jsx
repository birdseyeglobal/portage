/* Content hub — marketing studio chat + editor layout */

function ContentScreen() {
  const [msg, setMsg] = React.useState('');

  return <div className="page" style={{ maxWidth: 1280 }}>
    <div className="page-head">
      <div>
        <h1>Content hub</h1>
        <p style={{ marginTop: 8 }}>Drafts, briefs, and edits — grounded in your knowledge base and the prompts you're losing.</p>
      </div>
      <div className="spacer" />
      <Btn variant="outline" size="sm" icon="folder">My drafts · 12</Btn>
      <Btn icon="sparkles" size="sm">New from gap</Btn>
    </div>

    {/* Two-pane: chat on left, draft on right */}
    <div style={{ display: 'grid', gridTemplateColumns: '380px 1fr', gap: 12, height: 'calc(100vh - 220px)' }}>
      {/* Chat pane */}
      <div className="card" style={{ padding: 0, overflow: 'hidden', display: 'flex', flexDirection: 'column' }}>
        <div style={{ padding: '16px 18px', borderBottom: '1px solid var(--border-subtle)', display: 'flex', alignItems: 'center', gap: 10 }}>
          <div style={{ width: 32, height: 32, borderRadius: 8, background: 'var(--color-purpleAlpha-100)', color: 'var(--content-brand)', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
            <Icon name="sparkles" size={16} />
          </div>
          <div style={{ flex: 1 }}>
            <div style={{ fontFamily: 'var(--fontFamily-headings)', fontWeight: 600, fontSize: 14, color: 'var(--content-default)', letterSpacing: '-.14px' }}>Yolando Studio</div>
            <div style={{ fontFamily: 'var(--fontFamily-body)', fontSize: 12, color: 'var(--content-subtler)' }}>Grounded in your brand voice + KB</div>
          </div>
          <button className="icon-btn"><Icon name="more-horizontal" size={14} /></button>
        </div>

        <div style={{ flex: 1, overflowY: 'auto', padding: 16, display: 'flex', flexDirection: 'column', gap: 14, minHeight: 0 }}>
          <div style={{ fontFamily: 'var(--font-mono)', fontSize: 10, color: 'var(--content-subtlest)', textTransform: 'uppercase', letterSpacing: '.1em', textAlign: 'center' }}>Today · 10:42</div>

          <Msg role="user" text="Write an explainer for 'generative engine optimization vs SEO'. Competitors rank zero on Perplexity for this." />
          <Msg role="ai" text={<>Here's a draft — <b>"GEO vs SEO: What actually changed"</b>. I pulled three data points from your KB and kept the voice punchy. Opening line nods to your tagline. Ready to edit on the right?<div style={{ marginTop: 10, display: 'flex', gap: 8, flexWrap: 'wrap' }}>
            <Chip dot="#6d65e1">Draft created</Chip>
            <Chip>1,240 words</Chip>
            <Chip>3 citations</Chip>
          </div></>} />
          <Msg role="user" text="Make the intro sharper. And add a quick frame for marketing leaders who think this is hype." />
          <Msg role="ai" text="On it. New intro ends on 'AI changed the game. SEO didn't'. Added a 'Why this isn't hype' callout after the first H2. Diff is live in the editor." />
        </div>

        <div style={{ padding: 12, borderTop: '1px solid var(--border-subtle)' }}>
          <div style={{ display: 'flex', alignItems: 'flex-end', gap: 8, padding: '8px 10px', background: 'var(--bg-input-field-default)', border: '1px solid var(--border-input)', borderRadius: 12 }}>
            <input
              value={msg}
              onChange={e => setMsg(e.target.value)}
              placeholder="Ask anything"
              style={{ flex: 1, background: 'transparent', border: 0, outline: 'none', fontFamily: 'var(--fontFamily-body)', fontSize: 14, color: 'var(--content-default)', padding: '6px 0' }}
            />
            <button className="icon-btn" title="Attach"><Icon name="paperclip" size={14} /></button>
            <button className="icon-btn" style={{ background: msg ? 'var(--bg-brand)' : 'var(--bg-bolder)', color: msg ? '#000' : 'var(--content-subtlest)' }}>
              <Icon name="arrow-up" size={14} />
            </button>
          </div>
          <div className="row-flex" style={{ gap: 6, marginTop: 8 }}>
            <Chip>+ Use brand voice</Chip>
            <Chip>+ Ground in KB</Chip>
            <Chip>+ Include citations</Chip>
          </div>
        </div>
      </div>

      {/* Editor pane */}
      <div className="card" style={{ padding: 0, overflow: 'hidden', display: 'flex', flexDirection: 'column' }}>
        <div style={{ padding: '12px 18px', borderBottom: '1px solid var(--border-subtle)', display: 'flex', alignItems: 'center', gap: 10 }}>
          <div style={{ flex: 1 }}>
            <div style={{ fontFamily: 'var(--fontFamily-headings)', fontWeight: 600, fontSize: 14, color: 'var(--content-default)', letterSpacing: '-.14px' }}>
              GEO vs SEO: What actually changed
            </div>
            <div className="row-flex" style={{ gap: 8, fontSize: 11, color: 'var(--content-subtler)', marginTop: 2 }}>
              <span>Draft</span>
              <span>·</span>
              <span>Saved 12s ago</span>
              <span>·</span>
              <span>1,240 words</span>
            </div>
          </div>
          <Btn variant="ghost" size="sm" icon="history">Versions</Btn>
          <Btn variant="outline" size="sm" icon="eye">Preview</Btn>
          <Btn size="sm" icon="send">Publish</Btn>
        </div>

        {/* Toolbar */}
        <div style={{ padding: '6px 10px', borderBottom: '1px solid var(--border-subtle)', display: 'flex', gap: 2, alignItems: 'center' }}>
          {['bold','italic','underline'].map(t => <button key={t} className="icon-btn"><Icon name={t} size={14} /></button>)}
          <div style={{ width: 1, height: 18, background: 'var(--border-subtle)', margin: '0 4px' }} />
          {['heading-1','heading-2','list','list-ordered','quote'].map(t => <button key={t} className="icon-btn"><Icon name={t} size={14} /></button>)}
          <div style={{ width: 1, height: 18, background: 'var(--border-subtle)', margin: '0 4px' }} />
          {['link','image','code'].map(t => <button key={t} className="icon-btn"><Icon name={t} size={14} /></button>)}
          <div style={{ flex: 1 }} />
          <Btn variant="ghost" size="sm" icon="sparkles">Rewrite</Btn>
        </div>

        <div style={{ flex: 1, overflowY: 'auto', padding: '32px 48px', minHeight: 0, fontFamily: 'var(--fontFamily-body)' }}>
          <h1 style={{ fontFamily: 'var(--fontFamily-headings)', fontWeight: 700, fontSize: 32, letterSpacing: '-.48px', color: 'var(--content-default)', margin: '0 0 8px', lineHeight: 1.15 }}>
            GEO vs SEO: What actually changed
          </h1>
          <p style={{ fontSize: 15, color: 'var(--content-subtler)', margin: '0 0 24px', lineHeight: 1.5 }}>
            AI changed the game. SEO didn't.
          </p>

          <p style={{ fontSize: 15, color: 'var(--content-default)', lineHeight: 1.65, margin: '0 0 16px' }}>
            For twenty years, the question was: <i>will Google rank my page?</i> Now half your prospects are asking Claude, ChatGPT, and Perplexity instead — and those models don't rank pages. They cite sources, synthesize answers, and move on.
          </p>

          <p style={{ fontSize: 15, color: 'var(--content-default)', lineHeight: 1.65, margin: '0 0 16px', background: 'var(--color-purpleAlpha-100)', padding: '12px 16px', borderLeft: '3px solid var(--color-purple-500)', borderRadius: '4px 8px 8px 4px' }}>
            <b style={{ fontWeight: 600 }}>Why this isn't hype.</b> <span style={{ color: 'var(--content-brand)', fontFamily: 'var(--fontFamily-headings)', fontWeight: 600, fontSize: 12, letterSpacing: '.04em', textTransform: 'uppercase' }}>AI suggestion</span><br />
            34% of B2B research traffic already starts in an LLM, per Yolando data. If you're not inside the answer, you're not in the shortlist.
          </p>

          <h2 style={{ fontFamily: 'var(--fontFamily-headings)', fontWeight: 700, fontSize: 22, letterSpacing: '-.24px', color: 'var(--content-default)', margin: '28px 0 12px' }}>
            The three shifts
          </h2>

          <p style={{ fontSize: 15, color: 'var(--content-default)', lineHeight: 1.65, margin: '0 0 16px' }}>
            SEO optimized for <b>clicks</b>. GEO optimizes for <b>being cited</b> — the model's footnote, not your banner. The craft rotates in three ways:
          </p>

          <ol style={{ fontSize: 15, color: 'var(--content-default)', lineHeight: 1.65, paddingLeft: 22, margin: '0 0 16px' }}>
            <li style={{ marginBottom: 6 }}>Answers over keywords. Write like a senior analyst, not a marketer.</li>
            <li style={{ marginBottom: 6 }}>Facts the model can <i>lift</i>. Numbers, named people, direct quotes.</li>
            <li>Distribution to the corpus. Reddit, G2, Wikipedia — wherever the model trained.</li>
          </ol>

          <div style={{ marginTop: 24, padding: 14, background: 'var(--bg-bold)', borderRadius: 8, border: '1px dashed var(--border-default)', fontSize: 13, color: 'var(--content-subtler)' }}>
            ✶ Continue writing, or ask Yolando to draft the next section…
          </div>
        </div>
      </div>
    </div>
  </div>;
}

function Msg({ role, text }) {
  if (role === 'user') {
    return <div style={{ alignSelf: 'flex-end', maxWidth: '80%' }}>
      <div style={{ background: 'var(--bg-brand)', color: 'var(--content-button-primary)', padding: '10px 14px', borderRadius: '16px 16px 2px 16px', fontSize: 13, lineHeight: 1.45, fontFamily: 'var(--fontFamily-body)' }}>
        {text}
      </div>
    </div>;
  }
  return <div style={{ alignSelf: 'flex-start', maxWidth: '90%' }}>
    <div style={{ display: 'flex', gap: 8, alignItems: 'flex-start' }}>
      <div style={{ width: 24, height: 24, borderRadius: 6, background: 'var(--color-purpleAlpha-100)', color: 'var(--content-brand)', display: 'flex', alignItems: 'center', justifyContent: 'center', flexShrink: 0, marginTop: 2 }}>
        <Icon name="sparkles" size={12} />
      </div>
      <div style={{ fontFamily: 'var(--fontFamily-body)', fontSize: 13, color: 'var(--content-default)', lineHeight: 1.5 }}>
        {text}
      </div>
    </div>
  </div>;
}

Object.assign(window, { ContentScreen });
