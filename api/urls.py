from django.urls import path, re_path
from . import views

# Try using re_path then later on we would use path to 
# see if it maintains the same functionality . 
urlpatterns = [
    re_path('login', views.login),
    re_path('signup', views.signup),
    re_path('test_token', views.test_token),
]
