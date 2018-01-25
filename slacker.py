#!/usr/bin/env python

import sys
import signal

from slacker.commands.command import Command
from slacker.environment.common import COMMAND_PREFIX

def signal_handler(signal, frame):
  print("\nCaught sig.. {}".format(signal))
  sys.exit(0)

def main():
  # Find all slacker commands.
  for cmd in Command.find_all():
    # TODO: Register commands with registrar here instead when implemented!
    c = cmd()
    print(">> Found command {}".format(c.name()))

  while True:
    input(COMMAND_PREFIX)

if __name__ == '__main__':
  signal.signal(signal.SIGINT, signal_handler)

  main()
