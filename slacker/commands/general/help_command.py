from slacker.commands.command import Command

class HelpCommand(Command):
  def name(self):
    return "help"

  def description(self):
    return "Displays general help."

  def __show(self, cmd):
    self.logger.info("  {:<20}{}".format(cmd.name(), cmd.description()))

  def action(self, args = None):
    self.logger.info("Displaying available commands:")
    instances = []
    for cmd in Command.find_all():
      instances.append(cmd())
    instances.sort(key = lambda i: i.name())
    for instance in instances:
      self.__show(instance)
