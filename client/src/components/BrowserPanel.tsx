import { useState, useEffect } from 'react'
import { useToast } from '@/components/ui/use-toast'
import { Button } from '@/components/ui/button'
import { Card } from '@/components/ui/card'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { Input } from '@/components/ui/input'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { Textarea } from '@/components/ui/textarea'
import { Label } from '@/components/ui/label'
import { Globe, Search, RefreshCw, X, Camera, History, FileText, MousePointer, Code, Database, FormInput } from 'lucide-react'

interface BrowserPanelProps {
  roleId: string
  onClose?: () => void
}

interface BrowserSession {
  session_id: string
  current_url?: string
  title?: string
  is_mock?: boolean
}

export function BrowserPanel({ roleId, onClose }: BrowserPanelProps) {
  const { toast } = useToast()
  const [session, setSession] = useState<BrowserSession | null>(null)
  const [url, setUrl] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [screenshot, setScreenshot] = useState<string | null>(null)
  const [pageContent, setPageContent] = useState<string>('')
  const [extractMode, setExtractMode] = useState('auto')
  const [structuredData, setStructuredData] = useState<any>(null)
  const [formData, setFormData] = useState('')
  const [history, setHistory] = useState<{url: string, title: string}[]>([])
  const [activeTab, setActiveTab] = useState('screenshot')
  const [selector, setSelector] = useState('')
  const [jsCode, setJsCode] = useState('')
  const [isMockSession, setIsMockSession] = useState(false)
  
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
      
      // Check if this is a mock session
      const isMock = data.is_mock || false
      setIsMockSession(isMock)
      
      setSession({
        session_id: data.session_id,
        is_mock: isMock
      })
      
      toast({
        title: 'Session Created',
        description: isMock 
          ? 'Created mock browser session (limited functionality)' 
          : 'Browser session has been created successfully',
        variant: isMock ? 'default' : 'default'
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
      
      // Take a screenshot and get content after navigation
      await takeScreenshot()
      await getPageContent()
      await getBrowsingHistory()
      
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
  
  // Get page content with extraction mode
  const getPageContent = async () => {
    if (!session) return
    
    try {
      setIsLoading(true)
      
      // For structured data, use a different approach
      if (extractMode === 'structured') {
        await getStructuredData()
        return
      }
      
      // Regular content extraction with mode
      const response = await fetch(`/api/v1/browser/sessions/${session.session_id}/browse`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 
          url: session.current_url,
          extract_mode: extractMode 
        }),
      })
      
      if (!response.ok) {
        throw new Error('Failed to get page content')
      }
      
      const data = await response.json()
      setPageContent(data.content || 'No content available')
      setActiveTab('content')
    } catch (error) {
      toast({
        title: 'Content Error',
        description: `Failed to get page content: ${error instanceof Error ? error.message : 'Unknown error'}`,
        variant: 'destructive',
      })
    } finally {
      setIsLoading(false)
    }
  }
  
  // Get structured data from the page
  const getStructuredData = async () => {
    if (!session) return
    
    try {
      setIsLoading(true)
      
      // Execute JavaScript to extract structured data
      const structuredScript = `
        function extractStructuredData() {
          const result = {
            headings: [],
            links: [],
            images: [],
            lists: [],
            tables: [],
            forms: []
          };
          
          // Extract headings
          const headings = document.querySelectorAll('h1, h2, h3, h4, h5, h6');
          headings.forEach(h => {
            result.headings.push({
              level: parseInt(h.tagName.substring(1)),
              text: h.textContent.trim()
            });
          });
          
          // Extract links (limit to 20)
          const links = document.querySelectorAll('a[href]');
          let linkCount = 0;
          links.forEach(link => {
            if (linkCount < 20) {
              const href = link.getAttribute('href');
              if (href && !href.startsWith('#') && !href.startsWith('javascript:')) {
                result.links.push({
                  text: link.textContent.trim(),
                  url: href
                });
                linkCount++;
              }
            }
          });
          
          // Extract images (limit to 10)
          const images = document.querySelectorAll('img[src]');
          let imageCount = 0;
          images.forEach(img => {
            if (imageCount < 10) {
              result.images.push({
                alt: img.getAttribute('alt') || '',
                src: img.getAttribute('src')
              });
              imageCount++;
            }
          });
          
          // Extract lists (limit to 5)
          const lists = document.querySelectorAll('ul, ol');
          let listCount = 0;
          lists.forEach(list => {
            if (listCount < 5) {
              const items = Array.from(list.querySelectorAll('li')).map(li => li.textContent.trim());
              result.lists.push({
                type: list.tagName.toLowerCase(),
                items: items
              });
              listCount++;
            }
          });
          
          // Extract forms (limit to 3)
          const forms = document.querySelectorAll('form');
          let formCount = 0;
          forms.forEach(form => {
            if (formCount < 3) {
              const formInputs = [];
              form.querySelectorAll('input, select, textarea').forEach(input => {
                formInputs.push({
                  type: input.tagName.toLowerCase(),
                  name: input.getAttribute('name') || '',
                  id: input.getAttribute('id') || '',
                  placeholder: input.getAttribute('placeholder') || ''
                });
              });
              
              result.forms.push({
                id: form.getAttribute('id') || '',
                action: form.getAttribute('action') || '',
                method: form.getAttribute('method') || 'get',
                inputs: formInputs
              });
              formCount++;
            }
          });
          
          return result;
        }
        
        return extractStructuredData();
      `;
      
      const response = await fetch(`/api/v1/browser/sessions/${session.session_id}/evaluate`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ script: structuredScript }),
      });
      
      if (!response.ok) {
        throw new Error('Failed to extract structured data')
      }
      
      const data = await response.json();
      if (data.success && data.result) {
        setStructuredData(data.result);
        setPageContent(JSON.stringify(data.result, null, 2));
      } else {
        setPageContent('Failed to extract structured data');
        setStructuredData(null);
      }
      
      setActiveTab('content');
    } catch (error) {
      toast({
        title: 'Structured Data Error',
        description: `Failed to extract structured data: ${error instanceof Error ? error.message : 'Unknown error'}`,
        variant: 'destructive',
      });
    } finally {
      setIsLoading(false);
    }
  }
  
  // Get browsing history
  const getBrowsingHistory = async () => {
    if (!session) return
    
    try {
      setIsLoading(true)
      const response = await fetch(`/api/v1/browser/sessions/${session.session_id}/history`, {
        method: 'GET',
      })
      
      if (!response.ok) {
        throw new Error('Failed to get browsing history')
      }
      
      const data = await response.json()
      setHistory(data.history || [])
      setActiveTab('history')
    } catch (error) {
      toast({
        title: 'History Error',
        description: `Failed to get browsing history: ${error instanceof Error ? error.message : 'Unknown error'}`,
        variant: 'destructive',
      })
    } finally {
      setIsLoading(false)
    }
  }
  
  // Click an element
  const clickElement = async (selector: string) => {
    if (!session || !selector.trim()) return
    
    try {
      setIsLoading(true)
      const response = await fetch(`/api/v1/browser/sessions/${session.session_id}/click`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ selector }),
      })
      
      if (!response.ok) {
        throw new Error('Failed to click element')
      }
      
      toast({
        title: 'Element Clicked',
        description: `Successfully clicked element: ${selector}`,
      })
      
      // Refresh screenshot and content after interaction
      await takeScreenshot()
      await getPageContent()
    } catch (error) {
      toast({
        title: 'Click Error',
        description: `Failed to click element: ${error instanceof Error ? error.message : 'Unknown error'}`,
        variant: 'destructive',
      })
    } finally {
      setIsLoading(false)
    }
  }
  
  // Fill a form on the page
  const fillForm = async () => {
    if (!session || !formData.trim()) return
    
    try {
      setIsLoading(true)
      
      // Parse form data in format: selector1=value1,selector2=value2
      const formFields: Record<string, string> = {}
      formData.split(',').forEach(item => {
        if (item.includes('=')) {
          const [selector, value] = item.split('=', 2)
          formFields[selector.trim()] = value.trim()
        }
      })
      
      if (Object.keys(formFields).length === 0) {
        throw new Error('Invalid form data format. Use: selector1=value1,selector2=value2')
      }
      
      // Fill each field one by one
      for (const [selector, value] of Object.entries(formFields)) {
        const response = await fetch(`/api/v1/browser/sessions/${session.session_id}/fill`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ selector, value }),
        })
        
        if (!response.ok) {
          throw new Error(`Failed to fill field ${selector}`)
        }
        
        const data = await response.json()
        if (!data.success) {
          throw new Error(`Failed to fill field ${selector}: ${data.error || 'Unknown error'}`)
        }
      }
      
      toast({
        title: 'Success',
        description: `Successfully filled ${Object.keys(formFields).length} form fields`,
      })
      
      // Take a screenshot after filling to show the result
      await takeScreenshot()
    } catch (error) {
      toast({
        title: 'Form Fill Error',
        description: `${error instanceof Error ? error.message : 'Unknown error'}`,
        variant: 'destructive',
      })
    } finally {
      setIsLoading(false)
    }
  }
  
  // Execute JavaScript
  const executeJavaScript = async (code: string) => {
    if (!session || !code.trim()) return
    
    try {
      setIsLoading(true)
      const response = await fetch(`/api/v1/browser/sessions/${session.session_id}/evaluate`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ script: code }),
      })
      
      if (!response.ok) {
        throw new Error('Failed to execute JavaScript')
      }
      
      const data = await response.json()
      toast({
        title: 'JavaScript Executed',
        description: 'Script executed successfully',
      })
      
      // Refresh screenshot and content after interaction
      await takeScreenshot()
      await getPageContent()
    } catch (error) {
      toast({
        title: 'JavaScript Error',
        description: `Failed to execute script: ${error instanceof Error ? error.message : 'Unknown error'}`,
        variant: 'destructive',
      })
    } finally {
      setIsLoading(false)
    }
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
          <span className="text-xs text-muted-foreground ml-2 cursor-help" title="Use these commands in your queries to enable web browsing: [BROWSE_URL:url], [SEARCH_WEB:query], [CLICK_ELEMENT:selector], [FILL_FORM:selector=value]">ℹ️ Commands</span>
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
            <span className="block mt-2 text-xs italic">Tip: Use commands like <code>[BROWSE_URL:https://example.com]</code> or <code>[SEARCH_WEB:your query]</code> in your messages to the agent.</span>
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
            {session.current_url ? (
              <div className="overflow-auto">
                <div className="p-2 bg-muted/10 border-b">
                  <h3 className="text-sm font-semibold truncate">{session.title || 'Browser'}</h3>
                  <p className="text-xs text-muted-foreground truncate">{session.current_url}</p>
                </div>
                
                {isMockSession && (
                  <div className="bg-yellow-50 border-yellow-200 border p-2 text-xs text-yellow-700">
                    This is a mock browser session with limited functionality. Some features may not work.
                  </div>
                )}
                
                <Tabs defaultValue="screenshot" value={activeTab} onValueChange={setActiveTab} className="w-full">
                  <div className="px-4 pt-2">
                    <TabsList className="grid grid-cols-4">
                      <TabsTrigger value="screenshot" className="text-xs flex items-center gap-1">
                        <Camera className="h-3 w-3" /> View
                      </TabsTrigger>
                      <TabsTrigger value="content" className="text-xs flex items-center gap-1">
                        <FileText className="h-3 w-3" /> Content
                      </TabsTrigger>
                      <TabsTrigger value="interact" className="text-xs flex items-center gap-1">
                        <MousePointer className="h-3 w-3" /> Interact
                      </TabsTrigger>
                      <TabsTrigger value="history" className="text-xs flex items-center gap-1">
                        <History className="h-3 w-3" /> History
                      </TabsTrigger>
                    </TabsList>
                  </div>
                  
                  <TabsContent value="screenshot" className="p-4">
                    {screenshot ? (
                      <img 
                        src={screenshot} 
                        alt="Page Screenshot" 
                        className="w-full border rounded-lg shadow-sm"
                      />
                    ) : (
                      <div className="flex items-center justify-center p-8">
                        <Button onClick={takeScreenshot} disabled={isLoading}>
                          <Camera className="h-4 w-4 mr-2" /> Take Screenshot
                        </Button>
                      </div>
                    )}
                  </TabsContent>
                  
                  <TabsContent value="content" className="p-4">
                    <div className="mb-2 flex justify-between items-center">
                      <div className="flex items-center gap-2">
                        <h4 className="text-sm font-medium">Page Content</h4>
                        <Select value={extractMode} onValueChange={setExtractMode}>
                          <SelectTrigger className="h-8 text-xs w-[120px]">
                            <SelectValue placeholder="Extract mode" />
                          </SelectTrigger>
                          <SelectContent>
                            <SelectItem value="auto" title="Intelligently extracts main content">Auto</SelectItem>
                            <SelectItem value="article" title="Focuses on article content for news and blog sites">Article</SelectItem>
                            <SelectItem value="full" title="Retrieves the complete page content">Full Page</SelectItem>
                            <SelectItem value="structured" title="Extracts structured data (headings, links, images, forms, etc.)">Structured</SelectItem>
                          </SelectContent>
                        </Select>
                        <span className="text-xs text-muted-foreground ml-1 cursor-help" title="Use [BROWSE_URL:https://example.com:mode] to specify extraction mode">?</span>
                      </div>
                      <Button variant="outline" size="sm" onClick={getPageContent} disabled={isLoading}>
                        <RefreshCw className={`h-3 w-3 mr-1 ${isLoading ? 'animate-spin' : ''}`} /> Extract
                      </Button>
                    </div>
                    <div className="bg-muted/20 p-3 rounded-md text-sm max-h-[400px] overflow-auto">
                      {extractMode === 'structured' && structuredData ? (
                        <div className="space-y-3">
                          {structuredData.headings && structuredData.headings.length > 0 && (
                            <div>
                              <h5 className="text-xs font-semibold flex items-center gap-1 mb-1">
                                <Database className="h-3 w-3" /> Headings
                              </h5>
                              <ul className="space-y-1">
                                {structuredData.headings.map((heading: any, i: number) => (
                                  <li key={i} className="text-xs">
                                    <span className="bg-muted px-1 rounded text-[10px] mr-1">H{heading.level}</span>
                                    {heading.text}
                                  </li>
                                ))}
                              </ul>
                            </div>
                          )}
                          
                          {structuredData.links && structuredData.links.length > 0 && (
                            <div>
                              <h5 className="text-xs font-semibold flex items-center gap-1 mb-1">
                                <Globe className="h-3 w-3" /> Links
                              </h5>
                              <ul className="space-y-1">
                                {structuredData.links.map((link: any, i: number) => (
                                  <li key={i} className="text-xs truncate">
                                    <span className="text-blue-500">{link.text || 'Link'}</span>
                                    <span className="text-muted-foreground text-[10px] ml-1">{link.url}</span>
                                  </li>
                                ))}
                              </ul>
                            </div>
                          )}
                          
                          {structuredData.forms && structuredData.forms.length > 0 && (
                            <div>
                              <h5 className="text-xs font-semibold flex items-center gap-1 mb-1">
                                <FormInput className="h-3 w-3" /> Forms
                              </h5>
                              <ul className="space-y-2">
                                {structuredData.forms.map((form: any, i: number) => (
                                  <li key={i} className="text-xs border-l-2 border-blue-200 pl-2">
                                    <div className="font-medium">{form.id || `Form ${i+1}`}</div>
                                    <div className="text-[10px] text-muted-foreground mb-1">
                                      {form.method.toUpperCase()} {form.action}
                                    </div>
                                    {form.inputs && (
                                      <ul className="space-y-1">
                                        {form.inputs.map((input: any, j: number) => (
                                          <li key={j} className="text-[10px] flex items-center gap-1">
                                            <span className="bg-muted px-1 rounded">{input.type}</span>
                                            <span>{input.name || input.id || 'unnamed'}</span>
                                            {input.placeholder && (
                                              <span className="text-muted-foreground">"{input.placeholder}"</span>
                                            )}
                                          </li>
                                        ))}
                                      </ul>
                                    )}
                                  </li>
                                ))}
                              </ul>
                            </div>
                          )}
                        </div>
                      ) : pageContent ? (
                        <div dangerouslySetInnerHTML={{ __html: pageContent }} />
                      ) : (
                        <p className="text-muted-foreground text-xs">Select an extraction mode and click Extract to load page content</p>
                      )}
                    </div>
                  </TabsContent>
                  
                  <TabsContent value="interact" className="p-4">
                    <div className="space-y-4">
                      <div>
                        <h4 className="text-sm font-medium mb-2 flex items-center">
                        Click Element
                        <span className="ml-1 text-xs text-muted-foreground cursor-help" title="Use [CLICK_ELEMENT:#submit-button] in your messages to click elements automatically">ℹ️</span>
                      </h4>
                        <div className="flex gap-2">
                          <Input 
                            placeholder="CSS Selector (e.g., #submit-button)" 
                            value={selector}
                            onChange={(e) => setSelector(e.target.value)}
                            className="text-xs"
                          />
                          <Button size="sm" onClick={() => clickElement(selector)} disabled={!selector.trim() || isLoading}>
                            Click
                          </Button>
                        </div>
                      </div>
                      
                      <div>
                        <h4 className="text-sm font-medium mb-2 flex items-center">
                          Fill Form
                          <span className="ml-1 text-xs text-muted-foreground cursor-help" title="Use [FILL_FORM:#email=user@example.com,#password=secret] in your messages to fill forms automatically">ℹ️</span>
                        </h4>
                        <div className="flex flex-col gap-2">
                          <Label htmlFor="form-data" className="text-xs">
                            Format: #email=user@example.com,#password=secret
                          </Label>
                          <Input
                            id="form-data"
                            placeholder="#email=user@example.com,#password=secret"
                            value={formData}
                            onChange={(e) => setFormData(e.target.value)}
                            className="text-xs"
                          />
                          <Button size="sm" onClick={fillForm} disabled={!formData.trim() || isLoading}>
                            <FormInput className="h-3 w-3 mr-1" /> Fill Form
                          </Button>
                        </div>
                      </div>
                      
                      <div>
                        <h4 className="text-sm font-medium mb-2 flex items-center">
                        Execute JavaScript
                        <span className="ml-1 text-xs text-muted-foreground cursor-help" title="Advanced feature: Execute custom JavaScript on the page for complex interactions">ℹ️</span>
                      </h4>
                        <div className="flex flex-col gap-2">
                          <Textarea
                            placeholder="Enter JavaScript code..."
                            value={jsCode}
                            onChange={(e: React.ChangeEvent<HTMLTextAreaElement>) => setJsCode(e.target.value)}
                            className="text-xs h-[100px] font-mono"
                          />
                          <Button size="sm" onClick={() => executeJavaScript(jsCode)} disabled={!jsCode.trim() || isLoading}>
                            <Code className="h-3 w-3 mr-1" /> Execute
                          </Button>
                        </div>
                      </div>
                    </div>
                  </TabsContent>
                  
                  <TabsContent value="history" className="p-4">
                    <div className="mb-2 flex justify-between">
                      <h4 className="text-sm font-medium">Browsing History</h4>
                      <Button variant="outline" size="sm" onClick={getBrowsingHistory} disabled={isLoading}>
                        <RefreshCw className={`h-3 w-3 mr-1 ${isLoading ? 'animate-spin' : ''}`} /> Refresh
                      </Button>
                    </div>
                    
                    {history.length > 0 ? (
                      <ul className="space-y-2">
                        {history.map((item, index) => (
                          <li key={index} className="text-xs border-b pb-2">
                            <p className="font-medium truncate">{item.title}</p>
                            <p className="text-muted-foreground truncate">{item.url}</p>
                            <Button 
                              variant="link" 
                              size="sm" 
                              className="h-auto p-0 text-xs"
                              onClick={() => navigate(item.url)}
                            >
                              Visit Again
                            </Button>
                          </li>
                        ))}
                      </ul>
                    ) : (
                      <p className="text-muted-foreground text-xs">No browsing history yet</p>
                    )}
                  </TabsContent>
                </Tabs>
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
