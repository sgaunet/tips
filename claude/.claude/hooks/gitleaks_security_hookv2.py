#!/usr/bin/env python3
"""
Enhanced Gitleaks Security Hook with Logging
"""

import json
import subprocess
import sys
import os
import tempfile
import logging
from datetime import datetime
from pathlib import Path

# Set up logging
log_dir = Path.home() / '.claude' / 'logs'
log_dir.mkdir(parents=True, exist_ok=True)
log_file = log_dir / f"security_scan_{datetime.now().strftime('%Y%m%d')}.log"

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler(sys.stderr)
    ]
)

logger = logging.getLogger(__name__)

def get_gitleaks_config():
    """Get the path to custom gitleaks config if it exists."""
    config_path = Path.home() / '.claude' / '.gitleaks.toml'
    if config_path.exists():
        return str(config_path)
    return None

def run_gitleaks_on_content(content, file_path=None):
    """Run gitleaks on the provided content."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.tmp', delete=False) as tmp_file:
        tmp_file.write(content)
        tmp_file_path = tmp_file.name

    try:
        # Build gitleaks command
        cmd = ['gitleaks', 'detect', '--no-git', '-v', '--source', tmp_file_path, '--report-format', 'json']

        # Add custom config if available
        config = get_gitleaks_config()
        if config:
            cmd.extend(['--config', config])
            logger.info(f"Using custom config: {config}")

        # Run gitleaks
        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode == 1:  # Secrets found
            logger.warning(f"Secrets detected in {file_path or 'content'}")
            return True, result.stdout
        elif result.returncode == 0:  # Clean
            logger.info(f"No secrets found in {file_path or 'content'}")
            return False, None
        else:  # Error
            logger.error(f"Gitleaks error: {result.stderr}")
            return False, None
    except Exception as e:
        logger.error(f"Exception running gitleaks: {e}")
        return False, None
    finally:
        os.unlink(tmp_file_path)

def format_secret_report(details):
    """Format the secret detection report for display."""
    report = []
    try:
        leaked_data = json.loads(details)
        for leak in leaked_data:
            report.append({
                'type': leak.get('Description', 'Unknown'),
                'file': leak.get('File', 'Unknown'),
                'line': leak.get('StartLine', 0),
                'match': leak.get('Match', '')[:50] + '...' if len(leak.get('Match', '')) > 50 else leak.get('Match', '')
            })
    except:
        pass
    return report

def scan_content(tool_name, tool_input):
    """Scan content based on tool type."""
    results = []

    if tool_name == 'Write':
        content = tool_input.get('content', '')
        file_path = tool_input.get('file_path', '')
        if content:
            found, details = run_gitleaks_on_content(content, file_path)
            if found:
                results.append({
                    'file': file_path,
                    'secrets': format_secret_report(details)
                })

    elif tool_name in ['Edit', 'MultiEdit']:
        if tool_name == 'Edit':
            edits = [tool_input]
        else:
            edits = tool_input.get('edits', [])

        for edit in edits:
            content = edit.get('new_content', '')
            file_path = edit.get('file_path', '')
            if content:
                found, details = run_gitleaks_on_content(content, file_path)
                if found:
                    results.append({
                        'file': file_path,
                        'secrets': format_secret_report(details)
                    })

    return results

def main():
    # Read hook input
    try:
        hook_input = json.loads(sys.stdin.read())
    except json.JSONDecodeError:
        logger.error("Invalid JSON input")
        print(json.dumps({"continue": True, "suppressOutput": True}))
        sys.exit(0)

    # Log the hook event
    session_id = hook_input.get('session_id', 'unknown')
    tool_name = hook_input.get('tool_name', '')
    logger.info(f"Session {session_id}: Scanning {tool_name} operation")

    # Check if this is a file operation
    if tool_name not in ['Write', 'Edit', 'MultiEdit']:
        print(json.dumps({"continue": True, "suppressOutput": True}))
        sys.exit(0)

    # Scan for secrets
    secret_results = scan_content(tool_name, hook_input.get('tool_input', {}))

    if secret_results:
        # Log detailed results
        logger.warning(f"Session {session_id}: BLOCKED - Secrets detected")
        for result in secret_results:
            logger.warning(f"  File: {result['file']}")
            for secret in result.get('secrets', []):
                logger.warning(f"    - {secret['type']} at line {secret['line']}")

        # Create user-friendly message
        message_parts = ["🔒 SECURITY BLOCK: Detected potential secrets:\n"]
        for result in secret_results:
            message_parts.append(f"\n📄 {result['file']}:")
            for secret in result.get('secrets', [])[:3]:  # Show max 3 per file
                message_parts.append(f"  • {secret['type']} (line {secret['line']})")

        message_parts.append("\n\nPlease remove sensitive information before proceeding.")
        message_parts.append("Check ~/.claude/logs for detailed scan results.")

        # Block the operation
        print(json.dumps({
            "continue": False,
            "stopReason": ''.join(message_parts),
            "systemMessage": "Security scan blocked this operation to protect your credentials."
        }))
    else:
        logger.info(f"Session {session_id}: PASSED - No secrets detected")
        print(json.dumps({
            "continue": True,
            "suppressOutput": True
        }))

if __name__ == "__main__":
    main()