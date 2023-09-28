


from django.urls import path

from . import views



urlpatterns = [

    # index страница
    path("", views.index, name="index"),

    # upload
    path("upload/", views.upload.as_view(), name="upload"),

    # get game post

    # for js
    path("imgsbyid/", views.get_img_from_post_id.as_view(), name="getimgs")

]