from slacker.utility import parse_line

from prompt_toolkit.contrib.completers import WordCompleter

class Completer(WordCompleter):
  def __init__(self, words, meta_dict, registrar):
    self.__registrar = registrar
    super(Completer, self).__init__(words, meta_dict = meta_dict, ignore_case = True)

  def get_completions(self, document, complete_event):
    # If first command has been entered then use completer for command, if any, otherwise don't
    # try to complete further.
    text = document.text_before_cursor.lstrip()
    if ' ' in text:
      try:
        (cmd, args) = parse_line(text)
        completer = self.__registrar.get_completer(cmd)
        if not completer:
          return []
        return completer.get_completions(document, complete_event)
      except: pass
      return []

    # Fallback to the normal completer.
    return super(Completer, self).get_completions(document, complete_event)
