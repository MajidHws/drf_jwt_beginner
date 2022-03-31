from django.urls import path, include
from .views import register_view, login_view, user_view, logout_view


urlpatterns = [
    path('register/', register_view, name="register"),
    path('login/', login_view, name="login"),
    path('user/', user_view, name="user"),
    path('logout/', logout_view, name="logout"),
]