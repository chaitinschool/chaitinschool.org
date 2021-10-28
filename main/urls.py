from django.urls import path

from main import views

urlpatterns = [
    path("", views.index, name="index"),
    path(
        "workshops/<slug:slug>/",
        views.WorkshopDetailView.as_view(),
        name="workshop_detail",
    ),
    path("blog/", views.BlogView.as_view(), name="blog"),
    path("blog/<slug:slug>/", views.PostView.as_view(), name="post"),
    path(
        "unsubscribe/<uuid:key>/",
        views.unsubscribe_key,
        name="unsubscribe_key",
    ),
]
