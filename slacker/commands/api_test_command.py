import json
import requests
import uuid
from .command import Command

class ApiTestCommand(Command):
  def name(self):
    return "api.test"

  def description(self):
    return "Checks that the Slack API is online."

  def aliases(self):
    return []

  def action(self, args = None):
    self.logger.debug("Checking Slack...")
    url = "https://slack.com/api/api.test"
    nonce = uuid.uuid4().hex
    data = {"foo": nonce}
    response = requests.post(url, data = data)
    data = response.json()
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
