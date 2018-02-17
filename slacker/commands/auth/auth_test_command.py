from slacker.commands.command import Command
from slacker.commands.argument_parser import ArgumentParser
from slacker.environment.config import Config
from slacker.utility import verify_token

class AuthTestCommand(Command):
  def name(self):
    return "auth.test"

  def description(self):
    return "Checks authentication and describes user identity."

  def requires_token(self):
    return True

  def is_destructive(self):
    return False

  def make_parser(self):
    parser = ArgumentParser(prog=self.name(), description=self.description())
    parser.add_argument("-ws", "--workspace", choices=Config.get().workspaces(),
                        help="Check auth for specified workspace.")
    return parser

  def action(self, args=None):
    config = Config.get()
    if args and args.workspace:
      ws = args.workspace
      token = config.workspace_token(ws)
    else:
      ws = config.active_workspace()
      token = config.active_workspace_token()

    self.logger.debug("Checking auth for '{}'...".format(ws))

    data = verify_token(token)
    if not data:
      return False

    self.logger.info("Auth successful.")
    self.logger.debug("URL: {}".format(data["url"]))
    self.logger.debug("Workspace: {}".format(data["team"]))
    self.logger.debug("Workspace ID: {}".format(data["team_id"]))
    self.logger.debug("User: {}".format(data["user"]))
    self.logger.debug("User ID: {}".format(data["user_id"]))
    return True
