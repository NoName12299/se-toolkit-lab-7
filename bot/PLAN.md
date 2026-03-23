# Development Plan for Telegram Bot

## Project Overview
This document outlines the development plan for a Telegram bot that integrates with the LMS backend. The bot will allow users to interact with the learning management system through natural language, check system health, browse labs, view scores, and ask questions in plain language.

## Architecture Design
The bot follows a clean separation of concerns:
- **Handler Layer**: Pure functions that process commands and return responses. These functions have no knowledge of Telegram, making them testable.
- **Service Layer**: API clients for backend communication and LLM integration.
- **Entry Point**: `bot.py` with `--test` mode for offline verification.

## Task Breakdown

### Task 1: Plan and Scaffold (Current)
- Create project structure with bot/ directory
- Set up pyproject.toml with core dependencies
- Implement --test mode for offline testing
- Create placeholder handlers for all required commands
- Establish environment file template

### Task 2: Backend Integration
- Implement real HTTP requests to LMS backend
- Add error handling for network failures
- Format backend responses for Telegram users
- Support all P0 slash commands with real data

### Task 3: Intent-Based Routing
- Integrate Qwen Code API for natural language understanding
- Wrap all 9 backend endpoints as LLM tools
- Implement multi-step reasoning capabilities
- Handle plain text queries intelligently

### Task 4: Containerization
- Create Dockerfile for the bot
- Add bot service to docker-compose.yml
- Document deployment procedure in README

## Development Workflow
1. Create feature branch for each task
2. Develop and test locally with --test mode
3. Deploy to VM for Telegram testing
4. Create pull request for review
5. Merge after partner approval

## Testing Strategy
- **Unit Tests**: Test handlers in isolation
- **Integration Tests**: Test with actual backend using --test mode
- **Acceptance Tests**: Autochecker will verify all required commands
- **Manual Testing**: Interact with bot in Telegram

## Key Decisions
- Using python-telegram-bot v20+ for async support
- httpx for efficient HTTP requests
- pydantic-settings for type-safe configuration
- uv for fast dependency management
