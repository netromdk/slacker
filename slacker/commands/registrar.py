from slacker.logger import Logger
from slacker.environment.config import Config

class Registrar:
  """Registrar keeps commands that have been registered with it."""

  def __init__(self):
    self.__commands = {} # command name -> command instance
    self.__aliases = {} # alias -> command name
    self.logger = Logger(self.__class__.__name__, Config.get().log_level()).get()

  def register(self, command):
    """Registers a command by name and aliases."""

    # Add command.
    if command.name() in self.__commands:
      raise ValueError("Command already registered: {}".format(command.name()))
    self.__commands[command.name()] = command

    # Add aliases.
    if not command.aliases():
      return
    for alias in command.aliases():
      if alias in self.__commands:
        raise ValueError("Alias '{}' of command '{}' already registered as command '{}'"
                         .format(alias, command.name(), alias))
      elif alias in self.__aliases:
        other_cmd = self.__aliases[alias]
        raise ValueError("Alias '{}' of command '{}' already registered for command '{}'"
                         .format(alias, command.name(), other_cmd))
      self.__aliases[alias] = command.name()

  def find(self, name):
    """Lookup command by name and aliases."""

    if name in self.__commands:
      return self.__commands[name]

    if name in self.__aliases:
      return self.__commands[self.__aliases[name]]

    return None

  def action(self, name, args = None):
    """Convenience method to action command if name is found."""
    cmd = self.find(name)
    if cmd:
      cmd.action(args)
    else:
      self.logger.debug('Could not find and action command: {}'.format(name))

  def count(self):
    """Returns the amount of commands registered."""
    return len(self.__commands)

  def commands(self):
    """Returns all registered command instances."""
    return self.__commands.values()

  def names(self):
    """Returns all registered command names."""
    return self.__commands.keys()

  def aliases(self):
    """Returns all registered command aliases."""
    return self.__aliases.keys()
