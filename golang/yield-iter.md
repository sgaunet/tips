# Go Iterators with yield (Go 1.23+)

Go 1.23 introduced a new `yield` keyword that enables writing iterators in a more natural way. This feature allows functions to yield values one at a time, similar to generators in other languages.

## Basic Iterator Pattern

The `yield` keyword works within functions that have a specific signature, allowing them to produce a sequence of values:

```go
package main

import (
	"fmt"
	"strings"
)

// Backward returns an iterator that yields strings in reverse order
func Backward(s []string) func(yield func(string) bool) {
	return func(yield func(string) bool) {
		for i := len(s) - 1; i >= 0; i-- {
			if !yield(strings.ToUpper(s[i])) {
				return
			}
		}
	}
}

func ToUpperByIter() {
	sl := []string{"hello", "world", "golang"}
	
	// Range over the iterator
	for v := range Backward(sl) {
		fmt.Println(v)
		// Output:
		// GOLANG
		// WORLD
		// HELLO
	}
}
```

## How yield Works

- The `yield` function passed to your iterator accepts a value
- Return `false` from `yield` to stop iteration early
- Return `true` to continue
- The range loop automatically handles calling `yield` and checking its return value

## Iterator Function Signature

An iterator function must have the signature:

```go
func(yield func(T) bool)
```

Where `T` is the type of values being yielded.

## Practical Examples

### Filtering with Iterators

```go
// FilterStrings returns an iterator that yields only strings matching the predicate
func FilterStrings(s []string, predicate func(string) bool) func(yield func(string) bool) {
	return func(yield func(string) bool) {
		for _, str := range s {
			if predicate(str) && !yield(str) {
				return
			}
		}
	}
}

func ExampleFilterStrings() {
	words := []string{"apple", "banana", "cherry", "date"}
	
	// Get only words longer than 5 characters
	for word := range FilterStrings(words, func(s string) bool { return len(s) > 5 }) {
		fmt.Println(word)
		// Output: banana, cherry
	}
}
```

### Transforming with Iterators

```go
// MapStrings returns an iterator that transforms each string
func MapStrings(s []string, transform func(string) string) func(yield func(string) bool) {
	return func(yield func(string) bool) {
		for _, str := range s {
			if !yield(transform(str)) {
				return
			}
		}
	}
}

func ExampleMapStrings() {
	words := []string{"hello", "world"}
	
	// Convert to uppercase
	for word := range MapStrings(words, strings.ToUpper) {
		fmt.Println(word)
		// Output: HELLO, WORLD
	}
}
```

### Chaining Iterators

```go
// Chain combines multiple iterators into one
func Chain[T any](iterators ...func(yield func(T) bool)) func(yield func(T) bool) {
	return func(yield func(T) bool) {
		for _, iter := range iterators {
			iter(func(v T) bool {
				return yield(v)
			})
		}
	}
}

func ExampleChain() {
	iter1 := func(yield func(int) bool) {
		yield(1)
		yield(2)
	}
	
	iter2 := func(yield func(int) bool) {
		yield(3)
		yield(4)
	}
	
	// Combine both iterators
	for v := range Chain(iter1, iter2) {
		fmt.Println(v)
		// Output: 1, 2, 3, 4
	}
}
```

### Infinite Sequences

```go
// Count returns an iterator that yields integers starting from n
func Count(n int) func(yield func(int) bool) {
	return func(yield func(int) bool) {
		for i := n; ; i++ {
			if !yield(i) {
				return
			}
		}
	}
}

func ExampleCount() {
	// Get first 5 numbers starting from 10
	count := 0
	for v := range Count(10) {
		fmt.Println(v)
		count++
		if count >= 5 {
			break
		}
	}
	// Output: 10, 11, 12, 13, 14
}
```

## Iterator vs Slice

### When to Use Iterators

- **Large datasets**: Process items one at a time without loading all into memory
- **Lazy evaluation**: Compute values on-demand
- **Infinite sequences**: Generate values forever (until consumer stops)
- **Chaining operations**: Pipe multiple transformations together efficiently

### When to Use Slices

- **Small datasets**: When all data fits comfortably in memory
- **Random access**: Need to access elements by index
- **Multiple passes**: Need to iterate over data multiple times
- **Simplicity**: When the overhead of iterators isn't justified

## Performance Considerations

- **Memory**: Iterators use O(1) memory for the sequence itself
- **Speed**: Each `yield` call has a small overhead vs direct slice access
- **Allocation**: No heap allocation for the sequence (but individual values may allocate)

## Comparison with Other Approaches

### Before yield (Go 1.22 and earlier)

```go
// Using channels
func BackwardChannel(s []string) <-chan string {
	ch := make(chan string)
	go func() {
		defer close(ch)
		for i := len(s) - 1; i >= 0; i-- {
			ch <- strings.ToUpper(s[i])
		}
	}()
	return ch
}

// Using function that accepts a callback
func BackwardCallback(s []string, fn func(string)) {
	for i := len(s) - 1; i >= 0; i-- {
		fn(strings.ToUpper(s[i]))
	}
}
```

### With yield (Go 1.23+)

```go
// Cleaner and more idiomatic
func Backward(s []string) func(yield func(string) bool) {
	return func(yield func(string) bool) {
		for i := len(s) - 1; i >= 0; i-- {
			if !yield(strings.ToUpper(s[i])) {
				return
			}
		}
	}
}
```

## Best Practices

1. **Name iterators clearly**: Use verb-noun naming like `FilterStrings`, `MapInts`
2. **Document behavior**: Note if iterator stops early when yield returns false
3. **Handle errors**: Consider how errors are propagated (yield doesn't support error returns)
4. **Avoid blocking**: Don't block inside yield callbacks
5. **Consider composition**: Design iterators to be easily chained together
