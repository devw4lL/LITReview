from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import ListView

from accounts.models import CustomUser
from .models import UserFollows
from .filters import UserFilter


class GetCustomUser(LoginRequiredMixin, ListView):
    """
    Liste tout les utilisateurs enregistrés sur le site.
    """
    model = CustomUser
    template_name = "users_search.html"
    context_object_name = "users"

    def get_context_data(self, *, object_list=None, **kwargs):
        users = CustomUser.objects.all()
        social = FollowedFollowers()
        userfilter = UserFilter(self.request.GET, queryset=users)
        users = userfilter.qs
        context = {'filter': userfilter, 'users': users, 'followed_users': get_followed_users(self.request),
                   'followers': get_followers(self.request)}
        return super().get_context_data(**context)


class FollowedFollowers(LoginRequiredMixin, ListView):
    """
    Liste tout les utilisateurs qui suivent l'utilisateur connecté.
    Liste tout les utilisateurs que l'utilisateur connecté suit.
    """

    model = UserFollows
    paginate_by = 10
    template_name = "social.html"
    context_object_name = "users"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['followed_users'] = get_followed_users(self.request)
        context['followers'] = get_followers(self.request)
        return context


@login_required
def follow_user(request, pk=None):
    """

    Args:
        request: Données session utilisateur.
        pk: Primary Key de l'utilisateur à suivre.

    Returns: Ajoute l'utilisateur dans les followers.

    """
    user_to_follow = CustomUser.objects.get(pk=pk).pk
    follow = UserFollows()

    if request.method == "GET":
        if pk is not None:
            follow.user_id = get_current_user(request)
            follow.followed_user_id = user_to_follow
            follow.save()
            return redirect("followers:get-users")
    else:
        raise ValueError("Pas d'id utilisateur")


@login_required
def unfollow_user(request, pk=None):
    """

    Args:
        request: Données session utilisateur.
        pk: id utilisateur à ne plus suivre.

    Returns: Retire un utilisateur de la liste des followers pour l'utilisateur connecté.

    """
    user_to_unfollow = CustomUser.objects.get(pk=pk)

    if pk is not None:
        if request.method == 'GET':
            UserFollows.objects.filter(user_id=get_current_user(request), followed_user_id=user_to_unfollow).delete()
            return redirect("followers:social")
    else:
        raise ValueError('Pas de données dans request')


@login_required
def get_current_user(request):
    """

    Args:
        request: Données session utilisateur.

    Returns: Primary Key de l'utilisateur en cours.

    """
    if request is not None:
        return CustomUser.objects.get(pk=request.user.pk).pk
    else:
        raise ValueError('Pas de données dans request')


def get_followed_users(request):
    return [CustomUser.objects.get(pk=users.followed_user.pk) for users in
            UserFollows.objects.filter(user_id=request.user.pk)]


def get_followers(request):
    return [CustomUser.objects.get(pk=users.followed_user_id) for users in
            UserFollows.objects.filter(followed_user_id=request.user.pk)]
