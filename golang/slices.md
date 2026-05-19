# Go Slices Package Tips

The `slices` package (introduced in Go 1.21) provides generic functions for working with slices. Combined with `maps` and other generic packages, it enables powerful functional-style operations.

## Filtering and Collecting

Use `slices.Collect` with custom filter functions to transform maps into filtered slices:

```go
package main

import (
	"fmt"
	"maps"
	"slices"
)

// LongStrings returns a slice containing only strings with length >= n from a map
func LongStrings(m map[int]string, n int) []string {
	isLong := func(s string) bool {
		return len(s) >= n
	}
	return slices.Collect(maps.Values(m), isLong)
}

// Alternative for Go 1.21 (before slices.Filter was added)
func LongStrings121(m map[int]string, n int) []string {
	isLong := func(s string) bool {
		return len(s) >= n
	}
	
	var result []string
	for _, v := range maps.Values(m) {
		if isLong(v) {
			result = append(result, v)
		}
	}
	return result
}

func main() {
	data := map[int]string{
		1: "hello",
		2: "world",
		3: "golang",
		4: "a",
		5: "programming",
	}

	long := LongStrings(data, 5)
	fmt.Println(long) // Output: [hello world golang programming]
}
```

## Common Slices Operations

### Filter

```go
// Go 1.23+
numbers := []int{1, 2, 3, 4, 5, 6}
even := slices.Filter(numbers, func(n int) bool { return n%2 == 0 })
// even = [2, 4, 6]
```

### Map/Transform

```go
// Transform each element
doubled := make([]int, len(numbers))
for i, n := range numbers {
	doubled[i] = n * 2
}
// doubled = [2, 4, 6, 8, 10, 12]
```

### Reduce

```go
// Sum all elements
sum := 0
for _, n := range numbers {
	sum += n
}
// sum = 21
```

### Contains

```go
hasThree := slices.Contains(numbers, 3) // true
```

### Index

```go
idx := slices.Index(numbers, 4) // 3
idx = slices.IndexFunc(numbers, func(n int) bool { return n > 4 }) // 4 (first element > 4)
```

## Working with Maps

The `maps` package complements `slices` for working with maps:

```go
import "maps"

m := map[string]int{"a": 1, "b": 2, "c": 3}

// Get all keys
keys := maps.Keys(m)
// Get all values
values := maps.Values(m)

// Copy a map
m2 := maps.Clone(m)

// Equal comparison
equal := maps.Equal(m, map[string]int{"a": 1, "b": 2, "c": 3}) // true
```

## Practical Examples

### Filter Map Values by Condition

```go
type User struct {
	ID   int
	Name string
	Age  int
}

users := map[int]User{
	1: {ID: 1, Name: "Alice", Age: 25},
	2: {ID: 2, Name: "Bob", Age: 17},
	3: {ID: 3, Name: "Charlie", Age: 30},
}

// Get adult users (age >= 18)
adults := slices.Collect(maps.Values(users), func(u User) bool {
	return u.Age >= 18
})
```

### Extract Specific Fields

```go
// Get all user names
names := slices.Collect(maps.Values(users), func(u User) string {
	return u.Name
})
```

## When to Use

- **Use slices package**: For common operations on slices (filter, contains, index)
- **Use with maps package**: When transforming map values into slices
- **Consider performance**: For large datasets, traditional loops may be more efficient
- **Readability**: Functional style improves readability for complex transformations
