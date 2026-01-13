from django.contrib import admin
from django.utils.html import format_html

from feed.models import Ticket, Review, UserFollows

class TicketAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description', 'image_preview', 'user', 'time_created')

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height: 50px;" />',
                obj.image.url
            )
        return "—"

    image_preview.short_description = "Image"

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'ticket', 'headline', 'body', 'user', 'time_created')


admin.site.register(Ticket, TicketAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(UserFollows)
