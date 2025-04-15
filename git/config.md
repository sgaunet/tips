# Git Configuration

```ini
[user]
    email = 1552102+sgaunet@users.noreply.github.com
    name = Sylvain
[core]
    editor = vim
    whitespace = fix,-indent-with-non-tab,trailing-space,cr-at-eol
[alias]
    st=status
    co=checkout
    ci=commit
    lg = log --graph --date=relative --pretty=tformat:'%Cred%h%Creset -%C(auto)%d%Creset %s %Cgreen(%an %ad)%Creset'

[push]
        autoSetupRemote = true

[url "ssh://git@gitlab.com"]
	insteadof = https://gitlab.com

[includeIf "gitdir:~/work/"]
    path = ~/.gitconfig-work
```
