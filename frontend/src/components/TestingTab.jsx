import React, { useState } from 'react'
import {
  CheckCircle2,
  XCircle,
  Clock,
  Terminal,
  RotateCw,
  AlertTriangle,
  ChevronDown,
  ChevronUp,
} from 'lucide-react'

export default function TestingTab({ testReport, retryCount }) {
  const [showRawOutput, setShowRawOutput] = useState(false)

  if (!testReport) {
    return (
      <div className="glass-panel" style={{ padding: '40px', textAlign: 'center', color: 'var(--text-muted)' }}>
        Automated testing not yet executed.
      </div>
    )
  }

  const {
    executed,
    total_tests,
    passed_count,
    failed_count,
    skipped_count,
    execution_time_seconds,
    all_passed,
    test_cases,
    stdout,
    stderr,
    summary,
  } = testReport

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
      {/* Test Execution Summary Header */}
      <div className="glass-panel" style={{
        padding: '24px',
        borderLeft: all_passed ? '4px solid #10b981' : '4px solid #f43f5e',
      }}>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '16px' }}>
          <div>
            <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)', textTransform: 'uppercase' }}>
              Sandboxed Automated Verification
            </div>
            <h3 style={{ fontSize: '1.25rem', fontWeight: '800', color: 'var(--text-main)', marginTop: '2px' }}>
              {all_passed ? 'All Automated Tests Passed Successfully' : 'Test Failures Detected'}
            </h3>
            <p style={{ color: 'var(--text-muted)', fontSize: '0.88rem', marginTop: '4px' }}>
              {summary || 'Isolated sandbox execution completed.'}
            </p>
          </div>

          <span className={all_passed ? 'badge badge-emerald' : 'badge badge-rose'} style={{ padding: '6px 14px', fontSize: '0.85rem' }}>
            {all_passed ? 'PASSED (100%)' : 'TESTS FAILED'}
          </span>
        </div>

        {/* Metric Cards Row */}
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(130px, 1fr))', gap: '12px' }}>
          <div style={{ background: 'rgba(255, 255, 255, 0.02)', padding: '12px', borderRadius: 'var(--radius-sm)', border: '1px solid var(--border-subtle)', textAlign: 'center' }}>
            <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>Total Tests</div>
            <div style={{ fontSize: '1.4rem', fontWeight: '800', color: '#e2e8f0', marginTop: '2px' }}>{total_tests}</div>
          </div>

          <div style={{ background: 'rgba(16, 185, 129, 0.08)', padding: '12px', borderRadius: 'var(--radius-sm)', border: '1px solid rgba(16, 185, 129, 0.25)', textAlign: 'center' }}>
            <div style={{ fontSize: '0.75rem', color: '#34d399' }}>Passed</div>
            <div style={{ fontSize: '1.4rem', fontWeight: '800', color: '#34d399', marginTop: '2px' }}>{passed_count}</div>
          </div>

          <div style={{ background: failed_count > 0 ? 'rgba(244, 63, 94, 0.1)' : 'rgba(255, 255, 255, 0.02)', padding: '12px', borderRadius: 'var(--radius-sm)', border: failed_count > 0 ? '1px solid rgba(244, 63, 94, 0.3)' : '1px solid var(--border-subtle)', textAlign: 'center' }}>
            <div style={{ fontSize: '0.75rem', color: failed_count > 0 ? '#fb7185' : 'var(--text-muted)' }}>Failed</div>
            <div style={{ fontSize: '1.4rem', fontWeight: '800', color: failed_count > 0 ? '#fb7185' : '#94a3b8', marginTop: '2px' }}>{failed_count}</div>
          </div>

          <div style={{ background: 'rgba(255, 255, 255, 0.02)', padding: '12px', borderRadius: 'var(--radius-sm)', border: '1px solid var(--border-subtle)', textAlign: 'center' }}>
            <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>Execution Time</div>
            <div style={{ fontSize: '1.4rem', fontWeight: '800', color: '#818cf8', marginTop: '2px' }}>{execution_time_seconds}s</div>
          </div>

          <div style={{ background: 'rgba(255, 255, 255, 0.02)', padding: '12px', borderRadius: 'var(--radius-sm)', border: '1px solid var(--border-subtle)', textAlign: 'center' }}>
            <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>Retry Count</div>
            <div style={{ fontSize: '1.4rem', fontWeight: '800', color: '#f59e0b', marginTop: '2px' }}>{retryCount || 0}</div>
          </div>
        </div>
      </div>

      {/* Individual Test Cases List */}
      <div className="glass-panel" style={{ padding: '24px' }}>
        <h4 style={{ fontSize: '1rem', fontWeight: '700', color: 'var(--text-main)', marginBottom: '16px' }}>
          Individual Test Results ({test_cases?.length || 0})
        </h4>

        {(!test_cases || test_cases.length === 0) ? (
          <p style={{ color: 'var(--text-muted)', fontSize: '0.85rem' }}>
            No individual test cases recorded.
          </p>
        ) : (
          <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
            {test_cases.map((tc, idx) => {
              const isPassed = tc.status === 'PASSED'
              return (
                <div
                  key={idx}
                  style={{
                    background: isPassed ? 'rgba(16, 185, 129, 0.04)' : 'rgba(244, 63, 94, 0.08)',
                    border: isPassed ? '1px solid rgba(16, 185, 129, 0.2)' : '1px solid rgba(244, 63, 94, 0.3)',
                    borderRadius: 'var(--radius-sm)',
                    padding: '12px 16px',
                    display: 'flex',
                    flexDirection: 'column',
                    gap: '6px',
                  }}
                >
                  <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                      {isPassed ? (
                        <CheckCircle2 size={18} color="#34d399" />
                      ) : (
                        <XCircle size={18} color="#fb7185" />
                      )}
                      <span style={{ fontFamily: 'var(--font-mono)', fontWeight: '600', fontSize: '0.85rem', color: '#f8fafc' }}>
                        {tc.name}
                      </span>
                    </div>

                    <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                      <span style={{ fontSize: '0.75rem', color: 'var(--text-dim)' }}>
                        {tc.duration_seconds}s
                      </span>
                      <span className={isPassed ? 'badge badge-emerald' : 'badge badge-rose'}>
                        {tc.status}
                      </span>
                    </div>
                  </div>

                  {tc.error_message && (
                    <div style={{
                      background: 'rgba(0, 0, 0, 0.4)',
                      padding: '10px 12px',
                      borderRadius: 'var(--radius-sm)',
                      fontFamily: 'var(--font-mono)',
                      fontSize: '0.78rem',
                      color: '#fb7185',
                      whiteSpace: 'pre-wrap',
                      marginTop: '6px',
                    }}>
                      {tc.error_message}
                    </div>
                  )}
                </div>
              )
            })}
          </div>
        )}
      </div>

      {/* Raw Runner Console Output */}
      <div className="glass-panel" style={{ padding: '20px' }}>
        <button
          onClick={() => setShowRawOutput(!showRawOutput)}
          style={{
            background: 'transparent',
            border: 'none',
            color: 'var(--text-main)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            width: '100%',
            cursor: 'pointer',
            fontWeight: '600',
            fontSize: '0.9rem',
          }}
        >
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <Terminal size={17} color="#818cf8" />
            <span>Raw Test Runner Subprocess Console Output</span>
          </div>
          {showRawOutput ? <ChevronUp size={16} /> : <ChevronDown size={16} />}
        </button>

        {showRawOutput && (
          <div className="code-container" style={{ marginTop: '14px', padding: '14px', maxHeight: '320px' }}>
            <div style={{ color: '#94a3b8', marginBottom: '6px', fontSize: '0.75rem' }}>--- STDOUT ---</div>
            <pre style={{ margin: 0 }}><code>{stdout || 'No stdout'}</code></pre>
            {stderr && (
              <>
                <div style={{ color: '#fb7185', margin: '10px 0 6px', fontSize: '0.75rem' }}>--- STDERR ---</div>
                <pre style={{ margin: 0, color: '#fb7185' }}><code>{stderr}</code></pre>
              </>
            )}
          </div>
        )}
      </div>
    </div>
  )
}
