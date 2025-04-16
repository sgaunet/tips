
```go
func IsNil(x interface{}) bool {
   if x == nil {
     return true
   }
 ​
   return reflect.ValueOf(x).IsNil()
 }
```
