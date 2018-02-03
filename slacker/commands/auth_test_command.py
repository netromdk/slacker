import json
import requests
from .command import Command
from slacker.environment.config import Config

class AuthTestCommand(Command):
  def name(self):
    return "auth.test"

  def description(self):
    return "Checks authentication and describes user identity."

  def aliases(self):
    return ['t', 'test']

  def action(self, args = None):
    config = Config.get()
    ws = config.active_workspace()
    token = config.active_workspace_token()

    self.logger.debug("Checking auth for '{}'...".format(ws))

    url = "https://slack.com/api/auth.test"
    data = {"token": token}
    response = requests.post(url, data = data)
    data = response.json()
    if not 'ok' in data:
      self.logger.error('Invalid response! {}'.format(data))
      return

    if not data['ok']:
      error = ''
      if 'error' in data:
        error = data['error']
      self.logger.error('Unsuccessful: error: {}'.format(error))
      return

    self.logger.info("Auth successful!")
    self.logger.info("URL: {}".format(data['url']))
    self.logger.info("Workspace: {}".format(data['team']))
    self.logger.info("Workspace ID: {}".format(data['team_id']))
    self.logger.info("User: {}".format(data['user']))
    self.logger.info("User ID: {}".format(data['user_id']))
