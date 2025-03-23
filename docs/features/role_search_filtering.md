# Role Search and Filtering

## Overview

The Role Search and Filtering feature enhances the MCP server by providing powerful capabilities to search and filter roles based on various criteria. This allows users to quickly find the most appropriate AI advisor roles for their specific needs, improving the overall user experience and making the platform more accessible.

## Features

### Search Capabilities

- **Text-based Search**: Search for roles by keywords in their name, description, or instructions
- **Domain Filtering**: Filter roles by specific domains of expertise
- **Tone Filtering**: Filter roles by communication tone (analytical, strategic, creative, etc.)
- **Combined Filtering**: Apply multiple filters simultaneously for precise results

## API Endpoints

### Get Roles with Filtering

```http
GET /api/v1/roles?search=keyword&domains=domain1,domain2&tone=analytical
```

Retrieve all roles with optional filtering parameters.

**Query Parameters:**

- `search` (optional): Text to search in name, description, and instructions
- `domains` (optional, can be multiple): Domains to filter by
- `tone` (optional): Tone to filter by

**Response:**

```json
{
  "roles": [
    {
      "id": "finance-advisor",
      "name": "Finance Advisor",
      "description": "Provides financial advice and analysis",
      "instructions": "Analyze financial data and provide strategic advice",
      "domains": ["finance", "investment", "budgeting"],
      "tone": "analytical",
      "system_prompt": "You are a financial advisor with expertise in investment strategies.",
      "is_default": false
    }
  ]
}
```

### Dedicated Search Endpoint

```http
GET /api/v1/roles/search?query=keyword&domains=domain1,domain2&tone=analytical
```

Search for roles with a required query parameter and optional filters.

**Query Parameters:**

- `query` (required): Text to search in name, description, and instructions
- `domains` (optional, can be multiple): Domains to filter by
- `tone` (optional): Tone to filter by

**Response:** Same format as the Get Roles endpoint

### Get All Domains

```http
GET /api/v1/roles/domains
```

Retrieve all unique domains used across all roles.

**Response:**

```json
{
  "domains": ["finance", "investment", "marketing", "technology", "software"]
}
```

## Implementation Details

### Search Algorithm

The search functionality uses a case-insensitive text matching approach:

1. Converts the search query to lowercase
2. Checks if the query appears in the role's name, description, or instructions
3. Returns all roles that match the search criteria

### Domain Filtering

Domain filtering works by:

1. Checking if any of the role's domains match any of the requested domains
2. A role is included if it has at least one matching domain

### Tone Filtering

Tone filtering is exact matching against the role's tone attribute.

## Usage Examples

### Client-Side Search Implementation

```javascript
async function searchRoles() {
  const searchQuery = document.getElementById('searchInput').value;
  const selectedDomains = Array.from(document.querySelectorAll('.domain-checkbox:checked')).map(cb => cb.value);
  const selectedTone = document.querySelector('input[name="tone"]:checked')?.value;
  
  // Build query parameters
  const params = new URLSearchParams();
  if (searchQuery) params.append('query', searchQuery);
  selectedDomains.forEach(domain => params.append('domains', domain));
  if (selectedTone) params.append('tone', selectedTone);
  
  // Make API request
  const response = await fetch(`/api/v1/roles/search?${params.toString()}`);
  const data = await response.json();
  
  // Display results
  displayRoles(data.roles);
}
```

### Filtering UI Example

```html
<div class="search-container">
  <input type="text" id="searchInput" placeholder="Search roles..." />
  
  <div class="filter-section">
    <h3>Domains</h3>
    <div id="domainCheckboxes">
      <!-- Dynamically populated from /api/v1/roles/domains -->
    </div>
  </div>
  
  <div class="filter-section">
    <h3>Tone</h3>
    <div id="toneRadios">
      <!-- Dynamically populated from /api/v1/roles/tones -->
    </div>
  </div>
  
  <button onclick="searchRoles()">Search</button>
</div>

<div id="searchResults"></div>
```

## Best Practices

1. **Combine Search Methods**: For the best results, combine text search with domain and tone filtering
2. **Use the Domains Endpoint**: Dynamically populate domain filters using the `/roles/domains` endpoint
3. **Provide Clear UI**: Clearly indicate to users which filters are currently active
4. **Implement Instant Search**: Consider implementing real-time search as users type for a better experience

## Future Enhancements

1. **Fuzzy Search**: Implement fuzzy matching for more forgiving text searches
2. **Relevance Scoring**: Add relevance scores to search results
3. **Pagination**: Add pagination for large result sets
4. **Advanced Filtering**: Add more filtering options like creation date, popularity, etc.
5. **Search Analytics**: Track popular searches to improve role offerings
