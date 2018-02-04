import argparse

class DidNotExitException(BaseException):
  pass

class ArgumentParser(argparse.ArgumentParser):
  """Argument parser intended for use in commands only. It doesn't exit the program on help etc."""

  def exit(self, status = 0, message = None):
    raise DidNotExitException()
