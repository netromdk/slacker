import sys
import json

from slacker.commands.command import Command
from slacker.commands.argument_parser import ArgumentParser
from slacker.environment.config import Config

from prompt_toolkit.shortcuts import confirm

class ConfigCommand(Command):
  def name(self):
    return "config"

  def description(self):
    return "Shows current config state."

  def make_parser(self):
    parser = ArgumentParser(prog = self.name(), description = self.description())
    parser.add_argument("--set-read-only", dest = "read_only", action = 'store_true',
                        help = "Set read-only mode.")
    parser.add_argument("--unset-read-only", dest = "read_only", action = 'store_false',
                        help = "Unset read-only mode.")
    parser.add_argument("--reset", action = 'store_true',
                        help = "Reset all config values to default and exit slacker (be careful!).")
    parser.set_defaults(read_only = None)
    return parser

  def action(self, args = None):
    config = Config.get()

    if not args.read_only is None:
      config.set_read_only(args.read_only)
      config.save()

    elif args.reset:
      if config.read_only():
        self.logger.warning('Cannot reset config in read-only mode!')
        return
      if confirm('Resetting will close slacker and requires --init again.\n'
                 'Are you sure you want to reset the config? '):
        config.reset()
        config.save()
        sys.exit(0)
      return

    self.logger.info("Current config state of '{}'".format(config.file_path()))
    self.logger.info(json.dumps(config.safe_dict(), indent = 2))
