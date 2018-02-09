from slacker.commands.command import Command

class HelpCommand(Command):
  def __init__(self):
    super(HelpCommand, self).__init__()
    self.__instances = []

  def name(self):
    return "help"

  def description(self):
    return "Displays general help."

  def __show(self, cmd):
    self.logger.info("  {:<20}{}".format(cmd.name(), cmd.description()))

  def action(self, args = None):
    self.logger.info("Displaying available commands:")

    # Find and sort all command instances only the first time.
    if len(self.__instances) == 0:
      for cmd in Command.find_all():
        self.__instances.append(cmd())
      self.__instances.sort(key = lambda i: i.name())

    for instance in self.__instances:
      self.__show(instance)
