# slacker
Slacker is a tool designed to make it easier to do admin tasks and general utility for several workspaces (teams). It supports a REPL for inputting and evaluating commands, along with a CLI for running a single command.

# Table of Contents
* [First Run](#first-run)
* [Commands](#commands)
* [CLI Usage](#cli-usage)
* [Development Environment](#development-environment)
* [Contributing](#contributing)

# First Run
The first invocation of Slacker requires to setup a workspace using the `--init` argument:
```
% ./slacker.py --init
Input workspace token: ****************************************************************************
Added new workspace 'myworkspace' to config and made it active.
You can now run slacker normally.
myworkspace> 
```

Slacker is ready for use afterwards with "myworkspace" as the active workspace. _Note that it is recommended to employ a user token, not a bot token!_

# Commands
```
Displaying available commands:
  api.test            Checks that the Slack API is online.
  auth.test           Checks authentication and describes user identity.
  channels.list       Displays info about channels on Slack.
  chat.memessage      Post a me message to a channel on Slack.
  chat.postephemeral  Post ephemeral message to a channel on Slack that is only visible to assigned user.
  chat.postmessage    Post message to a channel on Slack.
  config              Shows current config state.
  emoji.list          Lists custom emojis in workspace
  exit                Exits Slacker.
  files.delete        Delete files uploaded to and stored on Slack.
  files.list          Displays info about files on Slack.
  help                Displays general help.
  log                 Displays current log level.
  users.list          Displays info about users on Slack.
  workspace           Displays predefined workspaces and which one is active.
```

# CLI Usage
```
usage: slacker.py [options] [-- command [args..]]

Useful Slack utilities and REPL.

optional arguments:
  -h, --help     show this help message and exit
  -V, --version  show program's version number and exit
  -v, --verbose  Sets the log level to DEBUG for this session.
  -q, --quiet    Disable stdout logging
  --init         Interactively initialize config and add workspace and API
                 token.
  --check        Checks that all commands are valid.
  --no-tests     Do not do API and auth tests at startup.

Most commands support -h|--help to see how they work. By passing '--', it
signals that Slacker arguments end and a single command and arguments begin.
Slacker will exit after running that command.
```

# Development Environment
Slacker is written in [Python 3](https://www.python.org/) and the required modules to be installed can be found in [requirements.txt](requirements.txt).

To setup a virtual development environment that doesn't pollute the general system it is expected that [virtualenv](https://virtualenv.pypa.io/en/stable/) for Python 3+ is installed.

Run `make setup` to install required modules to ".venv" in the root of the repository, and issue `source .venv/bin/activate` to activate the environment. From here, the `python`, `python3`, `pip` etc. will map to ".venv" and the modules installed into it.

# Contributing
See [CONTRIBUTING.md](CONTRIBUTING.md).
