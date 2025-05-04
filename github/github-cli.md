# GitHub CLI

## Create issue

```bash
gh issue create --title "My new issue" --body "Here are more details." --assignee @me --label "bug" 
```

## Create labels

```bash
gh label delete "enhancement" --yes
gh label delete "good first issue" --yes
gh label delete "help wanted" --yes
gh label delete "invalid" --yes
gh label create "cicd" --color 00FF00 --description "CI/CD related issues"
gh label create "feature" --color FFA500 --description "New feature"
gh label create "chore" --color FFFF00 --description "Chore"
```
