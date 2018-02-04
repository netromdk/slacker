import requests
import json

from slacker.environment.config import Config

class SlackAPIException(Exception):
  pass

class SlackAPI:
  """Encapsulates sending requests to the Slack API and getting back JSON responses."""

  def __init__(self, token = None):
    self.__endpoint = 'https://slack.com/api/%s'
    if token:
      self.__token = token
    else:
      self.__token = Config.get().active_workspace_token()

    # Methods that doesn't require the token to be sent.
    self.__token_unneeded = ('api.test',)

  def post(self, method, args = {}):
    """Send HTTP POST using method, as the part after https://slack.com/api/, and arguments as a
    dictionary of arguments."""
    if not method in self.__token_unneeded:
      args['token'] = self.__token
    response = requests.post((self.__endpoint % method), data = args)
    return response.json()
