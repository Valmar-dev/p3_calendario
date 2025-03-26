# evento/urls.py
from django.urls import path
from .views import EventoCadastro, EventoList, EventoDelete, EventoUpdate, EventoDetail, EventoMensal, EventoSempre

urlpatterns = [
    path('cadastro/', EventoCadastro.as_view(), name='evento-cadastro'),
    path('eventos/', EventoList.as_view(), name='retorna-eventos'),
    path('delete/<int:pk>/', EventoDelete.as_view(), name='deleta-eventos'),
    path('update/<int:pk>/', EventoUpdate.as_view(), name='atualiza-eventos'),
    path('unicoevento/<int:id>/', EventoDetail.as_view(), name='evento-detalhe'),
    path('eventos/mensal/', EventoMensal.as_view(), name='evento-mensal'),
    path('eventos/sempre/', EventoSempre.as_view(), name='eventos-sempre'),
]
