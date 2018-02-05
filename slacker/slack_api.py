import requests
import json

from slacker.environment.config import Config

class SlackAPIException(Exception):
  pass

class SlackAPI:
  """Encapsulates sending requests to the Slack API and getting back JSON responses."""

  def __init__(self, token = None):
    if token:
      self.__token = token
    else:
      self.__token = Config.get().active_workspace_token()

    # Methods that doesn't require the token to be sent.
    self.__token_unneeded = ['api.test']

  def post(self, method, args = {}):
    """Send HTTP POST using method, as the part after https://slack.com/api/, and arguments as a
    dictionary of arguments."""
    url = 'https://slack.com/api/{}'.format(method)
    if not method in self.__token_unneeded:
      args['token'] = self.__token

    response = requests.post(url, data = args)
    if response.status_code != 200:
      raise SlackAPIException('Unsuccessful API request: {} (code {})\nReason: {}\nResponse: {}'
                              .format(response.url, response.status_code, response.reason,
                                      response.text))

    data = response.json()
    if not 'ok' in data:
      raise SlackAPIException('Unsuccessful API request: {}\nInvalid response: {}'
                              .format(response.url, data))

    if not data['ok']:
      error = ''
      if 'error' in data:
        error = data['error']
      raise SlackAPIException('Unsuccessful API request: {}\nError: {}'.format(response.url, error))

    return data
