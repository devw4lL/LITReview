from django.forms import ModelForm, RadioSelect, inlineformset_factory, Textarea, CharField

from .models import Ticket, Review


class CreateTicketForm(ModelForm):
    class Meta:
        model = Ticket
        labels = {
            'title': 'Titre:',
            'description': 'Description de votre demande de critique:',
            'image': 'Sélectionner une image de l\'article ou de la couverture du livre.'
        }
        fields = {'title', 'description', 'image'}
        widgets = {
            "description": Textarea(attrs={'cols': 100, 'rows': 25}),
        }


class CreateReviewForm(ModelForm):
    class Meta:
        CHOICES = [(str(x), str(x)) for x in range(0, 6)]
        model = Review
        labels = {
            'headline': 'Avis',
            'body': 'Votre critique:',
            'rating': 'Score'
        }
        fields = ['headline', 'body', 'rating']
        widgets = {'rating': RadioSelect(choices=CHOICES, attrs={'class': 'form-check-inline'})}


ReviewFormSet = inlineformset_factory(Ticket, Review, fields=('id', ))
