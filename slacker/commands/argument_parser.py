import argparse

class DidNotExitException(BaseException):
  pass

class ArgumentParser(argparse.ArgumentParser):
  """Argument parser intended for use in commands only. It doesn't exit the program on help etc.,
  and it remembers the names of arguments and descriptions to be used for completion."""

  def __init__(self, *args, **kwargs):
    self.__words = []
    self.__meta = {}
    super(ArgumentParser, self).__init__(*args, **kwargs)

  def exit(self, status=0, message=None):
    raise DidNotExitException()

  def add_argument(self, *args, **kwargs):
    for arg in args:
      self.__words.append(arg)
      if "help" in kwargs:
        self.__meta[arg] = kwargs["help"]
    return super(ArgumentParser, self).add_argument(*args, **kwargs)

  def words(self):
    return self.__words

  def meta(self):
    return self.__meta
