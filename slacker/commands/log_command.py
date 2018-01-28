from .command import Command
from argparse import ArgumentParser
from slacker.environment.config import Config
from slacker.logger import Logger
import logging

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
    if not args:
      level = logging.getLevelName(self.logger.getEffectiveLevel())
      print("Log level: {}".format(level))

    elif args.level:
      level = Logger.level_from_name(args.level)
      self.logger.debug('Set log level to: {}'.format(args.level))

      config = Config.get()
      config.set_log_level(level)
      config.save()
