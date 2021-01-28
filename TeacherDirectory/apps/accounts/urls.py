from django.urls import path,include
from . views import LoginUser,LogoutUser

app_name="accounts"
urlpatterns=[
    path("user_login/",LoginUser,name="user-login"),
    path("user_logout/",LogoutUser,name="user-logout"),
]