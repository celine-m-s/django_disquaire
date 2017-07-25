# from django.views import generic
from django.shortcuts import render

from .models import Album

def index(request):
    albums = Album.objects.order_by('-created_at')[:12]
    context = {
        'albums': albums,
    }
    return render(request, 'store/index.html', context)
