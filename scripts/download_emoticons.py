#!/usr/bin/env python
#
# Download all emojis from a Slack workspace

import requests
import json
import sys
import os

class SlackAPIError(Exception):
  pass

class DownloadEmoticons():

  def __init__(self, local_save_path=None):
    self.save_path = local_save_path
    self.slack_api_endpoint = 'https://slack.com/api/emoji.list'
    self.bot_token = os.getenv('SLACKER_BOT_TOKEN', None)
    self.save_data_file = 'emojis.json'

    if self.save_path is not None and not os.path.exists(self.save_path):
      raise ValueError('Save path does not exist {}'.format(self.save_path))

    # Convert local_save_path to empty string so it's easier to work with
    if self.save_path is None:
      self.save_path = ""

    if self.bot_token is None:
      raise ValueError('Slacker bot token for Slack API not found in SLACKER_BOT_TOKEN')

  def _gen_request_body(self):
    return {
      'token' : self.bot_token
    }

  def _gen_request_headers(self):
    return {
      'content-type' : 'application/x-www-form-urlencoded'
    }

  def _send_request_for_emojis(self):
    headers = self._gen_request_headers()
    req_body = self._gen_request_body()

    res = requests.get(self.slack_api_endpoint, headers=headers, params=req_body)
    if res.status_code != 200:
      raise SlackAPIError('Error communicating with Slack API')

    return res.json()

  def _save_emoji_locally(self, res):
    save_data = {}

    for emoji in res:
      emoji_name = emoji
      emoji_source = res[emoji]

      # If the emoji is an alias just save the alias name and move on
      if emoji_source[:5] == 'alias':
        save_data[emoji_name] = emoji_source
        continue

      saved_path = self._download_emoji(emoji_name, emoji_source)
      save_data[emoji_name] = saved_path

    self._write_save_file(save_data)

  def _write_save_file(self, save_data):
    json_data = json.dumps(save_data, indent=2)

    with open(self.save_data_file, 'w') as f:
      f.write(json_data)

  def _download_emoji(self, emoji_name, url):
    res = requests.get(url, stream=True)
    if res.status_code != 200:
      raise SlackAPIError('Unable to download: {}'.format(url))

    image_type = res.headers['Content-Type'].split('/')[1]
    content_length = res.headers['Content-Length']

    emoji_file = '{}.{}'.format(emoji_name, image_type)
    local_save_path = os.path.join(self.save_path, emoji_file)

    print('{}({}) -> {}'.format(url, content_length, local_save_path))
    with open(local_save_path, 'wb') as f:
      for chunk in res.iter_content(1024):
        f.write(chunk)

    return local_save_path

  def execute(self):
    res = self._send_request_for_emojis()
    if 'emoji' not in res:
      raise ValueError('Emoji not in JSON response from Slack')

    self._save_emoji_locally(res['emoji'])


if __name__ == '__main__':
    emoji_downloader = DownloadEmoticons('/tmp')
    emoji_downloader.execute()
