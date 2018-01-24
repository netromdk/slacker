import os

# Slacker version
VERSION = '0.0.1'

# Bot token from Slack that Slacker uses.
SLACKER_BOT_TOKEN = os.getenv('SLACKER_BOT_TOKEN', None)

# Command prefix when dropping into an active TTY
COMMAND_PREFIX = '> '
