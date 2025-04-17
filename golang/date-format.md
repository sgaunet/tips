RFC3339 date-time in %Y-%M-%DT%h:%m:%sZ format

Next time, just write RFC 3339 instead
When you find yourself typing ISO 8601 in your code or documentation, just replace it with RFC 3339 and continue knowing you made dates a tiny bit easier for you and your API users.

https://ijmacd.github.io/rfc3339-iso8601/

Example in Go:

```go
package main

import (
    "fmt"
    "time"
)

func main() {
    now := time.Now().UTC()
    fmt.Println(now.Format(time.RFC3339))
}
```
