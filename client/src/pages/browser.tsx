import { useState, useEffect, useRef } from 'react'
import { useSearchParams } from 'react-router-dom'
import { useQuery, useMutation } from '@tanstack/react-query'
import { motion } from 'framer-motion'
import { Globe, Search, RefreshCw, ArrowLeft, ArrowRight, X, Camera, Code } from 'lucide-react'

import { Button } from '@/components/ui/button'
import { useToast } from '@/components/ui/use-toast'
import { Card } from '@/components/ui/card'

interface BrowserSession {
  session_id: string
  current_url?: string
  title?: string
}

interface BrowserHistory {
  url: string
  title: string
}

export default function BrowserPage() {
  const { toast } = useToast()
  const [searchParams, setSearchParams] = useSearchParams()
  const [session, setSession] = useState<BrowserSession | null>(null)
  const [url, setUrl] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [screenshot, setScreenshot] = useState<string | null>(null)
  const [history, setHistory] = useState<BrowserHistory[]>([])
  
  const iframeRef = useRef<HTMLIFrameElement>(null)
  
  // Create a new browser session
  const createSession = async () => {
    try {
      setIsLoading(true)
      const response = await fetch('/api/v1/browser/sessions', {
        method: 'POST',
      })
      
      if (!response.ok) {
        throw new Error('Failed to create browser session')
      }
      
      const data = await response.json()
      setSession({
        session_id: data.session_id
      })
      
      // Update URL params
      setSearchParams({ session: data.session_id })
      
      toast({
        title: 'Session Created',
        description: 'Browser session has been created successfully',
      })
    } catch (error) {
      toast({
        title: 'Error',
        description: `Failed to create session: ${error instanceof Error ? error.message : 'Unknown error'}`,
        variant: 'destructive',
      })
    } finally {
      setIsLoading(false)
    }
  }
  
  // Close the browser session
  const closeSession = async () => {
    if (!session) return
    
    try {
      setIsLoading(true)
      const response = await fetch(`/api/v1/browser/sessions/${session.session_id}`, {
        method: 'DELETE',
      })
      
      if (!response.ok) {
        throw new Error('Failed to close browser session')
      }
      
      setSession(null)
      setUrl('')
      setScreenshot(null)
      setHistory([])
      
      // Clear URL params
      setSearchParams({})
      
      toast({
        title: 'Session Closed',
        description: 'Browser session has been closed successfully',
      })
    } catch (error) {
      toast({
        title: 'Error',
        description: `Failed to close session: ${error instanceof Error ? error.message : 'Unknown error'}`,
        variant: 'destructive',
      })
    } finally {
      setIsLoading(false)
    }
  }
  
  // Navigate to a URL
  const navigate = async (targetUrl: string) => {
    if (!session) return
    
    try {
      setIsLoading(true)
      const response = await fetch(`/api/v1/browser/sessions/${session.session_id}/navigate`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ url: targetUrl }),
      })
      
      if (!response.ok) {
        throw new Error('Failed to navigate')
      }
      
      const data = await response.json()
      
      setSession({
        ...session,
        current_url: data.url,
        title: data.title
      })
      
      // Take a screenshot after navigation
      await takeScreenshot()
      
      // Update history
      await fetchHistory()
      
      toast({
        title: 'Navigation Successful',
        description: `Navigated to ${data.title}`,
      })
    } catch (error) {
      toast({
        title: 'Navigation Error',
        description: `Failed to navigate: ${error instanceof Error ? error.message : 'Unknown error'}`,
        variant: 'destructive',
      })
    } finally {
      setIsLoading(false)
    }
  }
  
  // Take a screenshot
  const takeScreenshot = async () => {
    if (!session) return
    
    try {
      const response = await fetch(`/api/v1/browser/sessions/${session.session_id}/screenshot`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({}),
      })
      
      if (!response.ok) {
        throw new Error('Failed to take screenshot')
      }
      
      const data = await response.json()
      setScreenshot(`data:image/png;base64,${data.data}`)
    } catch (error) {
      toast({
        title: 'Screenshot Error',
        description: `Failed to take screenshot: ${error instanceof Error ? error.message : 'Unknown error'}`,
        variant: 'destructive',
      })
    }
  }
  
  // Fetch browsing history
  const fetchHistory = async () => {
    if (!session) return
    
    try {
      const response = await fetch(`/api/v1/browser/sessions/${session.session_id}/history`)
      
      if (!response.ok) {
        throw new Error('Failed to fetch history')
      }
      
      const data = await response.json()
      setHistory(data.history)
    } catch (error) {
      console.error('Failed to fetch history:', error instanceof Error ? error.message : 'Unknown error')
    }
  }
  
  // Handle form submission
  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (!url.trim()) return
    
    // Add http:// if not present
    let targetUrl = url
    if (!targetUrl.startsWith('http://') && !targetUrl.startsWith('https://')) {
      targetUrl = `https://${targetUrl}`
    }
    
    navigate(targetUrl)
  }
  
  // Initialize session from URL params if available
  useEffect(() => {
    const sessionId = searchParams.get('session')
    if (sessionId) {
      setSession({
        session_id: sessionId
      })
      
      // Fetch current state
      fetchHistory()
    }
  }, [])
  
  return (
    <div className="flex flex-col h-[calc(100vh-13rem)]">
      <h1 className="text-2xl font-bold mb-4 flex items-center gap-2">
        <Globe className="h-6 w-6" />
        Web Browser
      </h1>
      
      {!session ? (
        <div className="flex-1 flex flex-col items-center justify-center p-6 bg-muted/30 rounded-lg">
          <Globe className="h-16 w-16 text-muted-foreground mb-4" />
          <h2 className="text-xl font-semibold mb-2">Start Web Browsing</h2>
          <p className="text-muted-foreground mb-6 text-center max-w-md">
            Create a new browser session to start browsing the web. This will allow you to navigate websites and interact with web content.
          </p>
          
          <Button 
            onClick={createSession} 
            disabled={isLoading}
            size="lg"
          >
            {isLoading ? (
              <>
                <RefreshCw className="h-4 w-4 mr-2 animate-spin" />
                Creating Session...
              </>
            ) : (
              <>Create Browser Session</>
            )}
          </Button>
        </div>
      ) : (
        <div className="flex-1 flex flex-col border rounded-lg overflow-hidden">
          {/* Browser toolbar */}
          <div className="p-2 border-b bg-muted/20 flex items-center gap-2">
            <Button 
              variant="outline" 
              size="icon" 
              onClick={() => history.length > 1 && navigate(history[history.length - 2].url)}
              disabled={history.length <= 1 || isLoading}
            >
              <ArrowLeft className="h-4 w-4" />
            </Button>
            
            <Button 
              variant="outline" 
              size="icon" 
              onClick={() => session.current_url && navigate(session.current_url)}
              disabled={!session.current_url || isLoading}
            >
              <RefreshCw className="h-4 w-4" />
            </Button>
            
            <form onSubmit={handleSubmit} className="flex-1 flex gap-2">
              <div className="relative flex-1">
                <Search className="absolute left-2 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground" />
                <input
                  type="text"
                  value={url}
                  onChange={(e) => setUrl(e.target.value)}
                  placeholder="Enter URL"
                  className="w-full pl-8 pr-4 py-2 rounded-md border bg-background"
                  disabled={isLoading}
                />
              </div>
              <Button type="submit" disabled={!url.trim() || isLoading}>
                {isLoading ? (
                  <RefreshCw className="h-4 w-4 animate-spin" />
                ) : (
                  <Search className="h-4 w-4" />
                )}
                <span className="ml-2 sr-only md:not-sr-only">Go</span>
              </Button>
            </form>
            
            <Button 
              variant="outline" 
              size="icon" 
              onClick={takeScreenshot}
              disabled={!session.current_url || isLoading}
            >
              <Camera className="h-4 w-4" />
            </Button>
            
            <Button 
              variant="outline" 
              size="icon" 
              onClick={closeSession}
              disabled={isLoading}
            >
              <X className="h-4 w-4" />
            </Button>
          </div>
          
          {/* Browser content */}
          <div className="flex-1 bg-white overflow-hidden">
            {screenshot ? (
              <div className="h-full overflow-auto p-4">
                <h3 className="text-lg font-semibold mb-2">{session.title || 'Screenshot'}</h3>
                <p className="text-sm text-muted-foreground mb-4">{session.current_url}</p>
                <img 
                  src={screenshot} 
                  alt="Page Screenshot" 
                  className="w-full border rounded-lg shadow-sm"
                />
              </div>
            ) : (
              <div className="h-full flex items-center justify-center">
                <div className="text-center p-6">
                  <Globe className="h-12 w-12 text-muted-foreground mx-auto mb-4" />
                  <h3 className="text-lg font-semibold mb-2">Enter a URL to start browsing</h3>
                  <p className="text-muted-foreground max-w-md">
                    Type a URL in the address bar above and press Go to navigate to a website.
                  </p>
                </div>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  )
}
