import json
from slacker.commands.command import Command
from slacker.environment.config import Config

class ConfigCommand(Command):
  def name(self):
    return "config"

  def description(self):
    return "Shows current config state."

  def action(self, args = None):
    config = Config.get()
    self.logger.info("Current config state of '{}'".format(config.file_path()))
    self.logger.info(json.dumps(config.safe_dict(), indent = 2))
