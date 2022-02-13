import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):
  rooms = {}
  
  async def connect(self):
    self.room_group_name = 'Global-Room'
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

    if action == 'make-new-room':
      room_name = receive_dict['message']['room_name']
      
      if room_name in self.rooms:
        print('Cannot make room: duplicate room name')
        return
      
      self.rooms[room_name] = [receive_dict['peer']]
      print('rooms dictionary is now:', self.rooms)
      await self.channel_layer.group_add(
        room_name,
        self.channel_name
      )

      await self.channel_layer.group_send(
        room_name,
        {  
          'type': 'send.welcome',
          'message': f'{receive_dict["peer"]} joined the room!'
        }
      )

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

    await self.send(text_data=json.dumps(receive_dict))

  async def send_welcome(self, event):
    message = event['message']

    await self.send(text_data=json.dumps(message))