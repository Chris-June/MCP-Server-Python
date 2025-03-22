import { useState, useEffect, useRef } from 'react'
import { useSearchParams } from 'react-router-dom'
import { useQuery, useMutation } from '@tanstack/react-query'
import { motion, AnimatePresence } from 'framer-motion'
import { Send, User, Bot, Loader2, Zap } from 'lucide-react'
import ReactMarkdown from 'react-markdown'

import { fetchRoles, processQuery, processQueryStream } from '@/lib/api'
import type { Role } from '@/types'
import { Button } from '@/components/ui/button'
import { useToast } from '@/components/ui/use-toast'

interface Message {
  id: string
  role: 'user' | 'assistant'
  content: string
  timestamp: Date
}

export default function ChatPage() {
  const [searchParams] = useSearchParams()
  const initialRoleId = searchParams.get('role')
  const { toast } = useToast()
  
  const [selectedRoleId, setSelectedRoleId] = useState<string | null>(initialRoleId)
  const [messages, setMessages] = useState<Message[]>([])
  const [input, setInput] = useState('')
  const [isStreaming, setIsStreaming] = useState(true)
  const [streamedResponse, setStreamedResponse] = useState('')
  const messagesEndRef = useRef<HTMLDivElement>(null)
  
  const { data: roles, isLoading: rolesLoading } = useQuery({
    queryKey: ['roles'],
    queryFn: fetchRoles
  })
  
  const queryMutation = useMutation({
    mutationFn: processQuery,
    onSuccess: (data) => {
      const newMessage: Message = {
        id: Date.now().toString(),
        role: 'assistant',
        content: data.response,
        timestamp: new Date(),
      }
      setMessages((prev) => [...prev, newMessage])
    },
    onError: (error) => {
      toast({
        title: 'Error',
        description: `Failed to process query: ${error.message}`,
        variant: 'destructive',
      })
    },
  })
  
  useEffect(() => {
    scrollToBottom()
  }, [messages])
  
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }
  
  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (!input.trim() || !selectedRoleId) return
    
    const newMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: input,
      timestamp: new Date(),
    }
    
    setMessages((prev) => [...prev, newMessage])
    setInput('')
    
    if (isStreaming) {
      // Create a placeholder message for the streaming response
      const placeholderId = Date.now().toString() + '-streaming'
      const placeholderMessage: Message = {
        id: placeholderId,
        role: 'assistant',
        content: '',
        timestamp: new Date(),
      }
      
      setMessages(prev => [...prev, placeholderMessage])
      setStreamedResponse('')
      
      // Use streaming API
      processQueryStream(
        { role_id: selectedRoleId, query: input },
        (chunk) => {
          setStreamedResponse(prev => prev + chunk)
          // Update the placeholder message with the streamed content
          setMessages(prev => 
            prev.map(msg => 
              msg.id === placeholderId 
                ? { ...msg, content: msg.content + chunk } 
                : msg
            )
          )
        }
      ).then(() => {
        // Reset the streamedResponse state when streaming is complete
        setStreamedResponse('')
      }).catch(error => {
        toast({
          title: 'Error',
          description: `Failed to process streaming query: ${error.message}`,
          variant: 'destructive',
        })
        // Also reset on error
        setStreamedResponse('')
      })
    } else {
      // Use regular API
      queryMutation.mutate({
        role_id: selectedRoleId,
        query: input,
      })
    }
  }
  
  const selectedRole = roles?.find(role => role.id === selectedRoleId)
  
  return (
    <div className="flex flex-col h-[calc(100vh-13rem)]">
      {!selectedRoleId ? (
        <div className="flex-1 flex flex-col items-center justify-center p-6 bg-muted/30 rounded-lg">
          <h2 className="text-2xl font-bold mb-4">Select a Role to Chat With</h2>
          <p className="text-muted-foreground mb-6 text-center max-w-md">
            Choose an AI role to start a conversation. Each role has different expertise and personality.
          </p>
          
          {rolesLoading ? (
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 w-full max-w-3xl">
              {roles?.map((role) => (
                <motion.button
                  key={role.id}
                  whileHover={{ scale: 1.02 }}
                  whileTap={{ scale: 0.98 }}
                  className="p-4 border rounded-lg bg-card text-left hover:border-primary transition-colors"
                  onClick={() => setSelectedRoleId(role.id)}
                >
                  <h3 className="font-semibold">{role.name}</h3>
                  <p className="text-sm text-muted-foreground mt-1">{role.description}</p>
                </motion.button>
              ))}
            </div>
          )}
        </div>
      ) : (
        <>
          <div className="flex items-center justify-between mb-4 p-4 border rounded-lg bg-card">
            <div>
              <h2 className="font-semibold">{selectedRole?.name}</h2>
              <p className="text-sm text-muted-foreground">{selectedRole?.description}</p>
            </div>
            <Button variant="outline" onClick={() => setSelectedRoleId(null)}>
              Change Role
            </Button>
          </div>
          
          <div className="flex-1 overflow-y-auto border rounded-lg mb-4 p-4 bg-muted/10">
            {messages.length === 0 ? (
              <div className="h-full flex flex-col items-center justify-center text-center p-6">
                <Bot className="h-12 w-12 text-muted-foreground mb-4" />
                <h3 className="text-lg font-semibold mb-2">Start a conversation</h3>
                <p className="text-muted-foreground max-w-md">
                  Send a message to start chatting with {selectedRole?.name}.
                  <span className="block mt-2 text-xs italic">
                    <span className="font-medium">Pro tip:</span> Use browser commands in your queries:
                    <code className="mx-1">[BROWSE_URL:https://example.com]</code>
                    <code className="mx-1">[SEARCH_WEB:query]</code>
                    <code className="mx-1">[CLICK_ELEMENT:#button]</code>
                  </span>
                </p>
              </div>
            ) : (
              <div className="space-y-4">
                <AnimatePresence>
                  {messages.map((message) => (
                    <motion.div
                      key={message.id}
                      initial={{ opacity: 0, y: 10 }}
                      animate={{ opacity: 1, y: 0 }}
                      exit={{ opacity: 0 }}
                      className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
                    >
                      <div
                        className={`max-w-[80%] p-4 rounded-lg ${message.role === 'user' ? 'bg-primary text-primary-foreground' : 'bg-card border'}`}
                      >
                        <div className="flex items-center gap-2 mb-2">
                          {message.role === 'user' ? (
                            <>
                              <span className="font-medium">You</span>
                              <User className="h-4 w-4" />
                            </>
                          ) : (
                            <>
                              <Bot className="h-4 w-4" />
                              <span className="font-medium">{selectedRole?.name}</span>
                            </>
                          )}
                        </div>
                        
                        {message.role === 'assistant' ? (
                          <div className="prose prose-sm dark:prose-invert max-w-none">
                            <ReactMarkdown>{message.content}</ReactMarkdown>
                          </div>
                        ) : (
                          <p>{message.content}</p>
                        )}
                        
                        <div className="mt-2 text-xs opacity-70 text-right">
                          {message.timestamp.toLocaleTimeString()}
                        </div>
                      </div>
                    </motion.div>
                  ))}
                </AnimatePresence>
                <div ref={messagesEndRef} />
              </div>
            )}
          </div>
          
          <div className="flex items-center justify-end mb-2">
            <div className="flex items-center gap-2">
              <Zap className={`h-4 w-4 ${isStreaming ? 'text-primary' : 'text-muted-foreground'}`} />
              <span className="text-sm">Streaming</span>
              <button
                type="button"
                onClick={() => setIsStreaming(!isStreaming)}
                className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 focus-visible:ring-offset-background ${
                  isStreaming ? 'bg-primary' : 'bg-input'
                }`}
              >
                <span
                  className={`pointer-events-none inline-block h-4 w-4 transform rounded-full bg-background shadow-lg ring-0 transition-transform ${
                    isStreaming ? 'translate-x-6' : 'translate-x-1'
                  }`}
                />
              </button>
            </div>
          </div>
          
          <form onSubmit={handleSubmit} className="flex gap-2">
            <div className="relative flex-1">
              <input
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                placeholder={`Message ${selectedRole?.name}...`}
                className="flex-1 p-3 rounded-lg border bg-background w-full"
                disabled={queryMutation.isPending || (isStreaming && streamedResponse !== '')}
              />
              <div className="absolute right-2 top-1/2 transform -translate-y-1/2">
                <span 
                  className="text-xs text-muted-foreground cursor-help"
                  title="Use browser commands: [BROWSE_URL:url], [SEARCH_WEB:query], [CLICK_ELEMENT:selector], [FILL_FORM:selector=value]"
                >
                  ℹ️ Browser commands
                </span>
              </div>
            </div>
            <Button 
              type="submit" 
              disabled={!input.trim() || queryMutation.isPending || (isStreaming && streamedResponse !== '')}
            >
              {queryMutation.isPending || (isStreaming && streamedResponse !== '') ? (
                <Loader2 className="h-4 w-4 animate-spin" />
              ) : (
                <Send className="h-4 w-4" />
              )}
              <span className="ml-2 sr-only md:not-sr-only">Send</span>
            </Button>
          </form>
        </>
      )}
    </div>
  )
}
