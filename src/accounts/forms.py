from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.db import models

from .models import CustomUser


class UserRegistrationForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({

        })
        self.fields['password1'].help_text = "Le mot de passe doit contenir au " \
                                             "minimum 8 charactères et être alphanumérique"

    class Meta:
        model = CustomUser
        fields = ("first_name", "last_name", "email", "password1", "password2",
                  "nick_name", "date_of_birth", "address", "zip_code", "city",
                  "profile_picture", "social_1", "social_2", "social_3",
        )


