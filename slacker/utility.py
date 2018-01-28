import calendar
from datetime import datetime, timedelta

def bool_response(msg, default = False):
  """Shows msg and retrieves input as yes/y or no/n, where the meaning of an empty/ENTER reply is
  defined by the default argument: if False it's "yN" and otherwise "Yn".
  """
  choices = "Yn" if default else "yN"
  while True:
    try:
      resp = input("{} [{}] ".format(msg.strip(), choices)).strip().lower()
      break

    # Ask again on ^D.
    except EOFError:
      print("")
      continue

  return resp == "y" or resp == "yes" or (default and len(resp) == 0)

def ts_add_days(days):
  """Add an amount (+/-) of days to current timestamp in UTC."""
  return calendar.timegm((datetime.now() + timedelta(days)).utctimetuple())
