from django.urls import include, path
from django.views.generic.base import RedirectView

from main import views

urlpatterns = [
    path("", views.index, name="index"),
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

# incidents
urlpatterns += [
    path("incidents/<int:pk>/", views.IncidentDetail.as_view(), name="incident_detail"),
]

# document pages
urlpatterns += [
    path("code-of-conduct/", views.coc, name="coc"),
    path("projects/", views.projects, name="projects"),
]

# redirects
urlpatterns += [
    path(
        "discord/",
        RedirectView.as_view(url="https://discord.gg/bzjKNG4bUU"),
        name="discord",
    ),
]

# user system
urlpatterns += [
    path("directory/", views.Directory.as_view(), name="directory"),
    path("profile/", views.profile, name="profile"),
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
