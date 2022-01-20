import django_filters
from django_filters import CharFilter

from accounts.models import CustomUser


class UserFilter(django_filters.FilterSet):

    def __init__(self, *args, **kwargs):
        super(UserFilter, self).__init__(*args, **kwargs)
        self.filters['user_nick_name'].label = "Nom d'utilisateur"

    user_nick_name = CharFilter(field_name="nick_name", lookup_expr="icontains")

    class Meta:
        model = CustomUser
        exclude = ["password", "last_login", "first_name", "last_name", "nick_name", "date_of_birth", "gender",
                   "address", "zip_code", "city", "email", "profile_picture", "social_1", "social_2", "social_3",
                   "date_joined", "is_active", "is_admin"]

