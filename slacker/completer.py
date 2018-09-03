from slacker.utility import parse_line

from prompt_toolkit.completion import WordCompleter

class Completer(WordCompleter):
  def __init__(self, words, meta_dict, registrar):
    self.__registrar = registrar
    self.__completers = {}
    super(Completer, self).__init__(words, meta_dict=meta_dict, ignore_case=True)

  def get_completions(self, document, complete_event):
    # If first command has been entered then use completer for command, if any, otherwise don't
    # try to complete further.
    text = document.text_before_cursor.lstrip()
    if ' ' in text:
      (cmd, args) = parse_line(text)

      completer = None
      if cmd in self.__completers:
        completer = self.__completers[cmd]
      else:
        completer = self.__registrar.get_completer(cmd)
      if not completer:
        return []
      self.__completers[cmd] = completer
      return completer.get_completions(document, complete_event)

    # Fallback to the normal completer.
    return super(Completer, self).get_completions(document, complete_event)
