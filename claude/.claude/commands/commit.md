Generate a git commit command for the actual changes. Use the conventional commit format: type(part): message
Format: git commit -m "<type>[optional scope]: <description>"

## Types

* feat: new feature
* fix: bug fix
* docs: documentation changes
* style: formatting, missing semicolons, etc.
* refactor: code restructuring without changing functionality
* test: adding or updating tests
* chore: maintenance tasks, dependency updates
* perf: performance improvements
* ci: CI/CD changes
* build: build system changes

## Optional Scope
The scope is the component, module, or area affected (e.g., auth, api, ui, database). It should be lowercase and without spaces.

## Message
The message should be in present tense, lowercase, no period, and under 50 characters.

Example: git commit -m "feat(auth): add oauth2 integration"


Now generate the commit command for the changes in the current git staging area. Ask the user the permission to commit the generated command before executing it.
