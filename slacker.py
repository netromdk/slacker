#!/usr/bin/env python

# Make sure v3+ is used.
import sys
vinfo = sys.version_info
if vinfo < (3, 0):
  print("Python v3+ is required! You are using v{}.{}.".format(vinfo.major, vinfo.minor))
  sys.exit(-1)

from slacker.main import start_slacker  # noqa: E402

if __name__ == "__main__":
  start_slacker()
