"""conf URL Configuration
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
"""
from django.urls import path
from . import views

app_name = 'votacion'
urlpatterns = [
    # Urna
    path('urnas/<int:pk>/', views.DisabledUrna.as_view(), name='disabled-urna'),
    path('urnas/<int:pk>/candidatos/', views.EnabledUrna.as_view(), name='enabled-urna'),
    path('urnas/<int:pk>/candidatos/<int:candidato>',
         views.Confirmar.as_view(), name='confirmar'),
    path('urnas/<slug:slug>/', views.UrnaListView.as_view(), name='urna-list'),
    #
    path('urnas/<slug:slug>/<int:pk>/',
         views.UrnaDetailView.as_view(), name='urna-detail'),
    path('urnas/<slug:slug>/<int:pk>/enabled/<int:elector_pk>',
         views.UrnaEnebledElectorView.as_view(), name='urna-enabled-elector'),
]
