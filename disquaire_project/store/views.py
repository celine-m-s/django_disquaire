from django.shortcuts import get_object_or_404, render, HttpResponseRedirect, reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils import timezone
from django.db import transaction, IntegrityError

from .models import Album, Artist, Contact, Booking
from .forms import ContactForm, ParagraphErrorList


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

    if request.method == 'POST':
        # Grab data from the existing form
        form = ContactForm(request.POST, error_class=ParagraphErrorList)

        # Validation made by forms.py > ContactForm
        if form.is_valid():
            email = form.cleaned_data['email']
            name = form.cleaned_data['name']

            # We use a transaction to secure our queries.
            # If one query fails, a rollback is performed and an IntegrityError is raised.
            try:
                with transaction.atomic():
                    contact = Contact.objects.filter(email=email)

                    if not contact.exists():
                        # If a contact is not registered, create a new one.
                        contact = Contact.objects.create(
                            email=email,
                            name=name
                        )
                    else:
                        # We need only 1 object and not a queryset
                        contact = contact.first()

                    # If no album matches the id, the form must have been tweaked so
                    # returning a 404 is the best solution.
                    album = get_object_or_404(Album, id=album_id)
                    booking = Booking.objects.create(
                        contact=contact,
                        album=album
                    )

                    # Make sure no one can book the album again
                    album.available = False
                    album.save()

                    # Then thank the user!
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
            # Form data don't match the expected format.
            # Add errors to the template.
            context['errors'] = form.errors.items()
    else:
        # If this is a GET method, we create a new form
        form = ContactForm()


    context = {
        'album_title': album.title,
        'artists_name': artists_name,
        'album_id': album.id,
        'form': form,
        'thumbnail': album.picture
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
