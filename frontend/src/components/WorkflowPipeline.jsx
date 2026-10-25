import React from 'react'
import {
  FileText,
  Calendar,
  Layers,
  ShieldCheck,
  Code2,
  CheckCircle,
  Bug,
  Lock,
  Zap,
  Award,
  BookOpen,
  Loader2,
  AlertCircle,
} from 'lucide-react'

const AGENT_STEPS = [
  { id: 'requirements', name: 'Requirements', role: 'RequirementsAgent', icon: FileText, stepNum: 1 },
  { id: 'plan', name: 'Planning', role: 'PlanningAgent', icon: Calendar, stepNum: 2 },
  { id: 'architecture', name: 'Architecture', role: 'ArchitectureAgent', icon: Layers, stepNum: 3 },
  { id: 'senior_review', name: 'Reasoning', role: 'SeniorReasoningAgent', altRole: 'SeniorEngineerAgent', icon: ShieldCheck, stepNum: 4 },
  { id: 'code', name: 'Coding', role: 'CodingAgent', icon: Code2, stepNum: 5 },
  { id: 'testing', name: 'Testing', role: 'TestingAgent', icon: CheckCircle, stepNum: 6 },
  { id: 'debugging', name: 'Debugging', role: 'DebuggingAgent', icon: Bug, stepNum: 7 },
  { id: 'security', name: 'Security', role: 'SecurityReviewAgent', icon: Lock, stepNum: 8 },
  { id: 'optimization', name: 'Optimization', role: 'CodeOptimizationAgent', icon: Zap, stepNum: 9 },
  { id: 'final_review', name: 'Final Review', role: 'FinalReviewAgent', icon: Award, stepNum: 10 },
  { id: 'documentation', name: 'Docs', role: 'DocumentationAgent', icon: BookOpen, stepNum: 11 },
]

export default function WorkflowPipeline({ workflow, activeTab, onTabSelect }) {
  if (!workflow) return null

  const currentStep = workflow.current_step || 0
  const isFailed = workflow.status === 'FAILED'
  const isCompleted = workflow.status === 'COMPLETED'
  const currentAgent = workflow.current_agent || ''
  const retryCount = workflow.retry_count || 0
  const provider = workflow.provider || 'gemini'

  return (
    <div className="glass-panel" style={{ padding: '20px 24px', margin: '24px 28px' }}>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '16px', flexWrap: 'wrap', gap: '12px' }}>
        <div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <span style={{ fontSize: '0.8rem', color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
              LangGraph Multi-Agent Orchestration • 11 Autonomous Agents
            </span>
            <span className="badge badge-indigo" style={{ textTransform: 'uppercase', fontSize: '0.7rem' }}>
              {provider}
            </span>
          </div>
          <h2 style={{ fontSize: '1.15rem', fontWeight: '800', color: 'var(--text-main)', marginTop: '2px' }}>
            {workflow.project_name || 'Software Lifecycle Pipeline'}
          </h2>
        </div>

        {/* Global Pipeline Status Pill */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
          {isCompleted && (
            <span className="badge badge-emerald">
              <CheckCircle size={13} /> Completed (100%)
            </span>
          )}
          {!isCompleted && !isFailed && (
            <span className="badge badge-indigo running-pulse">
              <Loader2 size={13} style={{ animation: 'spin 1s linear infinite' }} />
              Running: {currentAgent || 'Workflow Coordinator'} ({workflow.progress_percentage || 0}%)
            </span>
          )}
          {isFailed && (
            <span className="badge badge-rose">
              <AlertCircle size={13} /> Execution Failed
            </span>
          )}
          {retryCount > 0 && (
            <span className="badge badge-amber">
              <Bug size={13} /> Debug Retries: {retryCount}
            </span>
          )}
        </div>
      </div>

      {/* Progress Bar */}
      <div style={{
        width: '100%',
        height: '4px',
        background: 'rgba(255, 255, 255, 0.06)',
        borderRadius: '999px',
        overflow: 'hidden',
        marginBottom: '20px',
      }}>
        <div style={{
          width: `${workflow.progress_percentage || 0}%`,
          height: '100%',
          background: 'linear-gradient(90deg, #6366f1 0%, #a855f7 50%, #10b981 100%)',
          transition: 'width 0.4s ease',
        }} />
      </div>

      {/* Agents Pipeline Horizontal Sequence */}
      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(11, minmax(0, 1fr))',
        gap: '6px',
        overflowX: 'auto',
      }}>
        {AGENT_STEPS.map((step) => {
          const Icon = step.icon
          const isCurrent = (currentAgent === step.role || currentAgent === step.altRole) && !isCompleted && !isFailed
          const isDone = isCompleted || currentStep > step.stepNum
          const isStepFailed = isFailed && (currentAgent === step.role || currentAgent === step.altRole)
          const isSelected = activeTab === step.id

          let statusBg = 'rgba(255, 255, 255, 0.02)'
          let borderColor = 'var(--border-subtle)'
          let iconColor = 'var(--text-dim)'

          if (isDone) {
            statusBg = 'rgba(16, 185, 129, 0.08)'
            borderColor = 'rgba(16, 185, 129, 0.35)'
            iconColor = '#34d399'
          } else if (isCurrent) {
            statusBg = 'rgba(99, 102, 241, 0.15)'
            borderColor = 'rgba(99, 102, 241, 0.6)'
            iconColor = '#818cf8'
          } else if (isStepFailed) {
            statusBg = 'rgba(244, 63, 94, 0.12)'
            borderColor = 'rgba(244, 63, 94, 0.5)'
            iconColor = '#fb7185'
          }

          if (isSelected) {
            borderColor = '#6366f1'
          }

          return (
            <button
              key={step.id}
              onClick={() => onTabSelect(step.id)}
              style={{
                background: statusBg,
                border: `1px solid ${borderColor}`,
                borderRadius: 'var(--radius-md)',
                padding: '10px 4px',
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
                gap: '6px',
                cursor: 'pointer',
                transition: 'all 0.2s ease',
                position: 'relative',
                boxShadow: isCurrent ? '0 0 15px rgba(99, 102, 241, 0.3)' : 'none',
                minWidth: '68px',
              }}
            >
              <div style={{
                width: '30px',
                height: '30px',
                borderRadius: '8px',
                background: isDone ? 'rgba(16, 185, 129, 0.15)' : isCurrent ? 'rgba(99, 102, 241, 0.25)' : 'rgba(255,255,255,0.04)',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
              }}>
                {isCurrent ? (
                  <Loader2 size={15} color={iconColor} style={{ animation: 'spin 1.5s linear infinite' }} />
                ) : (
                  <Icon size={15} color={iconColor} />
                )}
              </div>

              <div style={{ textAlign: 'center' }}>
                <div style={{ fontSize: '0.72rem', fontWeight: '700', color: isDone || isCurrent ? 'var(--text-main)' : 'var(--text-muted)', whiteSpace: 'nowrap' }}>
                  {step.name}
                </div>
                <div style={{ fontSize: '0.62rem', color: isCurrent ? '#818cf8' : isDone ? '#34d399' : 'var(--text-dim)' }}>
                  {isCurrent ? 'Running' : isDone ? 'Done' : 'Pending'}
                </div>
              </div>

              {isSelected && (
                <div style={{
                  position: 'absolute',
                  bottom: '-1px',
                  width: '50%',
                  height: '2px',
                  background: '#6366f1',
                  borderRadius: '2px',
                }} />
              )}
            </button>
          )
        })}
      </div>
    </div>
  )
}
