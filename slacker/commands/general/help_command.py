from slacker.commands.command import Command
from slacker.commands.argument_parser import ArgumentParser, DidNotExitException

class HelpCommand(Command):
  def __init__(self):
    super(HelpCommand, self).__init__()
    self.__instances = []

  def name(self):
    return "help"

  def description(self):
    return "Displays general help."

  def make_parser(self):
    self.__find_and_sort()
    choices = []
    for instance in self.__instances:
      choices.append(instance.name())
    parser = ArgumentParser(prog = self.name(), description = self.description())
    parser.add_argument("command", type = str, nargs = "?", choices = choices, metavar = "command",
                        help = "Get help on a specific command (same as 'command --help'). "
                               "Valid choices: {}".format(choices))
    return parser

  def __show(self, cmd):
    self.logger.info("  {:<20}{}".format(cmd.name(), cmd.description()))

  def __find_help(self, name):
    self.__find_and_sort()
    for instance in self.__instances:
      if instance.name() == name.strip():
        try:
          args = instance.parse_args(["--help"])
          if not args is None:
            instance.action(args)
          else:
            self.logger.info(instance.description())
        except DidNotExitException:
          pass
        return

  def __find_and_sort(self):
    """Finds all commands and sorts lexicographically if not already done."""
    if len(self.__instances) == 0:
      for cmd in Command.find_all():
        self.__instances.append(cmd())
      self.__instances.sort(key = lambda i: i.name())

  def action(self, args = None):
    if args.command:
      self.__find_help(args.command)
      return

    self.logger.info("Displaying available commands:")
    self.__find_and_sort()
    for instance in self.__instances:
      self.__show(instance)
