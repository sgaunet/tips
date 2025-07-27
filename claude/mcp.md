

# List all configured servers
```bash
claude mcp list
```

# Get details for a specific server
```bash
claude mcp get my-server
```

# Remove a server
```bash
claude mcp remove my-server
```


# Add a new server with a specific command and environment variable

```bash
claude mcp add github-server -s user -- npx -y @modelcontextprotocol/server-github
```
