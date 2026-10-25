const BASE_URL = '' // Uses Vite proxy in dev, direct relative in production

export async function fetchConfig() {
  const res = await fetch(`${BASE_URL}/api/v1/config`)
  if (!res.ok) throw new Error('Failed to fetch system configuration')
  return res.json()
}

export async function fetchHealth() {
  const res = await fetch(`${BASE_URL}/health`)
  if (!res.ok) throw new Error('Backend health check failed')
  return res.json()
}

export async function startWorkflow({ projectName, requirement, techPreferences, provider, useMock }) {
  const res = await fetch(`${BASE_URL}/api/v1/workflows/run`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      project_name: projectName,
      requirement: requirement,
      tech_preferences: techPreferences,
      provider: provider || '',
      use_mock: Boolean(useMock || provider === 'mock'),
    }),
  })
  if (!res.ok) {
    const errorData = await res.json().catch(() => ({}))
    throw new Error(errorData.detail || 'Failed to start workflow')
  }
  return res.json()
}

export async function fetchWorkflowStatus(workflowId) {
  const res = await fetch(`${BASE_URL}/api/v1/workflows/${workflowId}/status`)
  if (!res.ok) throw new Error('Failed to fetch status')
  return res.json()
}

export async function fetchWorkflowDetails(workflowId) {
  const res = await fetch(`${BASE_URL}/api/v1/workflows/${workflowId}`)
  if (!res.ok) throw new Error('Failed to fetch workflow details')
  return res.json()
}

export async function listWorkflows() {
  const res = await fetch(`${BASE_URL}/api/v1/workflows`)
  if (!res.ok) throw new Error('Failed to list workflows')
  return res.json()
}

export function downloadProjectZip(workflowId) {
  window.open(`${BASE_URL}/api/v1/workflows/${workflowId}/download`, '_blank')
}
