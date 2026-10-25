import React from 'react'
import {
  Zap,
  Gauge,
  TrendingUp,
  FileCode,
  CheckCircle2,
  Cpu,
  Layers,
  ArrowRight,
} from 'lucide-react'

export default function OptimizationTab({ optimization }) {
  if (!optimization) {
    return (
      <div className="glass-panel" style={{ padding: '40px', textAlign: 'center', color: 'var(--text-muted)' }}>
        Code Optimization has not been performed yet. It executes automatically after security analysis.
      </div>
    )
  }

  const rating = optimization.performance_rating || 92
  const ratingColor = rating >= 90 ? '#34d399' : rating >= 75 ? '#fbbf24' : '#f87171'

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
      {/* Header Metric Card */}
      <div
        className="glass-panel"
        style={{
          padding: '24px',
          borderLeft: '4px solid #8b5cf6',
        }}
      >
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: '16px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '14px' }}>
            <div
              style={{
                width: '44px',
                height: '44px',
                borderRadius: '12px',
                background: 'rgba(139, 92, 246, 0.15)',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
              }}
            >
              <Zap size={26} color="#a78bfa" />
            </div>
            <div>
              <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
                Algorithmic & Performance Refactoring
              </div>
              <h3 style={{ fontSize: '1.25rem', fontWeight: '800', color: 'var(--text-main)', marginTop: '2px' }}>
                {optimization.estimated_speedup || 'Computational Efficiency Elevated'}
              </h3>
            </div>
          </div>

          <div style={{ display: 'flex', alignItems: 'center', gap: '18px' }}>
            <div style={{ textAlign: 'right' }}>
              <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>Performance Rating</div>
              <div style={{ fontSize: '1.5rem', fontWeight: '800', color: ratingColor }}>
                {rating}/100
              </div>
            </div>
            <span className="badge badge-purple" style={{ padding: '6px 14px', fontSize: '0.85rem' }}>
              <TrendingUp size={13} /> OPTIMIZED
            </span>
          </div>
        </div>

        {optimization.overall_improvement_summary && (
          <p style={{ marginTop: '16px', color: 'var(--text-muted)', fontSize: '0.9rem', lineHeight: '1.6' }}>
            {optimization.overall_improvement_summary}
          </p>
        )}
      </div>

      {/* Per-File Complexity & Refactoring Breakdown */}
      <div className="glass-panel" style={{ padding: '24px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '16px' }}>
          <Cpu size={18} color="#8b5cf6" />
          <h4 style={{ fontSize: '1rem', fontWeight: '700', color: 'var(--text-main)', margin: 0 }}>
            Big-O Algorithmic Refactoring & Per-File Analysis
          </h4>
        </div>

        {(!optimization.file_optimizations || optimization.file_optimizations.length === 0) ? (
          <div style={{ padding: '20px', textAlign: 'center', color: 'var(--text-muted)', background: 'rgba(255, 255, 255, 0.02)', borderRadius: '8px' }}>
            Codebase already operates at optimal Big-O bounds.
          </div>
        ) : (
          <div style={{ display: 'flex', flexDirection: 'column', gap: '14px' }}>
            {optimization.file_optimizations.map((fileOpt, idx) => (
              <div
                key={idx}
                style={{
                  padding: '18px',
                  borderRadius: '10px',
                  background: 'rgba(255, 255, 255, 0.02)',
                  border: '1px solid var(--border-subtle)',
                }}
              >
                <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: '10px', marginBottom: '12px' }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                    <FileCode size={16} color="#818cf8" />
                    <span style={{ fontWeight: '700', color: 'var(--text-main)', fontSize: '0.95rem' }}>
                      {fileOpt.path}
                    </span>
                    <span className="badge badge-purple" style={{ fontSize: '0.72rem' }}>
                      {fileOpt.optimization_type}
                    </span>
                  </div>

                  {/* Complexity Pill Badges */}
                  <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                    <div
                      style={{
                        display: 'flex',
                        alignItems: 'center',
                        gap: '6px',
                        background: 'rgba(0, 0, 0, 0.3)',
                        padding: '4px 10px',
                        borderRadius: '6px',
                        fontSize: '0.78rem',
                        fontFamily: 'monospace',
                      }}
                    >
                      <span style={{ color: 'var(--text-dim)' }}>Time:</span>
                      <span style={{ color: '#f87171' }}>{fileOpt.time_complexity_before}</span>
                      <ArrowRight size={12} color="var(--text-dim)" />
                      <span style={{ color: '#34d399', fontWeight: '700' }}>{fileOpt.time_complexity_after}</span>
                    </div>

                    <div
                      style={{
                        display: 'flex',
                        alignItems: 'center',
                        gap: '6px',
                        background: 'rgba(0, 0, 0, 0.3)',
                        padding: '4px 10px',
                        borderRadius: '6px',
                        fontSize: '0.78rem',
                        fontFamily: 'monospace',
                      }}
                    >
                      <span style={{ color: 'var(--text-dim)' }}>Space:</span>
                      <span style={{ color: '#f87171' }}>{fileOpt.space_complexity_before}</span>
                      <ArrowRight size={12} color="var(--text-dim)" />
                      <span style={{ color: '#34d399', fontWeight: '700' }}>{fileOpt.space_complexity_after}</span>
                    </div>
                  </div>
                </div>

                <p style={{ margin: 0, color: 'var(--text-muted)', fontSize: '0.88rem', lineHeight: '1.5' }}>
                  {fileOpt.changes_made}
                </p>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Best Practices Applied */}
      {optimization.best_practices_applied && optimization.best_practices_applied.length > 0 && (
        <div className="glass-panel" style={{ padding: '24px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '16px' }}>
            <CheckCircle2 size={18} color="#34d399" />
            <h4 style={{ fontSize: '1rem', fontWeight: '700', color: 'var(--text-main)', margin: 0 }}>
              Engineering Best Practices Applied
            </h4>
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '12px' }}>
            {optimization.best_practices_applied.map((bp, idx) => (
              <div
                key={idx}
                style={{
                  display: 'flex',
                  alignItems: 'flex-start',
                  gap: '10px',
                  padding: '12px',
                  borderRadius: '8px',
                  background: 'rgba(255, 255, 255, 0.02)',
                  fontSize: '0.88rem',
                  color: 'var(--text-muted)',
                }}
              >
                <div style={{ width: '6px', height: '6px', borderRadius: '50%', background: '#8b5cf6', marginTop: '6px', flexShrink: 0 }} />
                <span>{bp}</span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}
