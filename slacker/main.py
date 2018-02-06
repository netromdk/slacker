# Main entry point for slacker

import sys
import signal
import logging

from slacker.commands import auth_test_command
from slacker.commands.command import Command
from slacker.commands.registrar import Registrar
from slacker.commands.argument_parser import DidNotExitException
from slacker.environment.config import Config
from slacker.logger import Logger
from slacker.slack_api import SlackAPIException
from slacker.utility import readline, parse_line, signal_handler, parse_args

from prompt_toolkit import prompt
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.contrib.completers import WordCompleter
from prompt_toolkit.shortcuts import confirm

slacker_logger = None
config = None

def process(line, reg):
  (cmd, args) = parse_line(line)

  instance = reg.find(cmd.lower())
  if not instance:
    slacker_logger.info("Unknown command: {}".format(cmd))
    return

  # Try parsing even with no arguments so default values are returned in the arguments namespace, if
  # any.
  try:
    args = instance.parse_args([] if not args else args.split())
  except DidNotExitException:
    # If --help is used with a command then we don't exit the program!
    return
  except Exception as ex:
    slacker_logger.error('Error: {}'.format(ex))
    return

  try:
    instance.action(args)
  except Exception as e:
    slacker_logger.warning(str(e))

def check():
  slacker_logger.debug('Checking all commands for validty..')
  reg = Registrar()
  for cmd in Command.find_all():
    try:
      reg.register(cmd())
    except Exception as ex:
      slacker_logger.error('Command failed check: {}'.format(cmd))
      slacker_logger.error('Error: {}'.format(ex))
      sys.exit(-1)
  slacker_logger.info('All good: {} valid commands'.format(reg.count()))

def build_prompt_completer(register):
  """Build REPL completion dictionary"""
  cmds = []
  cmds_meta = {}
  for cmd in register.commands():
    cmd_name = cmd.name()
    cmds.append(cmd_name)
    cmds_meta[cmd_name] = cmd.description()

  return WordCompleter(cmds, meta_dict=cmds_meta, ignore_case=True)


def init():
  if config.active_workspace():
    resp = confirm("Config already has active workspace '{}'.\nContinue and overwrite? "
                   .format(config.active_workspace()))
    if not resp:
      slacker_logger.error("Aborting!")
      return
    config.reset()

  workspace = ""
  while len(workspace) == 0 or workspace in config.workspaces():
    workspace = input("Workspace name: ").strip()

  token = ""
  auth_test = auth_test_command.AuthTestCommand()
  while len(token) == 0 or not auth_test.check(workspace, token):
    token = prompt('API token: ', is_password = True).strip()

  config.add_workspace(workspace, token)
  config.set_active_workspace(workspace)
  config.save()

  slacker_logger.info("Added new workspace '{}' to config and made it active.\n"
                      "You can now run slacker normally.".format(workspace))

def start_slacker():
  signal.signal(signal.SIGINT, signal_handler)
  (args, cmd_args) = parse_args()

  global config
  config = Config.get(args.quiet)

  global slacker_logger
  slacker_logger = Logger(__name__, config.log_level()).get()

  # Disable the registered startup logger stream handlers
  if args.quiet:
    Logger.disable_stream_handlers()

  slacker_logger.debug('Starting Slacker...')

  if args.check:
    check()
    return

  if args.init:
    init()

  if not config.active_workspace():
    slacker_logger.error("No workspace active!")
    slacker_logger.error("Run slacker with --init to interactively create a workspace and config file.")
    return

  reg = Registrar()
  for cmd in Command.find_all():
    reg.register(cmd())

  if reg.count() == 0:
    slacker_logger.error("No commands found!")
    sys.exit(-1)

  if args.verbose:
    Logger.set_level(logging.DEBUG)
    slacker_logger.debug('Verbose mode setting debug session log level.')

  if args.quiet:
    Logger.disable_stream_handlers()

  try:
    if not args.no_tests:
      reg.action('api.test')
      reg.action('auth.test')
  except Exception as ex:
    slacker_logger.error(str(ex))
    slacker_logger.warning('Make sure you have internet access and verify your tokens!')
    sys.exit(-1)

  if cmd_args:
    process(" ".join(cmd_args), reg)
    return

  completer = build_prompt_completer(reg)
  in_memory_history = InMemoryHistory()

  while True:
    line = readline(completer, in_memory_history)
    if line is None: break
    elif not line: continue
    process(line, reg)
