# MCP Server Test Suite

This directory contains automated tests for the MCP (Multi-Context Processing) Server. The tests are organized by feature and use pytest as the testing framework.

## Test Structure

The test suite is organized into feature-specific test files:

- `test_context_switching.py` - Tests for context switching functionality
- `test_domain_analysis.py` - Tests for domain analysis capabilities
- `test_llm_providers.py` - Tests for multiple LLM provider integration
- `test_memory_features.py` - Tests for advanced memory features
- `test_multimodal.py` - Tests for multimodal content processing
- `test_role_editing.py` - Tests for role creation and editing
- `test_role_search.py` - Tests for role search and filtering
- `test_web_browsing.py` - Tests for web browsing capabilities

## Prerequisites

Before running the tests, ensure you have the following dependencies installed:

```bash
pip install pytest pytest-asyncio fastapi httpx anthropic openai
```

## Running Tests

### Run all tests

```bash
python -m pytest
```

### Run tests for a specific feature

```bash
python -m pytest test_memory_features.py
```

### Run tests with verbose output

```bash
python -m pytest -v
```

### Run tests with coverage report

```bash
pip install pytest-cov
python -m pytest --cov=app
```

## Test Environment

The tests use FastAPI's `TestClient` to simulate HTTP requests without actually starting a server. Most external dependencies (like LLM providers) are mocked to avoid making actual API calls during testing.

## Adding New Tests

When adding new features to the MCP Server, please follow these guidelines for creating tests:

1. Create a new test file named `test_feature_name.py`
2. Use the existing test files as templates for structure
3. Include tests for all API endpoints related to the feature
4. Mock external dependencies when appropriate
5. Include both positive and negative test cases

## Continuous Integration

These tests are designed to be run as part of a CI/CD pipeline. They should be fast, reliable, and not depend on external services or specific environment configurations.
