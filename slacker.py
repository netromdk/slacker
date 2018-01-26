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

def parse_line(line):
  if " " in line:
    return line.split(maxsplit = 1)
  return (line, None)

def process(line, reg):
  (cmd, args) = parse_line(line)

  instance = reg.find(cmd)
  if not instance:
    print("Unknown command: {}".format(cmd))
    return

  if args:
    try:
      args = instance.parse_args(args.split())
    except: return
  instance.action(args)

def main():
  # Find all slacker commands.
  reg = Registrar()
  for cmd in Command.find_all():
    reg.register(cmd())

  if reg.count() == 0:
    print("No commands found!")
    sys.exit(-1)

  if len(sys.argv) > 1:
    process(" ".join(sys.argv[1:]), reg)
    return

  while True:
    line = readline()
    if line is None: break
    elif not line: continue
    process(line, reg)

if __name__ == '__main__':
  signal.signal(signal.SIGINT, signal_handler)

  main()
