from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('signup', views.signup, name='signup'),
    path('post', views.post, name='post'),
    path('logout', views.logout,name='logout'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('new_post', views.new_post, name='new_post'),
    path('chat/<friend>', views.chat, name='chat'),
    path('delete/<id>', views.delete, name='chat')
]