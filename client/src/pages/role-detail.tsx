import React, { useState } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { motion } from 'framer-motion'
import { ArrowLeft, Save, Trash2, Globe } from 'lucide-react'



import { fetchRole, updateRole, deleteRole, fetchMemories, clearMemories } from '@/lib/api'
import type { Role, Memory } from '@/types'
import { Button } from '@/components/ui/button'
import { useToast } from '@/components/ui/use-toast'
import { formatDate } from '@/lib/utils'
import { BrowserPanel } from '@/components/BrowserPanel'

export default function RoleDetailPage() {
  const { roleId } = useParams<{ roleId: string }>()
  const navigate = useNavigate()
  const { toast } = useToast()
  const queryClient = useQueryClient()
  
  const [formData, setFormData] = useState<Partial<Role>>({})
  const [isEditing, setIsEditing] = useState(false)
  const [showBrowser, setShowBrowser] = useState(false)
  
  const { data: role, isLoading: roleLoading, error: roleError } = useQuery<Role>({
    queryKey: ['role', roleId],
    queryFn: () => fetchRole(roleId!),
    enabled: !!roleId,
  })

  // Update form data when role data is loaded
  React.useEffect(() => {
    if (role && !isEditing) {
      setFormData(role)
    }
  }, [role, isEditing])
  
  const { data: memories, isLoading: memoriesLoading } = useQuery({
    queryKey: ['memories', roleId],
    queryFn: () => fetchMemories(roleId!),
    enabled: !!roleId,
  })
  
  const updateMutation = useMutation({
    mutationFn: ({ id, data }: { id: string; data: Partial<Role> }) => updateRole(id, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['role', roleId] })
      setIsEditing(false)
      toast({
        title: 'Role updated',
        description: 'The role has been successfully updated.',
      })
    },
    onError: (error) => {
      toast({
        title: 'Error',
        description: `Failed to update role: ${error.message}`,
        variant: 'destructive',
      })
    },
  })
  
  const deleteMutation = useMutation({
    mutationFn: deleteRole,
    onSuccess: () => {
      navigate('/roles')
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
  
  const clearMemoriesMutation = useMutation({
    mutationFn: clearMemories,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['memories', roleId] })
      toast({
        title: 'Memories cleared',
        description: 'All memories for this role have been cleared.',
      })
    },
    onError: (error) => {
      toast({
        title: 'Error',
        description: `Failed to clear memories: ${error.message}`,
        variant: 'destructive',
      })
    },
  })
  
  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    const { name, value } = e.target
    setFormData((prev: Partial<Role>) => ({ ...prev, [name]: value }))
  }
  
  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (roleId) {
      updateMutation.mutate({ id: roleId, data: formData })
    }
  }
  
  const handleDelete = () => {
    if (window.confirm('Are you sure you want to delete this role? This action cannot be undone.')) {
      if (roleId) {
        deleteMutation.mutate(roleId)
      }
    }
  }
  
  const handleClearMemories = () => {
    if (window.confirm('Are you sure you want to clear all memories for this role? This action cannot be undone.')) {
      if (roleId) {
        clearMemoriesMutation.mutate(roleId)
      }
    }
  }
  
  if (roleLoading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div>
      </div>
    )
  }
  
  if (roleError) {
    return (
      <div className="p-6 bg-destructive/10 border border-destructive rounded-lg text-center">
        <h2 className="text-xl font-semibold mb-2">Error Loading Role</h2>
        <p className="text-muted-foreground mb-4">{(roleError as Error).message}</p>
        <Button onClick={() => navigate('/roles')}>Back to Roles</Button>
      </div>
    )
  }
  
  if (!role) {
    return null
  }
  
  return (
    <div>
      <div className="flex items-center gap-4 mb-8">
        <Button variant="outline" size="icon" onClick={() => navigate('/roles')}>
          <ArrowLeft className="h-4 w-4" />
        </Button>
        <div>
          <h1 className="text-3xl font-bold">{role.name}</h1>
          <p className="text-muted-foreground mt-1">{role.description}</p>
        </div>
      </div>
      
      <div className="grid md:grid-cols-3 gap-8">
        <div className="md:col-span-2">
          <div className="border rounded-lg p-6 bg-card mb-8">
            <div className="flex justify-between items-center mb-6">
              <h2 className="text-xl font-semibold">Role Details</h2>
              <div className="flex gap-2">
                {!isEditing ? (
                  <Button onClick={() => setIsEditing(true)}>Edit Role</Button>
                ) : (
                  <Button variant="outline" onClick={() => {
                    setIsEditing(false)
                    setFormData(role)
                  }}>
                    Cancel
                  </Button>
                )}
                {!role.is_default && (
                  <Button variant="destructive" onClick={handleDelete}>
                    <Trash2 className="h-4 w-4 mr-2" /> Delete
                  </Button>
                )}
              </div>
            </div>
            
            {isEditing ? (
              <form onSubmit={handleSubmit}>
                <div className="space-y-4">
                  <div>
                    <label className="block text-sm font-medium mb-1">Name</label>
                    <input
                      type="text"
                      name="name"
                      value={formData.name || ''}
                      onChange={handleInputChange}
                      className="w-full p-2 border rounded-md bg-background"
                      required
                    />
                  </div>
                  
                  <div>
                    <label className="block text-sm font-medium mb-1">Description</label>
                    <input
                      type="text"
                      name="description"
                      value={formData.description || ''}
                      onChange={handleInputChange}
                      className="w-full p-2 border rounded-md bg-background"
                      required
                    />
                  </div>
                  
                  <div>
                    <label className="block text-sm font-medium mb-1">Instructions</label>
                    <textarea
                      name="instructions"
                      value={formData.instructions || ''}
                      onChange={handleInputChange}
                      className="w-full p-2 border rounded-md bg-background min-h-[100px]"
                      required
                    />
                  </div>
                  
                  <div>
                    <label className="block text-sm font-medium mb-1">System Prompt</label>
                    <textarea
                      name="system_prompt"
                      value={formData.system_prompt || ''}
                      onChange={handleInputChange}
                      className="w-full p-2 border rounded-md bg-background min-h-[100px]"
                      required
                    />
                  </div>
                  
                  <div>
                    <label className="block text-sm font-medium mb-1">Tone</label>
                    <select
                      name="tone"
                      value={formData.tone || ''}
                      onChange={handleInputChange}
                      className="w-full p-2 border rounded-md bg-background"
                      required
                    >
                      <option value="strategic">Strategic</option>
                      <option value="analytical">Analytical</option>
                      <option value="creative">Creative</option>
                      <option value="supportive">Supportive</option>
                      <option value="methodical">Methodical</option>
                      <option value="persuasive">Persuasive</option>
                      <option value="consultative">Consultative</option>
                    </select>
                  </div>
                  
                  <div className="pt-4">
                    <Button type="submit" disabled={updateMutation.isPending}>
                      {updateMutation.isPending ? (
                        <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                      ) : (
                        <Save className="h-4 w-4 mr-2" />
                      )}
                      Save Changes
                    </Button>
                  </div>
                </div>
              </form>
            ) : (
              <div className="space-y-6">
                <div>
                  <h3 className="text-sm font-medium text-muted-foreground mb-1">ID</h3>
                  <p>{role.id}</p>
                </div>
                
                <div>
                  <h3 className="text-sm font-medium text-muted-foreground mb-1">Domains</h3>
                  <div className="flex flex-wrap gap-2">
                    {role.domains.map((domain: string) => (
                      <span
                        key={domain}
                        className="px-2 py-1 bg-primary/10 text-primary text-xs rounded-full"
                      >
                        {domain}
                      </span>
                    ))}
                  </div>
                </div>
                
                <div>
                  <h3 className="text-sm font-medium text-muted-foreground mb-1">Tone</h3>
                  <span className="px-2 py-1 bg-secondary text-secondary-foreground text-xs rounded-full">
                    {role.tone}
                  </span>
                </div>
                
                <div>
                  <h3 className="text-sm font-medium text-muted-foreground mb-1">Instructions</h3>
                  <p className="whitespace-pre-wrap">{role.instructions}</p>
                </div>
                
                <div>
                  <h3 className="text-sm font-medium text-muted-foreground mb-1">System Prompt</h3>
                  <p className="whitespace-pre-wrap">{role.system_prompt}</p>
                </div>
                
                {role.is_default && (
                  <div className="bg-primary/5 p-4 rounded-md">
                    <p className="text-sm">
                      This is a default role and cannot be deleted. You can still edit its properties.
                    </p>
                  </div>
                )}
              </div>
            )}
          </div>
        </div>
        
        <div>
          <div className="border rounded-lg p-6 bg-card mb-6">
            <div className="flex justify-between items-center mb-6">
              <h2 className="text-xl font-semibold">Memories</h2>
              <div className="flex gap-2">
                <Button
                  variant="outline"
                  size="sm"
                  onClick={handleClearMemories}
                  disabled={!memories || memories.length === 0}
                >
                  Clear All
                </Button>
              </div>
            </div>
            
            {memoriesLoading ? (
              <div className="flex justify-center items-center h-32">
                <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
              </div>
            ) : memories && memories.length > 0 ? (
              <div className="space-y-4">
                {memories.map((memory) => (
                  <motion.div
                    key={memory.id}
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="p-4 border rounded-md bg-background"
                  >
                    <div className="flex justify-between items-start mb-2">
                      <span className="px-2 py-1 bg-primary/10 text-primary text-xs rounded-full">
                        {memory.type}
                      </span>
                      <span className="text-xs text-muted-foreground">
                        {formatDate(new Date(memory.created_at))}
                      </span>
                    </div>
                    <p className="text-sm">{memory.content}</p>
                    <div className="mt-2 text-xs text-muted-foreground">
                      Expires: {formatDate(new Date(memory.expires_at))}
                    </div>
                  </motion.div>
                ))}
              </div>
            ) : (
              <div className="text-center p-6 bg-muted/30 rounded-md">
                <p className="text-muted-foreground">
                  No memories stored for this role yet.
                </p>
              </div>
            )}
          </div>
          
          <div className="border rounded-lg p-6 bg-card">
            <div className="flex justify-between items-center mb-6">
              <h2 className="text-xl font-semibold">Web Research</h2>
              <Button
                variant="outline"
                size="sm"
                onClick={() => setShowBrowser(!showBrowser)}
              >
                <Globe className="h-4 w-4 mr-2" />
                {showBrowser ? 'Hide Browser' : 'Show Browser'}
              </Button>
            </div>
            
            {showBrowser && (
              <motion.div
                initial={{ opacity: 0, height: 0 }}
                animate={{ opacity: 1, height: 'auto' }}
                exit={{ opacity: 0, height: 0 }}
                transition={{ duration: 0.3 }}
              >
                <BrowserPanel roleId={roleId!} onClose={() => setShowBrowser(false)} />
              </motion.div>
            )}
            
            <div className="text-sm text-muted-foreground">
              <p>Use the web browser to research information that can help this AI advisor provide better responses.</p>
              <p className="mt-2">You can also use special commands in your queries:</p>
              <ul className="list-disc pl-5 mt-2">
                <li><code>[SEARCH_WEB:query]</code> - Search the web for information</li>
                <li><code>[BROWSE_URL:https://example.com]</code> - Browse a specific URL</li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
