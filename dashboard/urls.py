from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('ajax-calculate/', views.ajax_calculate, name='ajax_calculate'),
    path('test/', views.test_view, name='test'),
]