from slacker.logger import Logger

class Registrar:
  """Registrar keeps commands that have been registered with it."""

  def __init__(self):
    self.__commands = {}  # command name -> command instance
    self.logger = Logger(self.__class__.__name__).get()

  def register(self, command):
    """Registers a command by name."""

    if command.name() in self.__commands:
      raise ValueError("Command already registered: {}".format(command.name()))
    self.__commands[command.name()] = command

  def find(self, name):
    """Lookup command by name."""

    if name in self.__commands:
      return self.__commands[name]

    return None

  def action(self, name, args=None):
    """Convenience method to action command if name is found."""
    cmd = self.find(name)
    if cmd:
      cmd.action(args)
    else:
      self.logger.debug("Could not find and action command: {}".format(name))

  def count(self):
    """Returns the amount of commands registered."""
    return len(self.__commands)

  def commands(self):
    """Returns all registered command instances."""
    return self.__commands.values()

  def names(self):
    """Returns all registered command names."""
    return self.__commands.keys()

  def get_completer(self, command):
    command = command.strip().lower()
    instance = self.find(command)
    if not instance:
      return None
    return instance.make_completer()
