import React, { useState, useEffect, useRef } from 'react'
import Header from './components/Header'
import WorkflowPipeline from './components/WorkflowPipeline'
import NewProjectModal from './components/NewProjectModal'
import RequirementsTab from './components/RequirementsTab'
import PlanTab from './components/PlanTab'
import ArchitectureTab from './components/ArchitectureTab'
import SeniorReviewTab from './components/SeniorReviewTab'
import CodeViewerTab from './components/CodeViewerTab'
import TestingTab from './components/TestingTab'
import DebuggingTab from './components/DebuggingTab'
import FinalReviewTab from './components/FinalReviewTab'
import DocumentationTab from './components/DocumentationTab'
import SecurityTab from './components/SecurityTab'
import OptimizationTab from './components/OptimizationTab'
import LiveLogsDrawer from './components/LiveLogsDrawer'

import {
  fetchConfig,
  listWorkflows,
  startWorkflow,
  fetchWorkflowStatus,
  fetchWorkflowDetails,
} from './services/api'

import {
  Bot,
  Play,
  Layers,
  Sparkles,
  CheckCircle2,
  Clock,
  ArrowRight,
  ShieldCheck,
  Code2,
  CheckCircle,
  Bug,
  Award,
  BookOpen,
  Calendar,
  FileText,
  Lock,
  Zap,
} from 'lucide-react'

const TABS = [
  { id: 'requirements', label: '1. Requirements', icon: FileText },
  { id: 'plan', label: '2. Plan', icon: Calendar },
  { id: 'architecture', label: '3. Architecture', icon: Layers },
  { id: 'senior_review', label: '4. Reasoning', icon: ShieldCheck },
  { id: 'code', label: '5. Generated Code', icon: Code2 },
  { id: 'testing', label: '6. Testing', icon: CheckCircle },
  { id: 'debugging', label: '7. Debugging', icon: Bug },
  { id: 'security', label: '8. Security', icon: Lock },
  { id: 'optimization', label: '9. Optimization', icon: Zap },
  { id: 'final_review', label: '10. Final Review', icon: Award },
  { id: 'documentation', label: '11. Documentation', icon: BookOpen },
]

export default function App() {
  const [config, setConfig] = useState(null)
  const [recentRuns, setRecentRuns] = useState([])
  const [activeWorkflowId, setActiveWorkflowId] = useState('')
  const [workflowData, setWorkflowData] = useState(null)
  const [activeTab, setActiveTab] = useState('requirements')
  const [isModalOpen, setIsModalOpen] = useState(false)
  const [loading, setLoading] = useState(true)

  const pollingRef = useRef(null)

  // 1. Initial Load: Config and Recent Runs
  useEffect(() => {
    async function init() {
      try {
        const [cfg, runs] = await Promise.all([
          fetchConfig().catch(() => null),
          listWorkflows().catch(() => []),
        ])
        setConfig(cfg)
        setRecentRuns(runs)

        // Select the most recent run if available
        if (runs.length > 0) {
          const latestId = runs[0].workflow_id
          setActiveWorkflowId(latestId)
          loadWorkflow(latestId)
        }
      } catch (err) {
        console.error('Initialization error:', err)
      } finally {
        setLoading(false)
      }
    }
    init()
  }, [])

  // 2. Load complete workflow details
  const loadWorkflow = async (id) => {
    if (!id) return
    try {
      const data = await fetchWorkflowDetails(id)
      setWorkflowData(data)
    } catch (err) {
      console.error('Failed to load workflow data:', err)
    }
  }

  // 3. Polling when workflow is actively executing
  useEffect(() => {
    if (!activeWorkflowId) return

    const isRunning =
      workflowData?.status &&
      workflowData.status !== 'COMPLETED' &&
      workflowData.status !== 'FAILED'

    if (isRunning) {
      pollingRef.current = setInterval(async () => {
        try {
          const statusRes = await fetchWorkflowStatus(activeWorkflowId)
          // Update lightweight status
          setWorkflowData((prev) => ({
            ...(prev || {}),
            status: statusRes.status,
            current_agent: statusRes.current_agent,
            current_step: statusRes.current_step,
            progress_percentage: statusRes.progress_percentage,
            retry_count: statusRes.retry_count,
            recent_logs: statusRes.recent_logs,
          }))

          // If reached terminal or step updated, fetch complete details
          if (
            statusRes.status === 'COMPLETED' ||
            statusRes.status === 'FAILED' ||
            statusRes.current_step !== workflowData?.current_step
          ) {
            const fullDetails = await fetchWorkflowDetails(activeWorkflowId)
            setWorkflowData(fullDetails)

            // Auto-switch to active tab
            if (statusRes.current_agent) {
              const matchingTab = TABS.find((t) =>
                statusRes.current_agent.toLowerCase().includes(t.id)
              )
              if (matchingTab) {
                setActiveTab(matchingTab.id)
              }
            }

            // Refresh recent runs list
            const runs = await listWorkflows()
            setRecentRuns(runs)
          }
        } catch (pollErr) {
          console.error('Polling error:', pollErr)
        }
      }, 1500)
    } else {
      if (pollingRef.current) clearInterval(pollingRef.current)
    }

    return () => {
      if (pollingRef.current) clearInterval(pollingRef.current)
    }
  }, [activeWorkflowId, workflowData?.status, workflowData?.current_step])

  // 4. Handle Starting a New Workflow
  const handleStartWorkflow = async (params) => {
    const res = await startWorkflow(params)
    setActiveWorkflowId(res.workflow_id)
    setActiveTab('requirements')

    // Initial placeholder state
    setWorkflowData({
      workflow_id: res.workflow_id,
      project_name: res.project_name,
      user_requirement: params.requirement,
      status: 'IDLE',
      current_agent: 'RequirementsAgent',
      current_step: 1,
      progress_percentage: 5,
      retry_count: 0,
      logs: [],
    })

    // Refresh runs list
    const runs = await listWorkflows().catch(() => [])
    setRecentRuns(runs)
  }

  return (
    <div style={{ minHeight: '100vh', display: 'flex', flexDirection: 'column', paddingBottom: '70px' }}>
      {/* Top Navigation */}
      <Header
        config={config}
        onOpenNewProject={() => setIsModalOpen(true)}
        activeWorkflow={workflowData}
        recentRuns={recentRuns}
        onSelectWorkflow={(id) => {
          setActiveWorkflowId(id)
          loadWorkflow(id)
        }}
      />

      {/* Main Content Area */}
      <main style={{ flex: 1 }}>
        {workflowData ? (
          <div>
            {/* Visual Pipeline Bar */}
            <WorkflowPipeline
              workflow={workflowData}
              activeTab={activeTab}
              onTabSelect={(tabId) => setActiveTab(tabId)}
            />

            {/* Navigation Tab Bar */}
            <div style={{
              margin: '0 28px 20px',
              borderBottom: '1px solid var(--border-subtle)',
              display: 'flex',
              gap: '6px',
              overflowX: 'auto',
            }}>
              {TABS.map((tab) => {
                const Icon = tab.icon
                const isActive = activeTab === tab.id
                return (
                  <button
                    key={tab.id}
                    onClick={() => setActiveTab(tab.id)}
                    style={{
                      background: 'transparent',
                      border: 'none',
                      borderBottom: isActive ? '2px solid #6366f1' : '2px solid transparent',
                      color: isActive ? '#ffffff' : 'var(--text-muted)',
                      padding: '10px 16px',
                      fontSize: '0.85rem',
                      fontWeight: isActive ? '700' : '500',
                      cursor: 'pointer',
                      display: 'flex',
                      alignItems: 'center',
                      gap: '8px',
                      transition: 'all 0.15s ease',
                      whiteSpace: 'nowrap',
                    }}
                  >
                    <Icon size={16} color={isActive ? '#818cf8' : 'var(--text-dim)'} />
                    <span>{tab.label}</span>
                  </button>
                )
              })}
            </div>

            {/* Tab Body View */}
            <div style={{ margin: '0 28px 28px' }}>
              {activeTab === 'requirements' && (
                <RequirementsTab requirements={workflowData.requirements} />
              )}
              {activeTab === 'plan' && (
                <PlanTab plan={workflowData.plan} />
              )}
              {activeTab === 'architecture' && (
                <ArchitectureTab architecture={workflowData.architecture} />
              )}
              {activeTab === 'senior_review' && (
                <SeniorReviewTab seniorReview={workflowData.senior_review} />
              )}
              {activeTab === 'code' && (
                <CodeViewerTab
                  workflowId={workflowData.workflow_id}
                  files={workflowData.generated_files}
                />
              )}
              {activeTab === 'testing' && (
                <TestingTab
                  testReport={workflowData.test_report}
                  retryCount={workflowData.retry_count}
                />
              )}
              {activeTab === 'debugging' && (
                <DebuggingTab
                  debuggingHistory={workflowData.debugging_history}
                  retryCount={workflowData.retry_count}
                />
              )}
              {activeTab === 'security' && (
                <SecurityTab securityReview={workflowData.security_review} />
              )}
              {activeTab === 'optimization' && (
                <OptimizationTab optimization={workflowData.optimization} />
              )}
              {activeTab === 'final_review' && (
                <FinalReviewTab finalReview={workflowData.final_review} />
              )}
              {activeTab === 'documentation' && (
                <DocumentationTab documentation={workflowData.documentation} />
              )}
            </div>
          </div>
        ) : (
          /* Empty / Landing State */
          <div style={{
            maxWidth: '820px',
            margin: '80px auto',
            padding: '40px',
            textAlign: 'center',
          }}>
            <div style={{
              width: '64px',
              height: '64px',
              borderRadius: '18px',
              background: 'linear-gradient(135deg, #6366f1 0%, #a855f7 100%)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              margin: '0 auto 20px',
              boxShadow: '0 0 35px rgba(99, 102, 241, 0.5)',
            }}>
              <Bot size={36} color="#ffffff" />
            </div>

            <h2 style={{ fontSize: '2rem', fontWeight: '800', letterSpacing: '-0.02em', marginBottom: '12px' }}>
              Welcome to SEAGENT
            </h2>
            <p style={{ color: 'var(--text-muted)', fontSize: '1rem', lineHeight: '1.6', marginBottom: '28px', maxWidth: '640px', margin: '0 auto 28px' }}>
              An autonomous Multi-Agent AI Software Engineering Framework powered by Google Gemini and LangGraph.
              Input a natural-language requirement and let 9 specialized agents analyze, design, code, test in a sandbox, debug, and document your project.
            </p>

            <button
              className="btn-primary"
              onClick={() => setIsModalOpen(true)}
              style={{ padding: '14px 28px', fontSize: '1rem' }}
            >
              <Play size={18} />
              <span>Create New Software Project</span>
            </button>
          </div>
        )}
      </main>

      {/* Live Logs Stream Drawer */}
      <LiveLogsDrawer logs={workflowData?.logs || workflowData?.recent_logs} />

      {/* New Project Input Modal */}
      <NewProjectModal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        onStart={handleStartWorkflow}
        config={config}
        isGeminiConfigured={config?.gemini_configured}
      />
    </div>
  )
}
