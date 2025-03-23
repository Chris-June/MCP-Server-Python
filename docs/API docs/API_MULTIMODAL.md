# Multi-Modal Processing API

This document provides comprehensive documentation for the multi-modal processing endpoints in the MCP Server, including example requests and responses.

## Table of Contents

- [Process Multi-Modal Content](#process-multi-modal-content)
- [Process Multi-Modal Content with Streaming Response](#process-multi-modal-content-with-streaming-response)

## Process Multi-Modal Content

```
POST /api/v1/multimodal/process
```

**Description:** Processes multi-modal content (text and images) using a specific role.

**Request Body (multipart/form-data):**
- `role_id`: String - The ID of the role to use for processing
- `query`: String - The text query to process
- `images`: File(s) - One or more image files to process
- `custom_instructions`: String (Optional) - Custom instructions for processing
- `provider`: String (Optional) - Specific LLM provider to use (openai, anthropic, gemini)

**Example Request:**
```bash
curl -X 'POST' \
  'http://localhost:8000/api/v1/multimodal/process' \
  -H 'accept: application/json' \
  -F 'role_id=product-analyst' \
  -F 'query=What can you tell me about this product based on the image?' \
  -F 'images=@product_image.jpg' \
  -F 'custom_instructions=Focus on design and usability aspects.' \
  -F 'provider=openai'
```

**Example Response:**
```json
{
  "role_id": "product-analyst",
  "query": "What can you tell me about this product based on the image?",
  "response": "# Product Analysis\n\n## Design and Usability Overview\n\nBased on the image provided, this appears to be a wireless ergonomic keyboard with the following notable features:\n\n### Design Elements\n* **Ergonomic Split Layout**: The keyboard has a split design that positions the hands at a more natural angle, potentially reducing wrist strain\n* **Low Profile Keys**: Chiclet-style keys with what appears to be short travel distance\n* **Compact Form Factor**: No separate number pad, making this a tenkeyless (TKL) design\n* **Wireless Connectivity**: No visible cables, suggesting Bluetooth or RF wireless connection\n* **Minimalist Aesthetic**: Clean design with a monochromatic color scheme (appears to be dark gray/black)\n\n### Usability Considerations\n* The split design promotes better ergonomics but may require an adjustment period for users\n* The compact size makes it portable and saves desk space\n* The key spacing appears comfortable for typing\n* Function keys appear to have dual purposes (media controls, etc.)\n* Palm rest appears to be integrated into the design\n\n### Potential User Experience\n* Learning curve: Moderate due to the split layout\n* Comfort: Likely high for extended typing sessions due to ergonomic design\n* Portability: Good due to wireless design and compact size\n* Typing experience: Likely quiet with medium key travel based on the visual profile\n\nFor a complete assessment, I would need additional information about connectivity options, battery life, and specific ergonomic adjustments available."
}
```

## Process Multi-Modal Content with Streaming Response

```
POST /api/v1/multimodal/process-stream
```

**Description:** Processes multi-modal content (text and images) using a specific role and returns a streaming response.

**Request Body (multipart/form-data):**
- `role_id`: String - The ID of the role to use for processing
- `query`: String - The text query to process
- `images`: File(s) - One or more image files to process
- `custom_instructions`: String (Optional) - Custom instructions for processing
- `provider`: String (Optional) - Specific LLM provider to use (openai, anthropic, gemini)

**Example Request:**
```bash
curl -X 'POST' \
  'http://localhost:8000/api/v1/multimodal/process-stream' \
  -H 'accept: text/event-stream' \
  -F 'role_id=product-analyst' \
  -F 'query=What can you tell me about this product based on the image?' \
  -F 'images=@product_image.jpg' \
  -F 'custom_instructions=Focus on design and usability aspects.' \
  -F 'provider=openai'
```

**Example Response:**
The response is a text/event-stream with data chunks that can be processed in real-time:

```
data: # Product Analysis

data: ## Design and Usability Overview

data: Based on the image provided, this appears to be a wireless ergonomic keyboard with the following notable features:

...

data: [DONE]
```
