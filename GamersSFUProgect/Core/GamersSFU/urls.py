


from django.urls import path

from . import views



urlpatterns = [

    # index страница
    path("", views.index, name="index"),

]