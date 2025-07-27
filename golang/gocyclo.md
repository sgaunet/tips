# Gocyclo - Cyclomatic Complexity Analysis for Go

## What is Cyclomatic Complexity?

Cyclomatic complexity measures the number of independent paths through a program's source code. Higher complexity indicates:
- More difficult to test code
- Higher likelihood of bugs
- Harder to maintain and understand

**Recommended complexity levels:**
- 1-10: Simple, low risk
- 11-20: Moderate complexity, medium risk
- 21-50: Complex, high risk
- 50+: Very complex, very high risk

## Installation

```bash
go install github.com/fzipp/gocyclo/cmd/gocyclo@latest
```

## Basic Usage

### Check specific package
```bash
# Analyze a package (recommended: keep complexity < 10-20)
gocyclo pkg/

# Show average complexity
gocyclo -avg pkg/

# Set complexity threshold (only show functions above threshold)
gocyclo -over 10 ./...

# Analyze all packages recursively
gocyclo ./...

# Top 10 most complex functions
gocyclo -top 10 ./...
```

### Output Examples
```bash
# Standard output
21 package/file.go:123 FunctionName

# With -avg flag
21 package/file.go:123 FunctionName
Average: 8.5
```

## GitLab CI Integration with Badge Generation

This example creates a cyclomatic complexity badge for your GitLab project:

```yaml
build_badge_gocyclo:
  stage: build
  except:
    - tags
  image: golang
  script: |
    # Install badge generator
    go install github.com/sgaunet/gobadger@latest
    
    # Install gocyclo
    go install github.com/fzipp/gocyclo/cmd/gocyclo@latest
    
    # Calculate average cyclomatic complexity
    value=$(gocyclo -avg pkg/ | grep ^Average | awk '{print $2}')
    
    # Determine badge color based on complexity
    # Green: < 10 (simple)
    # Orange: 10-20 (moderate)
    # Red: > 20 (complex)
    color=$(awk -v value=$value -v recommend_min_limit=10 -v recommend_max_limit=20 '
      BEGIN {
        if (value < recommend_min_limit)
          color = "#00FF00"  # Green
        else if (value < recommend_max_limit)
          color = "#FFA500"  # Orange
        else
          color = "#FF0000"  # Red
        print color
      }')
    
    # Generate SVG badge
    gobadger -o gocyclo.svg -t cyclomatic -v "$value" -c "${color}"
    
    # Badge will be available at:
    # https://gitlab.com/%{project_path}/-/jobs/artifacts/main/raw/gocyclo.svg?job=build_badge_gocyclo
  artifacts:
    name: gocyclo.svg
    paths:
      - gocyclo.svg
    expire_in: 2 days
```

### Using the Badge in README

```markdown
![Cyclomatic Complexity](https://gitlab.com/YOUR_PROJECT/-/jobs/artifacts/main/raw/gocyclo.svg?job=build_badge_gocyclo)
```

## GitHub Actions Integration

```yaml
name: Code Quality

on: [push, pull_request]

jobs:
  gocyclo:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - uses: actions/setup-go@v5
        with:
          go-version: '1.22'
      
      - name: Install gocyclo
        run: go install github.com/fzipp/gocyclo/cmd/gocyclo@latest
      
      - name: Run gocyclo
        run: |
          # Fail if any function has complexity > 20
          gocyclo -over 20 ./...
          
          # Show average complexity
          echo "Average complexity:"
          gocyclo -avg ./...
```

## Best Practices

### 1. Set Team Standards
```bash
# Add to Makefile
.PHONY: complexity
complexity:
	@echo "Checking cyclomatic complexity..."
	@gocyclo -over 15 ./... || (echo "Complexity threshold exceeded" && exit 1)
	@echo "Average complexity: $$(gocyclo -avg ./... | grep Average)"
```

### 2. Pre-commit Hook
```yaml
# .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: gocyclo
        name: Check cyclomatic complexity
        entry: bash -c 'gocyclo -over 15 ./...'
        language: system
        pass_filenames: false
        types: [go]
```

### 3. Reduce Complexity

**Before (complexity: 8):**
```go
func processData(data []int, operation string) int {
    result := 0
    for _, v := range data {
        if operation == "sum" {
            result += v
        } else if operation == "product" {
            result *= v
        } else if operation == "max" && v > result {
            result = v
        } else if operation == "min" && v < result {
            result = v
        }
    }
    return result
}
```

**After (complexity: 2):**
```go
func processData(data []int, operation string) int {
    ops := map[string]func([]int) int{
        "sum":     sum,
        "product": product,
        "max":     max,
        "min":     min,
    }
    
    if fn, ok := ops[operation]; ok {
        return fn(data)
    }
    return 0
}
```

### 4. Common Patterns to Reduce Complexity

- **Extract functions** for complex conditions
- **Use polymorphism** instead of switch/if-else chains
- **Apply early returns** to reduce nesting
- **Use table-driven tests** for multiple scenarios
- **Split large functions** into smaller, focused ones

## Integration with Other Tools

```bash
# Combine with other Go tools
go test -cover ./... && \
golint ./... && \
gocyclo -avg ./... && \
go vet ./...
```

## References

- [Gocyclo GitHub](https://github.com/fzipp/gocyclo)
- [Understanding Cyclomatic Complexity](https://en.wikipedia.org/wiki/Cyclomatic_complexity)
- [Go Code Review Comments](https://github.com/golang/go/wiki/CodeReviewComments)