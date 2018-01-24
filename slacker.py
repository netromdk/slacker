#!/usr/bin/env python

import sys
import signal

from slacker.environment.common import COMMAND_PREFIX

def signal_handler(signal, frame):
  print("\nCaught sig.. {}".format(signal))
  sys.exit(0)

def main():
  while True:
    input(COMMAND_PREFIX)

if __name__ == '__main__':
  signal.signal(signal.SIGINT, signal_handler)

  main()
