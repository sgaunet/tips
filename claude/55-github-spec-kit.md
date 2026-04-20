
## Install

Install a pinned stable release (recommended — replace `vX.Y.Z` with the latest tag):

```bash
uv tool install specify-cli --from git+https://github.com/github/spec-kit.git@vX.Y.Z
```

Or install the latest from `main` (may include unreleased changes):

```bash
uv tool install specify-cli --from git+https://github.com/github/spec-kit.git
```

Then use the tool directly:

```bash
specify version
specify init <PROJECT_NAME>
# Or initialize in the current directory
specify init . --ai copilot
specify init --here --ai copilot
specify check
```

One-time usage without installing:

```bash
uvx --from git+https://github.com/github/spec-kit.git@vX.Y.Z specify init <PROJECT_NAME>
```

To upgrade specify run:

```bash
uv tool install specify-cli --force --from git+https://github.com/github/spec-kit.git@vX.Y.Z
```

## Establish project principles

Launch your AI assistant in the project directory. Claude Code exposes spec-kit as `/speckit-*` slash commands; Codex CLI in skills mode uses `$speckit-*` instead.

Use the **`/speckit-constitution`** command to create your project's governing principles and development guidelines that will guide all subsequent development.

```bash
/speckit-constitution Prefer a simple, modular monolith over microservices unless there is a clear, documented need to split.

Keep the dependency graph shallow; avoid unnecessary frameworks and heavy abstraction layers.

Configuration is explicit and typed (no magical globals); environment-driven config is centralized in one package.

Public APIs and packages must have stable, versioned contracts; breaking changes require a migration note except for V0 or if the application has not been released.
Code quality

All Go code must follow gofmt, go vet, and idiomatic Go best practices.

Business logic must live in plain Go packages, decoupled from transport (HTTP/CLI/GRPC) and storage details.

No package should exceed a small, focused responsibility; prefer splitting cohesive subpackages over “god” packages.

Error handling must be explicit and contextualized; no silent failures or swallowed errors.
Testing standards

Every non-trivial function or method must have unit tests that cover both happy path and failure modes.

New behavior requires tests first or at the same time (TDD or at least test-complete for every change).

Table-driven tests are preferred for input/output heavy logic; avoid mocking where simple in‑memory fakes or real components are feasible.

Aim for high coverage on core business logic; critical paths (validation, auth, billing, data integrity) must have near-complete coverage.

CI must run go test ./... and fail on test flakiness or race detector issues.
User experience consistency

APIs must be predictable and consistent: stable resource naming, clear error codes, and machine-readable error responses.

Every user-visible error (CLI or HTTP) must be actionable: say what went wrong and how to fix it.

Default behaviors are safe and unsurprising; destructive actions require explicit confirmation or clearly documented flags.

Inputs are validated at the boundary, with clear messages and consistent HTTP status codes or CLI exit codes.
Performance and reliability

Prefer simple algorithms and data structures with known complexity; optimize only when a measurable bottleneck is demonstrated.

For HTTP APIs, target sub-200ms P95 latency for core operations under expected load; document any exceptions.

All I/O and network calls must have timeouts and sensible retries where appropriate.

Logging and metrics should be cheap and structured; they must not materially degrade performance.
Governance for AI-generated changes

The AI assistant must preserve these principles when generating specs, plans, and code.

Any suggestion that violates these principles (e.g., unnecessary microservices, over-engineered patterns, lack of tests) must be revised to comply.

When in doubt, the assistant should choose simpler designs, fewer dependencies, and more tests
```

### Create the spec

Use the **`/speckit-specify`** command to describe what you want to build. Focus on the **what** and **why**, not the tech stack.

```bash
/speckit-specify Build an application that can help me organize my photos in separate photo albums. Albums are grouped by date and can be re-organized by dragging and dropping on the main page. Albums are never in other nested albums. Within each album, photos are previewed in a tile-like interface.
```

### Clarify underspecified areas (optional, recommended)

Use **`/speckit-clarify`** before `/speckit-plan` for structured, coverage-based questioning that records answers in a Clarifications section of the spec (formerly `/quizme`).

```bash
/speckit-clarify
```

### Create a technical implementation plan

Use the **`/speckit-plan`** command to provide your tech stack and architecture choices.

```bash
/speckit-plan The application uses Vite with minimal number of libraries. Use vanilla HTML, CSS, and JavaScript as much as possible. Images are not uploaded anywhere and metadata is stored in a local SQLite database.
```

### Break down into tasks

Use **`/speckit-tasks`** to create an actionable task list from your implementation plan.

```bash
/speckit-tasks
```

### Generate quality checklists (optional)

Use **`/speckit-checklist`** to generate custom quality checklists that validate requirements completeness, clarity, and consistency ("unit tests for English").

```bash
/speckit-checklist
```

### Cross-artifact analysis (optional, recommended)

Use **`/speckit-analyze`** after `/speckit-tasks` and before `/speckit-implement` to run cross-artifact consistency and coverage analysis across the constitution, spec, plan, and tasks.

```bash
/speckit-analyze
```

### Convert tasks to GitHub issues (optional)

Use **`/speckit-taskstoissues`** to turn the generated task list into GitHub issues for tracking and execution.

```bash
/speckit-taskstoissues
```

### Execute implementation

Use **`/speckit-implement`** to execute all tasks and build your feature according to the plan.

```bash
/speckit-implement
```
