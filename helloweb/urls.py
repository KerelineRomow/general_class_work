from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('datetime/', views.current_datetime, name='current_datetime'),
    path('datetime_class/', views.CurrentDateTime.as_view()),
    path('citata/', views.citata, name='citata'),
]