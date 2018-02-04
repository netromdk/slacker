from slacker.commands.command import Command
from slacker.commands.argument_parser import ArgumentParser
from slacker.environment.config import Config

class WorkspaceCommand(Command):
  def name(self):
    return "workspace"

  def description(self):
    return "Displays predefined workspaces and which one is active."

  def aliases(self):
    return ["ws"]

  def make_parser(self):
    parser = ArgumentParser(prog = self.name(), description = "Displays predefined workspaces.")
    parser.add_argument("-s", "--set", metavar = "WORKSPACE",
                        help = "Set another workspace active.")
    return parser

  def action(self, args = None):
    config = Config.get()
    workspaces = config.workspaces()

    if args.set:
      workspace = args.set
      if workspace == config.active_workspace():
        self.logger.warning("Workspace already active!")
        return
      elif not workspace in workspaces:
        self.logger.warning("Unknown workspace: '{}'".format(workspace))
        return

      config.set_active_workspace(workspace)
      config.save()

    else:
      self.logger.info("Predefined workspaces:")
      for workspace in workspaces:
        active = " (active)" if (config.active_workspace() == workspace) else ""
        self.logger.info("  {}{}".format(workspace, active))
