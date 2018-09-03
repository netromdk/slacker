import os
import json
import requests

from slacker.task import Task, execute_tasks
from slacker.commands.command import Command
from slacker.commands.argument_parser import ArgumentParser

class EmojiDownloadTask(Task):
  def __init__(self, emoji_name, url, save_path):
    self.emoji_name = emoji_name
    self.__url = url
    self.save_path = save_path
    self.logs = []

  def run(self):
    self.logs.append("Downloading {}".format(self.__url))

    res = requests.get(self.__url, stream=True)
    if res.status_code != 200:
      self.logs.append("Unable to download {}: {}".format(self.emoji_name, self.__url))
      return False

    image_type = res.headers["Content-Type"].split("/")[1]
    content_length = res.headers["Content-Length"]

    emoji_file = "{}.{}".format(self.emoji_name, image_type)
    self.save_path = os.path.join(self.save_path, emoji_file)

    self.logs.append("Writing to disk {}({}) -> {}".format(self.__url, content_length,
                                                           self.save_path))
    with open(self.save_path, "wb") as f:
      for chunk in res.iter_content(1024):
        f.write(chunk)

    return self

class EmojiListCommand(Command):
  def name(self):
    return "emoji.list"

  def description(self):
    return "Lists custom emojis in workspace"

  def requires_token(self):
    return True

  def is_destructive(self):
    return False

  def make_parser(self):
    parser = ArgumentParser(prog=self.name(), description=self.description())
    parser.add_argument("-p", "--path", type=str,
                        help="Local file path where to save emojis to")
    parser.add_argument("-q", "--quiet", action="store_true",
                        help="Don't print response from Slack API")
    return parser

  def print_emojis(self, emojis):
    total = 0
    for emoji in emojis:
      self.logger.info("{:<25} {:<50}".format(emoji, emojis[emoji]))
      total += 1

    self.logger.info("{} custom emojis".format(total))

  def __download_emojis(self, emojis):
    save_data = {}
    download_tasks = []

    for emoji in emojis:
      emoji_url = emojis[emoji]
      if emoji_url.startswith("alias"):
        save_data[emoji] = emoji_url
        continue

      # queue the downloads
      task = EmojiDownloadTask(emoji, emoji_url, self.local_save_path)
      download_tasks.append(task)

    # Start the downloads
    results = execute_tasks(download_tasks)
    for r in results:
      if r:
        for log in r.logs:
          self.logger.info(log)

        save_data[r.emoji_name] = r.save_path

    self.__write_save_file(save_data)

  def __write_save_file(self, save_data):
    with open(self.save_data_file, "w") as f:
      json.dump(save_data, f, indent=2)

    self.logger.info("Emoji image files saved to {}".format(self.local_save_path))
    cwd_save_data = os.path.join(os.getcwd(), self.save_data_file)
    self.logger.info("Emoji save data file saved to {}".format(cwd_save_data))

  def __check_create_directory(self, directory):
    if not os.path.exists(directory):
      self.logger.debug("Creating directory for emoji download: {}".format(directory))
      os.makedirs(directory, exist_ok=True)

  def action(self, args=None):
    self.save_data_file = "emojis.json"
    self.logger.info("Contacting Slack API for emojis")

    emojis = self.slack_api_post("emoji.list")["emoji"]

    if not args.quiet:
      self.print_emojis(emojis)

    if args.path:
      self.local_save_path = args.path
      self.__check_create_directory(self.local_save_path)
      self.__download_emojis(emojis)
