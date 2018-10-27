import os
import json
import logging

from slacker.logger import Logger
from slacker.session import Session

DEFAULT_REPL_PROMPT = "${ro}${w}> "
DEFAULT_READ_ONLY_STR = "(read-only) "

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
      except Exception as ex:
        self.__logger.debug("Config does not exist: {}\n{}".format(self.file_path(), ex))

      # Assign singleton instance.
      Config.__instance = self

  @staticmethod
  def get():
    if not Config.__instance:
      Config()
    return Config.__instance

  def repl_prompt(self):
    return self.__repl_prompt

  def set_repl_prompt(self, repl_prompt):
    self.__repl_prompt = repl_prompt

  def active_workspace(self):
    """Active workspace name, if defined."""
    return self.__active_workspace

  def set_active_workspace(self, name):
    if name not in self.__workspaces:
      raise ValueError("Cannot set unknown workspace active: '{}'".format(name))
    self.__active_workspace = name

  def add_workspace(self, name, token):
    if name in self.__workspaces:
      raise ValueError("Cannot add workspace '{}' because it already exists!".format(name))
    self.__workspaces[name] = token

  def remove_workspace(self, name):
    if name not in self.__workspaces:
      raise ValueError("Cannot remove unknown workspace: '{}'".format(name))
    if self.active_workspace() == name:
      raise ValueError("Cannot remove active workspace: '{}'".format(name))
    del(self.__workspaces[name])

  def workspaces(self):
    return list(self.__workspaces.keys())

  def workspace_token(self, name):
    if name not in self.__workspaces:
      raise ValueError("Cannot get token for unknown workspace: '{}'".format(name))
    return self.__workspaces[name]

  def active_workspace_token(self):
    if not self.active_workspace():
      raise ValueError("No workspace is active!")
    return self.workspace_token(self.active_workspace())

  def set_log_level(self, level):
    if level not in Logger.levels():
      raise ValueError("Invalid log level: {}".format(level))
    self.__log_level = level
    Session.get().set_log_level(level)
    Logger.set_level(level)

  def log_level(self):
    return self.__log_level

  def read_only(self):
    return self.__read_only

  def set_read_only(self, enable):
    self.__read_only = enable

  def read_only_str(self):
    return self.__read_only_str

  def set_read_only_str(self, str):
    self.__read_only_str = str

  def file_path(self):
    return os.path.expanduser("~/.slacker")

  def safe_dict(self):
    """Returns a safe dictionary of current values excluding any tokens."""
    return {"repl_prompt": self.repl_prompt(),
            "workspaces": self.workspaces(),
            "active_workspace": self.active_workspace(),
            "log_level": self.log_level(),
            "read_only": self.read_only(),
            "read_only_str": self.read_only_str()}

  def save(self):
    data = {"repl_prompt": self.repl_prompt(),
            "workspaces": self.__workspaces,
            "active_workspace": self.active_workspace(),
            "log_level": self.log_level(),
            "read_only": self.read_only(),
            "read_only_str": self.read_only_str()}
    with open(self.file_path(), "w") as fp:
      json.dump(data, fp, indent=2)
      self.__logger.debug("Saved config to: {}".format(self.file_path()))

  def load(self):
    with open(self.file_path(), "r") as fp:
      data = json.load(fp)
      if "repl_prompt" in data:
        self.set_repl_prompt(data["repl_prompt"])
      if "workspaces" in data:
        self.__workspaces = data["workspaces"]
      if "active_workspace" in data:
        self.__active_workspace = data["active_workspace"]
      if "log_level" in data:
        self.set_log_level(data["log_level"])
      if "read_only" in data:
        self.set_read_only(data["read_only"])
      if "read_only_str" in data:
        self.set_read_only_str(data["read_only_str"])
      self.__logger.debug("Loaded config from: {}".format(self.file_path()))

  def reset(self):
    """Resets all values to default."""
    self.set_repl_prompt(DEFAULT_REPL_PROMPT)
    self.__workspaces = {}  # Workspace name -> API token
    self.__active_workspace = None
    self.__log_level = logging.INFO
    self.__read_only = False
    self.__read_only_str = DEFAULT_READ_ONLY_STR
