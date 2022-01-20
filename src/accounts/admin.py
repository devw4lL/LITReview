from django.contrib import admin

from .models import CustomUser


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "email",
                    "nick_name", "date_of_birth", "address", "zip_code", "city",
                    "profile_picture", "social_1", "social_2", "social_3",
                    )
    list_editable = ("last_name", "email",
                    "nick_name", "date_of_birth", "address", "zip_code", "city",
                    "profile_picture", "social_1", "social_2", "social_3",
                    )


admin.site.register(CustomUser, CustomUserAdmin)
