
Before using MCP servers, check the code or at least ensure you trust the source.

## List all configured servers
```bash
claude mcp list
```

## Get details for a specific server
```bash
claude mcp get my-server
```

## Remove a server
```bash
claude mcp remove my-server
```

## Add a new server with a specific command and environment variable

### github mcp server (stdio / need the binary installed)

```bash
# Github MCP server https://github.com/github/github-mcp-server
# Install https://github.com/github/github-mcp-server/blob/main/docs/installation-guides/install-claude.md
claude mcp add github -s user -- github-mcp-server stdio --env GITHUB_PERSONAL_ACCESS_TOKEN=$GITHUB_TOKEN # need local binary setup
```

### github mcp server (http / no need the binary installed)

```bash
claude mcp add --transport http github https://api.githubcopilot.com/mcp -H "Authorization: Bearer $GITHUB_TOKEN"
```

### taskmaster

```bash
# taskmaster: https://github.com/eyaltoledano/claude-task-master
claude mcp add taskmaster -s user -- npx -y @eyaltoledano/claude-task-master
```

### context7

```bash
# context7: https://github.com/upstash/context7
claude mcp add --transport http context7 https://api.context7.com
```

### gitlab-mcp (need env var GITLAB_TOKEN and binary installed)

```bash
# gitlab-mcp https://github.com/sgaunet/gitlab-mcp
claude mcp add gitlab-mcp -s user -- gitlab-mcp
```

### playwright-mcp-server

URL: https://github.com/microsoft/playwright-mcp
```bash
# playwright-mcp-server
claude mcp add playwright npx @playwright/mcp@latest
```

### postgresql-mcp

URL: https://github.com/sgaunet/postgresql-mcp
Install first with brew or from binary

```bash
# Make sense for local environment, so configure the agent in the project that needs it
claude mcp add -s project  --env "POSTGRES_URL=postgres://postgres:password@localhost:5432/postgres?sslmode=disable" --transport stdio postgresql postgresql-mcp
```

For MCP servers that execute requests on database, ensure the database user has read-only permissions to prevent unintended data modifications or that the server has this kind of option.

Another solution to get help from Claude about SQL is to use the tool tbls: https://github.com/k1LoW/tbls which can generate a markdown documentation of your database schema (and generate graph)

## tbls

```bash
tbls doc --rm-dist --dsn "postgresql://postgres:password@localhost:5432/postgres?sslmode=disable"
## will generate a dbdoc folder with documentation of your database
```


## List of useful MCP servers

Puppeteer-MCP: Enables LLMs to control and interact with web browsers using Puppeteer. This opens up possibilities for web scraping, automated testing, and generating web-based reports.

Jupyter-MCP: Could allow LLMs to interact with Jupyter notebooks, potentially executing code, analyzing results, or extracting insights from notebooks.

Jira-MCP: Enables LLMs to interact with Jira project management software. This could be used for retrieving issue details, tracking progress, or even creating new tickets.

## Resources

* https://mcpservers.org/
* https://github.com/wong2/awesome-mcp-servers
* https://github.com/brennercruvinel/CCPlugins/tree/main
* https://www.aitmpl.com/
* https://github.com/motherduckdb/mcp-server-motherduck
