from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("users/", include("users.urls")),
    path("currencies/", include("currencies.urls")),
    path("transactions/", include("transactions.urls")),
    path("exchanges/", include("exchanges.urls")),
]
