import React from 'react'
import { Award, CheckCircle2, ShieldCheck, ShieldAlert, AlertTriangle, ArrowUpRight } from 'lucide-react'

export default function FinalReviewTab({ finalReview }) {
  if (!finalReview) {
    return (
      <div className="glass-panel" style={{ padding: '40px', textAlign: 'center', color: 'var(--text-muted)' }}>
        Final engineering review not yet conducted.
      </div>
    )
  }

  const isSuccess = finalReview.status === 'SUCCESS'
  const isLimited = finalReview.status === 'COMPLETED WITH LIMITATIONS'

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
      {/* Final Status Header Card */}
      <div className="glass-panel" style={{
        padding: '24px',
        borderLeft: isSuccess ? '4px solid #10b981' : isLimited ? '4px solid #f59e0b' : '4px solid #f43f5e',
      }}>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '16px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
            <div style={{
              width: '42px',
              height: '42px',
              borderRadius: '10px',
              background: isSuccess ? 'rgba(16, 185, 129, 0.15)' : 'rgba(245, 158, 11, 0.15)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
            }}>
              <Award size={24} color={isSuccess ? '#34d399' : '#fbbf24'} />
            </div>
            <div>
              <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)', textTransform: 'uppercase' }}>
                End-of-Lifecycle Quality Audit
              </div>
              <h3 style={{ fontSize: '1.25rem', fontWeight: '800', color: 'var(--text-main)' }}>
                Final Deliverable Verdict: {finalReview.status}
              </h3>
            </div>
          </div>

          <span className={isSuccess ? 'badge badge-emerald' : isLimited ? 'badge badge-amber' : 'badge badge-rose'} style={{ padding: '6px 14px', fontSize: '0.85rem' }}>
            {finalReview.status}
          </span>
        </div>

        {/* Scores Gauges */}
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '14px', marginTop: '16px' }}>
          <div style={{ background: 'rgba(255, 255, 255, 0.02)', padding: '14px', borderRadius: 'var(--radius-sm)', border: '1px solid var(--border-subtle)' }}>
            <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>Requirements Coverage</div>
            <div style={{ fontSize: '1.6rem', fontWeight: '800', color: '#818cf8', marginTop: '2px' }}>
              {finalReview.requirements_coverage_score}%
            </div>
          </div>

          <div style={{ background: 'rgba(255, 255, 255, 0.02)', padding: '14px', borderRadius: 'var(--radius-sm)', border: '1px solid var(--border-subtle)' }}>
            <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>Code Quality Score</div>
            <div style={{ fontSize: '1.6rem', fontWeight: '800', color: '#34d399', marginTop: '2px' }}>
              {finalReview.code_quality_score}%
            </div>
          </div>
        </div>
      </div>

      {/* Security & Maintainability Reviews */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(360px, 1fr))', gap: '20px' }}>
        <div className="glass-panel" style={{ padding: '24px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '12px' }}>
            <ShieldCheck size={18} color="#34d399" />
            <h4 style={{ fontSize: '1rem', fontWeight: '700', color: 'var(--text-main)' }}>
              Security Evaluation
            </h4>
          </div>
          <p style={{ fontSize: '0.88rem', color: 'var(--text-muted)', lineHeight: '1.6' }}>
            {finalReview.security_assessment}
          </p>
        </div>

        <div className="glass-panel" style={{ padding: '24px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '12px' }}>
            <ShieldAlert size={18} color="#818cf8" />
            <h4 style={{ fontSize: '1rem', fontWeight: '700', color: 'var(--text-main)' }}>
              Maintainability Assessment
            </h4>
          </div>
          <p style={{ fontSize: '0.88rem', color: 'var(--text-muted)', lineHeight: '1.6' }}>
            {finalReview.maintainability_assessment}
          </p>
        </div>
      </div>

      {/* Test Coverage & Strengths */}
      <div className="glass-panel" style={{ padding: '24px' }}>
        <h4 style={{ fontSize: '1rem', fontWeight: '700', color: 'var(--text-main)', marginBottom: '14px' }}>
          Test Verification Summary
        </h4>
        <p style={{ fontSize: '0.88rem', color: '#cbd5e1', lineHeight: '1.6', marginBottom: '18px' }}>
          {finalReview.test_coverage_summary}
        </p>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))', gap: '20px' }}>
          <div>
            <div style={{ fontSize: '0.82rem', fontWeight: '700', color: 'var(--text-muted)', marginBottom: '8px' }}>
              Strengths:
            </div>
            <ul style={{ listStyle: 'none', display: 'flex', flexDirection: 'column', gap: '8px' }}>
              {finalReview.strengths?.map((s, idx) => (
                <li key={idx} style={{ display: 'flex', alignItems: 'flex-start', gap: '8px', fontSize: '0.85rem', color: '#e2e8f0' }}>
                  <CheckCircle2 size={16} color="#34d399" style={{ marginTop: '2px', flexShrink: 0 }} />
                  <span>{s}</span>
                </li>
              ))}
            </ul>
          </div>

          <div>
            <div style={{ fontSize: '0.82rem', fontWeight: '700', color: 'var(--text-muted)', marginBottom: '8px' }}>
              Future Enhancements:
            </div>
            <ul style={{ listStyle: 'none', display: 'flex', flexDirection: 'column', gap: '8px' }}>
              {finalReview.future_improvements?.map((imp, idx) => (
                <li key={idx} style={{ display: 'flex', alignItems: 'flex-start', gap: '8px', fontSize: '0.85rem', color: '#94a3b8' }}>
                  <ArrowUpRight size={16} color="#818cf8" style={{ marginTop: '2px', flexShrink: 0 }} />
                  <span>{imp}</span>
                </li>
              ))}
            </ul>
          </div>
        </div>
      </div>
    </div>
  )
}
