

https://github.com/Fission-AI/OpenSpec


commands for claude:

* /openspec:proposal
* /openspec:apply
* /openspec:archive


Install OpenSpec AI

```bash
npm install -g @fission-ai/openspec@latest
```

Initialize OpenSpec in your project

```bash
openspec init
```

Populate your project context:

```
"Please read openspec/project.md and help me fill it out with details about my project, tech stack, and conventions"
```

Create a new proposal:

```bash
/openspec:proposal Implement user authentication with JWT and OAuth2 support
```

Commands to manage your OpenSpec proposals:

```bash
$ openspec list                             # Confirm the change folder exists
$ openspec validate add-profile-filters     # Validate spec formatting
$ openspec show add-profile-filters         # Review proposal, tasks, and spec delta
```

To apply the proposal and generate tasks:

```bash
/openspec:apply add-profile-filters
```
