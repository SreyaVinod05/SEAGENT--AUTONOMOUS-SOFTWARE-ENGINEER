import React, { useState } from 'react'
import { BookOpen, Copy, Check, Terminal, FileText, CheckCircle2 } from 'lucide-react'

export default function DocumentationTab({ documentation }) {
  const [copied, setCopied] = useState(false)

  if (!documentation) {
    return (
      <div className="glass-panel" style={{ padding: '40px', textAlign: 'center', color: 'var(--text-muted)' }}>
        Documentation synthesis not yet generated.
      </div>
    )
  }

  const handleCopyReadme = () => {
    if (documentation.readme_markdown) {
      navigator.clipboard.writeText(documentation.readme_markdown)
      setCopied(true)
      setTimeout(() => setCopied(false), 2000)
    }
  }

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
      {/* README Header Card */}
      <div className="glass-panel" style={{ padding: '24px' }}>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '14px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
            <BookOpen size={20} color="#6366f1" />
            <h3 style={{ fontSize: '1.15rem', fontWeight: '700', color: 'var(--text-main)' }}>
              Project Documentation & GitHub README.md
            </h3>
          </div>

          <button className="btn-secondary" onClick={handleCopyReadme}>
            {copied ? <Check size={14} color="#34d399" /> : <Copy size={14} />}
            <span>{copied ? 'Copied Markdown!' : 'Copy README.md'}</span>
          </button>
        </div>

        <p style={{ color: 'var(--text-muted)', fontSize: '0.9rem', lineHeight: '1.6' }}>
          {documentation.project_overview}
        </p>
      </div>

      {/* Structured Guides: Setup & Testing */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(360px, 1fr))', gap: '20px' }}>
        <div className="glass-panel" style={{ padding: '24px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '12px' }}>
            <Terminal size={18} color="#34d399" />
            <h4 style={{ fontSize: '1rem', fontWeight: '700', color: 'var(--text-main)' }}>
              Setup & Installation Guide
            </h4>
          </div>
          <div className="code-container" style={{ padding: '12px', whiteSpace: 'pre-wrap' }}>
            {documentation.setup_instructions}
          </div>
        </div>

        <div className="glass-panel" style={{ padding: '24px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '12px' }}>
            <CheckCircle2 size={18} color="#818cf8" />
            <h4 style={{ fontSize: '1rem', fontWeight: '700', color: 'var(--text-main)' }}>
              Automated Testing Guide
            </h4>
          </div>
          <div className="code-container" style={{ padding: '12px', whiteSpace: 'pre-wrap' }}>
            {documentation.testing_guide}
          </div>
        </div>
      </div>

      {/* Full Rendered README Markdown Viewer */}
      <div className="glass-panel" style={{ padding: '24px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '16px' }}>
          <FileText size={18} color="#f59e0b" />
          <h4 style={{ fontSize: '1rem', fontWeight: '700', color: 'var(--text-main)' }}>
            Rendered README.md Content
          </h4>
        </div>

        <div className="code-container" style={{ padding: '20px', maxHeight: '520px', lineHeight: '1.7' }}>
          <pre style={{ margin: 0, whiteSpace: 'pre-wrap', color: '#e2e8f0', fontFamily: 'var(--font-mono)' }}>
            <code>{documentation.readme_markdown}</code>
          </pre>
        </div>
      </div>
    </div>
  )
}
