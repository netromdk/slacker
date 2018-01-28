import os
import json

from slacker.logger import Logger

class Config:
  __instance = None

  def __init__(self):
    """Get instance of Config via Config.get()."""
    if not Config.__instance:
      self.__logger = Logger(self.__class__.__name__).get()

      # Set default values.
      self.reset()

      # Load from file if it exists.
      try:
        self.load()
      except:
        self.__logger.debug('Config does not exist: {}'.format(self.__file_path()))

      # Assign singleton instance.
      Config.__instance = self

  @staticmethod
  def get():
    if not Config.__instance:
      Config()
    return Config.__instance

  def repl_prefix(self):
    return self.__repl_prefix

  def set_repl_prefix(self, repl_prefix):
    self.__repl_prefix = repl_prefix

  def active_workspace(self):
    """Active workspace name, if defined."""
    return self.__active_workspace

  def set_active_workspace(self, name):
    if not name in self.__workspaces:
      raise ValueError("Cannot set unknown workspace active: '{}'".format(name))
    self.__active_workspace = name

  def add_workspace(self, name, token):
    if name in self.__workspaces:
      raise ValueError("Cannot add workspace '{}' because it already exists!".format(name))
    self.__workspaces[name] = token

  def remove_workspace(self, name):
    if not name in self.__workspaces:
      raise ValueError("Cannot remove unknown workspace: '{}'".format(name))
    if self.active_workspace() == name:
      raise ValueError("Cannot remove active workspace: '{}'".format(name))
    del(self.__workspaces[name])

  def workspaces(self):
    return self.__workspaces.keys()

  def __file_path(self):
    return os.path.expanduser('~/.slacker')

  def save(self):
    data = {'repl_prefix': self.repl_prefix(),
            'workspaces': self.__workspaces,
            'active_workspace': self.active_workspace()}
    with open(self.__file_path(), 'w') as fp:
      json.dump(data, fp, indent = 2)
      self.__logger.info('Saved config to: {}'.format(self.__file_path()))

  def load(self):
    with open(self.__file_path(), 'r') as fp:
      data = json.load(fp)
      if 'repl_prefix' in data:
        self.set_repl_prefix(data['repl_prefix'])
      if 'workspaces' in data:
        self.__workspaces = data['workspaces']
      if 'active_workspace' in data:
        self.__active_workspace = data['active_workspace']
      self.__logger.info('Loaded config from: {}'.format(self.__file_path()))

  def reset(self):
    """Resets all values to default."""
    self.set_repl_prefix('> ')
    self.__workspaces = {} # Workspace name -> API token
    self.__active_workspace = None
