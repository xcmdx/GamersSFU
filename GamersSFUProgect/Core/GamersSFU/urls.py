


from django.urls import path

from . import views



urlpatterns = [

    # index страница
    path("", views.index, name="index"),

    # upload
    path("/upload", views.upload, name="upload")

    # download
    path("/download", views.dowload, name="download")

]