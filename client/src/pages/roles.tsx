import { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { Link } from 'react-router-dom'
import { motion } from 'framer-motion'
import { Edit, Plus, Trash2 } from 'lucide-react'

import { fetchRoles, deleteRole, createRole } from '@/lib/api'
import type { Role } from '@/types'
import { Button } from '@/components/ui/button'
import { useToast } from '@/components/ui/use-toast'
import { truncateText } from '@/lib/utils'

export default function RolesPage() {
  const { toast } = useToast()
  const queryClient = useQueryClient()
  const [showCreateForm, setShowCreateForm] = useState(false)
  const [formData, setFormData] = useState<Omit<Role, 'id' | 'is_default'>>({
    name: '',
    description: '',
    instructions: '',
    domains: [],
    tone: 'professional',
    system_prompt: ''
  })
  const [newDomain, setNewDomain] = useState('')

  const { data: roles, isLoading, error } = useQuery({
    queryKey: ['roles'],
    queryFn: fetchRoles
  })

  const createMutation = useMutation({
    mutationFn: createRole,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['roles'] })
      setShowCreateForm(false)
      setFormData({
        name: '',
        description: '',
        instructions: '',
        domains: [],
        tone: 'professional',
        system_prompt: ''
      })
      setNewDomain('')
      toast({
        title: 'Role created',
        description: 'The role has been successfully created.',
      })
    },
    onError: (error) => {
      toast({
        title: 'Error',
        description: `Failed to create role: ${error.message}`,
        variant: 'destructive',
      })
    },
  })

  const deleteMutation = useMutation({
    mutationFn: deleteRole,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['roles'] })
      toast({
        title: 'Role deleted',
        description: 'The role has been successfully deleted.',
      })
    },
    onError: (error) => {
      toast({
        title: 'Error',
        description: `Failed to delete role: ${error.message}`,
        variant: 'destructive',
      })
    },
  })

  const handleDelete = (roleId: string) => {
    if (window.confirm('Are you sure you want to delete this role?')) {
      deleteMutation.mutate(roleId)
    }
  }

  if (isLoading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="p-6 bg-destructive/10 border border-destructive rounded-lg text-center">
        <h2 className="text-xl font-semibold mb-2">Error Loading Roles</h2>
        <p className="text-muted-foreground mb-4">{(error as Error).message}</p>
        <Button onClick={() => queryClient.invalidateQueries({ queryKey: ['roles'] })}>
          Try Again
        </Button>
      </div>
    )
  }

  return (
    <div>
      <div className="flex justify-between items-center mb-8">
        <div>
          <h1 className="text-3xl font-bold">AI Roles</h1>
          <p className="text-muted-foreground mt-1">
            Manage specialized AI roles with different expertise and personalities.
          </p>
        </div>
        <Button onClick={() => setShowCreateForm(!showCreateForm)}>
          <Plus className="mr-2 h-4 w-4" />
          {showCreateForm ? 'Cancel' : 'Create Role'}
        </Button>
      </div>

      {showCreateForm && (
        <motion.div
          initial={{ opacity: 0, height: 0 }}
          animate={{ opacity: 1, height: 'auto' }}
          exit={{ opacity: 0, height: 0 }}
          className="mb-8 p-6 border rounded-lg bg-card"
        >
          <h2 className="text-xl font-semibold mb-4">Create New Role</h2>
          <form onSubmit={(e) => {
            e.preventDefault()
            // Add id to match the API's expected format
            const roleData = {
              ...formData,
              id: formData.name.toLowerCase().replace(/\s+/g, '-')
            }
            createMutation.mutate(roleData)
          }}>
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium mb-1">ID</label>
                <input
                  type="text"
                  name="id"
                  value={formData.name ? formData.name.toLowerCase().replace(/\s+/g, '-') : ''}
                  className="w-full p-2 border rounded-md bg-background text-muted-foreground"
                  disabled
                  placeholder="ID will be generated from name"
                />
                <p className="text-xs text-muted-foreground mt-1">ID is automatically generated from the name</p>
              </div>
              
              <div>
                <label className="block text-sm font-medium mb-1">Name</label>
                <p className="text-xs text-muted-foreground mb-2">A short, descriptive name for this AI role (e.g., Financial Advisor, Technical Support Specialist).</p>
                <input
                  type="text"
                  name="name"
                  value={formData.name}
                  onChange={(e) => setFormData({...formData, name: e.target.value})}
                  className="w-full p-2 border rounded-md bg-background"
                  placeholder="e.g., Financial Advisor, Technical Support Specialist"
                  required
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium mb-1">Description</label>
                <p className="text-xs text-muted-foreground mb-2">A brief summary of what this role does and its primary purpose.</p>
                <input
                  type="text"
                  name="description"
                  value={formData.description}
                  onChange={(e) => setFormData({...formData, description: e.target.value})}
                  className="w-full p-2 border rounded-md bg-background"
                  placeholder="e.g., Provides expert financial advice and retirement planning strategies"
                  required
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium mb-1">Domains</label>
                <p className="text-xs text-muted-foreground mb-2">Enter areas of expertise for this role (e.g., Finance, Marketing, Technical Support). These domains define what topics the AI role specializes in.</p>
                <div className="flex flex-wrap gap-2 mb-2">
                  {formData.domains.map((domain, index) => (
                    <span
                      key={domain}
                      className="px-2 py-1 bg-primary/10 text-primary text-xs rounded-full flex items-center"
                    >
                      {domain}
                      <button
                        type="button"
                        className="ml-1 text-primary/70 hover:text-primary"
                        onClick={() => {
                          const newDomains = [...formData.domains]
                          newDomains.splice(index, 1)
                          setFormData({...formData, domains: newDomains})
                        }}
                      >
                        ×
                      </button>
                    </span>
                  ))}
                </div>
                <div className="flex">
                  <input
                    type="text"
                    value={newDomain}
                    onChange={(e) => setNewDomain(e.target.value)}
                    className="flex-1 p-2 border rounded-l-md bg-background"
                    placeholder="e.g., Finance, Marketing, Technical Support"
                  />
                  <button
                    type="button"
                    className="px-4 py-2 bg-primary text-primary-foreground rounded-r-md"
                    onClick={() => {
                      if (newDomain.trim()) {
                        setFormData({
                          ...formData, 
                          domains: [...formData.domains, newDomain.trim()]
                        })
                        setNewDomain('')
                      }
                    }}
                  >
                    Add
                  </button>
                </div>
              </div>
              
              <div>
                <label className="block text-sm font-medium mb-1">Tone</label>
                <p className="text-xs text-muted-foreground mb-2">The communication style this role will use when responding to queries.</p>
                <select
                  name="tone"
                  value={formData.tone}
                  onChange={(e) => setFormData({...formData, tone: e.target.value})}
                  className="w-full p-2 border rounded-md bg-background"
                  required
                >
                  <option value="professional">Professional</option>
                  <option value="casual">Casual</option>
                  <option value="friendly">Friendly</option>
                  <option value="technical">Technical</option>
                  <option value="formal">Formal</option>
                </select>
              </div>
              
              <div>
                <label className="block text-sm font-medium mb-1">Instructions</label>
                <p className="text-xs text-muted-foreground mb-2">Specific guidelines for how this role should behave, respond, and what information it should prioritize.</p>
                <textarea
                  name="instructions"
                  value={formData.instructions}
                  onChange={(e) => setFormData({...formData, instructions: e.target.value})}
                  className="w-full p-2 border rounded-md bg-background min-h-[100px]"
                  placeholder="Example: You are a financial advisor with expertise in retirement planning. Always provide balanced advice considering both short-term and long-term financial goals. Explain concepts in simple terms and avoid financial jargon when possible."
                  required
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium mb-1">System Prompt</label>
                <p className="text-xs text-muted-foreground mb-2">Advanced configuration for the AI model. This defines the role's core behavior and capabilities in detail.</p>
                <textarea
                  name="system_prompt"
                  value={formData.system_prompt}
                  onChange={(e) => setFormData({...formData, system_prompt: e.target.value})}
                  className="w-full p-2 border rounded-md bg-background min-h-[100px]"
                  placeholder="Example: You are FinanceGPT, an AI assistant specialized in personal finance and investment strategies. You have extensive knowledge of retirement accounts, tax optimization, debt management, and investment vehicles. When providing advice, always consider risk tolerance, time horizon, and tax implications. Format your responses with clear sections and bullet points when appropriate."
                  required
                />
              </div>
              
              <div className="pt-4 flex justify-end">
                <Button type="submit" disabled={createMutation.isPending}>
                  {createMutation.isPending ? (
                    <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                  ) : (
                    <Plus className="h-4 w-4 mr-2" />
                  )}
                  Create Role
                </Button>
              </div>
            </div>
          </form>
        </motion.div>
      )}

      <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
        {roles?.map((role) => (
          <motion.div
            key={role.id}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="border rounded-lg overflow-hidden bg-card flex flex-col"
          >
            <div className="p-6 flex-1">
              <div className="flex justify-between items-start">
                <h3 className="text-xl font-semibold">{role.name}</h3>
                <div className="flex gap-2">
                  <Button variant="ghost" size="icon" asChild>
                    <Link to={`/roles/${role.id}`}>
                      <Edit className="h-4 w-4" />
                    </Link>
                  </Button>
                  <Button
                    variant="ghost"
                    size="icon"
                    onClick={() => handleDelete(role.id)}
                    disabled={role.is_default}
                  >
                    <Trash2 className="h-4 w-4" />
                  </Button>
                </div>
              </div>
              <p className="text-muted-foreground text-sm mt-1 mb-3">{role.description}</p>
              
              <div className="mt-4">
                <h4 className="text-sm font-medium mb-1">Domains</h4>
                <div className="flex flex-wrap gap-2">
                  {role.domains.map((domain) => (
                    <span
                      key={domain}
                      className="px-2 py-1 bg-primary/10 text-primary text-xs rounded-full"
                    >
                      {domain}
                    </span>
                  ))}
                </div>
              </div>
              
              <div className="mt-4">
                <h4 className="text-sm font-medium mb-1">Tone</h4>
                <span className="px-2 py-1 bg-secondary text-secondary-foreground text-xs rounded-full">
                  {role.tone}
                </span>
              </div>
              
              <div className="mt-4">
                <h4 className="text-sm font-medium mb-1">Instructions</h4>
                <p className="text-sm text-muted-foreground">
                  {truncateText(role.instructions, 100)}
                </p>
              </div>
            </div>
            
            <div className="p-4 border-t bg-muted/30 flex justify-between items-center">
              {role.is_default && (
                <span className="text-xs font-medium px-2 py-1 bg-primary/10 text-primary rounded-full">
                  Default Role
                </span>
              )}
              <Button asChild variant="outline" className="ml-auto">
                <Link to={`/chat?role=${role.id}`}>Chat with {role.name}</Link>
              </Button>
            </div>
          </motion.div>
        ))}
      </div>
      
      {roles?.length === 0 && (
        <div className="text-center p-12 border rounded-lg bg-muted/30">
          <h3 className="text-xl font-semibold mb-2">No Roles Found</h3>
          <p className="text-muted-foreground mb-4">
            Create your first AI role to get started.
          </p>
          <Button onClick={() => setShowCreateForm(true)}>
            <Plus className="mr-2 h-4 w-4" /> Create Role
          </Button>
        </div>
      )}
    </div>
  )
}
