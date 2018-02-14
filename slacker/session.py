import logging

class Session:
  __instance = None

  def __init__(self):
    """Get instance of Session via Session.get()."""
    if not Session.__instance:
      self.set_quiet_mode(False)
      self.set_log_level(logging.INFO)

      Session.__instance = self

  @staticmethod
  def get():
    if not Session.__instance:
      Session()
    return Session.__instance

  def quiet_mode(self):
    return self.__quiet_mode

  def set_quiet_mode(self, quiet_mode):
    self.__quiet_mode = quiet_mode

  def log_level(self):
    return self.__log_level

  def set_log_level(self, log_level):
    """The log level is maintained by Config but is saved in Session to sever the import cycle
    between Config and Logger."""
    self.__log_level = log_level
