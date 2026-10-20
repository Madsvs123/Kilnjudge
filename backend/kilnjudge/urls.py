from django.contrib import admin
from django.urls import include, path

admin.site.site_header = "Kilnjudge"
admin.site.site_title = "Kilnjudge"
admin.site.index_title = "Practice problems"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("judge.urls")),
]
