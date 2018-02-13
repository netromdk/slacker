from slacker.commands.command import Command
from slacker.commands.argument_parser import ArgumentParser
from slacker.slack_api import SlackAPI

class ChatPostEphemeralCommand(Command):
  def name(self):
    return "chat.postephemeral"

  def description(self):
    return "Post ephemeral message to a channel on Slack that is only visible to assigned user."

  def requires_token(self):
    return True

  def is_destructive(self):
    return True

  def make_parser(self):
    parser = ArgumentParser(prog = self.name(), description = self.description())
    parser.add_argument('-c', '--channel', type = str, help = "Channel ID to post to.")
    parser.add_argument('-u', '--user', type = str, help = "User ID to post ephemeral message to.")
    parser.add_argument('--as-user', action = 'store_true',
                        help = "Post as authed user instead of as bot.")
    parser.add_argument('text', type = str, help = "Text to post.")
    return parser

  def action(self, args = None):
    channel = args.channel
    user = args.user
    text = args.text
    self.logger.debug('Sending ephemeral message to {} in {}: {}'.format(user, channel, text))
    SlackAPI(command = self).post('chat.postEphemeral',
                                  {'channel': channel,
                                   'user': user,
                                   'text': text,
                                   'as_user': args.as_user})
