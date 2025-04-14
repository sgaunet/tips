### pre-commit

There are hooks executed in the git precommit stage. Once the project cloned on your disk, please install pre-commit:

> For Windows/Linux, Go to [https://pre-commit.com/#install](https://pre-commit.com/#install)
> For MacOS `brew install pre-commit`

Install tools:

```bash
task dev:prereq
```

And install the hooks:

```bash
task dev:install-pre-commit
```

To launch manually the pre-commmit hook:

```bash
task dev:pre-commit
```
