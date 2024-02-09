# socios/urls.py
from django.urls import path
from . import views


urlpatterns = [
    path('', views.lista_socios, name='lista_socios'),
    path('lista', views.lista_socios_altera, name='lista_socios_altera'),
    path('busca', views.buscar_socio, name='buscar_socio'),
    path('socios', views.buscar_socio, name='buscar_socio'),
    path('cart', views.search_socio, name='search_socio'),
    path('<int:socio_id>/', views.detalhes_socio, name='detalhes_socio'),
    path('cadastrar_socio/', views.cadastrar_socio, name='cadastrar_socio'),
    path('editar_socio/<int:pk>/', views.editar_socio, name='editar_socio'),
    path('excluir_socio/<int:pk>/', views.excluir_socio, name='excluir_socio'),
]
