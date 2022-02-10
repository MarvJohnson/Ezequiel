from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import User, DirectMessage
from .serializers import UserSerializer, DirectMessageSerializer
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

# Create your views here.

def vue_render(request):
  return render(request, 'ezequiel/base.html')

class DirectMessageDetail(APIView):
  authentication_classes = [TokenAuthentication]
  permission_classes = [IsAuthenticated]
  
  def delete(self, request, pk, format=None):
    user = request.user

    if user != None:
      dm = DirectMessage.objects.get(id=pk)
      user.direct_messages.remove(dm)
      return Response(None, status=200)
    
    return Response(None, status=401)


