# Contributing
Contributions are very welcome for bug fixes particularly but also features that make sense to the project. Any existing issues labeled ["help wanted"](https://github.com/netromdk/slacker/labels/help%20wanted) and ["good first issue"](https://github.com/netromdk/slacker/labels/good%20first%20issue) are free to be pursued. And don't hesitate to open new issues.

Before opening a pull request, please first run `make check` to make sure the environment, style, and commands are valid, especially the one you're making.

## Code Style Guidelines
We follow [PEP8](https://www.python.org/dev/peps/pep-0008/) as the general style guide with a few extra items:
* 2 spaces instead of a tab character
* Double quotes around strings and single quotes for substrings: `"Hello 'world'!"`

The following guidelines are **ignored** and not checked for:
* E111 indentation is not a multiple of four
* E114 indentation is not a multiple of four (comment)
* E121 continuation line under-indented for hanging indent
* E126 continuation line over-indented for hanging indent
* E302 expected 2 blank lines

## Adding a new command
Commands reside in `slacker.commands` under the their category, like "files/" or "chat/". "general/" is reserved for commands that aren't related to Slack API methods directly.

When adding a new command, follow these steps:
1. Implement `"slacker/commands/CATEGORY/name_command.py"`
2. In `"slacker/commands/__init__.py"`, import the new command, like `from .CATEGORY import name_command`, and add its name to `__all__`
3. Add to vulture whitelist in `".vulture_whitelist.py"`, like `wl.NewCommand`, to not give false positives in static analysis

Notes and requirements:
* The file name of the command must follow the name of the API method, like `files.list` -> `files_list_command.py`
* The command name must match `"([\w\d][\w\d\.]*)?[\w\d]+"`, which means it can be letters and digits with periods in between but not at the ends
* `slacker.commands.argument_parser.ArgumentParser` is required when needing command arguments so that the argument names and meta can be used in the REPL for auto-completion
* If `Command.requires_token` isn't overridden, it will default to `False` and the active workspace token isn't included when using Slack API methods in the command with `Command.slack_api_post` or `Command.slack_api_download_file`, for instance
* If `Command.is_destructive` isn't overridden, it will default to `True` and the command will not be run if read-only mode is active
