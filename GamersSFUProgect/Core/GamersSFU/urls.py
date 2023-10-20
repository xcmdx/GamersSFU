


from django.urls import path

from . import views



urlpatterns = [

    # index страница
    path("", views.index, name="index"),

    # get images for js
    path("imgsbyid/", views.get_img_from_post_id.as_view(), name="getimgs"),

    # search
    path("search/", views.search.as_view(), name="search"),
    
    # upload
    path("upload/", views.upload.as_view(), name="upload"),

    # get game post
    path("getpost/<int:post_id>/", views.getpost.as_view(), name="getpost"),

    # delete
    path("deletepost/<int:post_id>/", views.delete_post_from_post_id, name="deletepost"),

]