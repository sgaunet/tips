

```go
package smtpservertest

import (
	"log"
	"time"

	"context"
	"fmt"

	"github.com/testcontainers/testcontainers-go"
	"github.com/testcontainers/testcontainers-go/wait"
)

const SSHDDockerImage = "axllent/mailpit:v1.14.0"

// SMTPServerTest is an interface to be implemented by the test server
type SMTPServerTest interface {
	GetEndpoint() string
	Teardown()
}

// SMTPServerTestImpl is the implementation of the SMTPServerTest interface
type SMTPServerTestImpl struct {
	smtpServerC testcontainers.Container
	endpoint    string
}

// NewTestSFTPServer creates a new SFTP server for testing with default values
func NewTestSMTPServer() SMTPServerTest {
	newTestServer := &SMTPServerTestImpl{}
	ctx := context.Background()
	var err error
	req := testcontainers.ContainerRequest{
		Name:         "mailpit",
		Image:        SSHDDockerImage,
		ExposedPorts: []string{"1025/tcp"},
		WaitingFor:   wait.ForLog("[http] accessible via http://localhost:8025/"),
		Env:          map[string]string{},
	}
	newTestServer.smtpServerC, err = testcontainers.GenericContainer(ctx, testcontainers.GenericContainerRequest{
		ContainerRequest: req,
		Started:          true,
		Reuse:            true,
	})
	if err != nil {
		fmt.Println("Error creating container")
		log.Fatal(err.Error())
	}

	now := time.Now()
	for time.Since(now) < 10*time.Second && newTestServer.endpoint == "" {
		newTestServer.endpoint, err = newTestServer.smtpServerC.Endpoint(ctx, "")
		if err != nil {
			fmt.Println(err.Error())
			time.Sleep(500 * time.Millisecond)
		}
	}
	if err != nil {
		log.Fatal(err.Error())
	}
	return newTestServer
}

// Teardown stops the SFTP server
func (t *SMTPServerTestImpl) Teardown() {
	defer func() {
		if err := t.smtpServerC.Terminate(context.Background()); err != nil {
			panic(err)
		}
	}()
	fmt.Printf("\033[1;36m%s\033[0m", "> Teardown completed\n")
}

// GetEndpoint returns the endpoint of the SFTP server
func (t *SMTPServerTestImpl) GetEndpoint() string {
	return t.endpoint
}
```
