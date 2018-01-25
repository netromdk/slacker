#!/usr/bin/env python

import sys
import signal

from slacker.commands.command import Command
from slacker.commands.registrar import Registrar
from slacker.environment.common import COMMAND_PREFIX

def signal_handler(signal, frame):
  print("\nCaught sig.. {}".format(signal))
  sys.exit(0)

def readline():
  try:
    return input(COMMAND_PREFIX).strip().lower()

  # Handle EOF/^D nicely.
  except: return None

def process(line, reg):
  cmd = reg.find(line)
  if not cmd:
    print("Unknown command: {}".format(line))
    return

  cmd.action()

def main():
  # Find all slacker commands.
  reg = Registrar()
  for cmd in Command.find_all():
    reg.register(cmd())

  while True:
    line = readline()
    if line is None: break
    elif not line: continue
    process(line, reg)

if __name__ == '__main__':
  signal.signal(signal.SIGINT, signal_handler)

  main()
