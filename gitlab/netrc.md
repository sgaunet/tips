Configuring $HOME/.netrc is a good way to store your GitLab credentials for HTTPS access. This is especially useful when downloading private golang modules.

```bash
# Create or edit the .netrc file in your home directory
$ cat .netrc 
machine gitlab.com
    login yourlogin
    password <PERSONAL-ACCESS-TOKEN>
```
