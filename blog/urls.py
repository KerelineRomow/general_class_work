from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('contacts/', views.contact, name='contacts'),
    path('post/<slug:slug>', views.post_detail, name='post_detail'),
    path('category/<slug:slug>', views.category, name='category'),
    path('tag/<slug:slug>/', views.tag_detail, name='tag_filter'),
    path('search/', views.search, name='search'),
    path('create-post/', views.create_post, name='create_post'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('post/<slug:slug>/delete/', views.delete_post, name='delete_post'),
]
