import uuid
from .command import Command
from slacker.slack_api import SlackAPI, SlackAPIException

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
      raise SlackAPIException('Invalid response! {}'.format(data))

    if not data['ok']:
      error = ''
      if 'error' in data:
        error = data['error']
      raise SlackAPIException('Unsuccessful: error: {}'.format(error))

    foo = data['args']['foo']
    if foo != nonce:
      raise SlackAPIException("Received incorrect nonce: {} vs. {}".format(foo, nonce))

    self.logger.info("API is online.")
