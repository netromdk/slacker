from abc import ABC, abstractmethod

class Command(ABC):
  """Command encapsulates a Slacker command with a name, description, help text, alises, and the
  action to perform.
  """

  @abstractmethod
  def name(self):
    """Returns the name of the command. This is the actual command, like 'download'."""
    pass

  @abstractmethod
  def description(self):
    """Returns the description of the command."""
    pass

  def help(self):
    """Returns the help text of the command."""
    return self.description()

  def aliases(self):
    """Returns a list of aliases defined for this command."""
    return None

  def make_parser(self):
    """Override to define argparse.ArgumentParser."""
    return None

  def parse_args(self, args):
    """Parse arguments from a list of strings. The output can be given to action()."""
    parser = self.make_parser()
    if not parser:
      return None
    return parser.parse_args(args)

  @abstractmethod
  def action(self, args = None):
    """Executes the action of the command with optional arguments parsed via parse_args()."""
    pass

  @staticmethod
  def find_all():
    """Finds all command classes deriving from Command."""
    cmds = set()
    for child in Command.__subclasses__():
      if child not in cmds:
        cmds.add(child)
    return cmds

