# evento/urls.py
from django.urls import path
from .views import EventoList

urlpatterns = [
    path('mensal/', EventoList.as_view(), name='evento-list'),  # Alterei o caminho para apenas '/mensal/'
]
