# Git CLK

Git Command Line Kit, make it easier to use git from the command line.

Features:
- [x] Quick add all git platforms remote settings to git config.
- [x] Create github repository from command line.

## Quickstart

Clone & Install

```shell script
$ git clone https://github.com/lonsty/gitclk.git
$ cd gitclk

$ ./install.sh
```

### Commands

#### 1. `gitclk-remotes`

Quick add all git platforms remote settings to git config.

a. Configure git platforms

```shell script
$ gitclk-remotes config -e

# or
$ gitclk-remotes config
```

b. Add all Configured git platforms to git config

```shell script
$ gitclk-remotes add -n <repository-name>
```

#### 2. `gitclk-create`

Create github repository from command line.

```shell script
$ gitclk-create <user> <repository>
```

## Others

#### Uninstall

```shell script
$ ./uninstall.sh
```

#### Help

```shell script
$ gitclk-remotes --help
$ gitclk-create --help
```

#### Author

- [Allen Shaw](http://github.com/lonsty)

#### [Changelog](CHANGELOG.md)