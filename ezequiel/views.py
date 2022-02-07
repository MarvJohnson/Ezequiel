from django.shortcuts import render

# Create your views here.

def vue_render(request):
  return render(request, 'ezequiel/base.html')