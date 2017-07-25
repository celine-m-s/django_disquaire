from django.contrib import admin
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe
from django.contrib.contenttypes.models import ContentType

from .models import Artist, Contact, Booking, Album


# there is not easier way to do this, as per https://stackoverflow.com/questions/2470285/foreign-keys-in-django-admin-list-display
class AdminURLMixin(object):
    def get_admin_url(self, obj):
        content_type = ContentType.objects.get_for_model(obj.__class__)
        # as per https://docs.djangoproject.com/en/1.11/ref/contrib/admin/#admin-reverse-urls
        return reverse("admin:%s_%s_change" % (
            content_type.app_label,
            content_type.model),
            args=(obj.id,))


class BookingInline(admin.TabularInline, AdminURLMixin):
    model = Booking
    extra = 0
    readonly_fields = ["created_at", "contact", 'album_link']
    fieldsets = [
        (None, {'fields': ['contact', 'created_at', 'album_link', 'contacted']})
        ]
    verbose_name = "Réservation"
    verbose_name_plural = "Réservations"

    def album_link(self, obj):
        url = self.get_admin_url(obj.album)
        return mark_safe("<a href='{}'>{}</a>".format(url, obj.album.title))

    def has_add_permission(self, request):
        return False


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    inlines = [BookingInline,]

    def has_add_permission(self, request):
        return False


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin, AdminURLMixin):
    readonly_fields = ["created_at", "contact_link", "album_link"]

    fieldsets = [
        (None, {'fields': ['contact_link', 'album_link', 'created_at', 'contacted']})
        ]

    list_display = ['contact', 'album', 'created_at', 'contacted']

    list_filter = ['created_at', 'contacted']

    def contact_link(self, obj):
        url = self.get_admin_url(obj.contact)
        return mark_safe("<a href='{}'>{}</a>".format(url, obj.contact.name))

    def album_link(self, obj):
        url = self.get_admin_url(obj.album)
        return mark_safe("<a href='{}'>{}</a>".format(url, obj.album.title))

    def has_add_permission(self, request):
        return False


# this is the standard way to do it, as per
# https://docs.djangoproject.com/en/1.11/ref/contrib/admin/#working-with-many-to-many-models
class AlbumArtistInline(admin.TabularInline):
    model = Album.artists.through
    extra = 1
    verbose_name = "Disque"
    verbose_name_plural = "Disques"


@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    inlines = [AlbumArtistInline,]


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    search_fields = ['reference', 'title']
