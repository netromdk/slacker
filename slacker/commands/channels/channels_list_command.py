from slacker.commands.command import Command
from slacker.commands.argument_parser import ArgumentParser
from slacker.slack_api import SlackAPI

class ChannelsListCommand(Command):
  def name(self):
    return 'channels.list'

  def description(self):
    return 'Displays info about channels on Slack.'

  def requires_token(self):
    return True

  def is_destructive(self):
    return False

  def make_parser(self):
    parser = ArgumentParser(prog = self.name(), description = self.description())
    parser.add_argument('-l', '--limit', type = int, default = 50,
                        help = 'Maximum number of channels to return per page (defaults to 50).')
    parser.add_argument('-n', '--no-follow', action = 'store_true',
                        help = 'Don\'t follow cursors.')
    parser.add_argument('--exclude-archived', action = 'store_true',
                        help = 'Exclude archived channels.')
    return parser

  def action(self, args = None):
    self.logger.info('Listing channels..')
    exclude_members = True # We don't use the members list yet.
    results = 0
    cursor = ''
    slack_api = SlackAPI(command = self)
    while True:
      data = slack_api.post('channels.list',
                            {'limit': args.limit,
                             'exclude_archived': args.exclude_archived,
                             'exclude_members': exclude_members,
                             'cursor': cursor})

      channels = data['channels']
      results += len(channels)

      for channel in channels:
        info = []
        if channel['is_member']:
          info.append('member')
        if channel['is_archived']:
          info.append('archived')
        if channel['is_general']:
          info.append('general')
        if channel['is_private']:
          info.append('private')
        if channel['is_shared']:
          info.append('shared')
        info = ', '.join(info)
        self.logger.info('  #{} ({})'.format(channel['name'], channel['id']))
        self.logger.info('    {} members{}'.format(channel['num_members'],
                                                   ', ' + info if info else ''))

      if args.no_follow: break
      meta = data['response_metadata']
      cursor = meta['next_cursor'].strip()
      if len(cursor) == 0:
        break

    self.logger.info('{} channels'.format(results))
