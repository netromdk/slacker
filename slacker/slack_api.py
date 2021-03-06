import requests
import hashlib
import json
import os

from slacker.environment.config import Config
from slacker.logger import Logger

class SlackAPIException(Exception):
  def __init__(self, message, error=None):
    """Slack API exception with a general message and optional error code."""
    super(SlackAPIException, self).__init__(message)
    self.__error = error

  def error(self):
    """Returns error code if defined, otherwise the general message."""
    if self.__error:
      return self.__error
    return str(self)

class SlackAPI:
  """Encapsulates sending requests to the Slack API and getting back JSON responses."""

  def __init__(self, token=None, command=None, requires_token=False, is_destructive=True):
    config = Config.get()
    self.__logger = Logger(__name__).get()
    self.__url = "https://slack.com/api/{}"
    self.__cache = None if not command else command.cache
    self.__requires_token = requires_token if not command else command.requires_token()
    self.__is_destructive = is_destructive if not command else command.is_destructive()

    if token:
      self.__token = token
    else:
      self.__token = config.active_workspace_token()

  def __check_read_only_abort(self, method):
    """Returns exception to avoid sending requests to Slack API.

    If the command is marked as destructive or the REPL is in read-only mode
    requests to Slack API will not be sent.

    Arguments:
      method {str} -- Slack API method name

    Raises:
      SlackAPIException
    """
    if self.__is_destructive and Config.get().read_only():
      raise SlackAPIException(
        "Not executing '{}' due to read-only mode!".format(method))

  def post(self, method, args={}):
    """Send HTTP POST request to Slack API.

    Arguments:
      method {str} -- Slack API method name

    Keyword Arguments:
      args {dict} -- Arguments required by Slack API method (default: {{}})

    Returns:
      dict -- Slack API response
    """
    self.__check_read_only_abort(method)

    url = self.__url.format(method)
    if self.__requires_token:
      args["token"] = self.__token

    # Check for cached request
    cache_key = self.__generate_cache_key(url, args)
    cache_value = self.__get_cached_value(cache_key)
    if cache_value is not None:
      return cache_value

    response = requests.post(url, data=args)
    self.__validate_response(response)

    json_response = response.json()
    if cache_key is not None:
      self.__update_cache(cache_key, json_response)

    return json_response

  def get(self, method, args={}):
    """Send HTTP GET request to Slack API.

    Arguments:
      method {string} -- Slack API method name

    Keyword Arguments:
      args {dict} -- Arguments required by Slack API method (default: {{}})

    Returns:
      dict -- Slack API response
    """
    self.__check_read_only_abort(method)

    url = self.__url.format(method)
    if self.__requires_token:
      args["token"] = self.__token

    response = requests.get(url, params=args)
    self.__validate_response(response)

    return response.json()

  def download_file(self, file_id, folder):
    """Download file via ID to a folder. File IDs can be retrieved using the `files.list'
    command. Private files use Bearer authorization via the token."""
    if not os.path.exists(folder):
      os.makedirs(folder, exist_ok=True)

    headers = {}
    file_info = self.post("files.info", {"file": file_id})["file"]
    if file_info["is_public"]:
      url = file_info["url_download"]
    else:
      url = file_info["url_private_download"]
      headers["Authorization"] = "Bearer {}".format(self.__token)

    self.__logger.debug("Downloading {} to {}".format(url, folder))

    res = requests.get(url, stream=True, headers=headers)
    if res.status_code != 200:
      raise SlackAPIException("Unsuccessful API request: {} (code {})\nReason: {}"
                              .format(res.url, res.status_code, res.reason))

    file_name = os.path.join(folder, file_info["name"])
    self.__logger.debug("Writing to disk {} -> {}".format(url, file_name))
    with open(file_name, "wb") as f:
      for chunk in res.iter_content(1024):
        f.write(chunk)

    return file_name

  def __validate_response(self, response):
    """Check Slack API response for errors

    Arguments:
      response {requests.Response} -- [description]

    Raises:
      SlackAPIException
    """
    if response.status_code != 200:
      raise SlackAPIException("Unsuccessful API request: {} (code {})\nReason: {}\nResponse: {}"
                              .format(response.url, response.status_code, response.reason,
                                      response.text))

    data = response.json()
    if "ok" not in data:
      raise SlackAPIException("Unsuccessful API request: {}\nInvalid response: {}"
                              .format(response.url, data))

    if not data["ok"]:
      error = ""
      if "error" in data:
        error = data["error"]
      raise SlackAPIException("Unsuccessful API request: {}\nError: {}"
                              .format(response.url, error), error)

  def __get_cached_value(self, key):
    """Get value from cache given the hash key"""
    if self.__cache is None or key is None:
      return None

    val = self.__cache.get(key)
    if val is None:
      self.__logger.debug("Cache miss {}".format(key))
    else:
      self.__logger.debug("Cache hit {}".format(key))

    return val

  def __update_cache(self, key, resp):
    """Update cache value given a key"""
    self.__logger.debug("Updating cache: {}".format(key))
    self.__cache[key] = resp

  def __generate_cache_key(self, url, params):
    """Returns hash of the url and params"""
    if self.__cache is None:
      return None

    m = hashlib.sha256()
    m.update(url.encode("utf-8"))
    m.update(json.dumps(params).encode("utf-8"))
    return m.hexdigest()
