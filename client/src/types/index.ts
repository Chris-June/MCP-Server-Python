// Type definitions for the MCP client

export interface Role {
  id: string
  name: string
  description: string
  instructions: string
  domains: string[]
  tone: string
  system_prompt: string
  is_default: boolean
}

export interface Memory {
  id: string
  role_id: string
  content: string
  type: string
  importance: string
  embedding?: number[]
  created_at: string
  expires_at: string
}

export interface ProcessQueryRequest {
  role_id: string
  query: string
  custom_instructions?: string
}

export interface ProcessQueryResponse {
  role_id: string
  query: string
  response: string
}
