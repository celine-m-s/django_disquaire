from django.shortcuts import get_object_or_404, render

from .models import Album



def index(request):
    albums = Album.objects.filter(available=True).order_by('-created_at')[:12]
    context = {
        'albums': albums,
    }
    return render(request, 'store/index.html', context)


def detail(request, album_id):
    album = get_object_or_404(Album, pk=album_id)
    artists = [artist.name for artist in album.artists.all()]
    artists_name = " ".join(artists)
    context = {
        'album_title': album.title,
        'artists_name': artists_name
    }
    return render(request, 'store/detail.html', context)
