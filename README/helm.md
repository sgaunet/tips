## Development

### Prerequisites

* [task for development](https://taskfile.dev/#/)
* docker
* [pre-commit](https://pre-commit.com/)

### pre-commit hooks

There are hooks executed in the precommit stage. Once the project cloned on your disk, please install pre-commit and the hooks:

Install the hooks:

```bash
task dev:install-pre-commit
```

If you want to launch manually the pre-commmit hook:

```bash
task dev:pre-commit
```

## task

Use task to list available operations:

```bash
task -a
```

## CI/CD

On every commit:

* latest version is built and pushed to docker registry
* helm chart is packaged and deployed to unstable repository
* the latest version is deployed on PREPROD

On tag:

* version of the tag is built and pushed to docker registry
* helm chart is packaged and deployed to stable repository
* the version is deployed on PREPROD
* the version is deployed on PROD

