import os
import json
import requests

from slacker.commands.command import Command
from slacker.commands.argument_parser import ArgumentParser
from slacker.slack_api import SlackAPI

class EmojiListCommand(Command):
  def name(self):
    return 'emoji.list'

  def description(self):
    return 'Lists custom emojis in workspace'

  def make_parser(self):
    parser = ArgumentParser(prog = self.name(), description = self.description())
    parser.add_argument('-p', '--path', type = str,
                        help='Local file path where to save emojis to')
    parser.add_argument('-q', '--quiet', action='store_true',
                        help="Don't print response from Slack API")
    return parser

  def print_emojis(self, emojis):
    total = 0
    for emoji in emojis:
      print('{:<25} {:<50}'.format(emoji, emojis[emoji]))
      total += 1

    print('{} custom emojis'.format(total))

  def __download_emojis(self, emojis):
    save_data = {}

    for emoji in emojis:
      emoji_url = emojis[emoji]
      if emoji_url.startswith('alias'):
        save_data[emoji] = emoji_url
        continue

      saved_file_path = self.__download_emoji(emoji, emojis[emoji])
      save_data[emoji] = saved_file_path

    self.__write_save_file(save_data)

  def __download_emoji(self, emoji_name, url):
    self.logger.debug('Downloading {}'.format(url))

    res = requests.get(url, stream=True)
    if res.status_code != 200:
      self.logger.warning('Unable to download {}: {}'.format(emoji_name, url))

    image_type = res.headers['Content-Type'].split('/')[1]
    content_length = res.headers['Content-Length']

    emoji_file = '{}.{}'.format(emoji_name, image_type)
    local_save_path = os.path.join(self.local_save_path, emoji_file)

    self.logger.debug('Writing to disk {}({}) -> {}'.format(url, content_length, self.local_save_path))
    with open(local_save_path, 'wb') as f:
      for chunk in res.iter_content(1024):
        f.write(chunk)

    return local_save_path

  def __write_save_file(self, save_data):
    with open(self.save_data_file, 'w') as f:
      json.dump(save_data, f, indent=2)

    self.logger.info('Emoji image files saved to {}'.format(self.local_save_path))
    cwd_save_data = os.path.join(os.getcwd(), self.save_data_file)
    self.logger.info('Emoji save data file saved to {}'.format(cwd_save_data))

  def __check_create_directory(self, directory):
    if not os.path.exists(directory):
      self.logger.debug("Creating directory for emoji download: {}".format(directory))
      os.makedirs(directory, exist_ok = True)

  def action(self, args = None):
    self.save_data_file = 'emojis.json'
    self.logger.info('Contacting Slack API for emojis')

    slack_api = SlackAPI()
    emojis = slack_api.post('emoji.list')['emoji']

    if not args.quiet:
      self.print_emojis(emojis)

    if args.path:
      self.local_save_path = args.path
      self.__check_create_directory(self.local_save_path)
      self.__download_emojis(emojis)
