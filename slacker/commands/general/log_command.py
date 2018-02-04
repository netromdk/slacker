import logging

from slacker.commands.command import Command
from slacker.commands.argument_parser import ArgumentParser
from slacker.environment.config import Config
from slacker.logger import Logger

class LogCommand(Command):
  def name(self):
    return "log"

  def description(self):
    return "Displays current log level."

  def aliases(self):
    return ["l"]

  def make_parser(self):
    parser = ArgumentParser(prog = self.name(), description = self.description())
    parser.add_argument("-l", "--level", choices = Logger.level_names(),
                        help = "Set another log level.")
    return parser

  def action(self, args = None):
    if args.level:
      level = Logger.level_from_name(args.level)
      self.logger.debug('Set log level to: {}'.format(args.level))

      config = Config.get()
      config.set_log_level(level)
      config.save()

    else:
      level = logging.getLevelName(self.logger.getEffectiveLevel())
      self.logger.info("Log level: {}".format(level))
