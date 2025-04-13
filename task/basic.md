
## Development

This project is using :

* [task for development](https://taskfile.dev/#/)
* docker
* [pre-commit](https://pre-commit.com/)

There are hooks executed in the precommit stage. Once the project cloned on your disk, please install pre-commit and the hooks:

Install the hooks:

```bash
task dev:install-pre-commit
```

If you want to launch manually the pre-commmit hook:

```bash
task dev:pre-commit
```

## CI/CD

* Every commit launches
  * the build of the latest image
  * the push on the registry.
  * the deployment in PREPROD
* Tag the commit will build/push the docker image with the same tag. [Use semver.](https://semver.org/lang/fr/)
  * and deploy the version in PROD


Taskfile.yml

```yml
# https://taskfile.dev
version: '3'
vars:
  IMAGE: myregistry:latest

includes:
  dev: Taskfile_dev.yml

tasks:

  check:
    internal: true
    desc: "Check the configuration"
    preconditions:
      - sh: test -f .git/hooks/pre-commit
        msg: "Configure pre-commit hooks with 'task dev:install-pre-commit'"

  default:
    desc: "List all tasks"
    deps:
      - check
    cmds:
      - task -a

  build:
    desc: "Build and push the image to the registry"
    deps:
      - check
    cmds:
      - docker build . -t  {{.IMAGE}}
      - docker push {{.IMAGE}}
      
  unit-tests:
    desc: "Run unit tests"
    cmds:
      - go generate ./...
      # - go test -v -coverpkg=./... -coverprofile=profile.cov ./...
      - go test -coverpkg=./... -coverprofile=profile.cov ./...
      - sed -i '/cmd\/send-mail/d' profile.cov
      - sed -i '/internal\/sftpserver/d' profile.cov
      - sed -i '/internal\/smtpserver/d' profile.cov
      - sed -i '/pkg\/logger/d' profile.cov
      - go tool cover -func profile.cov
      - rm profile.cov

  scan:
    desc: "Scan the image for vulnerabilities"
    deps:
      - check
    cmds:
      - echo Scan with trivy
      # - trivy image --exit-code 1 --no-progress --severity CRITICAL  {{.IMAGE}}
      - trivy image --format table {{.IMAGE}}
      - echo Scan with osv-scanner
      - osv-scanner -r .
      
  lint:
    desc: "Run the linter"
    cmds:
      - golangci-lint run

  tbls:
    desc: "Generate the database schema"
    cmds:
      # - rm -rf dbdoc
      - tbls doc --rm-dist --dsn "postgresql://postgres:password@localhost:5432/postgres?sslmode=disable"
      
  godoc:
    desc: "godoc server"
    cmds:
      - go install golang.org/x/tools/cmd/godoc@latest
      - echo "http://localhost:8080"
      - godoc -http :8080
```

Taskfile_dev.yml

```yml
# https://taskfile.dev
version: '3'

tasks:
  # install hooks
  install-pre-commit:
    desc: "Install pre-commit hooks"
    cmds:
      - pre-commit install

  pre-commit:
    desc: "Run pre-commit hooks"
    cmds:
      - pre-commit run --all-files

  check-pre-commit-setup:
    desc: "Check pre-commit setup"
    cmds:
      - test -f .git/hooks/pre-commit
```
