


from django.urls import path

from . import views



urlpatterns = [

# обычные страницы

    # index страница
    path("", views.index, name="index"),

    # search
    path("search/", views.search.as_view(), name="search"),
    
    # upload
    path("upload/", views.upload.as_view(), name="upload"),

    # get game post
    path("getpost/<int:post_id>/", views.getpost.as_view(), name="getpost"),

    # register
    path("register/", views.register.as_view(), name="register"),

    # login
    path("login/", views.v_login.as_view(), name="login"),

    # logout
    path("logout/", views.v_logout, name="logout"),

# функциональные сслыки

    # get images for js
    path("imgsbyid/", views.get_img_from_post_id.as_view(), name="getimgs"),

    # delete
    path("deletepost/<int:post_id>/", views.delete_post_from_post_id, name="deletepost"),

]