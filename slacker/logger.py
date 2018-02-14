import logging

from slacker.session import Session

class Logger():
  """ Global logger class for handling module level logging to different streams
  and log formatters. Modules that should have logging should call Logger.get()
  """

  def __init__(self, module_name, log_level = logging.INFO):
    self.logger = logging.getLogger(module_name)

    # Check if the logger is already loaded for that module
    if self.logger.level != 0:
      return

    # Use log level of session if defined. This is to circumvent the need of importing Config
    # (circular!).
    session = Session.get()
    ll = session.log_level()
    log_level = log_level if ll is None else ll

    self.log_level = log_level
    self.logger.setLevel(log_level)

    # Config log handler
    self.file_handler = self.__file_handler('slacker.log')
    self.__configure_formatter(self.file_handler)
    self.logger.addHandler(self.file_handler)

    # Config STDOUT log handler if not in quiet mode.
    if not session.quiet_mode():
      self.stream_handler = self.__stream_handler()
      self.__configure_formatter(self.stream_handler, '%(message)s')
      self.logger.addHandler(self.stream_handler)

  def set_log_level(self, log_level):
    self.log_level = log_level
    self.logger.setLevel(log_level)

  def disable_stream_handler(self):
    self.logger.removeHandler(self.stream_handler)

  def __file_handler(self, log_file):
    fh = logging.FileHandler(log_file)
    fh.setLevel(self.log_level)
    return fh

  def __stream_handler(self):
    sh = logging.StreamHandler()
    sh.setLevel(self.log_level)
    return sh

  def __configure_formatter(self, logger,
                            fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'):
    formatter = logging.Formatter(fmt)
    logger.setFormatter(formatter)

  def get(self):
    return self.logger

  @staticmethod
  def levels():
    return [logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR, logging.CRITICAL]

  @staticmethod
  def level_from_name(name):
    for level in Logger.levels():
      if logging.getLevelName(level).lower() == name.lower():
        return level
    return None

  @staticmethod
  def level_names():
    return [logging.getLevelName(level) for level in Logger.levels()]

  @staticmethod
  def set_level(level):
    for logger in logging.Logger.manager.loggerDict.values():
      if not hasattr(logger, 'handlers'):
        continue

      logger.setLevel(level)
      for handler in logger.handlers:
        handler.setLevel(level)

  @staticmethod
  def disable_stream_handlers():
    for logger in logging.Logger.manager.loggerDict.values():
      if not hasattr(logger, 'handlers'):
        continue

      for handler in logger.handlers:
        if type(handler) == logging.StreamHandler:
          logger.removeHandler(handler)
