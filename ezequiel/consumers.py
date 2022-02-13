import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):
  testing = []
  
  async def connect(self):
    self.room_group_name = 'Global-Room'
    self.testing.append(self.channel_name)
    await self.channel_layer.group_add(
      self.room_group_name,
      self.channel_name
    )

    await self.accept()
    print('Connected!')

  async def disconnect(self, close_code):
    await self.channel_layer.group_discard(
      self.room_group_name,
      self.channel_name
    )

    print('Disconnected!')

  async def receive(self, text_data):
    receive_dict = json.loads(text_data)
    print('Received message from:', self.testing)
    # print('Received', receive_dict)
    message = receive_dict['message']
    action = receive_dict['action']

    if (action == 'new-offer') or (action == 'new-answer') or (action == 'new-ice-candidate'):
      receiver_channel_name = receive_dict['message']['receiver_channel_name']
      receive_dict['message']['receiver_channel_name'] = self.channel_name

      await self.channel_layer.send(
        receiver_channel_name,
        {
          'type': 'send.sdp',
          'receive_dict': receive_dict
        }
      )
      
      return


    receive_dict['message']['receiver_channel_name'] = self.channel_name

    await self.channel_layer.group_send(
      self.room_group_name,
      {
        'type': 'send.sdp',
        'receive_dict': receive_dict
      }
    )

  async def send_sdp(self, event):
    receive_dict = event['receive_dict']
    receive_dict['connections'] = self.testing

    await self.send(text_data=json.dumps(receive_dict))