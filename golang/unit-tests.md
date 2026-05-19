# Go HTTP Handler Unit Testing

Testing HTTP handlers and clients in Go requires proper setup of request/response objects and often mock servers. This guide covers common patterns.

## Testing HTTP Handlers

Use `net/http/httptest` to create test requests and response recorders:

```go
package mypackage

import (
	"net/http"
	"net/http/httptest"
	"testing"
	
	"github.com/stretchr/testify/assert"
)

func TestMyHandler(t *testing.T) {
	// Create a test request
	req := httptest.NewRequest(http.MethodGet, "/", nil)
	
	// For POST with JSON body:
	// userJSON := `{"name":"test","email":"test@example.com"}`
	// req := httptest.NewRequest(http.MethodPost, "/users", strings.NewReader(userJSON))
	
	// Create a response recorder
	res := httptest.NewRecorder()
	
	// Call your handler
	myHandlerToTest(res, req)
	
	// Assert the response
	assert.Equal(t, http.StatusOK, res.Code)
	assert.Contains(t, res.Body.String(), "expected content")
}
```

### Testing with Request Body

```go
func TestHandlerWithBody(t *testing.T) {
	user := User{Name: "John", Email: "john@example.com"}
	userJSON, _ := json.Marshal(user)
	
	req := httptest.NewRequest(
		http.MethodPost,
		"/users",
		strings.NewReader(string(userJSON)),
	)
	
	// Set headers if needed
	req.Header.Set("Content-Type", "application/json")
	
	res := httptest.NewRecorder()
	myHandlerToTest(res, req)
	
	assert.Equal(t, http.StatusCreated, res.Code)
}
```

## Testing HTTP Clients with Mock Servers

Use `httptest.NewServer` or `httptest.NewTLSServer` to create mock HTTP servers for testing clients:

```go
package mypackage

import (
	"encoding/json"
	"fmt"
	"net/http"
	"net/http/httptest"
	"testing"
	
	"github.com/google/go-cmp/cmp"
)

func TestGitLabService_GetStatistics(t *testing.T) {
	// Define expected response
	expectedResponse := gitlab.Statistics{
		Statistics: gitlab.Statistic{
			Counts: gitlab.Counts{
				All:    1,
				Closed: 1,
				Opened: 1,
			},
		},
	}
	
	// Marshal to JSON
	responseJSON, _ := json.Marshal(expectedResponse)
	
	// Create a test server that returns our mock response
	ts := httptest.NewTLSServer(
		http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
			w.Header().Set("Content-Type", "application/json")
			fmt.Fprintln(w, string(responseJSON))
		}),
	)
	defer ts.Close()
	
	// Create client that trusts the test server's certificate
	client := ts.Client()
	
	// Setup service with mock client
	service := gitlab.NewService()
	service.SetHttpClient(client)
	service.SetGitlabEndpoint(ts.URL)
	
	// Call the method under test
	req := gitlab.NewProjectStatistics(1)
	result, err := req.GetStatistics(service)
	
	// Assertions
	if err != nil {
		t.Errorf("GetStatistics() error = %v", err)
	}
	
	if !cmp.Equal(result, expectedResponse) {
		t.Errorf("GetStatistics() = %v, want %v", result, expectedResponse)
	}
}
```

## Testing Different HTTP Methods

```go
func TestHandlerMethods(t *testing.T) {
	tests := []struct {
		name     string
		method   string
		path     string
		body     string
		expected int
	}{
		{
			name:     "GET root",
			method:   http.MethodGet,
			path:     "/",
			expected: http.StatusOK,
		},
		{
			name:     "POST create",
			method:   http.MethodPost,
			path:     "/items",
			body:     `{"name":"test"}`,
			expected: http.StatusCreated,
		},
		{
			name:     "PUT update",
			method:   http.MethodPut,
			path:     "/items/1",
			body:     `{"name":"updated"}`,
			expected: http.StatusOK,
		},
		{
			name:     "DELETE remove",
			method:   http.MethodDelete,
			path:     "/items/1",
			expected: http.StatusNoContent,
		},
	}
	
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			var bodyReader io.Reader
			if tt.body != "" {
				bodyReader = strings.NewReader(tt.body)
			}
			
			req := httptest.NewRequest(tt.method, tt.path, bodyReader)
			res := httptest.NewRecorder()
			
			myHandlerToTest(res, req)
			
			assert.Equal(t, tt.expected, res.Code)
		})
	}
}
```

## Testing with Middleware

```go
func TestHandlerWithMiddleware(t *testing.T) {
	// Create handler with middleware
	handler := middleware.Chain(
		middleware.Logger,
		middleware.Auth,
	)(myHandlerToTest)
	
	// Test the wrapped handler
	req := httptest.NewRequest(http.MethodGet, "/protected", nil)
	req.Header.Set("Authorization", "Bearer valid-token")
	
	res := httptest.NewRecorder()
	handler.ServeHTTP(res, req)
	
	assert.Equal(t, http.StatusOK, res.Code)
}
```

## Best Practices

1. **Use table-driven tests** for multiple scenarios
2. **Always defer ts.Close()** for test servers
3. **Set proper Content-Type headers** when testing JSON APIs
4. **Use testify/assert or cmp** for cleaner assertions
5. **Test error cases** (invalid JSON, missing fields, etc.)
6. **Clean up** any resources created during tests
7. **Mock external dependencies** to make tests deterministic

## Common Test Dependencies

```bash
# Install commonly used testing packages
go get github.com/stretchr/testify/assert
go get github.com/google/go-cmp/cmp
```
