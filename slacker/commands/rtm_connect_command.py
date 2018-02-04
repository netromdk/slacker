import asyncio
import websockets

from .command import Command

from slacker.slack_api import SlackAPI

class RTMConnectCommand(Command):
  def name(self):
    return 'rtm.connect'

  def description(self):
    return 'Start connection to RTM streaming API'

  def aliases(self):
    return ['rtm']

  def action(self, args = None):
    response = SlackAPI().post('rtm.connect')
    if 'ok' not in response:
      self.logger.warning('Unable to connect to RTM API')

    web_url = response['url']
    async def tail_rtm():
      async with websockets.connect(web_url) as websocket:
          while True:
            message = await websocket.recv()
            print("RTM {}".format(message))

    asyncio.get_event_loop().run_until_complete(tail_rtm())
