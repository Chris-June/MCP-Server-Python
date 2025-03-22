import type { Role, Memory, ProcessQueryRequest, ProcessQueryResponse } from '@/types'

export interface CreateMemoryRequest {
  role_id: string
  content: string
  type: string
  importance: string
}

// API Client
const API_BASE = 'http://localhost:8000/api/v1'

// Enable CORS for development
const fetchOptions = {
  headers: {
    'Content-Type': 'application/json',
  },
  credentials: 'include' as RequestCredentials
}

export async function fetchRoles(): Promise<Role[]> {
  const response = await fetch(`${API_BASE}/roles`, fetchOptions)
  if (!response.ok) {
    throw new Error('Failed to fetch roles')
  }
  const data = await response.json()
  return data.roles
}

export async function fetchRole(roleId: string): Promise<Role> {
  const response = await fetch(`${API_BASE}/roles/${roleId}`, fetchOptions)
  if (!response.ok) {
    throw new Error(`Failed to fetch role: ${roleId}`)
  }
  const data = await response.json()
  return data.role
}

export async function createRole(role: Omit<Role, 'is_default'>): Promise<Role> {
  const response = await fetch(`${API_BASE}/roles`, {
    ...fetchOptions,
    method: 'POST',
    body: JSON.stringify(role),
  })
  if (!response.ok) {
    throw new Error('Failed to create role')
  }
  const data = await response.json()
  return data.role
}

export async function updateRole(roleId: string, role: Partial<Role>): Promise<Role> {
  const response = await fetch(`${API_BASE}/roles/${roleId}`, {
    ...fetchOptions,
    method: 'PATCH',
    body: JSON.stringify(role),
  })
  if (!response.ok) {
    throw new Error(`Failed to update role: ${roleId}`)
  }
  const data = await response.json()
  return data.role
}

export async function deleteRole(roleId: string): Promise<void> {
  const response = await fetch(`${API_BASE}/roles/${roleId}`, {
    method: 'DELETE',
  })
  if (!response.ok) {
    throw new Error(`Failed to delete role: ${roleId}`)
  }
}

export async function processQuery(request: ProcessQueryRequest): Promise<ProcessQueryResponse> {
  const response = await fetch(`${API_BASE}/roles/process`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(request),
  })
  if (!response.ok) {
    throw new Error('Failed to process query')
  }
  return await response.json()
}

export async function processQueryStream(request: ProcessQueryRequest, onChunk: (chunk: string) => void): Promise<string> {
  const response = await fetch(`${API_BASE}/roles/process/stream`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(request),
  })
  
  if (!response.ok) {
    throw new Error('Failed to process streaming query')
  }
  
  const reader = response.body?.getReader()
  const decoder = new TextDecoder()
  let fullResponse = ''
  
  if (!reader) {
    throw new Error('Stream reader not available')
  }
  
  try {
    while (true) {
      const { done, value } = await reader.read()
      if (done) break
      
      const chunk = decoder.decode(value, { stream: true })
      const lines = chunk.split('\n\n')
      
      for (const line of lines) {
        if (line.startsWith('data: ')) {
          const data = line.substring(6)
          if (data === '[DONE]') continue
          onChunk(data)
          fullResponse += data
        }
      }
    }
    return fullResponse
  } catch (error) {
    console.error('Error reading stream:', error)
    throw error
  } finally {
    reader.releaseLock()
  }
}

export async function fetchMemories(roleId: string): Promise<Memory[]> {
  const response = await fetch(`${API_BASE}/memories/${roleId}`)
  if (!response.ok) {
    throw new Error(`Failed to fetch memories for role: ${roleId}`)
  }
  const data = await response.json()
  return data.memories
}

export async function createMemory(memory: CreateMemoryRequest): Promise<Memory> {
  const response = await fetch(`${API_BASE}/memories`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(memory),
  })
  if (!response.ok) {
    throw new Error('Failed to create memory')
  }
  const data = await response.json()
  return data.memory
}

export async function clearMemories(roleId: string): Promise<void> {
  const response = await fetch(`${API_BASE}/memories/${roleId}`, {
    method: 'DELETE',
  })
  if (!response.ok) {
    throw new Error(`Failed to clear memories for role: ${roleId}`)
  }
}
