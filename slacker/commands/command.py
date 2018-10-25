import re
from cachetools import TTLCache

from abc import ABC, abstractmethod

from slacker.logger import Logger
from slacker.slack_api import SlackAPI

from prompt_toolkit.completion import WordCompleter

# The "." can only be in the middle of the command name.
COMMAND_NAME_REGEX = re.compile("([\w\d][\w\d\.]*)?[\w\d]+")

class Command(ABC):
  """Command encapsulates a Slacker command with a name, description, help text, and the action to
  perform.
  """

  def __init__(self):
    self.__validate()
    self.logger = Logger(self.__class__.__name__).get()
    self.cache = None

    if not self.is_destructive() and self.use_cache():
      ttl = self.cache_ttl()
      max_items = self.max_items_in_cache()
      self.logger.debug("Created {} command cache (maxitems={}, ttl={})"
                        .format(self.name(), max_items, ttl))
      self.cache = TTLCache(max_items, ttl)

  @abstractmethod
  def name(self):
    """Returns the name of the command. This is the actual command, like 'download'."""
    pass

  @abstractmethod
  def description(self):
    """Returns the description of the command."""
    pass

  def requires_token(self):
    """Whether or not the method requires the active workspace's token to function. It defaults to
    False to not send the token if not needed."""
    return False

  def is_destructive(self):
    """Whether or not the method is destructive, modifies state, or sends messages. It defaults to
    True to require attention if the command is viable in read-only mode."""
    return True

  def use_cache(self):
    """Whether the command API call should be cached and looked up later instead
    of sending and HTTP request to the Slack API. The cache should only be used
    on non destructive commands"""
    return False

  def cache_ttl(self):
    """Controls the TTL on cache keys for the command"""
    return 60

  def max_items_in_cache(self):
    """ In addition to TTL the cache implements LRU (least recently used). This
    controls the number of items allowed in the cache"""
    return 5

  def __validate(self):
    """Validates that the command is valid and conforming with the requirements."""
    derive_cls = type(self).__mro__[0]

    if not COMMAND_NAME_REGEX.fullmatch(self.name()):
      raise ValueError("Command name is invalid '{}' in {}".format(self.name(), derive_cls))

  def make_parser(self):
    """Override to define slacker.commands.argument_parser.ArgumentParser."""
    return None

  def make_completer(self):
    """Creates a word completer from arguments parser if defined."""
    parser = self.make_parser()
    if not parser:
      return None
    return WordCompleter(parser.words(), meta_dict=parser.meta(), ignore_case=True)

  def parse_args(self, args):
    """Parse arguments from a list of strings. The output can be given to action()."""
    parser = self.make_parser()
    if not parser:
      return None
    return parser.parse_args(args)

  @abstractmethod
  def action(self, args=None):
    """Executes the action of the command with optional arguments parsed via parse_args()."""
    pass

  @staticmethod
  def find_all():
    """Finds all command classes deriving from Command."""
    cmds = set()
    for child in Command.__subclasses__():
      if child not in cmds:
        cmds.add(child)
    return cmds

  def slack_api_post(self, method, args={}):
    return SlackAPI(command=self).post(method, args)

  def slack_api_download_file(self, file_id, folder):
    return SlackAPI(command=self).download_file(file_id, folder)
