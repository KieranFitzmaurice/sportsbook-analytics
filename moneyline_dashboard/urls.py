from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path('events/<int:pk>/', views.event_info, name='event_info'),
    path('upload_data', views.upload_data, name='upload_data')
]
