# Git Configuration

```ini
[user]
  email = 1552102+sgaunet@users.noreply.github.com
  name = Sylvain

[core]
  editor = vim
  whitespace = fix,-indent-with-non-tab,trailing-space,cr-at-eol
  compression = 9
  preloadindex = true

[status]
  showStash = true
  branch = true
  showUntrackedFiles = all

[pager]
  diff = diff-so-fancy | $PAGER

[diff-so-fancy]
  markEmptyLines = false

[color "diff"]
  meta = black bold
  frag = magenta
  context = white
  whitespace = yellow reverse
  old = red

[interactive]
  diffFilter = diff-so-fancy --patch
  singlekey = true

[push]
  autoSetupRemote = true
  followTags = true

[log]
  abbrevCommit = true
  graphColors = blue,yellow,cyan,magenta,green,red

[color "decorate"]
  branch = blue
  tag = yellow
  HEAD = red
  remoteBranch = magenta

[branch]
  sort = -committerdate

[tag]
  sort = -taggerdate

[alias]
  lg = log --graph --date=relative --pretty=tformat:'%Cred%h%Creset -%C(auto)%d%Creset %s %Cgreen(%an %ad)%Creset'

[url "ssh://git@gitlab.com"]
  insteadOf = https://gitlab.com

[includeIf "gitdir:~/work/"]
  path = ~/.gitconfig-work
```
