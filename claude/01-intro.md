
CLAUDE.md is the main documentation file for the Claude project. It provides an overview of the project, its features, and how to use it.

In CLAUDE.md, you can also reference other markdown files using the @ symbol:

## Imports

```md
@docs/API_GUIDELINES.md
@~/.claude/snippets.md
```

## Prompts

Use XML Tags for Laser-Focused Prompts

```xml
<task>
  <instructions>
    Refactor `userController.js` to use async/await.
  </instructions>
  <format>
    Output only a unified diff.
  </format>
  <constraints>
    Do not change unrelated code.
  </constraints>
</task>
```

This structure helps Claude understand exactly what you want, how to deliver it, and any boundaries to respect.

## Memory for current feature to implement

Don't hesitate to add notes about the feature you're working on. This helps Claude stay focused and aligned with your goals.

For example:

    CLAUDE.md → Rules for how Claude should behave
    docs/PRD-title.md → The big picture (Product Requirement Document)
    docs/PLANNING.md → Your project’s architecture and stack
    docs/TASKS.md → A living checklist of what to build

Prompt: Read docs/PLANNING.md, and docs/TASKS.md to understand the project. Then complete the first task on docs/TASKS.md.
Add a session summary to CLAUDE.md summarizing what we’ve done so far.


Example CLAUDE.md

```
# Project: [Your Project Name]

## Architecture Overview
- Frontend: React with TypeScript
- Backend: Node.js with Express
- Database: PostgreSQL
- Deployment: Docker containers

## Development Guidelines
- Use functional components with hooks
- Follow ESLint configuration
- Write tests for all API endpoints
- Use semantic commit messages

## Key Files
- `/src/components/` - Reusable UI components
- `/src/api/` - API route handlers
- `/src/utils/` - Utility functions
```

## Global CLAUDE.md

Create ~/.claude/CLAUDE.md for personal preferences that apply across all projects:

```md
# Global Development Preferences

## Coding Standards
- Prefer TypeScript over JavaScript
- Use functional programming patterns
- Write comprehensive error handling
- Include unit tests for all functions

## Security Practices
- Always validate input parameters
- Use environment variables for secrets
- Implement proper authentication checks
- Follow OWASP security guidelines

## Documentation Standards
- Include JSDoc comments for all functions
- Maintain README files for each module
- Document API endpoints with examples
```
