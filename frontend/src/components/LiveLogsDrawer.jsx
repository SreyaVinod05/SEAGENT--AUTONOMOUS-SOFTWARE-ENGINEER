import React, { useState } from 'react'
import { Terminal, ChevronUp, ChevronDown, Clock } from 'lucide-react'

export default function LiveLogsDrawer({ logs, isOpenDefault = false }) {
  const [isOpen, setIsOpen] = useState(isOpenDefault)

  if (!logs || logs.length === 0) return null

  return (
    <div style={{
      position: 'fixed',
      bottom: 0,
      left: 0,
      right: 0,
      zIndex: 40,
      background: 'rgba(8, 12, 20, 0.95)',
      backdropFilter: 'blur(16px)',
      borderTop: '1px solid var(--border-subtle)',
      transition: 'all 0.25s ease',
    }}>
      {/* Header bar toggle */}
      <button
        onClick={() => setIsOpen(!isOpen)}
        style={{
          width: '100%',
          padding: '10px 24px',
          background: 'transparent',
          border: 'none',
          color: 'var(--text-main)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          cursor: 'pointer',
          fontSize: '0.85rem',
          fontWeight: '600',
        }}
      >
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          <Terminal size={16} color="#818cf8" />
          <span>Real-Time Multi-Agent Execution Stream ({logs.length} events)</span>
          <span className="badge badge-indigo" style={{ padding: '2px 8px', fontSize: '0.7rem' }}>
            Live
          </span>
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: '8px', color: 'var(--text-muted)' }}>
          <span style={{ fontSize: '0.78rem' }}>{isOpen ? 'Collapse' : 'Expand Logs'}</span>
          {isOpen ? <ChevronDown size={16} /> : <ChevronUp size={16} />}
        </div>
      </button>

      {/* Expanded Logs Panel */}
      {isOpen && (
        <div style={{
          maxHeight: '220px',
          overflowY: 'auto',
          padding: '12px 24px',
          borderTop: '1px solid rgba(255, 255, 255, 0.05)',
          fontFamily: 'var(--font-mono)',
          fontSize: '0.78rem',
          display: 'flex',
          flexDirection: 'column',
          gap: '6px',
        }}>
          {logs.map((log, idx) => {
            const timeStr = log.timestamp?.split('T')?.[1]?.slice(0, 8) || ''
            const isError = log.level === 'ERROR'
            const isWarn = log.level === 'WARNING'

            return (
              <div key={idx} style={{
                display: 'flex',
                alignItems: 'baseline',
                gap: '12px',
                color: isError ? '#fb7185' : isWarn ? '#fbbf24' : '#cbd5e1',
                lineHeight: '1.4',
              }}>
                <span style={{ color: 'var(--text-dim)', flexShrink: 0 }}>
                  [{timeStr}]
                </span>
                <span style={{ color: '#818cf8', fontWeight: '600', flexShrink: 0 }}>
                  [{log.stage}]
                </span>
                <span>{log.message}</span>
              </div>
            )
          })}
        </div>
      )}
    </div>
  )
}
