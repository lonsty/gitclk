# Git CLK

Git Command Line Kit, make it easier to use git from the command line.

Features:
- [x] [Quick set all git platforms remote settings](user-content-2-gitclk-remotes).
- [x] [Create github repository from command line](user-content-2-gitclk-create).
- [x] [Git push all branchs/tags to all remotes](user-content-2-git-pushallpushalltags).

## Quickstart

Clone & Install

```sh
$ git clone https://github.com/lonsty/gitclk.git
$ cd gitclk

$ ./install.sh
```

### Commands

#### 1. *gitclk-remotes*

Quick set all git platforms remote settings to git config.

a. Configure git platforms

```sh
$ gitclk-remotes config

# or
$ gitclk-remotes config -e
```

b. Set all Configured git platforms to git config

```sh
$ gitclk-remotes set -n <repository-name>
```

#### 2. *gitclk-create*

Create github repository from command line.

```sh
$ gitclk-create <user> <repository>
```

#### 3. *git pushall/pushalltags*

Git push all branchs to all remotes.

```sh
$ git pushall
```

Git push all tags to all remotes.

```sh
$ git pushalltags
```

## Others

#### Uninstall

```sh
$ ./uninstall.sh
```

#### Help

```sh
$ gitclk-remotes --help
$ gitclk-create --help
```

#### Author

- [Allen Shaw](http://github.com/lonsty)

#### [Changelog](CHANGELOG.md)