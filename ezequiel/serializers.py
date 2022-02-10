from rest_framework import serializers
from .models import User, DirectMessage, Message

class MessageSerializer(serializers.ModelSerializer):
  sender = serializers.PrimaryKeyRelatedField(read_only=True)
  text = serializers.CharField()
  replies = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

  class Meta:
    model = Message
    fields = ('sender', 'text', 'replies',)

class DirectMessageSerializer(serializers.ModelSerializer):
  messages = MessageSerializer(many=True, read_only=True)

  class Meta:
    model = DirectMessage
    fields = ('users', 'messages',)

class UserSerializer(serializers.ModelSerializer):
  username = serializers.CharField(max_length=200)
  id = serializers.IntegerField(label='ID', read_only=True)
  direct_messages = DirectMessageSerializer(many=True, read_only=True)
  
  class Meta:
    model = User
    fields = ('id', 'username', 'direct_messages',)