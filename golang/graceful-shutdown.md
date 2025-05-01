
```go
 // Initializing the HTTP server
 server := &http.Server{Addr: ":8080"}

 // Create a channel to listen for OS signals
 stopChan := make(chan os.Signal, 5)

 // Notify the stopChan when an interrupt or terminate signal is received
 signal.Notify(stopChan, os.Interrupt, syscall.SIGINT, syscall.SIGTERM)

 // Start the HTTP server in a goroutine
 go func() {
  // If ListenAndServe returns an error and it's not a server closed error,
  // then log it as a fatal error.
  if err := server.ListenAndServe(); err != nil && err != http.ErrServerClosed {
   log.Fatalf("ListenAndServe(): %s", err)
  }
 }()

 // Wait until we get a stop signal
 <-stopChan
 // Log that the server is shutting down
 log.Println("Shutting down server...")

 // Create a context with a 15-second timeout
 ctx, cancel := context.WithTimeout(context.Background(), 15*time.Second)
 // Make sure to cancel the context when done
 defer cancel()

 // Initiate graceful shutdown
 // If it doesn't complete in 15 seconds, it will be forcefully stopped
 if err := server.Shutdown(ctx); err != nil {
  // Log if the shutdown failed
  log.Fatalf("Server Shutdown Failed:%+v", err)
 } else {
  // Log that the server has stopped gracefully
  log.Println("Server stopped gracefully")
 }
```

