
# Go Tool (go 1.24)

```bash
	$ go get tool github.com/matryer/moq
	$ go get tool github.com/sqlc-dev/sqlc/cmd/sqlc@v1.28.0
	$ go get tool github.com/a-h/templ/cmd/templ
```

```go
// go.mod

tool (
	github.com/matryer/moq
	github.com/sqlc-dev/sqlc/cmd/sqlc
	github.com/a-h/templ/cmd/templ
)
```

```go
// templ
//go:generate go tool github.com/a-h/templ/cmd/templ generate

// Example with sqlc
//go:generate go tool github.com/sqlc-dev/sqlc/cmd/sqlc generate -f ../../sqlc.yaml

// Example with moq

package storage

//go:generate go tool github.com/matryer/moq -out mockstore/mock_store.go -pkg mockstore . Store

type Store interface {
    Get(id string) (interface{}, error)
    Put(id string, v interface{}) error
}
```

