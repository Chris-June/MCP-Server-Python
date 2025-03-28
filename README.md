# MCP (Model Context Protocol) Server: Intelligent Conversational Platform

## Overview
MCP (Model Context Protocol) is a sophisticated AI-powered server designed to provide intelligent, context-aware conversational capabilities. This standalone server leverages multiple LLM providers (OpenAI, Anthropic, and Google Gemini), FastAPI, and Pyppeteer for web browsing capabilities to deliver nuanced, contextually relevant responses across various business domains.

**Note:** This repository contains only the MCP server implementation. While frontend examples are provided in the documentation for illustrative purposes, the actual frontend implementation is not included in this repository. The MCP server is designed to be integrated with any frontend through its RESTful API.

## Key Features
- 🤖 Role-based AI advisor system with customizable instructions and tones
- 🧠 Semantic memory management with vector similarity search
- 🌊 Real-time streaming responses for improved user experience
- 🌐 Integrated web browsing capabilities for AI-assisted research
- 🔄 Dynamic context switching based on conversation triggers
- 📝 Enhanced markdown formatting for professional-looking content
- 🖼️ Multi-modal context support for processing images and other media
- 🔍 Advanced role search and filtering by keywords, domains, and tone
- 🔗 Advanced memory features with tagging, sharing, and inheritance
- 🔄 Multiple LLM provider support (OpenAI, Anthropic, Google Gemini)

## Technology Stack
- **Backend**: Python with asyncio
- **Web Framework**: FastAPI
- **AI Models**: 
  - OpenAI GPT-4o-mini
  - Anthropic Claude models
  - Google Gemini models
- **Browser Automation**: Pyppeteer (Python port of Puppeteer)
- **API Documentation**: Swagger UI via FastAPI

## Setup and Installation

### Prerequisites
- Python 3.9+
- Node.js 18+ and npm
- OpenAI API key
- Git (for cloning the repository)

### Installation Steps
1. Clone the repository
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment: 
   - Windows: `venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Configure environment variables (see below)
6. Run the server: `python -m app.main`
7. Access the API documentation at `http://localhost:8000/docs`

## Configuration
Create a `.env` file based on `.env.example` with the following variables:

```
# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key
OPENAI_MODEL=gpt-4o-mini
OPENAI_VISION_MODEL=gpt-4o

# Anthropic Configuration (Optional)
ANTHROPIC_API_KEY=your_anthropic_api_key
ANTHROPIC_MODEL=claude-3-haiku-20240307

# Google Gemini Configuration (Optional)
GEMINI_API_KEY=your_gemini_api_key
GEMINI_MODEL=gemini-1.5-pro

# Default Provider Configuration
DEFAULT_PROVIDER=openai  # Options: openai, anthropic, gemini
EMBEDDING_MODEL=text-embedding-ada-002
```

## Recent Improvements

### Contextual Analysis for Specialized Domains
- Implemented domain-specific analysis capabilities for various business areas
- Created specialized analysis templates for finance, marketing, operations, sales, and more
- Added automatic extraction of domain-specific terminology and patterns
- Integrated domain-specific metrics and frameworks into AI responses
- Enhanced system prompts with domain-specific guidance
- Created API endpoints for domain analysis and template management
- Improved relevance and specificity of AI responses for specialized domains

### Advanced Memory Features
- Implemented memory tagging and categorization system for better organization
- Created hierarchical memory access control with role-based permissions
- Designed role-based memory inheritance mechanism for knowledge sharing
- Added configurable memory sharing permissions between roles
- Developed semantic search for cross-role memory retrieval
- Implemented memory embedding and similarity scoring for relevance ranking
- Added API endpoints for memory sharing and inheritance management
- Created comprehensive documentation for advanced memory features

### Role Search and Filtering
- Implemented advanced search capabilities for finding roles by keywords
- Added domain-based filtering to find roles with specific expertise
- Created tone-based filtering for communication style preferences
- Added API endpoints for role search with combined filtering options
- Implemented domain discovery endpoint to retrieve all unique domains
- Created comprehensive test suite for search and filtering functionality

### Multi-Modal Context Support
- Added support for processing images alongside text queries
- Implemented dedicated multi-modal processing service
- Created API endpoints for multi-modal content processing
- Added file upload capabilities for media content
- Integrated with vision-capable models across providers
- Added streaming support for multi-modal responses

### Multiple LLM Provider Support
- Implemented support for multiple LLM providers (OpenAI, Anthropic, Google Gemini)
- Created a modular provider architecture with a common interface
- Added provider-specific optimizations for each LLM service
- Implemented provider selection for all API endpoints

### Test Script Improvements
- Updated all test scripts to use the API prefix consistently across endpoints
- Enhanced test structure with proper skipping of unimplemented endpoints
- Improved test reliability by using consistent client fixtures
- Added comprehensive test coverage for role management, domain analysis, and memory features
- Implemented proper mocking for various services to isolate tests
- Fixed import errors and KeyError issues in test files
- Created dedicated provider routes for direct provider access
- Added fallback mechanisms for multi-modal content when primary provider lacks capabilities
- Implemented provider discovery endpoint to list available providers
- Updated configuration to support provider-specific settings

### Enhanced Formatting
- Added explicit formatting instructions to all prompts
- Standardized markdown formatting across different content types
- Improved client-side rendering of formatted content
- Enhanced CSS styling for better readability

### Streaming Functionality
- Implemented real-time streaming of AI responses
- Added visual indicators for streaming state
- Fixed string literal issues in SSE handling
- Improved UI to show different loading states

### Comprehensive Test Suite
- Created feature-specific test scripts for all major components
- Implemented tests for context switching functionality
- Added tests for memory features including tagging and retrieval
- Created tests for web browsing capabilities with mocked responses
- Implemented tests for multiple LLM provider integration
- Added tests for domain analysis capabilities
- Created tests for role editing and management features
- Implemented tests for role search and filtering
- Added tests for multimodal content processing
- Created comprehensive test documentation with usage instructions

## Development
- Use `requirements.txt` for server dependency management
- Use `package.json` for client dependencies
- Update `todo.txt` with new features and improvements after each iteration
- Update README.md after each new feature implementation

## Documentation
Detailed documentation is available in the `docs` directory:
- `ROUTES.md`: API endpoints and their functionality
- `MODELS.md`: Data structures and schemas
- `ARCHITECTURE.md`: System design and component interactions
- `SERVICES.md`: Core business logic implementation
- `SERVER_CAPABILITIES.md`: Features and capabilities
- `multimodal_context_support.md`: Multi-modal processing capabilities
- `role_search_filtering.md`: Role search and filtering functionality
- `role_editing.md`: Role management and editing features
- `CONTEXT_SWITCHING.md`: Dynamic context switching between roles
- `advanced_memory_features.md`: Advanced memory features including tagging, sharing, and inheritance

## Contributing
Please read CONTRIBUTING.md for details on our code of conduct and the process for submitting pull requests.

## License
[Specify License]

## Contact
[Your Contact Information]

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
- **Web Browsing Capability**: Integrated web browser for AI-assisted research and information gathering
- **Multi-Modal Analysis**: Process and analyze images alongside text for richer context

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

4. Install web browser dependencies:

```bash
pip install -r requirements-browser.txt
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
- `POST /api/v1/roles/process-stream` - Process a query with streaming response

#### Domain Analysis

- `GET /api/v1/domain-analysis/domains` - Get all available domain templates
- `GET /api/v1/domain-analysis/domains/{domain}` - Get a specific domain template
- `POST /api/v1/domain-analysis/analyze` - Analyze content based on role domains

#### Multi-Modal Processing

- `POST /api/v1/multimodal/process` - Process multi-modal content (text + images)
- `POST /api/v1/multimodal/process-stream` - Process multi-modal content with streaming response

#### LLM Provider Management

- `GET /api/v1/providers` - List all available LLM providers
- `GET /api/v1/providers/{provider_id}` - Get details for a specific provider
- `POST /api/v1/providers/{provider_id}/process` - Process a query with a specific provider

#### Context Switching

- `POST /api/v1/context/session` - Create a new context switching session
- `POST /api/v1/context/process` - Process a query with context switching
- `POST /api/v1/context/process-stream` - Process a query with context switching and streaming response
- `POST /api/v1/context/switch` - Manually switch context to a different role
- `GET /api/v1/context/sessions/{session_id}` - Get information about a session
- `GET /api/v1/context/sessions/{session_id}/history` - Get context switch history for a session
- `DELETE /api/v1/context/sessions/{session_id}` - Close a session

#### Web Browser

- `POST /api/v1/browser/sessions` - Create a new browser session
- `DELETE /api/v1/browser/sessions/{session_id}` - Close a browser session
- `POST /api/v1/browser/sessions/{session_id}/navigate` - Navigate to a URL
- `GET /api/v1/browser/sessions/{session_id}/content` - Get the current page content
- `POST /api/v1/browser/sessions/{session_id}/screenshot` - Take a screenshot of the page
- `POST /api/v1/browser/sessions/{session_id}/click` - Click an element on the page
- `POST /api/v1/browser/sessions/{session_id}/fill` - Fill out an input field
- `POST /api/v1/browser/sessions/{session_id}/evaluate` - Execute JavaScript in the browser
- `GET /api/v1/browser/sessions/{session_id}/history` - Get browsing history

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

### Web Browsing

The platform includes an integrated web browsing capability that allows AI advisors to access and interact with web content. This feature enables advisors to perform research, gather information, and provide more contextually relevant responses based on up-to-date information from the web.

#### Web Browsing Features

- **Browser Session Management**: Create and manage browser sessions for web research
- **Web Navigation**: Browse websites and follow links to gather information
- **Content Extraction**: Extract and analyze web page content with multiple extraction modes:
  - **Auto**: Intelligently extracts main content
  - **Article**: Focuses on article content for news and blog sites
  - **Full**: Retrieves the complete page content
  - **Structured**: Extracts structured data (headings, links, images, forms, etc.)
- **Screenshot Capture**: Take screenshots of web pages for reference
- **Interactive Elements**: Click buttons, fill forms, and interact with web content
- **JavaScript Execution**: Run custom scripts for advanced web interactions
- **Form Filling**: Automatically fill out forms with specified values
- **Mock Sessions**: Fallback mechanism when browser initialization fails
- **Session History**: Track and retrieve browsing history for each session
- **Interactive Tooltips**: Helpful tooltips explaining how to use browser features
- **Command Reference**: Clear documentation of special commands for browser interaction

#### Using Web Browsing

You can use web browsing in two ways:

1. **Through the Web Browser Interface**: Access the browser interface from the role detail page by clicking the "Show Browser" button in the Web Research section.
   - Navigate to websites using the URL bar
   - View page content in the browser panel
   - Take screenshots for reference
   - Interact with web elements through the interface

2. **Using Special Commands in Queries**: Include special commands in your queries to the AI advisor:
   - `[SEARCH_WEB:query]` - Search the web for information (uses DuckDuckGo)
   - `[BROWSE_URL:https://example.com]` - Browse a specific URL with optional extraction mode
   - `[BROWSE_URL:https://example.com:auto|article|full|structured]` - Browse with specific extraction mode
   - `[CLICK_ELEMENT:#submit-button]` - Click an element on the current page
   - `[EXTRACT_ELEMENT:.product-info]` - Extract text from specific elements
   - `[FILL_FORM:#email=user@example.com,#password=secret]` - Fill out a form

Example queries:
- "What are the latest small business tax deductions [SEARCH_WEB:small business tax deductions 2025]?"
- "Analyze this article [BROWSE_URL:https://example.com/article:article]"
- "Extract product information [BROWSE_URL:https://store.com/product:structured]"
- "Log into my account [FILL_FORM:#email=user@example.com,#password=secret] and then [CLICK_ELEMENT:#login-button]"

The browser interface includes helpful tooltips that explain these commands and how to use them effectively. Hover over the information icons (ℹ️) next to feature names to see detailed explanations.

#### API Endpoints

The following API endpoints are available for web browsing:

- **POST /api/browser/sessions** - Create a new browser session
- **DELETE /api/browser/sessions/{session_id}** - Close a browser session
- **POST /api/browser/sessions/{session_id}/navigate** - Navigate to a URL
- **GET /api/browser/sessions/{session_id}/content** - Get the current page content
- **POST /api/browser/sessions/{session_id}/screenshot** - Take a screenshot
- **POST /api/browser/sessions/{session_id}/click** - Click an element on the page
- **POST /api/browser/sessions/{session_id}/fill** - Fill out an input field
- **POST /api/browser/sessions/{session_id}/evaluate** - Execute JavaScript in the browser
- **GET /api/browser/sessions/{session_id}/history** - Get the browsing history

#### Implementation Details

The web browsing capability is implemented using:

- **Pyppeteer**: A Python port of Puppeteer for browser automation
- **Headless Chrome**: For browser rendering and interaction
- **FastAPI**: For RESTful API endpoints
- **React Components**: For frontend browser interface

#### Browser Integration with AI

The browser service is integrated with the AI processor through the `BrowserIntegration` class, which:

1. Maps role IDs to browser sessions
2. Processes special commands in user queries
3. Extracts relevant information from web pages using multiple extraction modes
4. Supports structured data extraction for better information organization
5. Enables interactive web page manipulation through element selection and form filling
6. Incorporates web content into AI responses with appropriate formatting

This integration allows AI advisors to seamlessly incorporate web information into their responses, providing more accurate and up-to-date advice based on current information available on the web.

#### Example Use Cases

- **Market Research**: Research industry trends and competitor analysis
- **Financial Guidance**: Look up current tax regulations or financial strategies
- **Technical Support**: Find documentation or troubleshooting guides
- **Legal Advice**: Research relevant laws and regulations
- **Marketing Strategy**: Analyze current marketing trends and best practices

```
POST /api/v1/browser/sessions - Create a new browser session
DELETE /api/v1/browser/sessions/{session_id} - Close a browser session
POST /api/v1/browser/sessions/{session_id}/navigate - Navigate to a URL
POST /api/v1/browser/sessions/{session_id}/screenshot - Take a screenshot
POST /api/v1/browser/sessions/{session_id}/click - Click an element
POST /api/v1/browser/sessions/{session_id}/fill - Fill an input field
POST /api/v1/browser/sessions/{session_id}/evaluate - Execute JavaScript
GET /api/v1/browser/sessions/{session_id}/history - Get browsing history
```

For more detailed information, refer to the [Web Browsing Documentation](docs/web_browsing.md).

### Context Switching

The context switching feature allows the AI to dynamically adapt to different roles based on the content of user queries, providing a more natural and seamless conversation experience.

#### How It Works

1. **Trigger Detection**: The system analyzes user queries for specific patterns that indicate a particular domain or expertise would be more appropriate.
2. **Role Matching**: Based on detected triggers, the system determines the best role to handle the query.
3. **Context Transition**: When switching roles, the system provides context about the transition to maintain conversation coherence.
4. **Session Management**: The system maintains session history across role transitions for a continuous experience.

#### Key Components

- **TriggerService**: Detects triggers in user queries and determines the most appropriate role
- **ContextSwitchingService**: Manages sessions and handles the process of switching between roles
- **Domain-specific Trigger Patterns**: Pre-configured patterns for common domains like finance, technology, healthcare, etc.

#### API Endpoints

The following API endpoints are available for context switching:

- **POST /api/context/sessions** - Create a new session with an initial role
- **GET /api/context/sessions/{session_id}** - Get session information
- **DELETE /api/context/sessions/{session_id}** - Close a session
- **POST /api/context/process** - Process a query with context switching
- **POST /api/context/process/stream** - Process a query with context switching and streaming response
- **POST /api/context/switch** - Manually switch context to a different role
- **GET /api/context/sessions/{session_id}/history** - Get context switch history

#### Example Use Case

Imagine a conversation that starts with technical questions but then shifts to financial considerations:

1. User asks about software implementation (handled by Technical Support role)
2. User then asks about cost implications (system detects financial triggers)
3. System automatically switches to Financial Advisor role
4. AI responds with financial expertise while maintaining conversation context
5. User receives seamless expertise across domains without manually switching roles

#### Benefits

- **Natural Conversations**: Users can freely change topics without explicitly switching roles
- **Specialized Expertise**: Each query is handled by the most appropriate role
- **Contextual Continuity**: Conversation history is maintained across role transitions
- **Improved User Experience**: Reduces friction in multi-domain conversations

For more detailed information, refer to the [Context Switching Documentation](docs/CONTEXT_SWITCHING.md).

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

#### CFO Advisor Conversation

**User**: Our small business is growing rapidly, but our cash flow is becoming a problem. How should we manage this?

**AI**: This is a common challenge for growing businesses. Let me provide some strategic guidance on managing your cash flow:

**Short-term Actions:**
* **Implement cash flow forecasting** - Create a 13-week rolling forecast to anticipate cash gaps
* **Optimize accounts receivable** - Consider offering early payment discounts and streamline your invoicing process
* **Review payment terms** - Negotiate longer payment terms with suppliers while shortening terms for customers

**Medium-term Strategies:**
* **Evaluate inventory management** - Identify slow-moving inventory and optimize order quantities
* **Consider financing options** - Explore lines of credit, invoice factoring, or equipment financing
* **Implement KPI tracking** - Monitor cash conversion cycle, days sales outstanding, and inventory turnover

**Long-term Planning:**
* **Develop a capital structure strategy** - Balance debt and equity to support growth while managing risk
* **Consider strategic pricing reviews** - Ensure your pricing strategy supports healthy margins

Would you like me to elaborate on any of these strategies or discuss specific financing options for your situation?

#### CMO Advisor Conversation

**User**: We need to increase our market share but have a limited marketing budget. What approach would you recommend?

**AI**: I understand the challenge of maximizing market impact with budget constraints. Here's a strategic approach:

**Market Analysis & Targeting:**
1. **Customer Segmentation**
   * Identify your most profitable customer segments
   * Focus resources on high-potential segments with lower acquisition costs
   * Develop detailed personas to guide messaging

2. **Competitive Positioning**
   * Identify underserved niches where you can establish dominance
   * Emphasize your unique value proposition in all communications
   * Consider a blue ocean strategy to create uncontested market space

3. **Digital Marketing Optimization**
   * Implement data-driven channel selection based on CAC and ROAS metrics
   * Leverage marketing automation to improve efficiency
   * Develop a content strategy focused on conversion, not just awareness

4. **Strategic Partnerships**
   * Identify complementary businesses for co-marketing opportunities
   * Consider channel partnerships to extend reach without additional spend

Would you like me to develop a more detailed plan for any of these areas or discuss specific digital marketing tactics that offer the best ROI for small businesses?

#### CEO Advisor Conversation

**User**: We're considering expanding into a new market. What strategic approach would you recommend for evaluating this opportunity?

**AI**: Expanding into new markets is a significant decision that requires careful strategic analysis. Here's a structured approach I recommend:

**Market Opportunity Assessment:**
1. **Market Size & Growth Analysis**
   * Evaluate the total addressable market (TAM) and serviceable obtainable market (SOM)
   * Analyze historical growth rates and future projections
   * Identify market trends and potential disruptors

2. **Competitive Landscape**
   * Map existing competitors and their market share
   * Assess barriers to entry and potential competitive advantages
   * Identify potential strategic partners or acquisition targets

**Internal Capability Evaluation:**
1. **Resource Requirements**
   * Estimate capital investment needed for market entry
   * Assess talent and operational capabilities required
   * Evaluate technology and infrastructure needs

2. **Risk Assessment**
   * Identify regulatory and compliance considerations
   * Evaluate potential impact on existing business operations
   * Develop contingency plans for various scenarios

Would you like me to help you develop a specific market entry strategy or discuss how to prioritize between multiple market opportunities?

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
Last Updated: March 23, 2025

&copy; 2025 IntelliSync Solutions. All rights reserved.
