# Web Browser API

This document provides comprehensive documentation for the web browser automation endpoints in the MCP Server, including example requests and responses.

## Table of Contents

- [Create Browser Session](#create-browser-session)
- [Close Browser Session](#close-browser-session)
- [Navigate to URL](#navigate-to-url)
- [Get Current Page Content](#get-current-page-content)
- [Take Screenshot](#take-screenshot)
- [Click Element](#click-element)
- [Fill Form Field](#fill-form-field)
- [Execute JavaScript](#execute-javascript)

## Create Browser Session

```
POST /api/v1/browser/sessions
```

**Description:** Creates a new browser automation session with optional configuration parameters.

**Request Body:**
```json
{
  "headless": boolean,  // Optional, default: true
  "viewport": {  // Optional
    "width": number,  // Default: 1280
    "height": number  // Default: 800
  },
  "user_agent": "string",  // Optional
  "timeout": number  // Optional, in milliseconds, default: 30000
}
```

**Example Request:**
```bash
curl -X 'POST' \
  'http://localhost:8000/api/v1/browser/sessions' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "headless": true,
  "viewport": {
    "width": 1920,
    "height": 1080
  },
  "timeout": 60000
}'
```

**Example Response:**
```json
{
  "session_id": "browser-abc123",
  "status": "created",
  "created_at": "2025-03-24T14:30:15Z",
  "config": {
    "headless": true,
    "viewport": {
      "width": 1920,
      "height": 1080
    },
    "timeout": 60000
  }
}
```

## Close Browser Session

```
DELETE /api/v1/browser/sessions/{session_id}
```

**Description:** Closes a browser session and releases associated resources.

**Parameters:**
- `session_id` (path parameter): The unique identifier of the browser session.

**Example Request:**
```bash
curl -X 'DELETE' 'http://localhost:8000/api/v1/browser/sessions/browser-abc123' -H 'accept: application/json'
```

**Example Response:**
```json
{
  "message": "Browser session browser-abc123 closed successfully"
}
```

## Navigate to URL

```
POST /api/v1/browser/sessions/{session_id}/navigate
```

**Description:** Navigates the browser to a specified URL.

**Parameters:**
- `session_id` (path parameter): The unique identifier of the browser session.

**Request Body:**
```json
{
  "url": "string",
  "wait_until": "string"  // Optional: "load", "domcontentloaded", "networkidle0", "networkidle2"
}
```

**Example Request:**
```bash
curl -X 'POST' \
  'http://localhost:8000/api/v1/browser/sessions/browser-abc123/navigate' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "url": "https://example.com",
  "wait_until": "networkidle0"
}'
```

**Example Response:**
```json
{
  "session_id": "browser-abc123",
  "url": "https://example.com",
  "title": "Example Domain",
  "status": 200
}
```

## Get Current Page Content

```
GET /api/v1/browser/sessions/{session_id}/content
```

**Description:** Retrieves the HTML content and metadata of the current page.

**Parameters:**
- `session_id` (path parameter): The unique identifier of the browser session.
- `include_html` (query parameter, optional): Whether to include full HTML content (default: true).

**Example Request:**
```bash
curl -X 'GET' 'http://localhost:8000/api/v1/browser/sessions/browser-abc123/content' -H 'accept: application/json'
```

**Example Response:**
```json
{
  "session_id": "browser-abc123",
  "url": "https://example.com",
  "title": "Example Domain",
  "metadata": {
    "description": "Example Domain for illustrative purposes",
    "og:title": "Example Domain",
    "og:type": "website"
  },
  "html": "<!doctype html><html><head>...</head><body>...</body></html>",
  "text_content": "Example Domain\nThis domain is for use in illustrative examples in documents..."
}
```

## Take Screenshot

```
POST /api/v1/browser/sessions/{session_id}/screenshot
```

**Description:** Takes a screenshot of the current page or a specific element.

**Parameters:**
- `session_id` (path parameter): The unique identifier of the browser session.

**Request Body:**
```json
{
  "selector": "string",  // Optional: CSS selector for a specific element
  "full_page": boolean,  // Optional, default: false
  "format": "string",   // Optional: "png" or "jpeg", default: "png"
  "quality": number      // Optional: 0-100, only for jpeg format
}
```

**Example Request:**
```bash
curl -X 'POST' \
  'http://localhost:8000/api/v1/browser/sessions/browser-abc123/screenshot' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "selector": "#main-content",
  "format": "jpeg",
  "quality": 80
}'
```

**Example Response:**
```json
{
  "session_id": "browser-abc123",
  "image_data": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQEASABIAAD/...",
  "timestamp": "2025-03-24T14:35:22Z",
  "dimensions": {
    "width": 800,
    "height": 600
  }
}
```

## Click Element

```
POST /api/v1/browser/sessions/{session_id}/click
```

**Description:** Clicks on an element identified by a CSS selector.

**Parameters:**
- `session_id` (path parameter): The unique identifier of the browser session.

**Request Body:**
```json
{
  "selector": "string",
  "button": "string",  // Optional: "left", "right", "middle", default: "left"
  "click_count": number,  // Optional, default: 1
  "delay": number  // Optional: delay between clicks in milliseconds
}
```

**Example Request:**
```bash
curl -X 'POST' \
  'http://localhost:8000/api/v1/browser/sessions/browser-abc123/click' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "selector": "button.submit-form",
  "click_count": 1
}'
```

**Example Response:**
```json
{
  "session_id": "browser-abc123",
  "selector": "button.submit-form",
  "success": true,
  "url_changed": true,
  "new_url": "https://example.com/submitted"
}
```

## Fill Form Field

```
POST /api/v1/browser/sessions/{session_id}/fill
```

**Description:** Fills a form field identified by a CSS selector with the specified value.

**Parameters:**
- `session_id` (path parameter): The unique identifier of the browser session.

**Request Body:**
```json
{
  "selector": "string",
  "value": "string",
  "delay": number  // Optional: typing delay in milliseconds
}
```

**Example Request:**
```bash
curl -X 'POST' \
  'http://localhost:8000/api/v1/browser/sessions/browser-abc123/fill' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "selector": "input[name=\'email\']",
  "value": "user@example.com",
  "delay": 10
}'
```

**Example Response:**
```json
{
  "session_id": "browser-abc123",
  "selector": "input[name='email']",
  "success": true
}
```

## Execute JavaScript

```
POST /api/v1/browser/sessions/{session_id}/execute
```

**Description:** Executes JavaScript code in the context of the current page.

**Parameters:**
- `session_id` (path parameter): The unique identifier of the browser session.

**Request Body:**
```json
{
  "script": "string",
  "args": ["any"]  // Optional: arguments to pass to the script
}
```

**Example Request:**
```bash
curl -X 'POST' \
  'http://localhost:8000/api/v1/browser/sessions/browser-abc123/execute' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "script": "return document.title + \" - \" + window.location.href;",
  "args": []
}'
```

**Example Response:**
```json
{
  "session_id": "browser-abc123",
  "result": "Example Domain - https://example.com",
  "success": true
}
```
