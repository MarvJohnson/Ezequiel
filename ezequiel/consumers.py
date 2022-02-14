import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):
  rooms = {}
  channelToRoom = {}
  roomOwners = {}
  
  async def connect(self):
    self.room_group_name = 'Global-Room'
    await self.channel_layer.group_add(
      self.room_group_name,
      self.channel_name
    )

    await self.accept()

    await self.channel_layer.send(
      self.channel_name,
      {
        'type': 'send.action',
        'action': {
          'type': 'get-all-rooms',
          'payload': {
            'rooms': [{ 'room_name': room['room_name'], 'peers': room['peers'], 'is_public': room['is_public'] } for room in self.rooms.values()]
          }
        }
      }
    )

  async def disconnect(self, close_code):
    await self.channel_layer.group_discard(
      self.room_group_name,
      self.channel_name
    )


    if self.channel_name in self.channelToRoom:
      del self.rooms[self.channelToRoom[self.channel_name]]['peers'][self.channel_name]

      if len(self.rooms[self.channelToRoom[self.channel_name]]['peers']) == 0:
        del self.rooms[self.channelToRoom[self.channel_name]]

      await self.channel_layer.group_send(
        self.room_group_name,
        {
          'type': 'send.action',
          'action': {
            'type': 'get-all-rooms',
            'payload': {
              'rooms': [{ 'room_name': room['room_name'], 'peers': room['peers'], 'is_public': room['is_public'] } for room in self.rooms.values()]
            }
          }
        }
      )

  async def receive(self, text_data):
    action = json.loads(text_data)
    action_type = action['type']
    
    if action_type == 'new-peer':
      room_name = action['payload']['room_name']
      action['sender_channel'] = self.channel_name
      await self.channel_layer.group_send(
        room_name or self.room_group_name,
        {
          'type': 'send.action',
          'action': action
        })

    if action_type == 'call' or action_type == 'answer' or action_type == 'ice-candidate':
      sender_channel = action['sender_channel']
      action['sender_channel'] = self.channel_name

      await self.channel_layer.send(
        sender_channel,
        {
          'type': 'send.action',
          'action': action
        }
      )
      return

    if action_type == 'message':
      await self.channel_layer.group_send(
        self.room_group_name,
        {
          'type': 'send.action',
          'action': action
        }
      )

    if action_type == 'make-new-room':
      room_name = action['payload']['room_name']
      
      if self.channel_name in self.roomOwners or room_name in self.rooms:
        print('Cannot make room')
        return
      
      new_room = {
        'room_name': room_name,
        'peers': {
          f'{self.channel_name}': { 
            'username': action['payload']['sender'], 'admin': True 
          }
        },
        'is_public': bool(action['payload']['is_public']),
        'passcode': action['payload']['passcode']
      }
      self.rooms[room_name] = new_room
      self.roomOwners[self.channel_name] = True
      self.channelToRoom[self.channel_name] = room_name
      
      await self.channel_layer.group_add(
        room_name,
        self.channel_name
      )

      action['payload']['sender_channel'] = self.channel_name
      action['payload']['new_room'] = new_room
      
      print('About to send:', action)
      
      await self.channel_layer.group_send(
        self.room_group_name,
        {
          'type': 'send.action',
          'action': {
            'type': 'make-new-room',
            'payload': {
              'room_name': room_name,
              'is_public': new_room['is_public'],
              'peers': [new_room['peers'][self.channel_name]]
            }
          }
        }
      )

      return

    if action_type == 'join-room':
      room_name = action['payload']['room_name']
      passcode = ''
      if 'passcode' in action['payload']:
        passcode = action['payload']['passcode']

      if passcode != self.rooms[room_name]['passcode']:
        return

      

      print(f'Peer ({action["payload"]["sender"]}) joining {room_name}')

      await self.channel_layer.group_add(
        room_name,
        self.channel_name
      )

      self.rooms[room_name]['peers'][self.channel_name] = { 'username': action['payload']['sender'] }
      self.channelToRoom[self.channel_name] = room_name

      action['payload']['message'] = f'{action["payload"]["sender"]} joined the room!'
      action['payload']['room'] = self.rooms[room_name]
      action['payload']['sender_channel'] = self.channel_name
      
      await self.channel_layer.group_send(
        room_name,
        {
          'type': 'send.action',
          'action': action
        }
      )

      await self.channel_layer.group_send(
      self.room_group_name,
      {
        'type': 'send.action',
        'action': {
          'type': 'get-all-rooms',
          'payload': {
            'rooms': [{ 'room_name': room['room_name'], 'peers': room['peers'], 'is_public': room['is_public'] } for room in self.rooms.values()]
          }
        }
      }
    )
      return

    if action_type == 'leave-room':
      if self.channel_name in self.channelToRoom:
        if self.channel_name in self.roomOwners:
          del self.roomOwners[self.channel_name]

        action['sender_channel'] = self.channel_name        
        await self.channel_layer.group_send(
          self.channelToRoom[self.channel_name],
          {
            'type': 'send.action',
            'action': action
          }
        )
        
        del self.rooms[self.channelToRoom[self.channel_name]]['peers'][self.channel_name]
        if len(self.rooms[self.channelToRoom[self.channel_name]]['peers']) == 0:
          del self.rooms[self.channelToRoom[self.channel_name]]
        
        await self.channel_layer.group_send(
          self.room_group_name,
          {
            'type': 'send.action',
            'action': {
              'type': 'get-all-rooms',
              'payload': {
                'rooms': [{ 'room_name': room['room_name'], 'peers': room['peers'], 'is_public': room['is_public'] } for room in self.rooms.values()]
              }
            }
          }
        )

        await self.channel_layer.group_discard(
          self.channelToRoom[self.channel_name],
          self.channel_name
        )
        
        del self.channelToRoom[self.channel_name]

    if action_type == 'check-passcode':
      room_name = action['payload']['room_name']
      passcode = action['payload']['passcode']

      if room_name in self.rooms and passcode == self.rooms[room_name]['passcode']:
        await self.channel_layer.send(
          self.channel_name,
          {
            'type': 'send.action',
            'action': {
              'type': 'check-passcode',
              'payload': {
                'is_correct': True
              }
            }
          }
        )
        return
      
      await self.channel_layer.send(
          self.channel_name,
          {
            'type': 'send.action',
            'action': {
              'type': 'check-passcode',
              'payload': {
                'is_correct': False
              }
            }
          }
        )

  async def send_action(self, event):
    action = event['action']

    await self.send(text_data=json.dumps(action))