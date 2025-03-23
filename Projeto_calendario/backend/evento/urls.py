# evento/urls.py
from django.urls import path
from .views import EventoCadastro, EventoList, EventoDelete, EventoUpdate

urlpatterns = [
    path('cadastro/', EventoCadastro.as_view(), name='evento-cadastro'),
    path('eventos/<int:mes>/<int:dia>/', EventoList.as_view(), name='retorna-eventos'),
    path('delete/<int:pk>/', EventoDelete.as_view(), name='deleta-eventos'),
    path('update/<int:pk>/', EventoUpdate.as_view(), name='atualiza-eventos'),
]
