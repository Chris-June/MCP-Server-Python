import { useState, useEffect } from 'react'
import { useToast } from '@/components/ui/use-toast'
import { Button } from '@/components/ui/button'
import { Card } from '@/components/ui/card'
import { Input } from './ui/input'
import { Globe, Search, RefreshCw, X, Camera } from 'lucide-react'

interface BrowserPanelProps {
  roleId: string
  onClose?: () => void
}

interface BrowserSession {
  session_id: string
  current_url?: string
  title?: string
}

export function BrowserPanel({ roleId, onClose }: BrowserPanelProps) {
  const { toast } = useToast()
  const [session, setSession] = useState<BrowserSession | null>(null)
  const [url, setUrl] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [screenshot, setScreenshot] = useState<string | null>(null)
  
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
  
  // Clean up session on unmount
  useEffect(() => {
    return () => {
      if (session) {
        fetch(`/api/v1/browser/sessions/${session.session_id}`, {
          method: 'DELETE',
        }).catch(console.error)
      }
    }
  }, [session])
  
  return (
    <Card className="p-4 border rounded-lg overflow-hidden">
      <div className="flex justify-between items-center mb-4">
        <h3 className="text-lg font-semibold flex items-center gap-2">
          <Globe className="h-5 w-5" />
          Web Browser
        </h3>
        {onClose && (
          <Button variant="ghost" size="icon" onClick={onClose}>
            <X className="h-4 w-4" />
          </Button>
        )}
      </div>
      
      {!session ? (
        <div className="flex flex-col items-center justify-center p-6 bg-muted/30 rounded-lg">
          <Globe className="h-12 w-12 text-muted-foreground mb-4" />
          <h2 className="text-lg font-semibold mb-2">Start Web Browsing</h2>
          <p className="text-muted-foreground mb-6 text-center max-w-md">
            Create a browser session to research information for this role.
          </p>
          
          <Button 
            onClick={createSession} 
            disabled={isLoading}
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
        <div className="flex flex-col">
          {/* Browser toolbar */}
          <div className="p-2 border rounded-md bg-muted/20 flex items-center gap-2 mb-4">
            <form onSubmit={handleSubmit} className="flex-1 flex gap-2">
              <div className="relative flex-1">
                <Search className="absolute left-2 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground" />
                <Input
                  type="text"
                  value={url}
                  onChange={(e: React.ChangeEvent<HTMLInputElement>) => setUrl(e.target.value)}
                  placeholder="Enter URL"
                  className="w-full pl-8"
                  disabled={isLoading}
                />
              </div>
              <Button type="submit" disabled={!url.trim() || isLoading} size="sm">
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
          <div className="bg-white overflow-hidden rounded-md border">
            {screenshot ? (
              <div className="overflow-auto p-4">
                <h3 className="text-sm font-semibold mb-2">{session.title || 'Screenshot'}</h3>
                <p className="text-xs text-muted-foreground mb-4">{session.current_url}</p>
                <img 
                  src={screenshot} 
                  alt="Page Screenshot" 
                  className="w-full border rounded-lg shadow-sm"
                />
              </div>
            ) : (
              <div className="flex items-center justify-center p-8">
                <div className="text-center">
                  <Globe className="h-8 w-8 text-muted-foreground mx-auto mb-4" />
                  <h3 className="text-sm font-semibold mb-2">Enter a URL to start browsing</h3>
                  <p className="text-xs text-muted-foreground max-w-md">
                    Type a URL in the address bar above and press Go to navigate to a website.
                  </p>
                </div>
              </div>
            )}
          </div>
        </div>
      )}
    </Card>
  )
}
