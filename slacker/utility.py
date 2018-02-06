import sys
import calendar

from argparse import ArgumentParser
from datetime import datetime, timedelta

from prompt_toolkit import prompt

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
    txt = "{}{}".format(config.active_workspace(), config.repl_prefix())
    return prompt(txt, completer=completer, history=history)

  # Handle EOF/^D nicely.
  except: return None

def parse_line(line):
  """ Parse line of text """
  if " " in line:
    return line.split(maxsplit = 1)
  return (line, None)

def create_logger(name):
  """Convenience function for creating a logger that respects quiet mode if set."""
  config = Config.get()
  logger = Logger(name, config.log_level()).get()
  if config.quiet_mode():
    logger.disable_stream_handler()
  return logger

def signal_handler(signal, frame):
  """Handle signal interrupts."""
  create_logger(__name__).info("Caught sig.. {}".format(signal))
  sys.exit(0)

def parse_args():
  # Divide arguments into slacker and single command args.
  args = sys.argv[1:]
  cmd_args = None
  try:
    div_index = args.index("--")
    cmd_args = args[div_index+1:]
    args = args[0:div_index]
  except: pass

  parser = ArgumentParser(description = "Useful Slack utilities and REPL.",
                          usage = "%(prog)s [options] [-- command [args..]]",
                          epilog = "Most commands support -h|--help to see how they work. By passing "
                                   "'--', it signals that Slacker arguments end and a "
                                   "single command and arguments begin. Slacker will exit after "
                                   "running that command.")
  parser.add_argument("-V", "--version", action = "version",
                      version = "%(prog)s {}".format(VERSION))
  parser.add_argument("-v", "--verbose", action = "store_true",
                      help = "Sets the log level to DEBUG for this session.")
  parser.add_argument("-q", "--quiet", action="store_true", help="Disable stdout logging")
  parser.add_argument("--init", action = "store_true",
                      help = "Interactively initialize config and add workspace and API token.")
  parser.add_argument("--check", action = "store_true",
                      help = "Checks that all commands are valid.")
  parser.add_argument("--no-tests", action = "store_true",
                      help = "Do not do API and auth tests at startup.")

  args = parser.parse_args(args)
  return (args, cmd_args)

def verify_token(token):
  try:
    return SlackAPI(token).post('auth.test')
  except Exception as ex:
    create_logger(__name__).warning(ex)
  return None
