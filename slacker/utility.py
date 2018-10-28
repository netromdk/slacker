import sys
import calendar
import shlex

from argparse import ArgumentParser
from datetime import datetime, timedelta
from string import Template

from prompt_toolkit import prompt
from prompt_toolkit.shortcuts import confirm

from slacker.environment.constants import VERSION
from slacker.environment.config import Config
from slacker.logger import Logger
from slacker.slack_api import SlackAPI

def ts_add_days(days):
  """Add an amount (+/-) of days to current timestamp in UTC."""
  return calendar.timegm((datetime.now() + timedelta(days)).utctimetuple())

def readline(completer, history):
  """ Set prompt and read input """
  try:
    config = Config.get()
    read_only = ""
    if config.read_only():
      read_only = config.read_only_str()
    tmpl_fill = dict(w=config.active_workspace(), ro=read_only)
    s = Template(config.repl_prompt())
    txt = s.safe_substitute(tmpl_fill)
    return prompt(txt, completer=completer, history=history)

  # Handle EOF/^D nicely.
  except BaseException:
    return None

def parse_line(line_or_args):
  """Parse line or list of text into (cmd, rest of args)."""
  if isinstance(line_or_args, list):
    return (line_or_args[0], line_or_args[1:])
  try:
    if " " in line_or_args:
      (cmd, args) = line_or_args.split(maxsplit=1)
      return (cmd, shlex.split(args))
  except ValueError:
    pass
  return (line_or_args.strip(), None)

def signal_handler(signal, _callback, *args):
  """Handle signal interrupts."""
  Logger(__name__).get().info("Caught sig.. {}".format(signal))
  sys.exit(0)

def parse_args():
  # Divide arguments into slacker and single command args.
  args = sys.argv[1:]
  cmd_args = None
  try:
    div_index = args.index("--")
    cmd_args = args[div_index + 1:]
    args = args[0:div_index]
  except ValueError:
    pass

  parser = ArgumentParser(description="Useful Slack utilities and REPL.",
                          usage="%(prog)s [options] [-- command [args..]]",
                          epilog="Most commands support -h|--help to see how they work. By passing "
                                 "'--', it signals that Slacker arguments end and a "
                                 "single command and arguments begin. Slacker will exit after "
                                 "running that command.")
  parser.add_argument("-V", "--version", action="version",
                      version="%(prog)s {}".format(VERSION))
  parser.add_argument("-v", "--verbose", action="store_true",
                      help="Sets the log level to DEBUG for this session.")
  parser.add_argument("-q", "--quiet", action="store_true", help="Disable stdout logging")
  parser.add_argument("--init", action="store_true",
                      help="Interactively initialize config and add workspace and API token.")
  parser.add_argument("--check", action="store_true",
                      help="Checks that all commands are valid.")
  parser.add_argument("--no-tests", action="store_true",
                      help="Do not do API and auth tests at startup.")

  args = parser.parse_args(args)
  return (args, cmd_args)

def verify_token(token):
  try:
    return SlackAPI(token=token, requires_token=True, is_destructive=False).post("auth.test")
  except Exception as ex:
    Logger(__name__).get().warning(ex)
  return None

def workspace_token_prompt(msg="Input workspace token: "):
  logger = Logger(__name__).get()
  config = Config.get()
  workspace = ""
  token = ""
  while True:
    token = prompt(msg, is_password=True).strip()
    if len(token) == 0:
      continue
    data = verify_token(token)
    if not data:
      continue
    workspace = data["team"]
    if workspace in config.workspaces():
      logger.warning("Workspace of token already exists: {}".format(workspace))
      continue
    return (workspace, token)

class AbortConfirmation(Exception):
    pass

def ask_abort(msg="Do you want to abort?", abort_on_yes=True):
  if confirm(msg.strip() + " ") == abort_on_yes:
    Logger(__name__).get().info("Aborting!")
    raise AbortConfirmation()
