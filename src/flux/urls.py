from django.urls import path, re_path

from .views import Flux, CreateTicket, CreateReview, ViewTicket, ViewReview, UpdateTicket, UpdateReview, DeleteTicket, DeleteReview, MyPost

app_name = "blog"

urlpatterns = [
    path('', Flux.as_view(), name="flux"),
    path('mypost/', MyPost.as_view(), name="my-post"),
    path('ticket/create/', CreateTicket.as_view(), name="create-ticket"),
    re_path(r'^review/create/(?P<pk>\d+)/$', CreateReview.as_view(), name="create-review"),
    path('ticket/<int:pk>/', ViewTicket.as_view(), name="view-ticket"),
    path('review/<int:pk>/', ViewReview.as_view(), name="view-review"),
    path('ticket/delete/<int:pk>/', DeleteTicket.as_view(), name="delete-ticket"),
    path('review/delete/<int:pk>/', DeleteReview.as_view(), name="delete-review"),
    path('ticket/update/<int:pk>/', UpdateTicket.as_view(), name="update-ticket"),
    path('review/update/<int:pk>/', UpdateReview.as_view(), name="update-review"),
    #path('create/review/<int:pk>/', CreateReview.as_view(), name="create-review"),
]