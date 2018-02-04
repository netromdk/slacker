from slacker.commands.command import Command
from slacker.commands.argument_parser import ArgumentParser
from slacker.environment.config import Config
from slacker.slack_api import SlackAPI, SlackAPIException

class AuthTestCommand(Command):
  def name(self):
    return "auth.test"

  def description(self):
    return "Checks authentication and describes user identity."

  def make_parser(self):
    parser = ArgumentParser(prog = self.name(), description = self.description())
    parser.add_argument("-ws", "--workspace", choices = Config.get().workspaces(),
                        help = "Check auth for specified workspace.")
    return parser

  def action(self, args = None):
    config = Config.get()
    if args and args.workspace:
      ws = args.workspace
      token = config.workspace_token(ws)
    else:
      ws = config.active_workspace()
      token = config.active_workspace_token()

    self.check(ws, token)

  def check(self, workspace, token):
    self.logger.debug("Checking auth for '{}'...".format(workspace))

    data = SlackAPI(token).post('auth.test')
    if not 'ok' in data:
      raise SlackAPIException('Invalid response! {}'.format(data))

    if not data['ok']:
      error = ''
      if 'error' in data:
        error = data['error']
      raise SlackAPIException('Unsuccessful: error: {}'.format(error))

    self.logger.info("Auth successful!")
    self.logger.info("URL: {}".format(data['url']))
    self.logger.info("Workspace: {}".format(data['team']))
    self.logger.info("Workspace ID: {}".format(data['team_id']))
    self.logger.info("User: {}".format(data['user']))
    self.logger.info("User ID: {}".format(data['user_id']))
    return True
