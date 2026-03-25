from django.urls import path
from . import views


urlpatterns = [
    path('', views.gallery_list, name='gallery'),
    path('upload/', views.upload, name='upload'),
]