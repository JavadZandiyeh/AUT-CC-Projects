from django.urls import path
from . import views

urlpatterns = [
    path('user/sign-up/', views.sign_up, name='sign-up'),
    path('user/login/', views.login, name='login'),
    path('file/upload/', views.file_upload, name='file-upload'),
    path('file/run/', views.file_run, name='file-run'),
    path('results/', views.get_results, name='get-results')
]
