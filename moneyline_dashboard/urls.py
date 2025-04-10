from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('upcoming_events', views.upcoming_events, name='upcoming_events'),
    path('upcoming_events/<int:pk>/', views.event_info, name='event_info'),
    path('portfolios', views.betting_portfolios, name='betting_portfolios'),
    path('upload_data', views.upload_data, name='upload_data')
]
