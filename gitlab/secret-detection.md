gitlab-ci.yml example:

```yml
stages:          
  - secret_scan

Secrets Detector:
  stage: secret_scan
  image:
    name: "registry.gitlab.com/gitlab-org/security-products/analyzers/secrets"
  needs: []
  only:
    - branches
  before_script:
    - apk add jq
  script:
    - /analyzer run
    - cat gl-secret-detection-report.json | jq '.'
    - if [[ $(jq '.vulnerabilities | length > 0' gl-secret-detection-report.json) == "true" ]]; then echo "secrets found" && exit 1; fi
```
