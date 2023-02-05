from django.urls import path
from . import views


urlpatterns = [

    path('', views.home, name='home'),
    # Auth urls
    path('sighup', views.sighup, name='sighup'),
    path('login', views.login, name='login'),
    # Tods
    path('currenttodos', views.current_to_do, name='currenttodos'),
]

