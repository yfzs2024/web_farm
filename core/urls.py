from django.urls import path
from . import views

app_name = 'core'
urlpatterns = [
    path('user_data', views.user_data),
]