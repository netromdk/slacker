from .command import Command

class HelpCommand(Command):
  def name(self):
    return "help"

  def description(self):
    return "Displays general help."

  def aliases(self):
    return ["h"]

  def __show(self, cmd):
    aliases = ""
    if cmd.aliases():
      aliases = " [{}]".format(", ".join(cmd.aliases()))
    self.logger.info("  {:<12}{:<12}{}".format(cmd.name(), aliases, cmd.description()))

  def action(self, args = None):
    self.logger.info("Displaying available commands:")
    for cmd in Command.find_all():
      self.__show(cmd())
