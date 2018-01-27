from abc import ABC, abstractmethod
from slacker.logger import Logger
import re

# The "." can only be in the middle of the command name.
COMMAND_NAME_REGEX = re.compile("([\w\d][\w\d\.]*)?[\w\d]+")

class Command(ABC):
  """Command encapsulates a Slacker command with a name, description, help text, alises, and the
  action to perform.
  """

  def __init__(self):
    self.__validate()
    self.logger = Logger(self.__class__.__name__).get()

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

  def __validate(self):
    """Validates that the command is valid and conforming with the requirements."""
    derive_cls = type(self).__mro__[0]

    if not COMMAND_NAME_REGEX.fullmatch(self.name()):
      raise ValueError("Command name is invalid '{}' in {}".format(self.name(), derive_cls))

    a = self.aliases()
    if a is not None and type(a) != type(()) and type(a) != type([]):
      raise ValueError("Command aliases must be either a set, a list or None: '{}', {} in {}"
                       .format(a, type(a), derive_cls))
    elif a:
      for alias in a:
        if not COMMAND_NAME_REGEX.fullmatch(alias):
          raise ValueError("Command alias is invalid '{}' in {}".format(alias, derive_cls))

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
