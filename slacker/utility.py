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
