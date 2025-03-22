# Web Browsing Functionality

## Overview

The MCP server now includes web browsing capabilities powered by Puppeteer, allowing AI advisors to access and interact with web content. This feature enables the AI to perform research, gather information, and provide more contextually relevant responses.

## Features

- **Browser Session Management**: Create and manage browser sessions
- **Web Navigation**: Browse websites and follow links
- **Content Extraction**: Extract and analyze web page content
- **Screenshot Capture**: Take screenshots of web pages
- **Interactive Elements**: Click buttons, fill forms, and interact with web content
- **JavaScript Execution**: Run custom scripts for advanced web interactions

## How to Use

### In AI Conversations

You can use special commands in your queries to trigger web browsing functionality:

1. **Search the Web**:
   ```
   [SEARCH_WEB:your search query]
   ```
   Example: "I need information about [SEARCH_WEB:small business tax deductions]"

2. **Browse a Specific URL**:
   ```
   [BROWSE_URL:https://example.com]
   ```
   Example: "Please analyze the content at [BROWSE_URL:https://www.sba.gov/business-guide]"

### API Endpoints

The following API endpoints are available for direct integration:

- `POST /api/v1/browser/sessions` - Create a new browser session
- `DELETE /api/v1/browser/sessions/{session_id}` - Close a browser session
- `POST /api/v1/browser/sessions/{session_id}/navigate` - Navigate to a URL
- `POST /api/v1/browser/sessions/{session_id}/screenshot` - Take a screenshot
- `POST /api/v1/browser/sessions/{session_id}/click` - Click an element
- `POST /api/v1/browser/sessions/{session_id}/fill` - Fill an input field
- `POST /api/v1/browser/sessions/{session_id}/evaluate` - Execute JavaScript
- `GET /api/v1/browser/sessions/{session_id}/history` - Get browsing history

## Example Code

### Python Example

```python
import httpx
import asyncio

async def search_web():
    # Create a session
    async with httpx.AsyncClient() as client:
        response = await client.post("http://localhost:8000/api/v1/browser/sessions")
        session_id = response.json()["session_id"]
        
        # Navigate to a search engine
        await client.post(
            f"http://localhost:8000/api/v1/browser/sessions/{session_id}/navigate",
            json={"url": "https://duckduckgo.com"}
        )
        
        # Fill the search box
        await client.post(
            f"http://localhost:8000/api/v1/browser/sessions/{session_id}/fill",
            json={"selector": "input[name=q]", "value": "small business advice"}
        )
        
        # Click the search button
        await client.post(
            f"http://localhost:8000/api/v1/browser/sessions/{session_id}/click",
            json={"selector": "button[type=submit]"}
        )
        
        # Take a screenshot
        response = await client.post(
            f"http://localhost:8000/api/v1/browser/sessions/{session_id}/screenshot"
        )
        
        # Close the session
        await client.delete(f"http://localhost:8000/api/v1/browser/sessions/{session_id}")

# Run the example
asyncio.run(search_web())
```

### JavaScript/React Example

```javascript
import { useState } from 'react';
import axios from 'axios';

function BrowserExample() {
  const [sessionId, setSessionId] = useState('');
  const [screenshot, setScreenshot] = useState('');
  
  const createSession = async () => {
    const response = await axios.post('/api/v1/browser/sessions');
    setSessionId(response.data.session_id);
  };
  
  const navigateToUrl = async (url) => {
    await axios.post(`/api/v1/browser/sessions/${sessionId}/navigate`, {
      url
    });
  };
  
  const takeScreenshot = async () => {
    const response = await axios.post(`/api/v1/browser/sessions/${sessionId}/screenshot`);
    setScreenshot(`data:image/png;base64,${response.data.data}`);
  };
  
  const closeSession = async () => {
    await axios.delete(`/api/v1/browser/sessions/${sessionId}`);
    setSessionId('');
    setScreenshot('');
  };
  
  return (
    <div>
      <h2>Browser Integration Example</h2>
      
      {!sessionId ? (
        <button onClick={createSession}>Create Browser Session</button>
      ) : (
        <div>
          <div>
            <input 
              type="text" 
              placeholder="Enter URL"
              onKeyDown={(e) => e.key === 'Enter' && navigateToUrl(e.target.value)}
            />
            <button onClick={takeScreenshot}>Take Screenshot</button>
            <button onClick={closeSession}>Close Session</button>
          </div>
          
          {screenshot && (
            <div>
              <h3>Screenshot</h3>
              <img src={screenshot} alt="Page screenshot" style={{ maxWidth: '100%' }} />
            </div>
          )}
        </div>
      )}
    </div>
  );
}
```

## Security Considerations

- The web browsing feature runs in a controlled environment with appropriate security measures
- Browser sessions are isolated and do not persist user data between sessions
- Access to the browser API endpoints should be properly authenticated in production environments
- Consider implementing rate limiting to prevent abuse

## Troubleshooting

- If a browser session becomes unresponsive, you can close it and create a new one
- Some websites may have anti-bot measures that prevent automated browsing
- For complex interactions, use the `evaluate` endpoint to run custom JavaScript
- Check the server logs for detailed error information

## Dependencies

The web browsing functionality requires the following dependencies:

- Pyppeteer: `pip install pyppeteer`
- Asyncio: `pip install asyncio`

These dependencies are included in the `requirements-browser.txt` file.
