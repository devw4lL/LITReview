import os

from django.contrib.auth.validators import UnicodeUsernameValidator, ASCIIUsernameValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.utils import timezone
from django.core import validators


from LITReview.utils import rename_picture, resize_image


class CustomUserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Vous devez entrer un email.")
        user = self.model(
            email=self.normalize_email(email)
        )

        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        user = self.create_user(email=email, password=password, **extra_fields)
        print('Custom CREATE SUPERUSER')
        user.is_admin = True
        user.save()
        return user


class CustomUser(AbstractBaseUser):

    class GenderChoices(models.TextChoices):
        HOMME = 'HOMME', _('HOMME')
        FEMME = 'FEMME', _('FEMME')

    class Meta:
        verbose_name = "Utilisateur"
        verbose_name_plural = "Utilisateurs"

    first_name = models.CharField(max_length=150, blank=False, validators=[ASCIIUsernameValidator], verbose_name="Nom")
    last_name = models.CharField(max_length=150, blank=False, validators=[ASCIIUsernameValidator],
                                 verbose_name="Prenom")
    nick_name = models.CharField(max_length=150, blank=True, unique=True, validators=[UnicodeUsernameValidator],
                                 verbose_name="Nom d'utilisateur (Public)")
    date_of_birth = models.DateTimeField(blank=True, null=True, verbose_name="Date de naissance")
    # password = models.CharField(max_length=128, blank=False, verbose_name="Mot de passe")
    gender = models.PositiveSmallIntegerField(choices=GenderChoices.choices, blank=True, null=True)
    address = models.CharField(max_length=500, blank=True, verbose_name="Adresse")
    zip_code = models.CharField(max_length=15, blank=True, verbose_name="Code postal")
    city = models.CharField(max_length=150, blank=True, verbose_name="Ville")
    email = models.EmailField(max_length=254, unique=True, verbose_name="Adresse email")
    profile_picture = models.ImageField(upload_to=rename_picture, default="no_profile_picture.png")
    social_1 = models.CharField(max_length=150, blank=True, validators=[ASCIIUsernameValidator],
                                verbose_name="Réseau Social #1")
    social_2 = models.CharField(max_length=150, blank=True, validators=[ASCIIUsernameValidator],
                                verbose_name="Réseau Social #2")
    social_3 = models.CharField(max_length=150, blank=True, validators=[ASCIIUsernameValidator],
                                verbose_name="Réseau Social #3")
    date_joined = models.DateTimeField(default=timezone.now, verbose_name="Date d\'inscription")
    # last_login = models.DateTimeField(blank=True, null=True, verbose_name="Dernière connexion")
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False, verbose_name='Membre du staff') #pour interface administration
    is_admin = models.BooleanField(default=False) #droit d'administration

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['nick_name']
    objects = CustomUserManager()

    def __str__(self):
        return f"{self.nick_name}"

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

    def save(self, *args, **kwargs):

        if not self.profile_picture:
            self.image = os.path.join(f"{self.profile_picture}", 'users', 'no-image-icon.png')
        super().save()
        resize_image(self.profile_picture.path, size='profile').save(self.profile_picture.path)
