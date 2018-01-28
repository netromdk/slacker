import logging

class Logger():
  """ Global logger class for handling module level logging to different streams
  and log formatters. Modules that should have logging should call Logger.get()
  """

  def __init__(self, module_name, log_level=logging.INFO):
    self.logger = logging.getLogger(module_name)
    self.logger.setLevel(log_level)
    self.file_handler = self.__file_handler('slacker.log', log_level)

    # Setup custom logging format
    self.__configure_formatter(self.file_handler)

    # Add the handlers
    self.logger.addHandler(self.file_handler)

  def set_log_level(self, log_level=logging.INFO):
    self.logger.setLevel(log_level)

  def __file_handler(self, log_file, log_level=logging.INFO):
    fh = logging.FileHandler(log_file)
    fh.setLevel(log_level)
    return fh

  def __configure_formatter(self, logger):
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
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
      logger.setLevel(level)
      for handler in logger.handlers:
        handler.setLevel(level)
