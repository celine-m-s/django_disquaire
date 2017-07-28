from django.shortcuts import get_object_or_404, render, HttpResponseRedirect, reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils import timezone
from django.db import transaction, IntegrityError

from .models import Album, Artist, Contact, Booking
from .forms import BookingForm


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
    form = BookingForm()
    context = {
        'album_title': album.title,
        'artists_name': artists_name,
        'album_id': album.id,
        'form': form
    }
    return render(request, 'store/detail.html', context)

def listing(request):
    albums_list = Album.objects.filter(available=True)
    paginator = Paginator(albums_list, 12)

    page = request.GET.get('page')
    try:
        albums = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        albums = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        albums = paginator.page(paginator.num_pages)

    return render(request, 'store/listing.html', {'albums': albums})


def search(request):
    query = request.GET.get('query')
    if not query:
        albums = Album.objects.all()
    else:
        # title contains the query is and query is not sensitive to case.
        albums = Album.objects.filter(title__icontains=query)
    if not albums.exists():
        # Don't do this but keep it as an example.
        # artists = Artist.objects.filter(name__icontains=query)
        # ids = [artist.id for artist in artists ]
        # albums = Album.objects.filter(id__in=ids)
        albums = Album.objects.filter(artists__name__icontains=query)
    title = "Résultats pour la requête %s"%query
    context = {
        'albums': albums,
        'query': title
    }
    return render(request, 'store/search.html', context)


def contact(request):
    form = BookingForm(request.POST)
    album_id = request.POST.get('album_id')
    if form.is_valid():
        email = form.cleaned_data['email']
        name = form.cleaned_data['name']
        try:
            with transaction.atomic():
                contact = Contact.objects.create(
                    email=email,
                    name=name
                )
                album = Album.objects.get(id=album_id)
                album.available = False
                booking = Booking.objects.create(
                    contact=contact,
                    created_at=timezone.now(),
                    album=album
                )
                context = {
                    'title': "Merci !",
                    'message': "Nous vous contacterons dès que notre radio retrouvera le chemin des ondes (en résumé : très vite)."
                }
        except IntegrityError:
            context = {
                'title': "Mince !",
                'message': "Une erreur technique est arrivée. Ne vous en faites pas : nous sommes déjà sur le pont du navire pour investiguer. Recommencez votre requête, moussaillon !"
            }
        return render(request, 'store/thanks.html', context)
    else:
        # TODO: see with Regis.
        # I wanted to do a redirection but the "form" object is not passed.
        # I wonder if it's a good practice to do something like:
        # url = reverse('store:detail', args=(album_id=album_id))
        # return HttpResponseRedirect('{}?{}'.format(url, form))
        # I think it's very bad in terms of security.
        # But this solution is bothering me because we repeat the exact thing se have in `detail`

        album = get_object_or_404(Album, pk=album_id)
        artists = [artist.name for artist in album.artists.all()]
        artists_name = " ".join(artists)
        context = {
            'album_title': album.title,
            'artists_name': artists_name,
            'album_id': album.id,
            'form': form,
            'errors': form.errors.items()
        }
        # import pdb; pdb.set_trace()
        return render(request, 'store/detail.html', context)
