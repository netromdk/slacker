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

  @abstractmethod
  def help(self):
    """Returns the help text of the command."""
    pass

  def aliases(self):
    """Returns a list of aliases defined for this command."""
    return None

  @abstractmethod
  def action(self):
    """Executes the action of the command."""
    pass

  @staticmethod
  def find_all():
    """Finds all command classes deriving from Command."""
    cmds = set()
    for child in Command.__subclasses__():
      if child not in cmds:
        cmds.add(child)
    return cmds

