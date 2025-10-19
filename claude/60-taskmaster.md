

Install  TaskMaster AI

```bash
npm install -g task-master-ai
task-master init --rules claude
```

And then add the plugin to Claude MCP:

```bash
claude mcp add taskmaster-ai -- npx -y task-master-ai
```

Prompts:

```
Learn what this project is about and write a PRD (Product Requirements Document) about the functionality described: [insert functionality description here]
```

To parse a PRD document and generate tasks:

```bash
task-master parse-prd .taskmaster/docs/prd.txt
```

To expand tasks into subtasks for more granular implementation:

```bash
task-master analyze-complexity --research
task-master expand --all --research
```

To view the generated tasks:

```bash
task-master list
```

To see the next task to work on:
```bash
task-master next
```
