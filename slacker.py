#!/usr/bin/env python

# Make sure v3+ is used.
import sys
vinfo = sys.version_info
if vinfo.major < 3:
  print("You are using Python v{}.{}. v3+ is required!".format(vinfo.major, vinfo.minor))
  sys.exit(-1)

from slacker.main import start_slacker

if __name__ == "__main__":
  start_slacker()
