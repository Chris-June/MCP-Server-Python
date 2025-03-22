# Small Business Executive Advisors

*Your Virtual C-Suite Team*

An AI-powered platform providing small businesses with executive-level advisory services through specialized AI agents that serve as virtual C-suite executives.

![Small Business Executive Advisors](https://via.placeholder.com/800x400?text=Small+Business+Executive+Advisors)

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Installation](#installation)
  - [Prerequisites](#prerequisites)
  - [Server Setup](#server-setup)
  - [Client Setup](#client-setup)
  - [Environment Configuration](#environment-configuration)
- [Usage](#usage)
  - [Starting the Server](#starting-the-server)
  - [Starting the Client](#starting-the-client)
  - [API Documentation](#api-documentation)
- [Core Concepts](#core-concepts)
  - [Roles](#roles)
  - [Memories](#memories)
  - [Query Processing](#query-processing)
- [Client Interface](#client-interface)
  - [Role Management](#role-management)
  - [Chat Interface](#chat-interface)
- [Examples](#examples)
  - [Creating a Financial Advisor Role](#creating-a-financial-advisor-role)
  - [Creating a Technical Support Role](#creating-a-technical-support-role)
  - [Sample Conversations](#sample-conversations)
- [Advanced Configuration](#advanced-configuration)
  - [Customizing System Prompts](#customizing-system-prompts)
  - [Fine-tuning Role Behavior](#fine-tuning-role-behavior)
- [Development](#development)
  - [Project Structure](#project-structure)
  - [Adding New Features](#adding-new-features)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## Overview

Small Business Executive Advisors is a powerful platform designed to provide small businesses with access to executive-level guidance and expertise through AI-powered advisors. Our platform offers a suite of virtual C-suite executives, each specialized in different business functions, to help small business owners make better decisions and grow their companies.

With advisors covering CEO, CFO, CMO, HR, Operations, and Sales functions, small business owners can access strategic guidance, financial planning, marketing expertise, and operational improvements without the cost of hiring full-time executives.

This platform allows you to:

1. Consult with specialized executive advisors in different business domains
2. Access a comprehensive business dashboard with key metrics and insights
3. Receive personalized advice based on your specific business context
4. Track business goals and progress through an intuitive interface

## Features

### Executive Advisory Features

- **CEO Advisory**: Strategic guidance on business leadership, growth, and decision-making
- **CFO Advisory**: Financial strategy, cash flow management, and investment planning
- **CMO Advisory**: Marketing strategy, brand development, and customer acquisition
- **HR Advisory**: Talent management, employee engagement, and team development
- **Operations Advisory**: Process optimization, efficiency improvements, and operational scaling
- **Sales Advisory**: Sales strategy, pipeline development, and customer relationship management
- **Contextual Memory**: Advisors remember previous consultations for continuity
- **Business-Specific Advice**: Tailored guidance based on your business context
- **Business Dashboard**: Visualize key metrics and advisor insights in one place

### Platform Features

- **Modern Interface**: Clean, professional design built with React and TailwindCSS
- **Responsive Design**: Mobile-friendly interface with dark/light theme support
- **Custom Advisor Creation**: Create specialized advisors for your unique business needs
- **Interactive Consultations**: Real-time conversation interface with executive advisors
- **Streaming Responses**: Real-time advisor responses as they're generated
- **OpenAI Integration**: Powered by OpenAI's GPT-4o-mini model for high-quality advice
- **Business Metrics**: Track revenue, customers, conversion rates, and expenses
- **Advisor Insights**: View and manage business insights from different executive advisors
- **Business Goals**: Set and track progress towards important business milestones

## Architecture

### System Architecture

The MCP Server follows a clean, modular architecture:

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  React      │     │  FastAPI    │     │  OpenAI     │
│  Client     │────▶│  Server     │────▶│  API        │
└─────────────┘     └─────────────┘     └─────────────┘
                           │
                           ▼
                    ┌─────────────┐
                    │  In-Memory  │
                    │  Database   │
                    └─────────────┘
```

- **Client Layer**: React application for user interaction
- **API Layer**: FastAPI server handling requests and business logic
- **Service Layer**: Core services for role management, memory handling, and AI processing
- **Data Layer**: In-memory storage for roles and memories

### Data Flow

1. User creates roles and interacts with them through the React client
2. Client sends API requests to the FastAPI server
3. Server processes requests, manages roles and memories
4. For query processing, the server:
   - Retrieves the specified role
   - Fetches relevant memories
   - Constructs a context-aware prompt
   - Sends the prompt to OpenAI's API
   - Returns the response to the client

## Installation

### Prerequisites

- Python 3.11+
- Node.js 18+ and npm
- OpenAI API key
- Git (for cloning the repository)

### Server Setup

1. Clone the repository:

```bash
git clone https://github.com/Chris-June/MCP-GPT-Builder.git
cd MCP-GPT-Builder
```

2. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install server dependencies:

```bash
pip install -r requirements.txt
```

### Client Setup

1. Navigate to the client directory:

```bash
cd client
```

2. Install client dependencies:

```bash
npm install
```

### Environment Configuration

1. Create a `.env` file in the root directory based on the example:

```bash
cp .env.example .env
```

2. Open the `.env` file and configure the following variables:

```
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4o-mini  # The model to use for AI processing
SERVER_HOST=0.0.0.0  # Host to bind the server to
SERVER_PORT=8000  # Port to run the server on
```

## Usage

### Starting the Server

1. From the root directory, with the virtual environment activated:

```bash
uvicorn server:app --reload --host 0.0.0.0 --port 8000
```

The server will be available at http://localhost:8000.

2. Access the API documentation at http://localhost:8000/docs to explore available endpoints.

### Starting the Client

1. From the client directory, in a separate terminal:

```bash
npm run dev
```

The client will be available at http://localhost:5173.

### API Documentation

The MCP Server provides a comprehensive API for managing roles, memories, and processing queries:

#### Role Management

- `GET /api/v1/roles` - List all roles
- `GET /api/v1/roles/{role_id}` - Get a specific role
- `POST /api/v1/roles` - Create a new role
- `PUT /api/v1/roles/{role_id}` - Update a role
- `DELETE /api/v1/roles/{role_id}` - Delete a role

#### Memory Management

- `GET /api/v1/memories/{role_id}` - Get memories for a role
- `POST /api/v1/memories` - Create a new memory
- `DELETE /api/v1/memories/{role_id}` - Clear all memories for a role

#### Query Processing

- `POST /api/v1/roles/process` - Process a query with role-specific context

## Core Concepts

### Roles

Roles are the foundation of the MCP Server. Each role represents a specialized AI assistant with specific expertise, personality traits, and behavior guidelines.

#### Role Properties

- **id**: Unique identifier for the role
- **name**: Display name for the role
- **description**: Brief description of the role's purpose
- **instructions**: Specific guidelines for how the role should behave
- **domains**: Areas of expertise (e.g., Finance, Marketing, Technical Support)
- **tone**: Communication style (professional, casual, friendly, technical, formal)
- **system_prompt**: Advanced configuration for the AI model
- **is_default**: Whether this is a default role

#### Creating Effective Roles

When creating roles, consider the following best practices:

1. **Be Specific**: Clearly define the role's expertise and limitations
2. **Set Clear Guidelines**: Provide detailed instructions on how the role should respond
3. **Define Tone**: Choose a tone that matches the role's purpose
4. **Craft System Prompts**: Use system prompts to fine-tune behavior

### Memories

Memories provide context for AI roles, allowing them to maintain information across conversations.

#### Memory Properties

- **id**: Unique identifier for the memory
- **role_id**: The role this memory belongs to
- **content**: The actual memory content
- **type**: Type of memory (e.g., conversation, fact, preference)
- **importance**: Importance level (affects retrieval priority)
- **embedding**: Vector representation for semantic search
- **created_at**: Timestamp when the memory was created

### Query Processing

Query processing combines roles, memories, and user input to generate contextually relevant responses.

#### Processing Flow

1. User sends a query for a specific role
2. Server retrieves the role configuration
3. Server fetches relevant memories for context
4. Server constructs a prompt with role instructions, tone, and memories
5. Server sends the prompt to OpenAI's API
6. Server returns the AI-generated response to the client

## Client Interface

### Role Management

The client provides a user-friendly interface for managing AI roles:

#### Role List

The Roles page displays all available roles with options to:
- View role details
- Edit existing roles
- Delete roles
- Create new roles

#### Role Creation

The role creation form allows you to define all aspects of a new AI role:

1. **Basic Information**:
   - Name: A descriptive name for the role
   - Description: Brief summary of the role's purpose

2. **Expertise Configuration**:
   - Domains: Areas of expertise for the role
   - Tone: Communication style

3. **Behavior Guidelines**:
   - Instructions: Specific guidelines for how the role should behave
   - System Prompt: Advanced configuration for the AI model

### Chat Interface

The Chat page provides an interactive interface for conversing with AI roles:

1. **Role Selection**: Choose from available roles
2. **Conversation**: Send messages and receive AI responses
3. **Context Awareness**: The AI maintains context throughout the conversation

## Examples

### Creating a Financial Advisor Role

```json
{
  "id": "financial-advisor",
  "name": "Financial Advisor",
  "description": "Expert in personal finance and investment strategies",
  "instructions": "You are a financial advisor with expertise in retirement planning. Always provide balanced advice considering both short-term and long-term financial goals. Explain concepts in simple terms and avoid financial jargon when possible.",
  "domains": ["Finance", "Investment", "Retirement", "Tax Planning"],
  "tone": "professional",
  "system_prompt": "You are FinanceGPT, an AI assistant specialized in personal finance and investment strategies. You have extensive knowledge of retirement accounts, tax optimization, debt management, and investment vehicles. When providing advice, always consider risk tolerance, time horizon, and tax implications. Format your responses with clear sections and bullet points when appropriate."
}
```

### Creating a Technical Support Role

```json
{
  "id": "tech-support",
  "name": "Technical Support Specialist",
  "description": "Expert in troubleshooting software and hardware issues",
  "instructions": "You are a technical support specialist. Always start by understanding the user's problem before suggesting solutions. Ask clarifying questions if needed. Provide step-by-step instructions that are easy to follow.",
  "domains": ["Software", "Hardware", "Networking", "Troubleshooting"],
  "tone": "friendly",
  "system_prompt": "You are TechGPT, an AI assistant specialized in technical support and troubleshooting. You have extensive knowledge of common software issues, hardware problems, and networking configurations. When helping users, first diagnose the problem by understanding the symptoms, then provide clear, step-by-step solutions. Use numbered lists for instructions and explain technical concepts in simple terms."
}
```

### Sample Conversations

#### Financial Advisor Conversation

**User**: I'm 35 and want to start saving for retirement. What should I do?

**AI**: Great question! Starting to save for retirement at 35 is still plenty of time to build a solid nest egg. Here's a balanced approach to get you started:

**First Steps:**
* **Establish an emergency fund** of 3-6 months of expenses before focusing heavily on retirement
* **Take advantage of employer matching** if your workplace offers a 401(k) match - this is essentially free money

**Retirement Account Options:**
* **401(k)/403(b)**: Try to contribute at least enough to get the full employer match
* **Roth IRA**: Consider opening one if you're eligible - contributions grow tax-free
* **Traditional IRA**: Another option with potential tax advantages now

**Investment Strategy:**
* At 35, you can still have a relatively aggressive portfolio (e.g., 70-80% stocks, 20-30% bonds)
* Consider low-cost index funds for diversification

Would you like me to explain any of these options in more detail?

#### Technical Support Conversation

**User**: My laptop keeps freezing randomly. What could be wrong?

**AI**: I'm sorry to hear about your laptop freezing issues! Let's figure this out together. 

**Possible Causes & Solutions:**

1. **Overheating**
   * Check if your laptop feels hot when it freezes
   * Ensure vents aren't blocked and consider using a cooling pad
   * Clean dust from internal fans (if you're comfortable opening it or get professional help)

2. **Resource-intensive applications**
   * Check Task Manager (Ctrl+Shift+Esc) to see what's using resources
   * Close unnecessary applications and browser tabs

3. **Outdated drivers or software**
   * Update your operating system
   * Update graphics and other device drivers

4. **Insufficient RAM or storage**
   * Check available storage space (aim for at least 10% free)
   * Consider upgrading RAM if your system is consistently using near 100%

Could you tell me a bit more about when the freezing happens? Does it occur during specific activities or at random times?

## Advanced Configuration

### Customizing System Prompts

System prompts are powerful tools for fine-tuning AI behavior. Here are some tips for crafting effective system prompts:

1. **Define Identity**: Clearly state who the AI is and its expertise
2. **Set Boundaries**: Define what the AI should and shouldn't do
3. **Specify Format**: Indicate how responses should be structured
4. **Include Examples**: Provide examples of ideal responses

### Fine-tuning Role Behavior

To fine-tune role behavior:

1. **Adjust Instructions**: Modify the role's instructions to guide behavior
2. **Change Tone**: Select a different tone to alter communication style
3. **Add Memories**: Create memories with important information
4. **Refine Domains**: Update expertise domains to focus the role's knowledge

## Development

### Project Structure

```
/
├── app/                    # Server application
│   ├── models/            # Data models
│   ├── routes/            # API endpoints
│   └── services/          # Business logic
├── client/                # React client
│   ├── src/               # Source code
│   │   ├── components/    # UI components
│   │   ├── lib/           # Utilities
│   │   ├── pages/         # Page components
│   │   └── types/         # TypeScript types
├── .env.example           # Example environment variables
├── requirements.txt       # Python dependencies
└── server.py              # Server entry point
```

### Adding New Features

#### Adding a New API Endpoint

1. Create a new route file in `app/routes/`
2. Define the endpoint and handlers
3. Register the route in `app/main.py`

#### Adding a New Client Feature

1. Create new components in `client/src/components/`
2. Add new pages in `client/src/pages/` if needed
3. Update API client in `client/src/lib/api.ts` if needed

## Troubleshooting

### Common Issues

#### Server Won't Start

- Check if the port is already in use
- Verify that all dependencies are installed
- Ensure the `.env` file is properly configured

#### Client Can't Connect to Server

- Verify the server is running
- Check CORS configuration in the server
- Ensure the API base URL is correct in the client

#### OpenAI API Errors

- Verify your API key is valid
- Check your OpenAI account has sufficient credits
- Ensure the model specified in `.env` is available to your account

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.







## Example API Usage

### Create a Custom Role

```bash
curl -X 'POST' \
  'http://localhost:8000/api/v1/roles' \
  -H 'Content-Type: application/json' \
  -d '{
  "id": "tech-writer",
  "name": "Technical Writer",
  "description": "Specializes in clear, concise technical documentation",
  "instructions": "Create documentation that is accessible to both technical and non-technical audiences",
  "domains": ["technical-writing", "documentation", "tutorials"],
  "tone": "technical",
  "system_prompt": "You are an experienced technical writer with expertise in creating clear, concise documentation for complex systems."
}'
```

### Process a Query

```bash
curl -X 'POST' \
  'http://localhost:8000/api/v1/roles/process' \
  -H 'Content-Type: application/json' \
  -d '{
  "role_id": "marketing-expert",
  "query": "How can I improve my social media engagement?",
  "custom_instructions": "Focus on B2B strategies"
}'
```

### Store a Memory

```bash
curl -X 'POST' \
  'http://localhost:8000/api/v1/memories' \
  -H 'Content-Type: application/json' \
  -d '{
  "role_id": "marketing-expert",
  "content": "The user prefers Instagram over TikTok for their business",
  "type": "user",
  "importance": "medium"
}'
```

## Docker Deployment

Build and run the container:

```bash
docker build -t role-specific-mcp .
docker run -p 8000:8000 --env-file .env role-specific-mcp
```

## Future Roadmap

### Core Platform Enhancements
- Vector database integration (ChromaDB, Supabase) for semantic memory retrieval
- Real-time context switching based on triggers
- Multi-modal context support
- Support for LangGraph agents and RAG pipelines
- Enhanced authentication and security features

### Advanced Memory Architecture
- Shared memory collections accessible across multiple AI agents
- Hierarchical memory access control system
- Role-based memory inheritance mechanisms
- Configurable memory sharing permissions
- Cross-role semantic search capabilities
- Memory embedding and similarity scoring
- Memory tagging and categorization system

---

## About

This documentation and software is authored by **IntelliSync Solutions**  
Written by: Chris June  
Last Updated: March 21, 2025

© 2025 IntelliSync Solutions. All rights reserved.
