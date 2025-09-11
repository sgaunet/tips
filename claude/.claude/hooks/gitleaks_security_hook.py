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

def run_gitleaks_on_content(content, file_path=None):
    """Run gitleaks on the provided content."""
    # Create a temporary file with the content
    with tempfile.NamedTemporaryFile(mode='w', suffix='.tmp', delete=False) as tmp_file:
        tmp_file.write(content)
        tmp_file_path = tmp_file.name

    try:
        # Run gitleaks on the temporary file
        result = subprocess.run(
            ['gitleaks', 'detect', '--no-git', '-v', '--source', tmp_file_path, '--report-format', 'json'],
            capture_output=True,
            text=True
        )

        # Parse the results
        if result.returncode == 1:  # Gitleaks found secrets
            return True, result.stdout
        elif result.returncode == 0:  # No secrets found
            return False, None
        else:  # Error occurred
            print(f"Error running gitleaks: {result.stderr}", file=sys.stderr)
            return False, None
    finally:
        # Clean up temporary file
        os.unlink(tmp_file_path)

def main():
    # Read the hook input from stdin
    try:
        hook_input = json.loads(sys.stdin.read())
    except json.JSONDecodeError:
        print("Error: Invalid JSON input", file=sys.stderr)
        sys.exit(1)

    # Extract relevant information based on the hook event
    hook_event = hook_input.get('hook_event_name', '')
    tool_name = hook_input.get('tool_name', '')
    tool_input = hook_input.get('tool_input', {})

    # Check if this is a file-related operation
    file_operations = ['Write', 'Edit', 'MultiEdit']
    if tool_name not in file_operations:
        # Not a file operation, allow it to proceed
        print(json.dumps({
            "continue": True,
            "suppressOutput": True
        }))
        sys.exit(0)

    # Extract file content based on the tool type
    content_to_scan = None
    file_path = None

    if tool_name == 'Write':
        content_to_scan = tool_input.get('content', '')
        file_path = tool_input.get('file_path', '')
    elif tool_name == 'Edit' or tool_name == 'MultiEdit':
        # For edits, scan the new content
        if tool_name == 'Edit':
            content_to_scan = tool_input.get('new_content', '')
            file_path = tool_input.get('file_path', '')
        else:  # MultiEdit
            # For multi-edit, we need to check all edits
            edits = tool_input.get('edits', [])
            secrets_found = False
            for edit in edits:
                file_path = edit.get('file_path', '')
                content = edit.get('new_content', '')
                if content:
                    found, details = run_gitleaks_on_content(content, file_path)
                    if found:
                        secrets_found = True
                        print(f"⚠️  SECURITY WARNING: Potential secrets detected in {file_path}", file=sys.stderr)
                        if details:
                            try:
                                leaked_data = json.loads(details)
                                for leak in leaked_data:
                                    print(f"  - {leak.get('Description', 'Unknown secret type')} found", file=sys.stderr)
                            except:
                                pass

            if secrets_found:
                # Block the operation
                print(json.dumps({
                    "continue": False,
                    "stopReason": "🔒 SECURITY BLOCK: Potential API credentials or secrets detected in the files. Please remove sensitive information before proceeding.",
                    "systemMessage": "Security scan detected potential secrets. Operation blocked to protect your credentials."
                }))
            else:
                # Allow the operation
                print(json.dumps({
                    "continue": True,
                    "suppressOutput": True
                }))
            sys.exit(0)

    # If we have content to scan
    if content_to_scan:
        secrets_found, details = run_gitleaks_on_content(content_to_scan, file_path)

        if secrets_found:
            print(f"⚠️  SECURITY WARNING: Potential secrets detected in {file_path}", file=sys.stderr)
            if details:
                try:
                    leaked_data = json.loads(details)
                    for leak in leaked_data:
                        print(f"  - {leak.get('Description', 'Unknown secret type')} at line {leak.get('StartLine', '?')}", file=sys.stderr)
                except:
                    pass

            # Block the operation
            print(json.dumps({
                "continue": False,
                "stopReason": f"🔒 SECURITY BLOCK: Potential API credentials or secrets detected in {file_path}. Please remove sensitive information before proceeding.",
                "systemMessage": "Security scan detected potential secrets. Operation blocked to protect your credentials."
            }))
        else:
            # No secrets found, allow the operation
            print(json.dumps({
                "continue": True,
                "suppressOutput": True
            }))
    else:
        # No content to scan, allow the operation
        print(json.dumps({
            "continue": True,
            "suppressOutput": True
        }))

if __name__ == "__main__":
    main()