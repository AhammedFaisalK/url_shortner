from django.urls import re_path
from . import views

app_name = "api_v1_shortener"

urlpatterns = [
    re_path(r"^$", views.home, name="home"),  # API v1 root/docs
    re_path(r"^urls/$", views.URLCreateView.as_view(), name="create_url"),
    re_path(r"^urls/list/$", views.URLListView.as_view(), name="list_urls"),
    re_path(r"^stats/(?P<short_code>[\w-]+)/$", views.url_stats, name="url_stats"),
    re_path(r"^health/$", views.health_check, name="health_check"),
    re_path(r"^(?P<short_code>[\w-]+)/$", views.redirect_short_url, name="redirect_short_url"),
]
