import uuid
from slacker.commands.command import Command
from slacker.slack_api import SlackAPI, SlackAPIException

class ApiTestCommand(Command):
  def name(self):
    return "api.test"

  def description(self):
    return "Checks that the Slack API is online."

  def is_destructive(self):
    return False

  def action(self, args = None):
    self.logger.debug("Checking Slack...")
    nonce = uuid.uuid4().hex
    data = SlackAPI(command = self).post('api.test', {'foo': nonce})

    foo = data['args']['foo']
    if foo != nonce:
      raise SlackAPIException("Received incorrect nonce: {} vs. {}".format(foo, nonce))

    self.logger.info("API is online.")
