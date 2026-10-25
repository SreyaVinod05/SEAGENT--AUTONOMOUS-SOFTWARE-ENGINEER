import React from 'react'
import { CheckCircle2, User, ShieldAlert, FileText, Target, HelpCircle } from 'lucide-react'

export default function RequirementsTab({ requirements }) {
  if (!requirements) {
    return (
      <div className="glass-panel" style={{ padding: '40px', textAlign: 'center', color: 'var(--text-muted)' }}>
        Requirements analysis not yet completed.
      </div>
    )
  }

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
      {/* Project Overview Card */}
      <div className="glass-panel" style={{ padding: '24px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '10px' }}>
          <FileText size={20} color="#818cf8" />
          <h3 style={{ fontSize: '1.15rem', fontWeight: '700', color: 'var(--text-main)' }}>
            {requirements.project_name}
          </h3>
        </div>
        <p style={{ color: 'var(--text-muted)', fontSize: '0.9rem', lineHeight: '1.6' }}>
          {requirements.summary}
        </p>
      </div>

      {/* Two columns: Functional vs Non-Functional */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(360px, 1fr))', gap: '20px' }}>
        {/* Functional Requirements */}
        <div className="glass-panel" style={{ padding: '24px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '16px' }}>
            <Target size={18} color="#34d399" />
            <h4 style={{ fontSize: '1rem', fontWeight: '700', color: 'var(--text-main)' }}>
              Functional Requirements ({requirements.functional_requirements?.length || 0})
            </h4>
          </div>
          <ul style={{ listStyle: 'none', display: 'flex', flexDirection: 'column', gap: '10px' }}>
            {requirements.functional_requirements?.map((req, idx) => (
              <li key={idx} style={{ display: 'flex', alignItems: 'flex-start', gap: '10px', fontSize: '0.85rem', color: '#cbd5e1' }}>
                <CheckCircle2 size={16} color="#34d399" style={{ flexShrink: 0, marginTop: '2px' }} />
                <span>{req}</span>
              </li>
            ))}
          </ul>
        </div>

        {/* Non-Functional Requirements */}
        <div className="glass-panel" style={{ padding: '24px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '16px' }}>
            <ShieldAlert size={18} color="#818cf8" />
            <h4 style={{ fontSize: '1rem', fontWeight: '700', color: 'var(--text-main)' }}>
              Non-Functional Requirements ({requirements.non_functional_requirements?.length || 0})
            </h4>
          </div>
          <ul style={{ listStyle: 'none', display: 'flex', flexDirection: 'column', gap: '10px' }}>
            {requirements.non_functional_requirements?.map((nfr, idx) => (
              <li key={idx} style={{ display: 'flex', alignItems: 'flex-start', gap: '10px', fontSize: '0.85rem', color: '#cbd5e1' }}>
                <div style={{ width: '6px', height: '6px', borderRadius: '50%', background: '#818cf8', marginTop: '6px' }} />
                <span>{nfr}</span>
              </li>
            ))}
          </ul>
        </div>
      </div>

      {/* Actors & Acceptance Criteria */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(360px, 1fr))', gap: '20px' }}>
        {/* Actors & Use Cases */}
        <div className="glass-panel" style={{ padding: '24px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '14px' }}>
            <User size={18} color="#f59e0b" />
            <h4 style={{ fontSize: '1rem', fontWeight: '700', color: 'var(--text-main)' }}>
              User Actors & Key Scenarios
            </h4>
          </div>
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px', marginBottom: '16px' }}>
            {requirements.actors?.map((actor, idx) => (
              <span key={idx} className="badge badge-amber">
                {actor}
              </span>
            ))}
          </div>
          <div style={{ fontSize: '0.82rem', fontWeight: '600', color: 'var(--text-muted)', marginBottom: '8px' }}>
            Key Use Cases:
          </div>
          <ul style={{ listStyle: 'none', display: 'flex', flexDirection: 'column', gap: '8px' }}>
            {requirements.use_cases?.map((uc, idx) => (
              <li key={idx} style={{ fontSize: '0.85rem', color: '#cbd5e1', paddingLeft: '12px', borderLeft: '2px solid rgba(245, 158, 11, 0.4)' }}>
                {uc}
              </li>
            ))}
          </ul>
        </div>

        {/* Acceptance Criteria */}
        <div className="glass-panel" style={{ padding: '24px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '14px' }}>
            <CheckCircle2 size={18} color="#06b6d4" />
            <h4 style={{ fontSize: '1rem', fontWeight: '700', color: 'var(--text-main)' }}>
              Acceptance Criteria ({requirements.acceptance_criteria?.length || 0})
            </h4>
          </div>
          <ul style={{ listStyle: 'none', display: 'flex', flexDirection: 'column', gap: '10px' }}>
            {requirements.acceptance_criteria?.map((ac, idx) => (
              <li key={idx} style={{ display: 'flex', alignItems: 'flex-start', gap: '10px', fontSize: '0.85rem', color: '#cbd5e1' }}>
                <span style={{ color: '#06b6d4', fontWeight: '700', fontSize: '0.8rem' }}>AC-{idx + 1}:</span>
                <span>{ac}</span>
              </li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  )
}
