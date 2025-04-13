
## Release Process

Please note that this project does not currently have an automated CI/CD pipeline. The release process is manual and involves the following steps:

### Building and Publishing a Release

- Create a Git Tag:
  - Tag the desired commit with the new version number
  - Example: git tag v1.0.0
- Build Docker Image:
    - Manually build the Docker image for the release
    - Example: docker build -t myproject:v1.0.0 .
- Push to Docker Registry:
    - Push the newly built image to your Docker registry
    - Example: docker push myregistry.com/myproject:v1.0.0

## Deployment

Use the ... project to deploy the application

### Important Notes

* Always ensure you're working with the latest code before creating a release
* Test the Docker image locally before pushing to the registry
* Verify the Kubernetes manifests are correctly updated before deployment

**This manual process allows for careful control over releases but requires attention to detail. Future improvements may include automating this process through a CI/CD pipeline.**
