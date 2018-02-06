from slacker.commands.command import Command
from slacker.commands.argument_parser import ArgumentParser
from slacker.environment.config import Config
from slacker.utility import workspace_token_prompt

class WorkspaceCommand(Command):
  def name(self):
    return "workspace"

  def description(self):
    return "Displays predefined workspaces and which one is active."

  def make_parser(self):
    parser = ArgumentParser(prog = self.name(), description = "Displays predefined workspaces.")
    parser.add_argument("-s", "--set", metavar = "WORKSPACE",
                        help = "Set another workspace active.")
    parser.add_argument("-c", "--create", action = 'store_true', help = "Create a workspace.")
    parser.add_argument("-r", "--remove", metavar = "WORKSPACE", help = "Remove a workspace.")
    return parser

  def action(self, args = None):
    config = Config.get()

    if args.set:
      workspace = args.set
      if workspace == config.active_workspace():
        self.logger.warning("Workspace already active!")
        return
      elif not workspace in config.workspaces():
        self.logger.warning("Unknown workspace: '{}'".format(workspace))
        return

      config.set_active_workspace(workspace)
      config.save()

    elif args.create:
      (workspace, token) = workspace_token_prompt()
      config.add_workspace(workspace, token)
      config.save()

    elif args.remove:
      workspace = args.remove
      config.remove_workspace(workspace)
      config.save()

    self.logger.info("Workspaces:")
    for workspace in config.workspaces():
      active = " (active)" if (config.active_workspace() == workspace) else ""
      self.logger.info("  {}{}".format(workspace, active))
