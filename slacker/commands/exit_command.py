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
    print("Exitting..")
    sys.exit(0)
