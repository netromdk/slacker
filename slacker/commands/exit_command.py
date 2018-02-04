from .command import Command
import sys

class ExitCommand(Command):
  def name(self):
    return "exit"

  def description(self):
    return "Exits Slacker."

  def aliases(self):
    return ["q", "quit"]

  def action(self, args = None):
    self.logger.info("Exiting..")
    sys.exit(0)
