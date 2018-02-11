import json

from slacker.commands.command import Command
from slacker.commands.argument_parser import ArgumentParser
from slacker.environment.config import Config

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
    parser.set_defaults(read_only = None)
    return parser

  def action(self, args = None):
    config = Config.get()

    if not args.read_only is None:
      config.set_read_only(args.read_only)
      config.save()

    self.logger.info("Current config state of '{}'".format(config.file_path()))
    self.logger.info(json.dumps(config.safe_dict(), indent = 2))
