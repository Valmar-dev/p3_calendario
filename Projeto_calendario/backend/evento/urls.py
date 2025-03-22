# evento/urls.py
from django.urls import path
from .views import EventoCadastro

urlpatterns = [
    path('cadastro/', EventoCadastro.as_view(), name='evento-cadastro'),
]
