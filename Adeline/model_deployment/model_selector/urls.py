from django.urls import path
from . import views

app_name = 'model_selector'

urlpatterns = [
    path('', views.home, name='home'),
    path('predict/', views.index, name='predict'),
]