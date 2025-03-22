# evento/urls.py
from django.urls import path
from .views import EventoCadastro, EventoList, EventoDelete

urlpatterns = [
    path('cadastro/', EventoCadastro.as_view(), name='evento-cadastro'),
    path('eventos/', EventoList.as_view(), name='retorna-eventos'),
    path('delete/<int:pk>/', EventoDelete.as_view(), name='deleta-eventos'),
]
