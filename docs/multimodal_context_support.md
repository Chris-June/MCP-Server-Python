# Multi-Modal Context Support

## Overview

The Multi-Modal Context Support feature enhances the MCP server by enabling it to process and analyze different types of media alongside text. This allows for richer, more contextual interactions with AI models that can understand and respond to various forms of content, including images, audio, and potentially other media formats in the future.

## Features

### Supported Media Types

- **Images**: Process and analyze images alongside text queries
- **Text**: Enhanced text processing with contextual awareness of media
- **Future Support**: Framework in place for audio and video content (pending API capabilities)

### API Endpoints

#### Process Multi-Modal Content

```http
POST /api/v1/multimodal/process
```

Process a multi-modal query using a specific role.

**Request Body:**

```json
{
  "role_id": "cfo-advisor",
  "content": {
    "text": "What insights can you provide about our financial performance based on this chart?",
    "media": [{
      "type": "image",
      "base64_data": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQEAYABgAAD...",
      "mime_type": "image/jpeg",
      "alt_text": "Financial performance chart"
    }]
  },
  "custom_instructions": "Focus on cash flow implications"
}
```

**Response:**

```json
{
  "role_id": "cfo-advisor",
  "response": "Based on the financial performance chart you've shared, I can see several important cash flow trends...",
  "processed_media": [
    {
      "index": 0,
      "type": "image",
      "processed": true,
      "alt_text": "Financial performance chart"
    }
  ]
}
```

#### Process Multi-Modal Content with Streaming Response

```http
POST /api/v1/multimodal/process/stream
```

Process a multi-modal query with a streaming response.

**Request Body:** Same as the non-streaming endpoint

**Response:** Server-sent events stream with chunks of the response

#### Upload File for Multi-Modal Processing

```http
POST /api/v1/multimodal/upload
```

Upload a file for multi-modal processing.

**Request Form Data:**
- `file`: The file to upload
- `description`: Optional description of the file

**Response:**

```json
{
  "filename": "quarterly_report.jpg",
  "content_type": "image/jpeg",
  "size": 245678,
  "base64_data": "base64-encoded-content",
  "description": "Q2 2024 Financial Report"
}
```

#### Analyze Image

```http
POST /api/v1/multimodal/analyze/image
```

Analyze an image with a specific prompt.

**Request Form Data:**
- `image_url`: URL or base64 data of the image
- `prompt`: The analysis prompt

**Response:**

```json
{
  "analysis": "The chart shows a steady increase in revenue over the past four quarters..."
}
```

## Implementation Details

### Models

The multi-modal feature introduces several new models:

- `ContentType`: Enum for different types of media content (text, image, audio, video, file)
- `MediaContent`: Model for media content with type, URL/data, and metadata
- `MultiModalContent`: Model combining text and media content
- `MultiModalProcessRequest`: Request model for processing multi-modal queries
- `MultiModalProcessResponse`: Response model for processed multi-modal queries

### Services

- `MultiModalProcessor`: Service for processing multi-modal content using OpenAI's vision-capable models

### Configuration

The feature uses the following configuration settings:

- `openai_model`: Standard text model (default: gpt-4o-mini)
- `openai_vision_model`: Vision-capable model for multi-modal content (default: gpt-4o)

## Usage Examples

### Processing an Image with Text Query

```javascript
// Example client-side code
async function processImageWithQuery() {
  // Get the image file from an input element
  const imageFile = document.getElementById('imageInput').files[0];
  const query = document.getElementById('queryInput').value;
  
  // Convert image to base64
  const reader = new FileReader();
  reader.readAsDataURL(imageFile);
  
  reader.onload = async () => {
    const base64Data = reader.result;
    
    // Prepare the request
    const requestData = {
      role_id: "cfo-advisor",
      content: {
        text: query,
        media: [{
          type: "image",
          base64_data: base64Data,
          mime_type: imageFile.type,
          alt_text: "Uploaded image for analysis"
        }]
      }
    };
    
    // Send the request
    const response = await fetch('/api/v1/multimodal/process', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(requestData)
    });
    
    const result = await response.json();
    document.getElementById('responseOutput').textContent = result.response;
  };
}
```

## Future Enhancements

1. **Audio Processing**: Add support for audio file analysis and transcription
2. **Video Processing**: Add support for video content analysis
3. **Document Analysis**: Enhanced support for document parsing and analysis
4. **Multi-Turn Conversations**: Maintain context across multiple interactions with mixed media
5. **Media Generation**: Add capabilities for AI to generate images or other media in responses

## Technical Considerations

### Performance

- Multi-modal processing, especially with images, requires more computational resources
- Consider implementing caching for frequently accessed media
- Be mindful of rate limits and token usage with the OpenAI API

### Security

- Validate and sanitize all uploaded media content
- Implement proper access controls for media storage
- Consider privacy implications when processing user-uploaded media

### Limitations

- Vision models have token limits that restrict the size and number of images
- Some complex visual elements may not be accurately interpreted
- Processing time increases with the complexity and number of media elements
