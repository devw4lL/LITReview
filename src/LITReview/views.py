from django.views.generic import ListView


class Home(ListView):
    context_object_name = "posts"
    model = 'dsfqsdf'

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_authenticated:
            return queryset
        return queryset.filter(published=True)