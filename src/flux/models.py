import os

from django.db import models
from django.conf import settings
from django.template.defaultfilters import slugify
from django.core.validators import MinValueValidator, MaxValueValidator
from PIL import Image

from LITReview.utils import rename_picture, resize_image


class Ticket(models.Model):
    title = models.CharField(max_length=128)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    description = models.TextField(max_length=2048, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True, upload_to=rename_picture)
    time_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-time_created']
        verbose_name = "Ticket"

    def __str__(self):
        return f'TICKET {self.time_created.strftime("%Y - %H:%M:%S - %Z")} - {self.title}'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)

        elif not self.image:
            self.image = os.path.join('tickets', 'no-image-icon.png')
        super().save()
        resize_image(self.image.path, 'ticket_image').save(self.image.path)


class Review(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(default=0,
                                              validators=[MinValueValidator(0), MaxValueValidator(5)])
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    headline = models.CharField(max_length=128)
    body = models.TextField(max_length=8192, blank=True)
    time_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'REVIEW {self.time_created.strftime("%Y - %H:%M:%S - %Z")} - {self.headline}'

    @property
    def get_rating(self):
        return round(self.rating)



