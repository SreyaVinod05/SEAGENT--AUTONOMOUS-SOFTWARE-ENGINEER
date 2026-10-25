import React from 'react'
import { ShieldCheck, ShieldAlert, Award, ThumbsUp, AlertCircle, Lightbulb } from 'lucide-react'

export default function SeniorReviewTab({ seniorReview }) {
  if (!seniorReview) {
    return (
      <div className="glass-panel" style={{ padding: '40px', textAlign: 'center', color: 'var(--text-muted)' }}>
        Senior Engineer review not yet performed.
      </div>
    )
  }

  const isApproved = seniorReview.approved
  const score = seniorReview.overall_score || 8

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
      {/* Review Verdict Card */}
      <div className="glass-panel" style={{
        padding: '24px',
        borderLeft: isApproved ? '4px solid #10b981' : '4px solid #f59e0b',
      }}>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '14px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
            <div style={{
              width: '40px',
              height: '40px',
              borderRadius: '10px',
              background: isApproved ? 'rgba(16, 185, 129, 0.15)' : 'rgba(245, 158, 11, 0.15)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
            }}>
              {isApproved ? <ShieldCheck size={24} color="#34d399" /> : <ShieldAlert size={24} color="#fbbf24" />}
            </div>
            <div>
              <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)', textTransform: 'uppercase' }}>
                Engineering Gate Review
              </div>
              <h3 style={{ fontSize: '1.2rem', fontWeight: '800', color: 'var(--text-main)' }}>
                {isApproved ? 'Architecture & Plan Approved for Code Generation' : 'Revision Required Before Proceeding'}
              </h3>
            </div>
          </div>

          <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
            <div style={{ textAlign: 'right' }}>
              <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>Quality Rating</div>
              <div style={{ fontSize: '1.4rem', fontWeight: '800', color: score >= 8 ? '#34d399' : '#fbbf24' }}>
                {score}/10
              </div>
            </div>
            <span className={isApproved ? 'badge badge-emerald' : 'badge badge-amber'} style={{ padding: '6px 14px', fontSize: '0.85rem' }}>
              {isApproved ? 'APPROVED' : 'REVISION'}
            </span>
          </div>
        </div>
      </div>

      {/* Two columns: Strengths vs Issues */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(360px, 1fr))', gap: '20px' }}>
        {/* Strengths */}
        <div className="glass-panel" style={{ padding: '24px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '16px' }}>
            <ThumbsUp size={18} color="#34d399" />
            <h4 style={{ fontSize: '1rem', fontWeight: '700', color: 'var(--text-main)' }}>
              Identified Strengths ({seniorReview.strengths?.length || 0})
            </h4>
          </div>
          <ul style={{ listStyle: 'none', display: 'flex', flexDirection: 'column', gap: '10px' }}>
            {seniorReview.strengths?.map((str, idx) => (
              <li key={idx} style={{ display: 'flex', alignItems: 'flex-start', gap: '10px', fontSize: '0.85rem', color: '#cbd5e1' }}>
                <div style={{ width: '6px', height: '6px', borderRadius: '50%', background: '#34d399', marginTop: '6px' }} />
                <span>{str}</span>
              </li>
            ))}
          </ul>
        </div>

        {/* Issues & Gaps */}
        <div className="glass-panel" style={{ padding: '24px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '16px' }}>
            <AlertCircle size={18} color="#f59e0b" />
            <h4 style={{ fontSize: '1rem', fontWeight: '700', color: 'var(--text-main)' }}>
              Critical Issues / Gaps ({seniorReview.issues?.length || 0})
            </h4>
          </div>
          {seniorReview.issues?.length === 0 ? (
            <p style={{ fontSize: '0.85rem', color: '#94a3b8' }}>
              No critical architectural flaws or contradictions detected.
            </p>
          ) : (
            <ul style={{ listStyle: 'none', display: 'flex', flexDirection: 'column', gap: '10px' }}>
              {seniorReview.issues?.map((iss, idx) => (
                <li key={idx} style={{ display: 'flex', alignItems: 'flex-start', gap: '10px', fontSize: '0.85rem', color: '#cbd5e1' }}>
                  <div style={{ width: '6px', height: '6px', borderRadius: '50%', background: '#f59e0b', marginTop: '6px' }} />
                  <span>{iss}</span>
                </li>
              ))}
            </ul>
          )}
        </div>
      </div>

      {/* Actionable Recommendations */}
      <div className="glass-panel" style={{ padding: '24px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '16px' }}>
          <Lightbulb size={18} color="#818cf8" />
          <h4 style={{ fontSize: '1rem', fontWeight: '700', color: 'var(--text-main)' }}>
            Senior Engineering Recommendations
          </h4>
        </div>
        <ul style={{ listStyle: 'none', display: 'flex', flexDirection: 'column', gap: '10px' }}>
          {seniorReview.recommendations?.map((rec, idx) => (
            <li key={idx} style={{ display: 'flex', alignItems: 'flex-start', gap: '10px', fontSize: '0.85rem', color: '#cbd5e1' }}>
              <span style={{ color: '#818cf8', fontWeight: '700', fontSize: '0.8rem' }}>#{idx + 1}</span>
              <span>{rec}</span>
            </li>
          ))}
        </ul>
      </div>
    </div>
  )
}
