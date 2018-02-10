import requests
import json
import os

from slacker.environment.config import Config
from slacker.logger import Logger

class SlackAPIException(Exception):
  pass

class SlackAPI:
  """Encapsulates sending requests to the Slack API and getting back JSON responses."""

  def __init__(self, token = None):
    config = Config.get()
    self.__logger = Logger(__name__, config.log_level()).get()

    if token:
      self.__token = token
    else:
      self.__token = config.active_workspace_token()

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

  def download_file(self, file_id, folder):
    """Download file via ID to a folder. File IDs can be retrieved using the `files.list'
    command. Private files use Bearer authorization via the token."""
    if not os.path.exists(folder):
      os.makedirs(folder, exists_ok = True)

    headers = {}
    file_info = self.post('files.info', {'file': file_id})['file']
    if file_info['is_public']:
      url = file_info['url_download']
    else:
      url = file_info['url_private_download']
      headers['Authorization'] = 'Bearer {}'.format(self.__token)

    self.__logger.debug('Downloading {} to {}'.format(url, folder))

    res = requests.get(url, stream = True, headers = headers)
    if res.status_code != 200:
      raise SlackAPIException('Unsuccessful API request: {} (code {})\nReason: {}'
                              .format(res.url, res.status_code, res.reason))

    file_name = os.path.join(folder, file_info['name'])
    self.__logger.debug('Writing to disk {} -> {}'.format(url, file_name))
    with open(file_name, 'wb') as f:
      for chunk in res.iter_content(1024):
        f.write(chunk)

    return file_name
