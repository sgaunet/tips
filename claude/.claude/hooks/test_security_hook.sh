#!/bin/bash
# Test script for the Gitleaks security hook

echo "Testing Gitleaks Security Hook..."
echo "================================="

# Test 1: Clean content
echo -e "\n1. Testing clean content..."
echo '{
  "hook_event_name": "PreToolUse",
  "session_id": "test-123",
  "tool_name": "Write",
  "tool_input": {
    "file_path": "test.py",
    "content": "def hello():\n    print(\"Hello World\")"
  }
}' | python3 ~/.claude/hooks/gitleaks_security_hook.py

# Test 2: Content with API key
echo -e "\n2. Testing content with API key..."
echo '{
  "hook_event_name": "PreToolUse",
  "session_id": "test-456",
  "tool_name": "Write",
  "tool_input": {
    "file_path": "config.py",
    "content": "API_KEY = \"sk-1234567890abcdef1234567890abcdef\""
  }
}' | python3 ~/.claude/hooks/gitleaks_security_hook.py

# Test 3: Content with AWS credentials
echo -e "\n3. Testing content with AWS credentials..."
echo '{
  "hook_event_name": "PreToolUse",
  "session_id": "test-789",
  "tool_name": "Edit",
  "tool_input": {
    "file_path": ".env",
    "new_content": "AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE\nAWS_SECRET_ACCESS_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
  }
}' | python3 ~/.claude/hooks/gitleaks_security_hook.py

echo -e "\n================================="
echo "Tests completed. Check the output above."