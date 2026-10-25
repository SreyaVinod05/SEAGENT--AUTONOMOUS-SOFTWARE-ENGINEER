import React from 'react'
import { Calendar, CheckCircle2, Flag, ArrowRight, Package } from 'lucide-react'

export default function PlanTab({ plan }) {
  if (!plan) {
    return (
      <div className="glass-panel" style={{ padding: '40px', textAlign: 'center', color: 'var(--text-muted)' }}>
        Development plan not yet generated.
      </div>
    )
  }

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
      {/* Objective Card */}
      <div className="glass-panel" style={{ padding: '24px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '10px' }}>
          <Calendar size={20} color="#6366f1" />
          <h3 style={{ fontSize: '1.15rem', fontWeight: '700', color: 'var(--text-main)' }}>
            Project Development Objective
          </h3>
        </div>
        <p style={{ color: 'var(--text-muted)', fontSize: '0.9rem', lineHeight: '1.6' }}>
          {plan.project_objective}
        </p>
      </div>

      {/* Ordered Development Steps */}
      <div className="glass-panel" style={{ padding: '24px' }}>
        <h4 style={{ fontSize: '1rem', fontWeight: '700', color: 'var(--text-main)', marginBottom: '16px' }}>
          Ordered Implementation Steps ({plan.steps?.length || 0})
        </h4>

        <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
          {plan.steps?.map((step) => {
            const isHigh = step.priority?.toLowerCase() === 'high'
            return (
              <div
                key={step.step_number}
                style={{
                  background: 'rgba(255, 255, 255, 0.02)',
                  border: '1px solid var(--border-subtle)',
                  borderRadius: 'var(--radius-md)',
                  padding: '16px',
                  display: 'flex',
                  alignItems: 'flex-start',
                  gap: '16px',
                }}
              >
                {/* Step Number Badge */}
                <div style={{
                  width: '36px',
                  height: '36px',
                  borderRadius: '10px',
                  background: 'linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%)',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  fontWeight: '800',
                  color: '#fff',
                  flexShrink: 0,
                  fontSize: '0.95rem',
                }}>
                  {step.step_number}
                </div>

                {/* Content */}
                <div style={{ flex: 1 }}>
                  <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '6px' }}>
                    <div style={{ fontWeight: '700', fontSize: '0.95rem', color: 'var(--text-main)' }}>
                      {step.title}
                    </div>
                    <span className={isHigh ? 'badge badge-rose' : 'badge badge-indigo'}>
                      {step.priority} Priority
                    </span>
                  </div>

                  <p style={{ fontSize: '0.85rem', color: 'var(--text-muted)', marginBottom: '10px', lineHeight: '1.5' }}>
                    {step.description}
                  </p>

                  <div style={{ display: 'flex', flexWrap: 'wrap', gap: '14px', fontSize: '0.78rem' }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '6px', color: '#34d399' }}>
                      <Package size={14} />
                      <span>Deliverable: <strong>{step.deliverable}</strong></span>
                    </div>

                    {step.dependencies?.length > 0 && (
                      <div style={{ display: 'flex', alignItems: 'center', gap: '6px', color: 'var(--text-dim)' }}>
                        <ArrowRight size={14} />
                        <span>Requires: {step.dependencies.join(', ')}</span>
                      </div>
                    )}
                  </div>
                </div>
              </div>
            )
          })}
        </div>
      </div>

      {/* Milestones & Deliverables */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(360px, 1fr))', gap: '20px' }}>
        <div className="glass-panel" style={{ padding: '24px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '14px' }}>
            <Flag size={18} color="#f59e0b" />
            <h4 style={{ fontSize: '1rem', fontWeight: '700', color: 'var(--text-main)' }}>
              Key Milestones
            </h4>
          </div>
          <ul style={{ listStyle: 'none', display: 'flex', flexDirection: 'column', gap: '10px' }}>
            {plan.milestones?.map((m, idx) => (
              <li key={idx} style={{ display: 'flex', alignItems: 'center', gap: '10px', fontSize: '0.85rem', color: '#cbd5e1' }}>
                <CheckCircle2 size={16} color="#f59e0b" />
                <span>{m}</span>
              </li>
            ))}
          </ul>
        </div>

        <div className="glass-panel" style={{ padding: '24px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '14px' }}>
            <Package size={18} color="#06b6d4" />
            <h4 style={{ fontSize: '1rem', fontWeight: '700', color: 'var(--text-main)' }}>
              Project Deliverables
            </h4>
          </div>
          <ul style={{ listStyle: 'none', display: 'flex', flexDirection: 'column', gap: '10px' }}>
            {plan.deliverables?.map((d, idx) => (
              <li key={idx} style={{ display: 'flex', alignItems: 'center', gap: '10px', fontSize: '0.85rem', color: '#cbd5e1' }}>
                <CheckCircle2 size={16} color="#06b6d4" />
                <span>{d}</span>
              </li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  )
}
