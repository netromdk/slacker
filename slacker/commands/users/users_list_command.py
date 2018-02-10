from slacker.commands.command import Command
from slacker.commands.argument_parser import ArgumentParser
from slacker.slack_api import SlackAPI

class UsersListCommand(Command):
  def name(self):
    return 'users.list'

  def description(self):
    return 'Displays info about users on Slack.'

  def make_parser(self):
    parser = ArgumentParser(prog = self.name(), description = self.description())
    parser.add_argument('-l', '--limit', type = int, default = 50,
                        help = 'Maximum number of users to return per page (defaults to 50).')
    parser.add_argument('-n', '--no-follow', action = 'store_true',
                        help = 'Don\'t follow cursors.')
    parser.add_argument('--include-locale', action = 'store_true',
                        help = 'Include locale of users.')
    return parser

  def action(self, args = None):
    self.logger.info('Listing users..')
    results = 0
    cursor = ''
    slack_api = SlackAPI()
    while True:
      data = slack_api.post('users.list',
                            {'limit': args.limit,
                             'include_locale': args.include_locale,
                             'cursor': cursor})

      users = data['members']
      results += len(users)

      for user in users:
        self.logger.info('  {} ({})'.format(user['name'], user['id']))

        info = []
        if 'real_name' in user and user['real_name']:
          info.append(user['real_name'])
        if 'tz' in user and user['tz']:
          info.append(user['tz'])
        if 'is_admin' in user and user['is_admin']:
          info.append('admin')
        if 'is_owner' in user and user['is_owner']:
          info.append('owner')
        if 'is_primary_owner' in user and user['is_primary_owner']:
          info.append('primary owner')
        if 'is_bot' in user and user['is_bot']:
          info.append('bot')
        if 'is_restricted' in user and user['is_restricted']:
          info.append('restricted')
        if 'has_2fa' in user and user['has_2fa']:
          info.append('2fa')
        if 'locale' in user:
          info.append(user['locale'])
        info = ', '.join(info)
        if info:
          self.logger.info('    {}'.format(info))

      if args.no_follow: break
      meta = data['response_metadata']
      cursor = meta['next_cursor'].strip()
      if len(cursor) == 0:
        break

    self.logger.info('{} users'.format(results))
