
```bash
export GOMEMLIMIT=500000000 # 500MB
```

In this case, if the program tries to use more than 500MB of memory, the Go runtime will limit the memory allocation.

GOMAXPROCS: You can control the number of OS threads used for executing Goroutines by setting the GOMAXPROCS variable.
By default, Go uses as many OS threads as there are CPU cores available on the machine.

In containers, some libraries can handle this automatically:

* https://github.com/uber-go/automaxprocs
* https://github.com/KimMachineGun/automemlimit
