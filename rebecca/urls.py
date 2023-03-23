from django.urls import path
from . import views

urlpatterns = [
    # VIEWS
    path('encarregado/', views.encarregado, name='encarregado-view'),
    path('', views.trelas, name='trelas-view'),
 
    # ACTIONS
    path('upload/', views.upload, name='file-upload'),
    path('procurar/', views.procurar, name='schedule-search'),
    path('modificar/', views.modificar, name='modificar-excel'),

    path('getOrdemData/', views.getOrdemData, name='getOrdemData-request'),
    path('getGruasData/', views.getGruasData, name='getGruasData-request'),
    path('getHoraData/', views.getHoraData, name='getHoraData-request'),

    path('updateData/', views.updateData, name='updateData-request')
]
