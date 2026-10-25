import React from 'react'
import { Sparkles, Bot, PlusCircle, CheckCircle2, AlertTriangle, Layers } from 'lucide-react'

export default function Header({ config, onOpenNewProject, activeWorkflow, recentRuns, onSelectWorkflow }) {
  const geminiReady = config?.gemini_configured
  const modelName = config?.model || 'gemini-2.5-flash'

  return (
    <header style={{
      borderBottom: '1px solid var(--border-subtle)',
      background: 'rgba(10, 15, 26, 0.85)',
      backdropFilter: 'blur(12px)',
      position: 'sticky',
      top: 0,
      zIndex: 50,
      padding: '14px 28px',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'space-between',
    }}>
      {/* Brand */}
      <div style={{ display: 'flex', alignItems: 'center', gap: '14px' }}>
        <div style={{
          width: '42px',
          height: '42px',
          borderRadius: '12px',
          background: 'linear-gradient(135deg, #6366f1 0%, #a855f7 100%)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          boxShadow: '0 0 20px rgba(99, 102, 241, 0.4)',
        }}>
          <Bot size={24} color="#ffffff" />
        </div>
        <div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <h1 style={{ fontSize: '1.25rem', fontWeight: '800', letterSpacing: '-0.02em', background: 'linear-gradient(90deg, #fff 0%, #cbd5e1 100%)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent' }}>
              SEAGENT
            </h1>
            <span className="badge badge-indigo">Multi-Agent AI</span>
          </div>
          <p style={{ fontSize: '0.78rem', color: 'var(--text-muted)' }}>
            Autonomous Software Engineering Framework & Lifecycle Pipeline
          </p>
        </div>
      </div>

      {/* Center status: Provider & Model */}
      <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
        <div style={{
          background: 'rgba(255, 255, 255, 0.03)',
          border: '1px solid var(--border-subtle)',
          borderRadius: 'var(--radius-md)',
          padding: '6px 14px',
          display: 'flex',
          alignItems: 'center',
          gap: '10px',
          fontSize: '0.8rem',
        }}>
          <Sparkles size={16} color="#818cf8" />
          <span style={{ color: 'var(--text-muted)' }}>Engine:</span>
          <span style={{ fontWeight: '600', color: 'var(--text-main)', fontFamily: 'var(--font-mono)' }}>
            Google {modelName}
          </span>
          {geminiReady ? (
            <span className="badge badge-emerald" style={{ padding: '2px 8px' }}>
              <CheckCircle2 size={12} /> Key Active
            </span>
          ) : (
            <span className="badge badge-amber" style={{ padding: '2px 8px' }}>
              <AlertTriangle size={12} /> Key Unset (Test Mode Ready)
            </span>
          )}
        </div>

        {/* Recent Workflows dropdown */}
        {recentRuns && recentRuns.length > 0 && (
          <select
            value={activeWorkflow?.workflow_id || ''}
            onChange={(e) => onSelectWorkflow(e.target.value)}
            style={{
              background: 'var(--bg-secondary)',
              color: 'var(--text-main)',
              border: '1px solid var(--border-subtle)',
              borderRadius: 'var(--radius-md)',
              padding: '8px 12px',
              fontSize: '0.82rem',
              cursor: 'pointer',
              outline: 'none',
            }}
          >
            <option value="">Recent Projects ({recentRuns.length})</option>
            {recentRuns.map((run) => (
              <option key={run.workflow_id} value={run.workflow_id}>
                {run.project_name} ({run.status})
              </option>
            ))}
          </select>
        )}

        {/* Primary Action Button */}
        <button className="btn-primary" onClick={onOpenNewProject}>
          <PlusCircle size={17} />
          <span>New Project</span>
        </button>
      </div>
    </header>
  )
}
