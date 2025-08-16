from django.urls import path

from app import views

urlpatterns = [
    path('', views.main, name='main'),
    path('<str:text>/', views.search, name='search'),
]
