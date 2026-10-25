import React from 'react'
import {
  ShieldCheck,
  ShieldAlert,
  AlertTriangle,
  Lock,
  CheckCircle,
  FileCode,
  Wrench,
  Check,
} from 'lucide-react'

export default function SecurityTab({ securityReview }) {
  if (!securityReview) {
    return (
      <div className="glass-panel" style={{ padding: '40px', textAlign: 'center', color: 'var(--text-muted)' }}>
        Security Review has not been performed yet. It runs automatically after automated testing completes.
      </div>
    )
  }

  const score = securityReview.security_score || 95
  const isPassed = securityReview.status === 'PASSED'
  const isWarning = securityReview.status === 'WARNINGS_DETECTED'

  const scoreColor = score >= 90 ? '#34d399' : score >= 75 ? '#fbbf24' : '#f87171'

  const getSeverityBadgeClass = (severity) => {
    switch ((severity || '').toUpperCase()) {
      case 'CRITICAL':
        return 'badge badge-rose'
      case 'HIGH':
        return 'badge badge-rose'
      case 'MEDIUM':
        return 'badge badge-amber'
      default:
        return 'badge badge-indigo'
    }
  }

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
      {/* Header Verdict Card */}
      <div
        className="glass-panel"
        style={{
          padding: '24px',
          borderLeft: isPassed
            ? '4px solid #10b981'
            : isWarning
            ? '4px solid #f59e0b'
            : '4px solid #ef4444',
        }}
      >
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: '16px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '14px' }}>
            <div
              style={{
                width: '44px',
                height: '44px',
                borderRadius: '12px',
                background: isPassed ? 'rgba(16, 185, 129, 0.15)' : 'rgba(245, 158, 11, 0.15)',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
              }}
            >
              {isPassed ? <ShieldCheck size={26} color="#34d399" /> : <ShieldAlert size={26} color="#fbbf24" />}
            </div>
            <div>
              <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
                Application Security & OWASP Audit
              </div>
              <h3 style={{ fontSize: '1.25rem', fontWeight: '800', color: 'var(--text-main)', marginTop: '2px' }}>
                {isPassed
                  ? 'Codebase Verified Secure & OWASP Compliant'
                  : isWarning
                  ? 'Security Warnings Detected — Review Remediation'
                  : 'Vulnerabilities Detected — Remediation Required'}
              </h3>
            </div>
          </div>

          <div style={{ display: 'flex', alignItems: 'center', gap: '18px' }}>
            <div style={{ textAlign: 'right' }}>
              <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>Security Health Score</div>
              <div style={{ fontSize: '1.5rem', fontWeight: '800', color: scoreColor }}>
                {score}/100
              </div>
            </div>
            <span
              className={isPassed ? 'badge badge-emerald' : isWarning ? 'badge badge-amber' : 'badge badge-rose'}
              style={{ padding: '6px 14px', fontSize: '0.85rem' }}
            >
              {securityReview.status}
            </span>
          </div>
        </div>

        {securityReview.summary && (
          <p style={{ marginTop: '16px', color: 'var(--text-muted)', fontSize: '0.9rem', lineHeight: '1.6' }}>
            {securityReview.summary}
          </p>
        )}
      </div>

      {/* Vulnerabilities Section */}
      <div className="glass-panel" style={{ padding: '24px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '16px' }}>
          <AlertTriangle size={18} color="#f59e0b" />
          <h4 style={{ fontSize: '1rem', fontWeight: '700', color: 'var(--text-main)', margin: 0 }}>
            Detected Vulnerabilities & Risk Analysis ({securityReview.vulnerabilities?.length || 0})
          </h4>
        </div>

        {(!securityReview.vulnerabilities || securityReview.vulnerabilities.length === 0) ? (
          <div style={{ padding: '20px', textAlign: 'center', color: '#34d399', background: 'rgba(16, 185, 129, 0.08)', borderRadius: '8px' }}>
            ✓ No critical or high-risk vulnerabilities found in the generated source code.
          </div>
        ) : (
          <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
            {securityReview.vulnerabilities.map((vuln, idx) => (
              <div
                key={idx}
                style={{
                  padding: '16px',
                  borderRadius: '10px',
                  background: 'rgba(255, 255, 255, 0.02)',
                  border: '1px solid var(--border-subtle)',
                }}
              >
                <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '8px' }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                    <span className={getSeverityBadgeClass(vuln.severity)} style={{ fontSize: '0.75rem', fontWeight: '700' }}>
                      {vuln.severity}
                    </span>
                    <span style={{ fontWeight: '700', color: 'var(--text-main)', fontSize: '0.95rem' }}>
                      {vuln.vulnerability_type}
                    </span>
                  </div>
                  {vuln.file_path && (
                    <div style={{ display: 'flex', alignItems: 'center', gap: '6px', fontSize: '0.8rem', color: 'var(--text-dim)' }}>
                      <FileCode size={13} />
                      <span>{vuln.file_path}{vuln.line_number ? `:${vuln.line_number}` : ''}</span>
                    </div>
                  )}
                </div>

                <p style={{ fontSize: '0.88rem', color: 'var(--text-muted)', margin: '0 0 10px 0', lineHeight: '1.5' }}>
                  {vuln.description}
                </p>

                {vuln.remediation && (
                  <div
                    style={{
                      display: 'flex',
                      alignItems: 'flex-start',
                      gap: '8px',
                      padding: '10px 12px',
                      background: 'rgba(99, 102, 241, 0.08)',
                      borderRadius: '6px',
                      fontSize: '0.82rem',
                      color: '#c7d2fe',
                    }}
                  >
                    <Wrench size={14} style={{ marginTop: '2px', flexShrink: 0 }} />
                    <div>
                      <strong>Remediation:</strong> {vuln.remediation}
                    </div>
                  </div>
                )}
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Two Columns: OWASP Compliance Checklist & Secure Design Patterns */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(360px, 1fr))', gap: '20px' }}>
        {/* OWASP Checklist */}
        <div className="glass-panel" style={{ padding: '24px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '16px' }}>
            <Lock size={18} color="#818cf8" />
            <h4 style={{ fontSize: '1rem', fontWeight: '700', color: 'var(--text-main)', margin: 0 }}>
              OWASP Top 10 Compliance Verification
            </h4>
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
            {(securityReview.owasp_compliance || []).map((item, idx) => (
              <div
                key={idx}
                style={{
                  display: 'flex',
                  alignItems: 'flex-start',
                  gap: '10px',
                  fontSize: '0.88rem',
                  color: 'var(--text-muted)',
                }}
              >
                <Check size={16} color="#34d399" style={{ marginTop: '2px', flexShrink: 0 }} />
                <span>{item}</span>
              </div>
            ))}
          </div>
        </div>

        {/* Secure Patterns & Remediation Steps */}
        <div className="glass-panel" style={{ padding: '24px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '16px' }}>
            <ShieldCheck size={18} color="#34d399" />
            <h4 style={{ fontSize: '1rem', fontWeight: '700', color: 'var(--text-main)', margin: 0 }}>
              Implemented Security Safeguards
            </h4>
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '10px', marginBottom: '20px' }}>
            {(securityReview.secure_design_patterns || []).map((pat, idx) => (
              <div
                key={idx}
                style={{
                  display: 'flex',
                  alignItems: 'flex-start',
                  gap: '10px',
                  fontSize: '0.88rem',
                  color: 'var(--text-muted)',
                }}
              >
                <CheckCircle size={15} color="#818cf8" style={{ marginTop: '2px', flexShrink: 0 }} />
                <span>{pat}</span>
              </div>
            ))}
          </div>

          {securityReview.remediation_steps && securityReview.remediation_steps.length > 0 && (
            <>
              <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)', textTransform: 'uppercase', marginBottom: '8px', letterSpacing: '0.05em' }}>
                Recommended Defense Upgrades
              </div>
              <ul style={{ margin: 0, paddingLeft: '18px', color: 'var(--text-muted)', fontSize: '0.85rem', lineHeight: '1.6' }}>
                {securityReview.remediation_steps.map((step, idx) => (
                  <li key={idx}>{step}</li>
                ))}
              </ul>
            </>
          )}
        </div>
      </div>
    </div>
  )
}
