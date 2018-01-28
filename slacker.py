#!/usr/bin/env python

import sys
import signal
from argparse import ArgumentParser

from slacker.commands.command import Command
from slacker.commands.registrar import Registrar
from slacker.environment.constants import VERSION
from slacker.environment.config import Config
from slacker.logger import Logger
from slacker.utility import bool_response

def signal_handler(signal, frame):
  print("\nCaught sig.. {}".format(signal))
  sys.exit(0)

def readline():
  try:
    config = Config.get()
    txt = "{}{}".format(config.active_workspace(), config.repl_prefix())
    return input(txt).strip()

  # Handle EOF/^D nicely.
  except: return None

def parse_line(line):
  if " " in line:
    return line.split(maxsplit = 1)
  return (line, None)

def process(line, reg):
  (cmd, args) = parse_line(line)

  instance = reg.find(cmd.lower())
  if not instance:
    print("Unknown command: {}".format(cmd))
    return

  if args:
    try:
      args = instance.parse_args(args.split())
    except: return
  instance.action(args)

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

  args = parser.parse_args(args)
  return (args, cmd_args)

def init():
  config = Config.get()
  if config.active_workspace():
    resp = bool_response("Config already has active workspace '{}'.\nContinue and overwrite?"
                         .format(config.active_workspace()))
    if not resp:
      print("Aborting!")
      return
    config.reset()

  workspace = ""
  while len(workspace) == 0:
    workspace = input("Workspace name: ").strip()

  token = ""
  while len(token) == 0:
    token = input("API token: ").strip()

  config.add_workspace(workspace, token)
  config.set_active_workspace(workspace)
  config.save()

  print("Added new workspace '{}' to config and made it active.\nYou can now run slacker normally."
        .format(workspace))

def main():
  slacker_logger = Logger(__name__).get()
  slacker_logger.debug('Starting Slacker...')

  # Load config explicitly.
  config = Config.get()

  (args, cmd_args) = parse_args()

  if args.init:
    init()
    return

  if not config.active_workspace():
    print("No workspace active!")
    print("Run slacker with --init to interactively create a workspace and config file.")
    return

  reg = Registrar()
  for cmd in Command.find_all():
    reg.register(cmd())

  if reg.count() == 0:
    print("No commands found!")
    sys.exit(-1)

  if cmd_args:
    process(" ".join(cmd_args), reg)
    return

  while True:
    line = readline()
    if line is None: break
    elif not line: continue
    process(line, reg)

if __name__ == '__main__':
  signal.signal(signal.SIGINT, signal_handler)

  main()
