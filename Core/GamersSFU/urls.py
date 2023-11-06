


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


    # login
    path("login/", views.get_login, name="login"),

    # logout
    path("logout/", views.get_logout, name="logout"),

# post sheet

    # register post
    path("post_register/", views.register.as_view(), name="post_register"),

    # login post
    path("post_login/", views.v_login.as_view(), name="post_login"),


# функциональные сслыки

    # get images for js
    path("imgsbyid/", views.get_img_from_post_id.as_view(), name="getimgs"),

    # delete
    path("deletepost/<int:post_id>/", views.delete_post_from_post_id, name="deletepost"),

]