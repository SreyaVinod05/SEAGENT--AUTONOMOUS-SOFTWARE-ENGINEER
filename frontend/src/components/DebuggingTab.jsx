import React from 'react'
import { Bug, CheckCircle, ArrowRight, FileCode, Wrench, ShieldCheck } from 'lucide-react'

export default function DebuggingTab({ debuggingHistory, retryCount }) {
  if (!debuggingHistory || debuggingHistory.length === 0) {
    return (
      <div className="glass-panel" style={{ padding: '40px', textAlign: 'center', color: 'var(--text-muted)' }}>
        <CheckCircle size={32} color="#34d399" style={{ margin: '0 auto 12px' }} />
        <h3 style={{ fontSize: '1.1rem', fontWeight: '700', color: 'var(--text-main)', marginBottom: '4px' }}>
          No Debugging Cycles Triggered
        </h3>
        <p style={{ fontSize: '0.85rem' }}>
          All automated tests passed on initial execution without requiring diagnostic intervention.
        </p>
      </div>
    )
  }

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
      <div className="glass-panel" style={{ padding: '24px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '8px' }}>
          <Bug size={20} color="#f59e0b" />
          <h3 style={{ fontSize: '1.15rem', fontWeight: '700', color: 'var(--text-main)' }}>
            Autonomous Debugging & Patch History ({debuggingHistory.length} Iterations)
          </h3>
        </div>
        <p style={{ color: 'var(--text-muted)', fontSize: '0.88rem' }}>
          When unit tests fail during execution, the DebuggingAgent autonomously inspects the traceback,
          diagnoses the root cause, applies code corrections, and dispatches the patched codebase for re-testing.
        </p>
      </div>

      {debuggingHistory.map((entry, idx) => (
        <div key={idx} className="glass-panel" style={{ padding: '24px', borderLeft: '4px solid #f59e0b' }}>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '14px' }}>
            <span className="badge badge-amber">Iteration {idx + 1} Diagnostic</span>
            {entry.affected_files?.length > 0 && (
              <span style={{ fontSize: '0.78rem', color: 'var(--text-dim)', fontFamily: 'var(--font-mono)' }}>
                Target: {entry.affected_files.join(', ')}
              </span>
            )}
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '14px' }}>
            {/* Root Cause */}
            <div style={{ background: 'rgba(244, 63, 94, 0.06)', padding: '14px', borderRadius: 'var(--radius-sm)', border: '1px solid rgba(244, 63, 94, 0.2)' }}>
              <div style={{ fontSize: '0.8rem', fontWeight: '700', color: '#fb7185', marginBottom: '4px', display: 'flex', alignItems: 'center', gap: '6px' }}>
                <Bug size={14} /> Root Cause Analysis
              </div>
              <div style={{ fontSize: '0.85rem', color: '#e2e8f0', lineHeight: '1.5' }}>
                {entry.root_cause}
              </div>
            </div>

            {/* Proposed Fix */}
            <div style={{ background: 'rgba(16, 185, 129, 0.06)', padding: '14px', borderRadius: 'var(--radius-sm)', border: '1px solid rgba(16, 185, 129, 0.2)' }}>
              <div style={{ fontSize: '0.8rem', fontWeight: '700', color: '#34d399', marginBottom: '4px', display: 'flex', alignItems: 'center', gap: '6px' }}>
                <Wrench size={14} /> Applied Architectural Correction
              </div>
              <div style={{ fontSize: '0.85rem', color: '#e2e8f0', lineHeight: '1.5' }}>
                {entry.proposed_fix}
              </div>
            </div>

            {/* Corrected Files */}
            {entry.corrected_files?.length > 0 && (
              <div>
                <div style={{ fontSize: '0.8rem', fontWeight: '600', color: 'var(--text-muted)', marginBottom: '8px' }}>
                  Patched Source Files:
                </div>
                <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px' }}>
                  {entry.corrected_files.map((cf, cIdx) => (
                    <span key={cIdx} className="badge badge-indigo" style={{ fontFamily: 'var(--font-mono)' }}>
                      <FileCode size={12} /> {cf.path}
                    </span>
                  ))}
                </div>
              </div>
            )}
          </div>
        </div>
      ))}
    </div>
  )
}
