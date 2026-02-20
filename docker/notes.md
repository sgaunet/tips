# Docker Tips & Notes

## Multi-Architecture Docker Images

### Example Projects (Go + GoReleaser)
* [gitlab-backup](https://github.com/sgaunet/gitlab-backup) - GitLab backup utility
* [s3xplorer](https://github.com/sgaunet/s3xplorer) - S3 bucket explorer

## OCI Image Labels

Standard labels for container metadata:

```dockerfile
# Required labels
LABEL org.opencontainers.image.source="https://github.com/owner/repo"
LABEL org.opencontainers.image.description="Brief description of the image"
LABEL org.opencontainers.image.licenses="MIT"

# Optional but recommended
LABEL org.opencontainers.image.authors="Your Name <email@example.com>"
LABEL org.opencontainers.image.documentation="https://github.com/owner/repo"
LABEL org.opencontainers.image.version="${VERSION}"
LABEL org.opencontainers.image.created="${BUILD_DATE}"
```

## Multi-Architecture Builds with Buildx

```bash
docker run --privileged --rm tonistiigi/binfmt --install all
```

### Setup Builder
```bash
# Create multi-arch builder
docker buildx create --name multi-arch \
  --platform "linux/arm64,linux/amd64,linux/arm/v7" \
  --driver "docker-container"

# Use the builder
docker buildx use multi-arch

# Verify platforms
docker buildx inspect --bootstrap
```

### Security
```dockerfile
# Run as non-root
RUN adduser -D -g '' appuser
USER appuser

# Use distroless or minimal base images
FROM gcr.io/distroless/static:nonroot

# Don't expose unnecessary ports
# Scan images: docker scout cves image:tag
```
