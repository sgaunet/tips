## hooks

Hooks can be configured to run at multiple key points (more than the list below here: https://docs.anthropic.com/en/docs/claude-code/hooks):

    PreToolUse — before tool execution
    PostToolUse — after successful tool completion
    Notification — when notifications are sent
    Stop — when Claude finishes responding

### Understanding the Four Hook Types

Now let’s break down each hook type.

#### PreToolUse Hooks

PreToolUse hooks run before Claude executes any tool. This is your quality control checkpoint.

These hooks are your first line of defense. They can validate inputs, check permissions, or completely block dangerous operations.

Use Cases

    Block edits to production configuration files
    Validate code syntax before Claude writes it
    Check if required dependencies exist
    Enforce naming conventions

When a PreToolUse hook exits with code 2, it stops Claude. The hook can send feedback directly to Claude about what went wrong, and Claude will adjust and try again.

#### PostToolUse Hooks

PostToolUse hooks run immediately after Claude completes a tool operation. This is where you can format code, run tests, and make documentation updates.

Use Cases

    Auto-format code with Prettier or Black
    Run relevant tests after file changes
    Generate documentation from code comments
    Log changes for compliance tracking

PostToolUse hooks can provide feedback to Claude about what just happened. If your tests fail, Claude can see the results and fix the issues.

#### Notification Hooks

Notification hooks trigger when Claude sends you notifications, such as asking for permission or reporting task completion.

Don’t like Claude’s default notifications-Replace them entirely.

Use Cases

    Send Slack messages to your team channel
    Email reports to the team
    Desktop notifications with custom styling
    Integration with monitoring systems

You can suppress Claude’s default notifications and implement your system that fits your workflow.
Stop Hooks

Stop hooks run when Claude finishes responding and is about to stop.

This can be used to trigger the next steps automatically.

Use Cases

    Automatically deploy after successful tests
    Trigger CI/CD pipelines
    Generate reports and summaries
    Start related tasks

Stop hooks can prevent Claude from stopping by returning the right exit code. This lets you build complex, multi-step workflows.

Now that we understand the different types of hooks, let's create our first hook.
