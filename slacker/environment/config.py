import os
import json

class Config:
  __instance = None

  def __init__(self):
    """Get instance of Config via Config.get()."""
    if not Config.__instance:
      # Set default values.
      self.set_repl_prefix('> ')

      # Load from file if it exists.
      self.load()

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

  def __file_path(self):
    return os.path.expanduser('~/.slacker')

  def save(self):
    data = {'repl_prefix': self.repl_prefix()}
    with open(self.__file_path(), 'w') as fp:
      json.dump(data, fp, indent = 2)

  def load(self):
    with open(self.__file_path(), 'r') as fp:
      data = json.load(fp)
      if 'repl_prefix' in data:
        self.set_repl_prefix(data['repl_prefix'])

