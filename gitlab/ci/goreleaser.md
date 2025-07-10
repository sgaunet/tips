
# GoReleaser GitLab CI Configuration

This GitLab CI configuration provides automated build and release pipeline for Go applications using GoReleaser. It includes unit testing, snapshot builds for development, and automated releases with Docker image publishing to both GitLab Container Registry and optional external registries.

```yaml
# create an access token for the specific project (scope api / role developer)
# add the generated token in the variables of CI/CD: GITLAB_TOKEN
#
.snippets:
  config-docker-script: |
    test ! -d $HOME/.docker && mkdir $HOME/.docker
    if [ -z "$EXTERNAL_CI_REGISTRY" ] || [ -z "$EXTERNAL_CI_REGISTRY_USER" ] || [ -z "$EXTERNAL_CI_REGISTRY_PASSWORD" ]
    then
      echo "INFO: No EXTERNAL REGISTRY SETUP"
      echo "{ \"auths\": { \"${CI_REGISTRY}\": { \"username\": \"${CI_REGISTRY_USER}\", \"password\": \"${CI_JOB_TOKEN}\" } } }" > "$HOME/.docker/config.json"
    else
      CI_REGISTRY_AUTH=$(echo -n ${CI_REGISTRY_USER}:${CI_JOB_TOKEN} | base64 | tr -d "\n")
      EXTERNAL_CI_REGISTRY_AUTH=$(echo -n ${EXTERNAL_CI_REGISTRY_USER}:${EXTERNAL_CI_REGISTRY_PASSWORD} | base64 | tr -d "\n")

      echo -e "{ \"auths\": { \"${CI_REGISTRY}\": \n{ \"auth\": \"${CI_REGISTRY_AUTH}\" } ,\n\
                  \"${EXTERNAL_CI_REGISTRY}\": \n{ \"auth\": \"${EXTERNAL_CI_REGISTRY_AUTH}\" } }}" > "$HOME/.docker/config.json"
    fi

  config-netrc: |
    echo "machine gitlab.com" > ~/.netrc
    echo "  login gitlab-ci-token" >> ~/.netrc
    echo "  password ${CI_JOB_TOKEN}" >> ~/.netrc
    chmod 600 ~/.netrc

stages:
  - build
  - test
  - release
  - deploy

unit-tests:
  stage: test
  services:
    - docker:20.10.16-dind
  image:
    name: golang:1.22.1
    entrypoint: [""]
  script:
    - !reference [ .snippets, config-netrc ]
    - go test -v ./...

build-snapshot:
  stage: build
  image:
    name: goreleaser/goreleaser:v1.25.0-nightly
    # name: goreleaser/goreleaser:v1.25.0
    entrypoint: ['']
  # only:
  #   - tags
  services:
    - docker:20.10.16-dind
  variables:
    # Disable shallow cloning so that goreleaser can diff between tags to
    # generate a changelog.
    GIT_DEPTH: 0
  script:
    - !reference [ .snippets, config-netrc ]
    - goreleaser --snapshot --clean
    # create latest
    - !reference [ .snippets, config-docker-script ]
    - docker tag registry.gitlab.com/my-namespace/my-project:latest-amd64 registry.gitlab.com/my-namespace/my-project:latest
    - docker push registry.gitlab.com/my-namespace/my-project:latest

build-release:
  stage: release
  image:
    name: goreleaser/goreleaser:v1.25.0-nightly
    # name: goreleaser/goreleaser:v1.25.0
    entrypoint: ['']
  only:
    - tags
  services:
    - docker:20.10.16-dind
  variables:
    # Disable shallow cloning so that goreleaser can diff between tags to
    # generate a changelog.
    GIT_DEPTH: 0
    # GITLAB_TOKEN: $GITLAB_TOKEN
  script:
    - !reference [ .snippets, config-netrc ]
    - !reference [ .snippets, config-docker-script ]
    - goreleaser --clean
```
