
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


```bash
specify init --here --ai claude
```

```bash
specify check
```

To upgrade specify run:

```bash
uv tool install specify-cli --force --from git+https://github.com/github/spec-kit.git@vX.Y.Z
```

## Establish project principles

Launch your AI assistant in the project directory. Claude Code exposes spec-kit as `/speckit-*` slash commands; Codex CLI in skills mode uses `$speckit-*` instead.

Use the **`/speckit-constitution`** command to create your project's governing principles and development guidelines that will guide all subsequent development.

```bash
/speckit-constitution <constitution principles>
```

Example principles:

```
Prefer a simple, modular monolith over microservices unless there is a clear, documented need to split.

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

When in doubt, the assistant asks the end user somes questions to help to find the good solutions and should choose simpler designs, fewer dependencies, and more tests
```

### Constitution examples by project type

Below are compact, ready-to-paste constitutions tailored to the kinds of projects you build most often. Pick the one that matches and pass it to `/speckit-constitution`. Tune individual bullets to the project at hand.

#### Go CLI

```
**Scope**
- Single static binary, no runtime dependencies; cross-compile via goreleaser.
- Stay a tool, not a framework: one focused job per binary, composable via pipes.

**Code quality**
- `gofmt`, `go vet`, `staticcheck` clean; idiomatic Go (small interfaces, errors as values).
- Commands are thin wrappers (cobra or stdlib `flag`); business logic lives in plain packages with no CLI imports.
- Errors wrap with `fmt.Errorf("...: %w", err)`; the final user-facing message says what failed and how to fix it.

**UX**
- Stdout = data (machine-parseable, `--output=text|json`); stderr = humans (logs, errors, progress).
- Exit codes are meaningful and documented (`0` ok, `1` generic failure, `2` usage error, `≥10` domain-specific).
- Respect `NO_COLOR`, `--quiet`, `--verbose`; never assume a TTY when output is piped.
- Config precedence is documented: flags > env vars > config file > defaults.
- Destructive actions require `--yes` or an interactive confirmation; `--help` is complete and accurate.

**Reliability**
- Long-running operations honor `context.Context` and cancel cleanly on `SIGINT`/`SIGTERM`.
- All I/O has timeouts; retries are bounded with backoff.

**Testing & release**
- Unit tests cover argument parsing, exit codes, and stdout/stderr separation; integration tests invoke the built binary.
- Releases via `goreleaser` with checksums and SBOM; binaries reproducible.
```

#### Go HTTP/REST API

```
**Architecture**
- Standard library `net/http` plus a lightweight router (`chi` or similar); avoid heavyweight frameworks.
- Handlers are thin; business logic lives in domain packages decoupled from `http`, storage, and transport.
- Versioned routes (`/v1/...`); breaking changes bump the version — never silently mutate a released contract.

**Code quality**
- `gofmt`, `go vet`, `staticcheck` clean; idiomatic Go.
- Errors wrap with `%w`; no silent failures.

**API contract**
- Request validation at the boundary; structured error responses with stable codes (RFC 7807 `application/problem+json` or an equivalent in-house shape).
- Consistent resource naming, pagination, and filtering conventions across endpoints.
- Auth and authz enforced in middleware, not inside handlers.

**Reliability & observability**
- Every handler receives a `context.Context` carrying request ID, deadline, and cancellation; propagated to all I/O.
- Outbound calls (DB, HTTP, queues) have timeouts and bounded retries with backoff.
- Structured logging (`slog`) with request ID, route, status, latency; no secrets in logs.
- Prometheus metrics, `/healthz` and `/readyz` endpoints, OpenTelemetry tracing where available.

**Data**
- Migrations are versioned, idempotent, and reversible when feasible using a migration tool like `goose` or `migrate` or `dbmate`; applied automatically on startup with a lock to prevent concurrent runs.
- use sqlc for type-safe SQL queries; use query builders only when dynamic query generation is required.


**Testing & performance**
- Table-driven handler tests with `httptest`; integration tests run against a real database (Testcontainers / docker compose), not mocks.
- P95 latency targets documented per critical endpoint; load tests for the hot paths.
```

#### Bash script — Linux only

```
**Shape**
- Shebang `#!/usr/bin/env bash`; bash 4+ features (associative arrays, `mapfile`) are allowed.
- Strict mode at top: `set -Eeuo pipefail` and `IFS=$'\n\t'`.
- `main "$@"` pattern; no top-level side effects so the script is safe to `source` for testing.
- Functions for anything used twice; keep the script under ~300 lines or split into a small library.

**Quality**
- `shellcheck` clean — disabled warnings require an inline justifying comment.
- All variables quoted (`"$var"`, `"${arr[@]}"`); use `[[ ... ]]` over `[ ... ]`.

**UX**
- `--help` and `--version` flags; usage printed on bad invocation; meaningful, documented exit codes.
- Errors to stderr via a `log_err()` helper; success data to stdout; respect `--quiet` / `--verbose`.
- Long-running steps log progress with timestamps.

**Safety**
- Trap `ERR` and `EXIT` to clean up temp files (`mktemp -d`) and partial state.
- No `curl | bash` of remote scripts; pin URLs and verify checksums for anything downloaded.
- Destructive operations require `--yes` or an interactive confirmation.

**Testing**
- `bats` (or equivalent) covers the happy path and key failure modes; CI runs `shellcheck` plus the test suite on the target distro.
```

#### Bash script — Linux + macOS portable

```
**Shape**
- Shebang `#!/usr/bin/env bash`; target bash 3.2 (macOS default) — no associative arrays, no `mapfile`, no `${var^^}`. Gate on `BASH_VERSINFO` only if higher features are truly needed, and exit cleanly with an upgrade hint otherwise.
- Strict mode `set -Eeuo pipefail`; `main "$@"` pattern; no top-level side effects.

**Portability**
- Prefer POSIX utilities; when GNU and BSD diverge, detect OS once via `uname -s` (`Linux` vs `Darwin`) and branch at the lowest possible level.
- Known divergences to handle: `sed -i ''` (BSD) vs `sed -i` (GNU); `date -u -d` (GNU) vs `date -u -j -f` (BSD); `readlink -f`, `realpath`, GNU `getopt`, `stat`, `mktemp --tmpdir`, `grep -P` are all unsafe — implement portable shims.
- Probe every external tool with `command -v`; fail fast with an actionable message listing what is missing and how to install it per OS (`apt`, `brew`, …).
- Default install paths handle macOS `/opt/homebrew` and `/usr/local` as well as Linux `/usr/local` / `$XDG_*`.

**Quality**
- `shellcheck --shell=bash` clean.
- All variables quoted; `[[ ... ]]` is fine, but avoid `=~` regex differences between bash versions.

**UX & safety**
- `--help` and `--version`; meaningful exit codes; errors to stderr, data to stdout.
- Temp files via portable `mktemp` (no `--tmpdir`); cleaned up via `trap ... EXIT`.
- Document required tools and minimum versions (`bash`, `awk`, `sed`, `grep`, `curl`) in the script header.

**Testing**
- CI runs the script and `shellcheck` on `ubuntu-latest`; both must stay green before merge.
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
/speckit-plan The application uses Golang with minimal number of libraries. Use vanilla HTML, CSS, and JavaScript as much as possible. Images are not uploaded anywhere and metadata is stored in a local SQLite database.
```

### Break down into tasks

Use **`/speckit-tasks`** to create an actionable task list from your implementation plan.

```bash
/speckit-tasks
```

### Cross-artifact analysis (optional, recommended)

Use **`/speckit-analyze`** after `/speckit-tasks` and before `/speckit-implement` to run cross-artifact consistency and coverage analysis across the constitution, spec, plan, and tasks.

```bash
/speckit-analyze
```

### Execute implementation

Use **`/speckit-implement`** to execute all tasks and build your feature according to the plan.

```bash
/speckit-implement
```
