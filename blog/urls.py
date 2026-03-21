from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

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
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),
    path('subscribe/', views.subscribe, name='subscribe'),


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
