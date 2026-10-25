import React from 'react'
import { Layers, Database, Globe, Server, Shield, Cpu, ArrowRight } from 'lucide-react'

export default function ArchitectureTab({ architecture }) {
  if (!architecture) {
    return (
      <div className="glass-panel" style={{ padding: '40px', textAlign: 'center', color: 'var(--text-muted)' }}>
        Architecture design not yet generated.
      </div>
    )
  }

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
      {/* Overview & Style Card */}
      <div className="glass-panel" style={{ padding: '24px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '10px' }}>
          <Layers size={20} color="#a855f7" />
          <h3 style={{ fontSize: '1.15rem', fontWeight: '700', color: 'var(--text-main)' }}>
            System Architecture: {architecture.architecture_style}
          </h3>
        </div>
        <p style={{ color: 'var(--text-muted)', fontSize: '0.9rem', lineHeight: '1.6', marginBottom: '14px' }}>
          <strong>Design Rationale:</strong> {architecture.architectural_decisions_rationale}
        </p>

        {/* Visual Architecture Diagram Box */}
        <div style={{
          background: 'rgba(0, 0, 0, 0.4)',
          border: '1px solid var(--border-subtle)',
          borderRadius: 'var(--radius-md)',
          padding: '20px',
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
          gap: '14px',
          alignItems: 'center',
        }}>
          {/* Layer 1: Client/Frontend */}
          <div style={{
            background: 'rgba(99, 102, 241, 0.1)',
            border: '1px solid rgba(99, 102, 241, 0.3)',
            borderRadius: 'var(--radius-sm)',
            padding: '14px',
            textAlign: 'center',
          }}>
            <Globe size={22} color="#818cf8" style={{ margin: '0 auto 8px' }} />
            <div style={{ fontWeight: '700', fontSize: '0.85rem' }}>Presentation Layer</div>
            <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', marginTop: '4px' }}>
              {architecture.frontend_architecture}
            </div>
          </div>

          {/* Layer 2: Service/Backend */}
          <div style={{
            background: 'rgba(168, 85, 247, 0.1)',
            border: '1px solid rgba(168, 85, 247, 0.3)',
            borderRadius: 'var(--radius-sm)',
            padding: '14px',
            textAlign: 'center',
          }}>
            <Server size={22} color="#c084fc" style={{ margin: '0 auto 8px' }} />
            <div style={{ fontWeight: '700', fontSize: '0.85rem' }}>Core Domain & API</div>
            <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', marginTop: '4px' }}>
              {architecture.backend_architecture}
            </div>
          </div>

          {/* Layer 3: Storage */}
          <div style={{
            background: 'rgba(16, 185, 129, 0.1)',
            border: '1px solid rgba(16, 185, 129, 0.3)',
            borderRadius: 'var(--radius-sm)',
            padding: '14px',
            textAlign: 'center',
          }}>
            <Database size={22} color="#34d399" style={{ margin: '0 auto 8px' }} />
            <div style={{ fontWeight: '700', fontSize: '0.85rem' }}>Data & State Store</div>
            <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', marginTop: '4px' }}>
              {architecture.database_storage}
            </div>
          </div>
        </div>
      </div>

      {/* REST API Endpoints Specification */}
      <div className="glass-panel" style={{ padding: '24px' }}>
        <h4 style={{ fontSize: '1rem', fontWeight: '700', color: 'var(--text-main)', marginBottom: '16px' }}>
          REST API Interface Specification ({architecture.api_design?.length || 0})
        </h4>

        <div style={{ overflowX: 'auto' }}>
          <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left', fontSize: '0.85rem' }}>
            <thead>
              <tr style={{ borderBottom: '1px solid var(--border-subtle)', color: 'var(--text-muted)' }}>
                <th style={{ padding: '10px 14px' }}>Method</th>
                <th style={{ padding: '10px 14px' }}>Endpoint</th>
                <th style={{ padding: '10px 14px' }}>Description</th>
                <th style={{ padding: '10px 14px' }}>Request / Response</th>
              </tr>
            </thead>
            <tbody>
              {architecture.api_design?.map((ep, idx) => {
                const methodColor =
                  ep.method === 'GET' ? 'badge-indigo' :
                  ep.method === 'POST' ? 'badge-emerald' :
                  ep.method === 'DELETE' ? 'badge-rose' : 'badge-amber'
                return (
                  <tr key={idx} style={{ borderBottom: '1px solid rgba(255, 255, 255, 0.04)' }}>
                    <td style={{ padding: '12px 14px' }}>
                      <span className={`badge ${methodColor}`}>{ep.method}</span>
                    </td>
                    <td style={{ padding: '12px 14px', fontFamily: 'var(--font-mono)', fontWeight: '600', color: '#e2e8f0' }}>
                      {ep.path}
                    </td>
                    <td style={{ padding: '12px 14px', color: 'var(--text-muted)' }}>
                      {ep.description}
                    </td>
                    <td style={{ padding: '12px 14px', color: 'var(--text-dim)', fontSize: '0.78rem' }}>
                      <div>Resp: {ep.response}</div>
                      {ep.request_body && <div>Body: {ep.request_body}</div>}
                    </td>
                  </tr>
                )
              })}
            </tbody>
          </table>
        </div>
      </div>

      {/* Modules & Data Flow */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(360px, 1fr))', gap: '20px' }}>
        {/* Major Modules */}
        <div className="glass-panel" style={{ padding: '24px' }}>
          <h4 style={{ fontSize: '1rem', fontWeight: '700', color: 'var(--text-main)', marginBottom: '14px' }}>
            Modular Decomposition
          </h4>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
            {architecture.major_modules?.map((mod, idx) => (
              <div key={idx} style={{ background: 'rgba(255, 255, 255, 0.02)', padding: '12px 16px', borderRadius: 'var(--radius-sm)', border: '1px solid var(--border-subtle)' }}>
                <div style={{ fontWeight: '700', color: '#c084fc', fontSize: '0.88rem', fontFamily: 'var(--font-mono)' }}>
                  {mod.name}
                </div>
                <div style={{ fontSize: '0.82rem', color: 'var(--text-muted)', marginTop: '4px' }}>
                  {mod.responsibility}
                </div>
                {mod.key_classes_or_functions?.length > 0 && (
                  <div style={{ fontSize: '0.75rem', color: 'var(--text-dim)', marginTop: '6px' }}>
                    Classes/Methods: {mod.key_classes_or_functions.join(', ')}
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>

        {/* Data Flow & Security */}
        <div className="glass-panel" style={{ padding: '24px' }}>
          <h4 style={{ fontSize: '1rem', fontWeight: '700', color: 'var(--text-main)', marginBottom: '14px' }}>
            Data Flow & Security Safeguards
          </h4>
          <div style={{ marginBottom: '16px' }}>
            <div style={{ fontSize: '0.82rem', fontWeight: '600', color: 'var(--text-muted)', marginBottom: '8px' }}>
              Execution Flow:
            </div>
            <ul style={{ listStyle: 'none', display: 'flex', flexDirection: 'column', gap: '8px' }}>
              {architecture.data_flow?.map((flow, idx) => (
                <li key={idx} style={{ fontSize: '0.82rem', color: '#cbd5e1', display: 'flex', alignItems: 'center', gap: '8px' }}>
                  <ArrowRight size={14} color="#6366f1" />
                  <span>{flow}</span>
                </li>
              ))}
            </ul>
          </div>

          <div style={{ borderTop: '1px solid var(--border-subtle)', paddingTop: '14px' }}>
            <div style={{ fontSize: '0.82rem', fontWeight: '600', color: 'var(--text-muted)', marginBottom: '8px' }}>
              Security & Validation:
            </div>
            <ul style={{ listStyle: 'none', display: 'flex', flexDirection: 'column', gap: '6px' }}>
              {architecture.security_considerations?.map((sec, idx) => (
                <li key={idx} style={{ fontSize: '0.82rem', color: '#94a3b8' }}>
                  • {sec}
                </li>
              ))}
            </ul>
          </div>
        </div>
      </div>
    </div>
  )
}
