from django.urls import path
from . import views

urlpatterns = [
    path('link-shortener/', views.link_shortener, name='link-shortener'),
]
