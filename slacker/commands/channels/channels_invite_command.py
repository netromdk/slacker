from slacker.commands.command import Command
from slacker.commands.argument_parser import ArgumentParser
from slacker.slack_api import SlackAPIException
from slacker.utility import ask_abort

class ChannelsInviteCommand(Command):
  def name(self):
    return "channels.invite"

  def description(self):
    return "Invite people to channels on Slack."

  def requires_token(self):
    return True

  def is_destructive(self):
    return True

  def make_parser(self):
    parser = ArgumentParser(prog=self.name(), description=self.description())
    parser.add_argument("-a", "--all", action="store_true", help="Invite all users to channel.")
    parser.add_argument("-u", "--user", type=str, help="User ID to send invite to.")
    parser.add_argument("channel", type=str, help="Channel ID to invite user to.")
    return parser

  def __invite(self, user, channel):
    self.logger.info("Inviting {} to channel {}".format(user, channel))
    self.slack_api_post("channels.invite",
                        {"user": user,
                         "channel": channel})

  def action(self, args=None):
    if not args.all and not args.user:
      self.logger.error("You must specify either --user or --all!")
      return

    if args.user:
      self.__invite(args.user, args.channel)

    elif args.all:
      ask_abort("Are you sure you want to send an invite to all users?", abort_on_yes=False)

      cursor = ""
      while True:
        data = self.slack_api_post("users.list",
                                   {"limit": 50,
                                    "cursor": cursor})
        for user in data["members"]:
          try:
            self.__invite(user["id"], args.channel)
          except SlackAPIException as ex:
            self.logger.error("Error: {}".format(ex.error()))
            continue

        meta = data["response_metadata"]
        cursor = meta["next_cursor"].strip()
        if len(cursor) == 0:
          break
