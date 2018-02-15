from slacker.commands.command import Command
from slacker.commands.argument_parser import ArgumentParser

class ChatPostMessageCommand(Command):
  def name(self):
    return "chat.postmessage"

  def description(self):
    return "Post message to a channel on Slack."

  def requires_token(self):
    return True

  def is_destructive(self):
    return True

  def make_parser(self):
    parser = ArgumentParser(prog = self.name(), description = self.description())
    parser.add_argument("-c", "--channel", type = str, help = "Channel ID to post to.")
    parser.add_argument("--as-user", action = "store_true",
                        help = "Post as authed user instead of as bot.")
    parser.add_argument("-u", "--user", type = str,
                        help = "Bot user name to use. Must be specified when not using --as-user.")
    parser.add_argument("--no-markdown", action = "store_true",
                        help = "Disable Slack markup parsing.")
    parser.add_argument("text", type = str, help = "Text to post.")
    return parser

  def action(self, args = None):
    if not args.as_user and not args.user:
      self.logger.error("You must specify --user when using --as-user!")
      return
    channel = args.channel
    text = args.text
    markdown = not args.no_markdown
    self.logger.debug("Sending message to {}: {}".format(channel, text))
    self.slack_api_post("chat.postMessage",
                        {"channel": channel,
                         "text": text,
                         "as_user": args.as_user,
                         "username": args.user,
                         "mrkdwn": markdown})
