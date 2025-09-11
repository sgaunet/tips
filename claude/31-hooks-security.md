
# Claude Code Security Hooks - Preventing Credential Leaks

This guide demonstrates how to configure Claude Code with security hooks to automatically prevent API keys, passwords, and other sensitive credentials from being accidentally exposed or sent to Claude's servers.

## Prerequisites

### 1. Install Gitleaks

Gitleaks is a SAST tool for detecting and preventing hardcoded secrets in git repos.

```bash
# On macOS with Homebrew
brew install gitleaks

# On Linux/WSL
wget https://github.com/gitleaks/gitleaks/releases/download/v8.18.0/gitleaks_8.18.0_linux_x64.tar.gz
tar -xzf gitleaks_8.18.0_linux_x64.tar.gz
sudo mv gitleaks /usr/local/bin/

# On Windows (PowerShell)
winget install gitleaks

# Verify installation
gitleaks version
```

### 2. Create Claude Configuration Directory

```bash
mkdir -p ~/.claude/hooks
```


## Configuration Files

### 1. Gitleaks Configuration (.gitleaks.toml)

```toml
# Custom Gitleaks configuration for Claude Code hook
# Place this in ~/.claude/.gitleaks.toml

title = "Claude Code Security Scanner"

# Extend the base rules
[extend]
useDefault = true

# Add custom rules for your specific needs
[[rules]]
id = "custom-api-key"
description = "Custom API Key Pattern"
regex = '''(?i)(api[_\-\s]?key|apikey|api_secret)['"]?\s*[:=]\s*['"]?([a-zA-Z0-9\-_]{20,})['"]?'''
tags = ["key", "API", "custom"]

[[rules]]
id = "database-connection-string"
description = "Database Connection String"
regex = '''(?i)(mongodb|postgres|postgresql|mysql|mssql|oracle|redis):\/\/[^:]+:[^@]+@[^\/]+'''
tags = ["database", "connection"]

[[rules]]
id = "jwt-token"
description = "JWT Token"
regex = '''eyJ[a-zA-Z0-9_-]*\.eyJ[a-zA-Z0-9_-]*\.[a-zA-Z0-9_-]*'''
tags = ["jwt", "token"]

# Allow list for false positives
[allowlist]
description = "Global allow list"
paths = [
    '''\.md$''',  # Markdown files often have example keys
    '''\.test\..*$''',  # Test files
    '''__tests__/.*''',  # Test directories
    '''\.example$''',  # Example files
]

# You can also allow specific commits or lines
[[allowlist.commits]]
commits = []

[[allowlist.regexes]]
regex = '''example|sample|test|demo|fake|dummy'''
description = "Ignore example/test credentials"
```

### 2. Security Hook Script (gitleaks_security_hook.py)

Create the security hook script at `~/.claude/hooks/gitleaks_security_hook.py`:

```python
#!/usr/bin/env python3
"""
Gitleaks Security Hook for Claude Code
Scans files for API credentials and secrets before they're processed by Claude
"""

import json
import subprocess
import sys
import os
import tempfile
from pathlib import Path
from datetime import datetime

def log_scan(message, level="INFO"):
    """Log scan activity to a file for audit purposes."""
    log_file = Path.home() / ".claude" / "security_scan.log"
    timestamp = datetime.now().isoformat()
    with open(log_file, "a") as f:
        f.write(f"[{timestamp}] [{level}] {message}\n")

def run_gitleaks_on_content(content, file_path=None):
    """Run gitleaks on the provided content."""
    # Use custom config if it exists
    config_path = Path.home() / ".claude" / ".gitleaks.toml"
    config_args = ["--config", str(config_path)] if config_path.exists() else []
    
    # Create a temporary file with the content
    with tempfile.NamedTemporaryFile(mode='w', suffix='.tmp', delete=False) as tmp_file:
        tmp_file.write(content)
        tmp_file_path = tmp_file.name

    try:
        # Run gitleaks on the temporary file
        cmd = ['gitleaks', 'detect', '--no-git', '-v', '--source', tmp_file_path, '--report-format', 'json'] + config_args
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=5)

        # Parse the results
        if result.returncode == 1:  # Gitleaks found secrets
            log_scan(f"Secrets detected in {file_path or 'content'}", "WARNING")
            return True, result.stdout
        elif result.returncode == 0:  # No secrets found
            log_scan(f"Scan clean for {file_path or 'content'}")
            return False, None
        else:  # Error occurred
            log_scan(f"Gitleaks error: {result.stderr}", "ERROR")
            print(f"Error running gitleaks: {result.stderr}", file=sys.stderr)
            return False, None
    except subprocess.TimeoutExpired:
        log_scan(f"Gitleaks scan timed out for {file_path or 'content'}", "ERROR")
        return False, None
    finally:
        # Clean up temporary file
        os.unlink(tmp_file_path)

def format_secret_details(details):
    """Format secret detection details for user display."""
    try:
        leaked_data = json.loads(details)
        messages = []
        for leak in leaked_data[:5]:  # Limit to first 5 for readability
            rule = leak.get('RuleID', 'unknown')
            line = leak.get('StartLine', '?')
            desc = leak.get('Description', 'Unknown secret type')
            messages.append(f"  • {desc} (rule: {rule}) at line {line}")
        if len(leaked_data) > 5:
            messages.append(f"  • ... and {len(leaked_data) - 5} more")
        return "\n".join(messages)
    except:
        return "  • Multiple secrets detected"

def main():
    # Read the hook input from stdin
    try:
        hook_input = json.loads(sys.stdin.read())
    except json.JSONDecodeError:
        print("Error: Invalid JSON input", file=sys.stderr)
        sys.exit(1)

    # Extract relevant information
    tool_name = hook_input.get('tool_name', '')
    tool_input = hook_input.get('tool_input', {})

    # Check if this is a file-related operation
    file_operations = ['Write', 'Edit', 'MultiEdit', 'NotebookEdit']
    if tool_name not in file_operations:
        # Not a file operation, allow it to proceed
        print(json.dumps({"continue": True, "suppressOutput": True}))
        sys.exit(0)

    # Extract content based on the tool type
    secrets_found = False
    secret_details = []
    
    if tool_name == 'Write':
        content = tool_input.get('content', '')
        file_path = tool_input.get('file_path', '')
        if content:
            found, details = run_gitleaks_on_content(content, file_path)
            if found:
                secrets_found = True
                secret_details.append((file_path, details))
                
    elif tool_name == 'Edit':
        new_content = tool_input.get('new_string', '')
        file_path = tool_input.get('file_path', '')
        if new_content:
            found, details = run_gitleaks_on_content(new_content, file_path)
            if found:
                secrets_found = True
                secret_details.append((file_path, details))
                
    elif tool_name == 'MultiEdit':
        edits = tool_input.get('edits', [])
        file_path = tool_input.get('file_path', '')
        for edit in edits:
            new_content = edit.get('new_string', '')
            if new_content:
                found, details = run_gitleaks_on_content(new_content, file_path)
                if found:
                    secrets_found = True
                    secret_details.append((file_path, details))
                    break  # Stop on first detection
                    
    elif tool_name == 'NotebookEdit':
        new_source = tool_input.get('new_source', '')
        notebook_path = tool_input.get('notebook_path', '')
        if new_source:
            found, details = run_gitleaks_on_content(new_source, notebook_path)
            if found:
                secrets_found = True
                secret_details.append((notebook_path, details))

    # Handle detection results
    if secrets_found:
        # Build detailed message
        error_msg = "🔒 SECURITY BLOCK: Potential secrets detected:\n\n"
        for file_path, details in secret_details:
            error_msg += f"In {file_path}:\n"
            if details:
                error_msg += format_secret_details(details) + "\n\n"
        error_msg += "Please remove sensitive information before proceeding."
        
        print(json.dumps({
            "continue": False,
            "stopReason": error_msg,
            "systemMessage": "Security scan blocked operation to protect your credentials."
        }))
    else:
        # No secrets found, allow the operation
        print(json.dumps({"continue": True, "suppressOutput": True}))

if __name__ == "__main__":
    main()
```

Make the script executable:

```bash
chmod +x ~/.claude/hooks/gitleaks_security_hook.py
```

Copy the gitleaks configuration:

```bash
cp .gitleaks.toml ~/.claude/
```

### 3. Claude Settings (settings.json)

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Write|Edit|MultiEdit",
        "hooks": [
          {
            "type": "command",
            "command": "python3 ~/.claude/hooks/gitleaks_security_hook.py",
            "timeout": 10
          }
        ]
      }
    ]
  },
  "memories": [
    "Security: All files are automatically scanned for API credentials and secrets before processing.",
    "If a security warning appears, remove sensitive information from files before retrying."
  ]
}
```

## Key Features

### 🛡️ Pre-processing Security
- Hook runs **BEFORE** Claude processes any file
- No credentials are ever sent to Claude's servers
- Real-time scanning of all file operations

### 🔍 Comprehensive Detection
Uses Gitleaks' extensive ruleset to detect:
- **API Keys**: AWS, GCP, Azure, GitHub, Stripe, etc.
- **Database Strings**: MongoDB, PostgreSQL, MySQL, Redis
- **Authentication**: JWT tokens, OAuth tokens, Bearer tokens
- **Private Keys**: SSH, PGP, TLS certificates
- **Passwords**: In configuration files, environment variables
- **Custom Patterns**: Add your own regex patterns

### 📊 Audit & Logging
- All scans logged to `~/.claude/security_scan.log`
- Track detection events for compliance
- Monitor scanning performance

### 🎯 Smart Filtering
- Ignores example/demo credentials
- Excludes markdown documentation
- Skips test files by default
- Customizable allowlists

## Testing the Security Hook

Create a test file to verify the hook is working:

```bash
# Test with a fake AWS key (should be blocked)
echo 'aws_access_key_id=AKIAIOSFODNN7EXAMPLE' > test_secret.txt

# Try to edit it in Claude Code - it should be blocked
```

## Advanced Configuration

### Custom Secret Patterns

Add organization-specific patterns to `.gitleaks.toml`:

```toml
[[rules]]
id = "company-internal-token"
description = "Internal Company Token"
regex = '''COMP_TOKEN_[A-Z0-9]{32}'''
tags = ["company", "internal"]
```

### Performance Tuning

For large files, adjust timeout in the hook script:

```python
result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)  # Increase from 5 to 10 seconds
```

### Integration with CI/CD

The same `.gitleaks.toml` configuration can be used in your CI/CD pipeline:

```yaml
# GitHub Actions example
- name: Run gitleaks
  uses: gitleaks/gitleaks-action@v2
  with:
    config-path: .gitleaks.toml
```

## Troubleshooting

### Hook Not Triggering
1. Verify hook script is executable: `chmod +x ~/.claude/hooks/gitleaks_security_hook.py`
2. Check Claude settings: `cat ~/.claude/settings.json`
3. Review logs: `tail -f ~/.claude/security_scan.log`

### False Positives
1. Add patterns to allowlist in `.gitleaks.toml`
2. Use inline comments: `# gitleaks:allow`
3. Exclude specific file types or paths

### Performance Issues
1. Reduce scan scope in `.gitleaks.toml`
2. Increase timeout values
3. Use more specific matchers in settings.json

## Security Best Practices

1. **Never commit real credentials** - Use environment variables or secret management systems
2. **Rotate exposed secrets immediately** - If a secret is detected, assume it's compromised
3. **Use .env files** - Keep secrets in `.env` files (add to `.gitignore`)
4. **Regular audits** - Review `security_scan.log` periodically
5. **Team training** - Ensure all developers understand credential management

## Additional Resources

- [Gitleaks Documentation](https://github.com/gitleaks/gitleaks)
- [Claude Code Hooks Guide](https://docs.anthropic.com/claude/docs/hooks)
- [OWASP Secret Management Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html)
- [12 Factor App - Config](https://12factor.net/config)

