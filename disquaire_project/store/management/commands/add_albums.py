import os
import logging as lg

import yaml
from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand
from store.models import Album, Artist


# this probably shouldn't go here. It's the role of the settings to define the
# log level. Then, if you want to decrease the logging level, you should do it
# for this module only. For example if the '--verbose' option is passed to the
# script
# lg.basicConfig(level=lg.DEBUG)


# So you are using custom commands; does that mean you will need to present them in the course?
# If you don't want to do that, you can use `./manage.py loaddata albums.json` instead: 
# https://docs.djangoproject.com/en/1.10/ref/django-admin/#loaddata
class Command(BaseCommand):
    help = 'Add albums to the database from a yml file located in data/'

    def handle(self, *args, **options):
        reference = 0
        # open file with data
        directory = os.path.dirname(os.path.dirname(__file__))
        path = os.path.join(directory, 'data', 'albums.yml')
        with open(path) as file:
            data = yaml.load(file)
            albums = data['albums']
            for album in albums:
                # Create artists
                artists = []
                for artist in album['artists']:
                    # Note that you can simplify this whole try:... except block by writing:
                    # stored_artist, created = Artist.objects.get_or_create(name=artist)
                    # if created:
                    #     lg.info('Artist created: %s', stored_artist)
                    # else:
                    #     lg.info('Artist found: %s', stored_artist)

                    try:
                        stored_artist = Artist.objects.get(name=artist)
                        lg.info('Artist found: %s', stored_artist)
                    except ObjectDoesNotExist:
                        stored_artist = Artist.objects.create(name=artist)
                        lg.info('Artist created: %s', stored_artist)
                    artists.append(stored_artist)
                # Find or create album
                # If we didn't have to take care of the reference field, we could also use `get_or_create` here.
                try:
                    stored_album = Album.objects.get(title=album['title'])
                    lg.info('Album found: %s', stored_album.title)
                    # If the album already exists, we don't add artists to it?
                except ObjectDoesNotExist:
                    # The reference field is a major issue, I think. It should
                    # be unique, and auto-generated. If we run this script
                    # twice, there are going to be duplicate reference fields.
                    # Note that, implicitly, there is already an auto-incremented id field in every model
                    reference += 1
                    album = Album.objects.create(
                        title=album['title'],
                        reference=reference
                    )
                    # I don't think this is going to work because the album is not saved after that call.
                    # album.artists = artists
                    # As per https://docs.djangoproject.com/en/1.11/ref/models/relations/#django.db.models.fields.related.RelatedManager.add
                    # we should probably write instead:
                    album.artists.add(*artists, bulk=True)
                    lg.info('New album: %s', stored_artist)
