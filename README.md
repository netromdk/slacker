# slacker
Slacker is a tool designed to make it easier to do admin tasks and general utility for several workspaces (teams). It supports a REPL for inputting and evaluating commands, along with a CLI for running a single command.

# Table of Contents
* [First Run](#first-run)
* [General Commands](#general-commands)
* [CLI Usage](#cli-usage)
* [Development Environment](#development-environment)
* [Contributing](#contributing)

# First Run
The first invocation of Slacker requires to setup a workspace using the `--init` argument:
```sh
% ./slacker.py --init
Workspace name: myworkspace
API token: myworkspacetoken
Added new workspace 'myworkspace' to config and made it active.
You can now run slacker normally.
myworkspace> 
```

Slacker is ready for use afterwards with "myworkspace" as the active workspace. _Note that it is recommended to employ a user token, not a bot token!_

# General Commands
```
help         [h]        Displays general help.
workspace    [ws]       Displays predefined workspaces and which one is active.
log          [l]        Displays current log level.
auth.test    [t, test]  Checks authentication and describes user identity.
api.test                Checks that the Slack API is online.
exit         [q, quit]  Exits Slacker.
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

By passing '--', it signals that Slacker arguments end and a single command
and arguments begin. Slacker will exit after running that command.
```

# Development Environment
Slacker is written in [Python 3](https://www.python.org/) and the required modules to be installed can be found in [requirements.txt](requirements.txt).

To setup a virtual development environment that doesn't pollute the general system it is expected that [virtualenv](https://virtualenv.pypa.io/en/stable/) for Python 3+ is installed.

Run `make setup` to install required modules to ".venv" in the root of the repository, and issue `source .venv/bin/activate` to activate the environment. From here, the `python`, `python3`, `pip` etc. will map to ".venv" and the modules installed into it.

# Contributing
See [CONTRIBUTING.md](CONTRIBUTING.md).
