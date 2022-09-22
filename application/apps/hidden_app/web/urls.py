from django.urls import path

from . import views


# Register your urls here

urlpatterns = [path("", views.simple_view)]

# To register this URLS
# path("hidden_app/", include("apps.hidden_app.web.urls"))
