import React, { useState, useEffect } from 'react'
import { X, Play, Sparkles, BookOpen, Check, Cpu, Bot, ShieldCheck } from 'lucide-react'

const DEMO_PRESETS = [
  {
    title: 'Task Management Engine (Primary Acceptance Demo)',
    projectName: 'TaskMaster Pro',
    requirement: 'Build a task management web application where users can create, update, delete and complete tasks. Each task should have a title, description, priority and completion status.',
    tech: 'Python, modular service architecture, unittest',
  },
  {
    title: 'REST URL Shortener Service',
    projectName: 'QuickLink Service',
    requirement: 'Create a URL shortener service that takes long URLs, creates a 6-character unique slug, tracks click counts, and allows retrieval and deletion of links.',
    tech: 'Python in-memory store with collision-resistant hashing',
  },
  {
    title: 'E-Commerce Cart & Discount Calculator',
    projectName: 'CartFlow Core',
    requirement: 'Build a shopping cart service that allows adding items with quantities and prices, applying promo codes with percentage discounts, and calculating subtotal, tax, and total.',
    tech: 'Clean dataclasses and business logic service',
  },
]

export default function NewProjectModal({ isOpen, onClose, onStart, config, isGeminiConfigured }) {
  const [projectName, setProjectName] = useState('TaskMaster Pro')
  const [requirement, setRequirement] = useState(
    'Build a task management web application where users can create, update, delete and complete tasks. Each task should have a title, description, priority and completion status.'
  )
  const [techPreferences, setTechPreferences] = useState('Python modular service with standard unittest suite')
  
  const isOpenAIConfigured = config?.openai_configured
  const isGeminiAvailable = config?.gemini_configured ?? isGeminiConfigured
  
  const [provider, setProvider] = useState('mock')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  useEffect(() => {
    // Default to Offline Mock mode so users never hit unexpected 429 quota errors during viva/testing
    if (config?.default_provider && config.default_provider !== 'openai') {
      setProvider(config.default_provider)
    } else {
      setProvider('mock')
    }
  }, [config])

  if (!isOpen) return null

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!requirement.trim()) {
      setError('Please provide a software requirement.')
      return
    }
    setError('')
    setLoading(true)
    try {
      await onStart({
        projectName: projectName.trim(),
        requirement: requirement.trim(),
        techPreferences: techPreferences.trim(),
        provider: provider,
        useMock: provider === 'mock',
      })
      onClose()
    } catch (err) {
      setError(err.message || 'Failed to start workflow')
    } finally {
      setLoading(false)
    }
  }

  const applyPreset = (preset) => {
    setProjectName(preset.projectName)
    setRequirement(preset.requirement)
    setTechPreferences(preset.tech)
  }

  return (
    <div style={{
      position: 'fixed',
      top: 0,
      left: 0,
      right: 0,
      bottom: 0,
      background: 'rgba(0, 0, 0, 0.75)',
      backdropFilter: 'blur(8px)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      zIndex: 100,
      padding: '20px',
    }}>
      <div className="glass-panel" style={{
        maxWidth: '720px',
        width: '100%',
        maxHeight: '90vh',
        overflowY: 'auto',
        padding: '30px',
        borderRadius: 'var(--radius-lg)',
        boxShadow: '0 25px 50px -12px rgba(0, 0, 0, 0.5)',
        border: '1px solid var(--border-light)',
      }}>
        {/* Modal Header */}
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '24px' }}>
          <div>
            <h3 style={{ fontSize: '1.3rem', fontWeight: '800', color: 'var(--text-main)' }}>
              New Autonomous Software Project
            </h3>
            <p style={{ fontSize: '0.85rem', color: 'var(--text-muted)', marginTop: '4px' }}>
              SEAGENT coordinates 11 specialized AI agents across the entire SDLC pipeline.
            </p>
          </div>
          <button
            onClick={onClose}
            style={{
              background: 'transparent',
              border: 'none',
              color: 'var(--text-dim)',
              cursor: 'pointer',
              padding: '6px',
            }}
          >
            <X size={20} />
          </button>
        </div>

        {error && (
          <div style={{
            background: 'rgba(244, 63, 94, 0.1)',
            border: '1px solid rgba(244, 63, 94, 0.3)',
            borderRadius: 'var(--radius-md)',
            padding: '12px 16px',
            color: '#fb7185',
            fontSize: '0.88rem',
            marginBottom: '20px',
          }}>
            {error}
          </div>
        )}

        {/* Demo Presets Quick-Select */}
        <div style={{ marginBottom: '22px' }}>
          <label style={{ display: 'flex', alignItems: 'center', gap: '6px', fontSize: '0.8rem', fontWeight: '700', color: 'var(--text-muted)', textTransform: 'uppercase', marginBottom: '8px', letterSpacing: '0.05em' }}>
            <Sparkles size={14} color="#818cf8" /> Quick-Start Project Templates
          </label>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(210px, 1fr))', gap: '10px' }}>
            {DEMO_PRESETS.map((p, idx) => (
              <button
                key={idx}
                type="button"
                onClick={() => applyPreset(p)}
                style={{
                  background: projectName === p.projectName ? 'rgba(99, 102, 241, 0.12)' : 'rgba(255, 255, 255, 0.02)',
                  border: projectName === p.projectName ? '1px solid #6366f1' : '1px solid var(--border-subtle)',
                  borderRadius: 'var(--radius-md)',
                  padding: '10px 12px',
                  textAlign: 'left',
                  cursor: 'pointer',
                  transition: 'all 0.15s ease',
                }}
              >
                <div style={{ fontSize: '0.82rem', fontWeight: '700', color: 'var(--text-main)', marginBottom: '3px' }}>
                  {p.projectName}
                </div>
                <div style={{ fontSize: '0.72rem', color: 'var(--text-dim)', lineHeight: '1.4' }}>
                  {p.title}
                </div>
              </button>
            ))}
          </div>
        </div>

        <form onSubmit={handleSubmit}>
          {/* Project Name */}
          <div style={{ marginBottom: '18px' }}>
            <label style={{ display: 'block', fontSize: '0.82rem', fontWeight: '600', color: 'var(--text-main)', marginBottom: '6px' }}>
              Project Title
            </label>
            <input
              type="text"
              value={projectName}
              onChange={(e) => setProjectName(e.target.value)}
              placeholder="e.g. Distributed Task Orchestrator"
              style={{
                width: '100%',
                background: 'rgba(0, 0, 0, 0.3)',
                border: '1px solid var(--border-subtle)',
                borderRadius: 'var(--radius-md)',
                padding: '10px 14px',
                color: 'var(--text-main)',
                fontSize: '0.9rem',
                outline: 'none',
              }}
            />
          </div>

          {/* Software Requirement */}
          <div style={{ marginBottom: '18px' }}>
            <label style={{ display: 'block', fontSize: '0.82rem', fontWeight: '600', color: 'var(--text-main)', marginBottom: '6px' }}>
              Natural-Language Software Requirement <span style={{ color: '#ef4444' }}>*</span>
            </label>
            <textarea
              rows={4}
              value={requirement}
              onChange={(e) => setRequirement(e.target.value)}
              placeholder="Describe your software requirement in plain English. The 11 AI agents will analyze requirements, build architecture, write code, run automated tests, debug failures, perform security review, optimize complexity, and generate technical documentation."
              style={{
                width: '100%',
                background: 'rgba(0, 0, 0, 0.3)',
                border: '1px solid var(--border-subtle)',
                borderRadius: 'var(--radius-md)',
                padding: '12px 14px',
                color: 'var(--text-main)',
                fontSize: '0.9rem',
                lineHeight: '1.5',
                outline: 'none',
                resize: 'vertical',
              }}
            />
          </div>

          {/* Technology Preferences */}
          <div style={{ marginBottom: '18px' }}>
            <label style={{ display: 'block', fontSize: '0.82rem', fontWeight: '600', color: 'var(--text-main)', marginBottom: '6px' }}>
              Optional Technology Preferences / Constraints
            </label>
            <input
              type="text"
              value={techPreferences}
              onChange={(e) => setTechPreferences(e.target.value)}
              placeholder="e.g. Clean layered architecture, Python 3.10+, in-memory repository"
              style={{
                width: '100%',
                background: 'rgba(0, 0, 0, 0.3)',
                border: '1px solid var(--border-subtle)',
                borderRadius: 'var(--radius-md)',
                padding: '10px 14px',
                color: 'var(--text-main)',
                fontSize: '0.9rem',
                outline: 'none',
              }}
            />
          </div>

          {/* LLM Engine Selection */}
          <div style={{ marginBottom: '24px' }}>
            <label style={{ display: 'block', fontSize: '0.82rem', fontWeight: '700', color: 'var(--text-muted)', textTransform: 'uppercase', marginBottom: '8px', letterSpacing: '0.05em' }}>
              Select LLM Provider Engine
            </label>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '10px' }}>
              {/* Option 1: Mock Provider */}
              <div
                onClick={() => setProvider('mock')}
                style={{
                  border: provider === 'mock' ? '2px solid #6366f1' : '1px solid var(--border-subtle)',
                  background: provider === 'mock' ? 'rgba(99, 102, 241, 0.12)' : 'rgba(255, 255, 255, 0.02)',
                  borderRadius: 'var(--radius-md)',
                  padding: '12px',
                  cursor: 'pointer',
                  transition: 'all 0.15s ease',
                }}
              >
                <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '4px' }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '6px', fontWeight: '700', fontSize: '0.85rem', color: 'var(--text-main)' }}>
                    <ShieldCheck size={16} color="#34d399" />
                    Offline Mock
                  </div>
                  <span className="badge badge-emerald" style={{ fontSize: '0.65rem' }}>FREE</span>
                </div>
                <div style={{ fontSize: '0.72rem', color: 'var(--text-dim)', lineHeight: '1.4' }}>
                  Deterministic dry run for viva evaluation & testing without API costs.
                </div>
              </div>

              {/* Option 2: OpenAI */}
              <div
                onClick={() => setProvider('openai')}
                style={{
                  border: provider === 'openai' ? '2px solid #6366f1' : '1px solid var(--border-subtle)',
                  background: provider === 'openai' ? 'rgba(99, 102, 241, 0.12)' : 'rgba(255, 255, 255, 0.02)',
                  borderRadius: 'var(--radius-md)',
                  padding: '12px',
                  cursor: 'pointer',
                  transition: 'all 0.15s ease',
                }}
              >
                <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '4px' }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '6px', fontWeight: '700', fontSize: '0.85rem', color: 'var(--text-main)' }}>
                    <Cpu size={16} color="#818cf8" />
                    OpenAI GPT
                  </div>
                  <span className={isOpenAIConfigured ? 'badge badge-indigo' : 'badge badge-amber'} style={{ fontSize: '0.65rem' }}>
                    {isOpenAIConfigured ? 'READY' : 'NEEDS KEY'}
                  </span>
                </div>
                <div style={{ fontSize: '0.72rem', color: 'var(--text-dim)', lineHeight: '1.4' }}>
                  {config?.openai_model || 'gpt-4o-mini'} structured outputs via OpenAI SDK.
                </div>
              </div>

              {/* Option 3: Google Gemini */}
              <div
                onClick={() => setProvider('gemini')}
                style={{
                  border: provider === 'gemini' ? '2px solid #6366f1' : '1px solid var(--border-subtle)',
                  background: provider === 'gemini' ? 'rgba(99, 102, 241, 0.12)' : 'rgba(255, 255, 255, 0.02)',
                  borderRadius: 'var(--radius-md)',
                  padding: '12px',
                  cursor: 'pointer',
                  transition: 'all 0.15s ease',
                }}
              >
                <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '4px' }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '6px', fontWeight: '700', fontSize: '0.85rem', color: 'var(--text-main)' }}>
                    <Bot size={16} color="#a78bfa" />
                    Google Gemini
                  </div>
                  <span className={isGeminiAvailable ? 'badge badge-purple' : 'badge badge-amber'} style={{ fontSize: '0.65rem' }}>
                    {isGeminiAvailable ? 'READY' : 'NEEDS KEY'}
                  </span>
                </div>
                <div style={{ fontSize: '0.72rem', color: 'var(--text-dim)', lineHeight: '1.4' }}>
                  {config?.gemini_model || 'gemini-2.5-flash'} via official Google GenAI SDK.
                </div>
              </div>
            </div>
          </div>

          {/* Actions */}
          <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '12px' }}>
            <button type="button" className="btn-secondary" onClick={onClose} disabled={loading}>
              Cancel
            </button>
            <button type="submit" className="btn-primary" disabled={loading}>
              <Play size={16} />
              <span>{loading ? 'Initializing...' : 'Start SEAGENT Pipeline'}</span>
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}
