# Optional Pattern in Go (Functional Options)

The functional options pattern is an idiomatic Go approach for configuring objects with many optional parameters while maintaining clean, readable, and type-safe APIs.

## Problem

When creating structs with many optional fields, you face several challenges:

- **Constructor explosion**: Multiple `NewX()` variants for different combinations
- **Poor readability**: Long parameter lists with many nil/zero values
- **Brittle APIs**: Adding new options breaks existing calls

## Solution: Functional Options Pattern

Define option functions that modify a receiver struct, then accept variadic options in your constructor.

```go
package main

import (
	"log"
	"time"
)

type Server struct {
	host    string
	port    int
	timeout time.Duration
}

func (s *Server) Run() {
	log.Printf("Server running %s:%d with timeout %v", s.host, s.port, s.timeout)
}

// OptionsServerFunc defines the function signature for server options
type OptionsServerFunc func(s *Server) error

// WithTimeout sets the server timeout
func WithTimeout(t time.Duration) OptionsServerFunc {
	return func(s *Server) error {
		s.timeout = t
		return nil
	}
}

// WithPort sets the server port
func WithPort(p int) OptionsServerFunc {
	return func(s *Server) error {
		s.port = p
		return nil
	}
}

// WithHost sets the server host
func WithHost(h string) OptionsServerFunc {
	return func(s *Server) error {
		s.host = h
		return nil
	}
}

// NewServer creates a server with sensible defaults and applies provided options
func NewServer(opts ...OptionsServerFunc) (*Server, error) {
	server := &Server{
		host:    "127.0.0.1",
		port:    8080,
		timeout: 3 * time.Second,
	}

	for _, opt := range opts {
		if err := opt(server); err != nil {
			return nil, err
		}
	}

	return server, nil
}

func main() {
	// Create server with custom timeout and port
	server, err := NewServer(
		WithTimeout(5*time.Second),
		WithPort(7000),
	)
	if err != nil {
		log.Fatal(err)
	}
	server.Run()

	// Create server with all defaults
	defaultServer, _ := NewServer()
	defaultServer.Run()

	// Create server with custom host
	customServer, _ := NewServer(WithHost("0.0.0.0"))
	customServer.Run()
}
```

## Benefits

- **Type-safe**: Compile-time checking of all options
- **Self-documenting**: Option names clearly indicate what they configure
- **Extensible**: New options can be added without breaking existing code
- **Readable**: Call sites clearly show which options are being set
- **Default values**: Sensible defaults are built into the constructor

## Variations

### Without Error Returns

For simpler cases where options cannot fail:

```go
type Option func(s *Server)

func WithTimeout(t time.Duration) Option {
	return func(s *Server) { s.timeout = t }
}

func NewServer(opts ...Option) *Server {
	server := &Server{host: "127.0.0.1", port: 8080, timeout: 3 * time.Second}
	for _, opt := range opts {
		opt(server)
	}
	return server
}
```

### With Validation

Add validation in the constructor after applying options:

```go
func NewServer(opts ...OptionsServerFunc) (*Server, error) {
	server := &Server{host: "127.0.0.1", port: 8080, timeout: 3 * time.Second}

	for _, opt := range opts {
		if err := opt(server); err != nil {
			return nil, err
		}
	}

	// Validate after all options applied
	if server.port < 1 || server.port > 65535 {
		return nil, fmt.Errorf("invalid port: %d", server.port)
	}

	return server, nil
}
```

## When to Use

- Configuring structs with 3+ optional fields
- Library APIs where extensibility matters
- When you want to avoid long parameter lists
- When defaults make sense for most use cases

## Alternatives

- **Builder pattern**: More verbose but provides better IDE support
- **Config struct**: Pass a struct with all options (simpler but less flexible)
- **Method chaining**: `New().SetX(x).SetY(y)` (mutable, less idiomatic in Go)
