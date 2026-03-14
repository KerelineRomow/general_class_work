from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('contacts/', views.contact, name='contacts'),
    path('post/<slug:slug>', views.post_detail, name='post_detail'),
    path('category/<slug:slug>', views.category, name='category'),
    path('tag/<slug:slug>/', views.tag_detail, name='tag_filter'),
]
