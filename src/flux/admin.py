from django.contrib import admin

from .models import Ticket, Review


class CustomTicket(admin.ModelAdmin):
    list_display = ("title", "slug", "description", "image", "user", "time_created", )
    list_display_links = ("title", )
    list_editable = ("description", "image", )


class CustomReview(admin.ModelAdmin):
    list_display = ("headline", "body", "rating", "user", "time_created", )
    list_display_links = ("headline", )
    list_editable = ("body", "rating", )


admin.site.register(Ticket, CustomTicket)
admin.site.register(Review, CustomReview)
