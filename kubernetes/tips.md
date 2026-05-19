# Kubernetes Tips and Tricks

A collection of useful kubectl commands and patterns for working with Kubernetes.

## Pod Management

### Kill Pod Stuck in Terminating State

When a pod is stuck in Terminating state, force delete it:

```bash
kubectl delete pod $POD_NAME --grace-period=0 --force -n $NAMESPACE
```

**Explanation:**
- `--grace-period=0`: Don't wait for graceful shutdown
- `--force`: Force deletion (bypasses finalizers)
- `-n $NAMESPACE`: Specify namespace

**Short alias:**
```bash
alias kill-pod='kubectl delete pod $1 --grace-period=0 --force -n $2'
```

## Querying Resources

### Custom Columns

Display specific fields in a custom format:

```bash
# Basic custom columns for pods
kubectl get pods -o custom-columns='NAME:metadata.name,IMAGES:spec.containers[*].image'

# For deployments
kubectl get deploy -o custom-columns='NAME:metadata.name,IMAGES:spec.template.spec.containers[*].image'

# With labels
kubectl get deploy -o custom-columns='NAME:metadata.name,IMAGES:spec.template.spec.containers[*].image,L:spec.template.metadata.labels'
```

### Extract Specific Label Values

```bash
# Get a specific label value
kubectl get deploy -o custom-columns="NAME:metadata.name,L:spec.template.metadata.labels['app']"

# Get a different label
kubectl get deploy -o custom-columns="NAME:metadata.name,L:spec.template.metadata.labels['period']"

# Get selector labels
kubectl get deploy -o custom-columns="NAME:metadata.name,L:spec.template.metadata.labels['period'],S:spec.selector['matchLabels']['app']"
```

### JSONPath Queries

Extract specific fields using JSONPath:

```bash
# Get selfLink of a deployment
kubectl get deployment.apps "$DEPLOYMENT_NAME" -o jsonpath={.metadata.selfLink}

# Get scale selector
kubectl get --raw /apis/apps/v1/namespaces/$NAMESPACE/deployments/$DEPLOYMENT/scale | jq -r .status.selector

# Get pods by selector
kubectl get pods -l "app=$APP_NAME"
```

## Resource Information

### Get Resource SelfLink

```bash
kubectl get deployment.apps "prodauto-backupcdb" -o jsonpath={.metadata.selfLink}
# Output: /apis/apps/v1/namespaces/mtrg/deployments/prodauto-backupcdb
```

### Get Scale Information

```bash
# Get the selector used for scaling
kubectl get --raw /apis/apps/v1/namespaces/mtrg/deployments/prodauto-backupcdb/scale | jq -r .status.selector
# Output: app=prodauto-backupcdb

# Get pods matching the selector
kubectl get pods -l "app=prodauto-backupcdb"
```

## Common One-Liners

### Check Pod Status

```bash
# Get all pods with their status
kubectl get pods -o wide

# Get pods with node information
kubectl get pods -o custom-columns='NAME:metadata.name,NODE:spec.nodeName,STATUS:status.phase'
```

### Check Resource Usage

```bash
# Get pod CPU/Memory usage
kubectl top pods

# Get node CPU/Memory usage
kubectl top nodes
```

### Logs and Debugging

```bash
# Get logs from a pod
kubectl logs $POD_NAME

# Get logs with timestamps
kubectl logs $POD_NAME --timestamps

# Get logs from previous instance
kubectl logs $POD_NAME --previous

# Get logs from a specific container in a pod
kubectl logs $POD_NAME -c $CONTAINER_NAME

# Follow logs in real-time
kubectl logs -f $POD_NAME

# Execute command in a pod
kubectl exec -it $POD_NAME -- /bin/bash
```

## Label and Selector Tips

### Filter by Labels

```bash
# Get resources with specific label
kubectl get pods -l app=myapp

# Get resources with multiple labels
kubectl get pods -l app=myapp,env=prod

# Get resources with label containing value
kubectl get pods -l 'app in (app1, app2)'

# Get resources with label key (regardless of value)
kubectl get pods -l 'app'
```

### Update Labels

```bash
# Add or update a label
kubectl label pod $POD_NAME new-label=value

# Remove a label
kubectl label pod $POD_NAME label-to-remove-

# Update labels on deployment
kubectl label deployment $DEPLOYMENT_NAME app=new-value
```

## Namespace Operations

```bash
# List all namespaces
kubectl get namespaces

# Get resources in all namespaces
kubectl get pods --all-namespaces

# Set default namespace in context
kubectl config set-context --current --namespace=$NAMESPACE
```

## Configuration Tips

### View Resource Configuration

```bash
# View full YAML of a resource
kubectl get pod $POD_NAME -o yaml

# View specific fields
kubectl get pod $POD_NAME -o jsonpath='{.spec.containers[0].image}'

# Describe a resource (events, conditions, etc.)
kubectl describe pod $POD_NAME
```

### Edit Resources

```bash
# Edit a resource in-place
kubectl edit pod $POD_NAME

# Patch a resource
kubectl patch pod $POD_NAME -p '{"spec":{"containers":[{"name":"mycontainer","image":"newimage:tag"}]}}'

# Scale a deployment
kubectl scale deployment $DEPLOYMENT_NAME --replicas=3
```

## Networking

```bash
# Port-forward to a pod
kubectl port-forward pod/$POD_NAME 8080:80

# Port-forward to a service
kubectl port-forward svc/$SERVICE_NAME 8080:80

# Get service endpoint
kubectl get endpoints $SERVICE_NAME

# Get service details
kubectl get svc $SERVICE_NAME -o wide
```

## Cleanup

```bash
# Delete a resource
kubectl delete pod $POD_NAME

# Delete resources by label
kubectl delete pods -l app=myapp

# Delete all resources in a namespace (careful!)
kubectl delete all --all -n $NAMESPACE

# Delete completed jobs
kubectl delete jobs --field-selector status.successful=1
```

## Useful Aliases

Add these to your `~/.bashrc` or `~/.zshrc`:

```bash
# Kubernetes aliases
alias k='kubectl'
alias kgp='kubectl get pods'
alias kgd='kubectl get deployments'
alias kgs='kubectl get services'
alias kgn='kubectl get namespaces'
alias kgcm='kubectl get configmaps'
alias kdesc='kubectl describe'
alias klogs='kubectl logs'
alias kexec='kubectl exec -it'
alias kdel='kubectl delete'

# Context and namespace
alias kns='kubectl config set-context --current --namespace'
alias kctx='kubectl config use-context'

# Shortcuts
alias kcf='kubectl create -f'
alias kaf='kubectl apply -f'
alias kdf='kubectl delete -f'
```

## Troubleshooting

### Common Issues

**Pod stuck in Pending:**
```bash
# Check if there are enough resources
kubectl describe pod $POD_NAME | grep -i event

# Check node resources
kubectl describe node $NODE_NAME | grep -A 5 Allocatable
```

**Pod stuck in ContainerCreating:**
```bash
# Check image pull issues
kubectl describe pod $POD_NAME | grep -A 10 Events

# Check if image exists
kubectl get pod $POD_NAME -o jsonpath='{.spec.containers[0].image}'
```

**Pod CrashLoopBackOff:**
```bash
# Check logs
kubectl logs $POD_NAME --previous

# Check exit code
kubectl describe pod $POD_NAME | grep -A 5 LastState
```
