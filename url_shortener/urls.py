from django.contrib import admin
from django.urls import re_path, include
from shortener.api.v1.views import redirect_short_url, home

urlpatterns = [
    re_path(
        r"^api/v1/",
        include([
            re_path(r"^shortner/", include("shortener.api.v1.urls", namespace="api_v1_shortener")),
        ])
    ),
    re_path(r"^admin/", admin.site.urls),
    # Root homepage and short-code redirect
    re_path(r"^$", home, name="home"),
    re_path(r"^(?P<short_code>[\w-]+)/$", redirect_short_url, name="redirect_short_url_root"),
]
