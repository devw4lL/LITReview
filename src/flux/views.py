from itertools import chain

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Value, CharField, BooleanField
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView

from .models import Ticket, Review
from .forms import CreateTicketForm, CreateReviewForm
from followers.models import UserFollows


class Flux(LoginRequiredMixin, ListView):
    """
        Génere le flux de ticket/review pour l'utilisateur connecté.
    """
    model = Ticket
    template_name = "flux.html"
    context_object_name = "posts"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        ticket_with_review, ticket_without_review = get_users_viewable_tickets(get_users_viewable_ids(self.request))
        reviews = get_users_viewable_reviews(get_users_viewable_ids(self.request))
        feed = sorted(chain(*reviews, *ticket_with_review, *ticket_without_review), key=lambda post: post.time_created,
                      reverse=True)
        context['posts'] = feed
        return context


class MyPost(Flux):
    """
    Génere le flux de posts de l'utilisateur connecté.
    """

    def get_context_data(self, *, object_list=None, **kwargs):
        context = {}
        ticket_with_review, ticket_without_review = get_users_viewable_tickets([self.request.user.id])
        reviews = get_users_viewable_reviews([self.request.user.id])
        feed = sorted(chain(*reviews, *ticket_with_review, *ticket_without_review), key=lambda post: post.time_created,
                      reverse=True)
        context['mypost'] = True
        context['posts'] = feed
        print(context)
        return context


class CreateTicket(LoginRequiredMixin, CreateView):
    template_name = "create_ticket.html"
    model = Ticket
    form_class = CreateTicketForm
    success_url = reverse_lazy('blog:flux')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class CreateReview(LoginRequiredMixin, CreateView):
    template_name = "create_review.html"
    model = Review
    form_class = CreateTicketForm
    success_url = reverse_lazy('blog:flux')

    def get(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if kwargs and kwargs['pk'] != '0':
            ticket_form = CreateTicketForm(instance=Ticket.objects.get(pk=kwargs['pk']))
            ticket = Ticket.objects.get(pk=kwargs['pk'])
            review_form = CreateReviewForm()
            return self.render_to_response(self.get_context_data(ticket=ticket, review=review_form))
        else:
            ticket_form = CreateTicketForm()
            review_form = CreateReviewForm()
            return self.render_to_response(self.get_context_data(ticket=ticket_form, review=review_form))

    def post(self, request, *args, **kwargs):
        self.object = None
        if self.kwargs and kwargs['pk'] != '0':
            review_form = CreateReviewForm(self.request.POST, self.request.FILES)
            if review_form.is_valid():
                form = CreateTicketForm(instance=Ticket.objects.get(pk=kwargs['pk']))
                return self.form_valid(form, review_form)
            else:
                raise ValueError('Review Form invalid')

        else:
            form_class = self.get_form_class()
            form = self.get_form(form_class)
            review_form = CreateReviewForm(self.request.POST, self.request.FILES)
            if form.is_valid() and review_form.is_valid():
                return self.form_valid(form, review_form)

    def form_valid(self, form, review_form):
        if form:
            form.instance.user = self.request.user
            form.save()
            review_form.instance.ticket = Ticket.objects.get(pk=form.instance.pk)
            review_form.instance.user = self.request.user
            review_form.save()
            return super().form_valid(form)
        else:
            review_form.instance.ticket = Ticket.objects.get(pk=self.kwargs['pk'])
            review_form.instance.user = self.request.user
            review_form.save()
            return super().form_valid(review_form)


class UpdateTicket(LoginRequiredMixin, UpdateView):
    model = Ticket
    form_class = CreateTicketForm
    template_name = "update_ticket.html"
    context_object_name = "ticket"

    def get(self, request, *args, **kwargs):
        if self.request.user.id == Ticket.objects.get(pk=kwargs['pk']).user.id:
            return super().get(request, *args, **kwargs)
        else:
            return redirect('blog:flux')


class UpdateReview(LoginRequiredMixin, UpdateView):
    model = Review
    form_class = CreateReviewForm
    template_name = "update_review.html"
    context_object_name = "review"

    def get(self, request, *args, **kwargs):
        if self.request.user == Review.objects.get(pk=kwargs['pk']).user:
            return super().get(request, *args, **kwargs)
        else:
            return redirect('blog:flux')


class DeleteTicket(LoginRequiredMixin, DeleteView):
    model = Ticket
    template_name = 'delete_ticket.html'
    success_url = reverse_lazy('blog:flux')

    def get(self, request, *args, **kwargs):
        ticket = Ticket.objects.get(pk=kwargs['pk'])
        if kwargs['pk'] and request.user == ticket.user:
            self.object = self.get_object()
            context = self.get_context_data(object=self.object)
            return self.render_to_response(self.get_context_data(context=context, ticket=ticket))
        else:
            return redirect('blog:flux')


class DeleteReview(LoginRequiredMixin, DeleteView):
    model = Review
    template_name = 'delete_review.html'
    success_url = reverse_lazy('blog:flux')

    def get(self, request, *args, **kwargs):
        review = Review.objects.get(pk=kwargs['pk'])
        post = {}
        if kwargs['pk'] and request.user == review.user:
            self.object = self.get_object()
            context = self.get_context_data(object=self.object)
            post['ticket'] = Ticket.objects.get(pk=review.ticket_id)
            return self.render_to_response(self.get_context_data(context=context, post=post))
        else:
            return redirect('blog:flux')

    def get_object(self, queryset=None):
        obj = super().get_object()
        obj_ticket = Ticket.objects.get(pk=obj.ticket_id)

        return obj, obj_ticket

    def get_success_url(self):
        if self.success_url:
            return self.success_url

    def form_valid(self, form):
        success_url = self.get_success_url()
        [post_object.delete() for post_object in self.object]
        return HttpResponseRedirect(success_url)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        return redirect('blog:flux')


class ViewTicket(LoginRequiredMixin, DetailView):
    template_name = 'ticket.html'
    model = Ticket


class ViewReview(LoginRequiredMixin, DetailView):
    template_name = 'review.html'
    model = Review

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data()
        context['ticket'] = Ticket.objects.get(pk=context['review'].ticket.id)
        return context


def get_users_viewable_reviews(users_ids):
    """

    Args:
        users_ids: ids du ou des utilisateurs.

    Returns: Queryset de Review associées au ids.

    """

    return [
        Review.objects.filter(user_id=ids, ticket_id__isnull=False).annotate(content_type=Value('REVIEW', CharField()))
        for ids in users_ids]


def get_users_viewable_tickets(users_ids):
    """

    Args:
        users_ids: ids du ou des utilisateurs.

    Returns: Two list of QuerySet with TICKET annotation and Boolean has_review=True if ticket has review
            - ticket_with_review
            - ticket_without_review
    """

    ticket_with_review = [Ticket.objects.filter(user_id=ids, review__isnull=False).annotate(
        content_type=Value('TICKET', CharField()),
        has_review=Value(True, BooleanField())) for ids in users_ids]

    ticket_without_review = [
        Ticket.objects.filter(user_id=ids, review__isnull=True).annotate(
            content_type=Value('TICKET', CharField()),
            has_review=Value(False, BooleanField())) for ids in users_ids]
    return ticket_with_review, ticket_without_review


def get_users_viewable_ids(request):
    """

    Args:
        request: Données request id de l'utilisateur connecté.

    Returns: Liste d'ids utilisateur de l'on suit, qui nous suivent.

    """
    followed_users = [user.followed_user_id for user in UserFollows.objects.filter(user_id=request.user.id)]
    followed_users.append(request.user.id)
    return followed_users




