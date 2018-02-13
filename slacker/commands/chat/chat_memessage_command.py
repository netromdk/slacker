from slacker.commands.command import Command
from slacker.commands.argument_parser import ArgumentParser
from slacker.slack_api import SlackAPI

class ChatMeMessageCommand(Command):
  def name(self):
    return "chat.memessage"

  def description(self):
    return "Post a me message to a channel on Slack."

  def requires_token(self):
    return True

  def is_destructive(self):
    return True

  def make_parser(self):
    parser = ArgumentParser(prog = self.name(), description = self.description())
    parser.add_argument('-c', '--channel', type = str, help = "Channel ID to post to.")
    parser.add_argument('text', type = str, help = "Text to post.")
    return parser

  def action(self, args = None):
    channel = args.channel
    text = args.text
    self.logger.debug('Sending me message to {}: {}'.format(channel, text))
    SlackAPI(command = self).post('chat.meMessage',
                                  {'channel': channel,
                                   'text': text})
