import sys
import calendar

from argparse import ArgumentParser
from datetime import datetime, timedelta

from slacker.environment.constants import VERSION
from slacker.environment.config import Config
from slacker.logger import Logger

logger = Logger(__name__, Config.get().log_level()).get()

def bool_response(msg, default = False):
  """Shows msg and retrieves input as yes/y or no/n, where the meaning of an empty/ENTER reply is
  defined by the default argument: if False it's "yN" and otherwise "Yn".
  """
  choices = "Yn" if default else "yN"
  while True:
    try:
      resp = input("{} [{}] ".format(msg.strip(), choices)).strip().lower()
      break

    # Ask again on ^D.
    except EOFError:
      print("")
      continue

  return resp == "y" or resp == "yes" or (default and len(resp) == 0)

def ts_add_days(days):
  """Add an amount (+/-) of days to current timestamp in UTC."""
  return calendar.timegm((datetime.now() + timedelta(days)).utctimetuple())

def readline():
  """ Set prompt and read input """
  try:
    config = Config.get()
    txt = "{}{}".format(config.active_workspace(), config.repl_prefix())
    return input(txt).strip()

  # Handle EOF/^D nicely.
  except: return None

def parse_line(line):
  """ Parse line of text """
  if " " in line:
    return line.split(maxsplit = 1)
  return (line, None)

def signal_handler(signal, frame):
  """ Handle signal interrupts """
  logger.info("Caught sig.. {}".format(signal))
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
                          epilog = "By passing '--', it signals that Slacker arguments end and a "
                                   "single command and arguments begin. Slacker will exit after "
                                   "running that command.")
  parser.add_argument("-V", "--version", action = "version",
                      version = "%(prog)s {}".format(VERSION))
  parser.add_argument("--init", action = "store_true",
                      help = "Interactively initialize config and add workspace and API token.")
  parser.add_argument("-v", "--verbose", action = "store_true",
                      help = "Sets the log level to DEBUG for this session.")

  parser.add_argument("-q", "--quiet", action="store_true", help="Disable stdout logging")

  args = parser.parse_args(args)
  return (args, cmd_args)
