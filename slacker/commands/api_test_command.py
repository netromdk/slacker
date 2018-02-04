import uuid
from .command import Command
from slacker.slack_api import SlackAPI

class ApiTestCommand(Command):
  def name(self):
    return "api.test"

  def description(self):
    return "Checks that the Slack API is online."

  def aliases(self):
    return []

  def action(self, args = None):
    self.logger.debug("Checking Slack...")
    nonce = uuid.uuid4().hex
    data = SlackAPI().post('api.test', {'foo': nonce})
    if not 'ok' in data or not 'args' in data or not 'foo' in data['args']:
      self.logger.warning('Invalid response! {}'.format(data))
      return

    if not data['ok']:
      error = ''
      if 'error' in data:
        error = data['error']
      self.logger.warning('Unsuccessful: error: {}'.format(error))
      return

    foo = data['args']['foo']
    if foo != nonce:
      self.logger.warning("Received incorrect nonce: {} vs. {}".format(foo, nonce))
      return

    self.logger.info("API is online.")
