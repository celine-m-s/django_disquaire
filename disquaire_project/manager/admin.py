from django.contrib import admin
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe
from django.contrib.contenttypes.models import ContentType

from .models import Artist, Contact, Booking, Disk


class AdminURLMixin(object):
    def get_admin_url(self, obj):
        content_type = ContentType.objects.get_for_model(obj.__class__)
        return reverse("admin:%s_%s_change" % (
            content_type.app_label,
            content_type.model),
            args=(obj.id,))


class BookingInline(admin.TabularInline, AdminURLMixin):
    model = Booking
    extra = 0
    readonly_fields = ["created_at", "contact", 'disk_link']
    fieldsets = [
        (None, {'fields': ['contact', 'created_at', 'disk_link', 'contacted']})
        ]
    verbose_name = "Réservation"
    verbose_name_plural = "Réservations"

    def disk_link(self, obj):
        url = self.get_admin_url(obj.disk)
        return mark_safe("<a href='{}'>{}</a>".format(url, obj.disk.title))

    def has_add_permission(self, request):
        return False


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    inlines = [BookingInline,]

    def has_add_permission(self, request):
        return False


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin, AdminURLMixin):
    readonly_fields = ["created_at", "contact_link", "disk_link"]

    fieldsets = [
        (None, {'fields': ['contact_link', 'disk_link', 'created_at', 'contacted']})
        ]

    list_display = ['contact', 'disk', 'created_at', 'contacted']

    list_filter = ['created_at', 'contacted']

    def contact_link(self, obj):
        url = self.get_admin_url(obj.contact)
        return mark_safe("<a href='{}'>{}</a>".format(url, obj.contact.name))

    def disk_link(self, obj):
        url = self.get_admin_url(obj.disk)
        return mark_safe("<a href='{}'>{}</a>".format(url, obj.disk.title))

    def has_add_permission(self, request):
        return False


class DiskArtistInline(admin.TabularInline):
    model = Disk.artists.through
    extra = 1
    verbose_name = "Disque"
    verbose_name_plural = "Disques"


@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    inlines = [DiskArtistInline,]


@admin.register(Disk)
class DiskAdmin(admin.ModelAdmin):
    search_fields = ['reference', 'title']
