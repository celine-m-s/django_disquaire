from django.db import models

class Artist(models.Model):
    name = models.CharField('nom', max_length=200)

    class Meta:
        verbose_name = "artiste"

    def __str__(self):
        return self.name

class Contact(models.Model):
    email = models.CharField('e-mail', max_length=100)
    name = models.CharField('nom', max_length=200)

    class Meta:
        verbose_name = "prospect"

    def __str__(self):
        return self.name

class Album(models.Model):
    reference = models.IntegerField('référence', blank=True)
    created_at = models.DateTimeField('Date de création', auto_now_add=True)
    available = models.BooleanField('Disponible', default=True)
    title = models.CharField('Titre', max_length=200)
    artists = models.ManyToManyField(Artist, related_name='disks', blank=True)

    class Meta:
        verbose_name = "disque"

    def __str__(self):
        return self.title

class Booking(models.Model):
    created_at = models.DateTimeField('Demande effectuée le', auto_now_add=True)
    contacted = models.BooleanField('Demande traitée', default=False)
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE)
    album = models.OneToOneField(Album)

    class Meta:
        verbose_name = "réservation"

    def __str__(self):
        return self.contact.name
