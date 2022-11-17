from django.urls import include, path
from django.views.generic.base import RedirectView

from main import views

urlpatterns = [
    path("", views.index, name="index"),
    path("subscribe/", views.subscribe, name="subscribe"),
    path("blog/", views.BlogView.as_view(), name="blog"),
    path("blog/<slug:slug>/", views.PostView.as_view(), name="post"),
    path(
        "broadcast/",
        views.Broadcast.as_view(),
        name="broadcast",
    ),
    path(
        "unsubscribe/<uuid:key>/",
        views.unsubscribe_key,
        name="unsubscribe_key",
    ),
]

# mentorships
urlpatterns += [
    path("mentorships/", views.MentorshipList.as_view(), name="mentorship_list"),
    path(
        "mentorships/<slug:slug>/",
        views.MentorshipDetail.as_view(),
        name="mentorship_detail",
    ),
]

# workshops / event pages
urlpatterns += [
    path("events/", views.WorkshopList.as_view(), name="workshop_list"),
    path(
        "events/upcoming/", views.WorkshopList.as_view(), name="workshop_list_upcoming"
    ),
    path("events/past/", views.WorkshopList.as_view(), name="workshop_list_past"),
    path("events.ics", views.WorkshopListICS.as_view(), name="workshop_list_ics"),
    path(
        "workshops/", RedirectView.as_view(url="/events/"), name="workshop_list_redir"
    ),
    path(
        "workshops/<slug:slug>/",
        views.AttendanceView.as_view(),
        name="workshop",
    ),
    path(
        "workshops/<slug:slug>/ics/",
        views.workshop_ics,
        name="workshop_ics",
    ),
    path(
        "workshops/<slug:slug>/announce/",
        views.AnnounceView.as_view(),
        name="announce",
    ),
    path(
        "workshops/<slug:slug>/confirm/",
        views.confirm,
        name="confirm",
    ),
]

# images
urlpatterns += [
    path("images/<slug:slug>.<slug:extension>", views.image_raw, name="image_raw"),
    path("images/", views.ImageUpload.as_view(), name="image_list"),
]

# document pages
urlpatterns += [
    path("about/", views.about, name="about"),
    path("philosophy/", views.philosophy, name="philosophy"),
    path("what-we-do/", views.whatwedo, name="whatwedo"),
    path("code-of-conduct/", views.coc, name="coc"),
    path("processes/", views.processes, name="processes"),
    path("values/", views.values, name="values"),
    path("vision/", views.vision, name="vision"),
    path("funding/", views.funding, name="funding"),
    path("office-hours/", views.officehours, name="officehours"),
]

# user system
urlpatterns += [
    path("~<slug:username>/", views.UserDetail.as_view(), name="user_detail"),
    path("accounts/logout/", views.Logout.as_view(), name="logout"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("accounts/create/", views.UserCreate.as_view(), name="user_create"),
    path("accounts/edit/", views.UserUpdate.as_view(), name="user_update"),
    path("accounts/edit/photo/", views.UserAvatar.as_view(), name="user_avatar"),
    path(
        "accounts/edit/photo/remove/",
        views.UserAvatarRemove.as_view(),
        name="user_avatar_remove",
    ),
    path("accounts/delete/", views.UserDelete.as_view(), name="user_delete"),
]
