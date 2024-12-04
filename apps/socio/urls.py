# socios/urls.py
from django.urls import path
from . import views



urlpatterns = [
    path('', views.lista_socios, name='lista_socios'),
    path('lista', views.lista_socios_altera, name='lista_socios_altera'),
    path('listad', views.lista_dependentes, name='lista_dependentes'),
    path('listacart', views.lista_socioscart, name='lista_socioscart'),
    path('busca', views.buscar_socio, name='buscar_socio'),
    path('socios', views.buscar_socio, name='buscar_socio'),
    path('cart', views.search_socio, name='search_socio'),
    path('<int:socio_id>/', views.detalhes_socio, name='detalhes_socio'),
    path('carteirinha/<int:pk>', views.carteirinha, name='carteirinha'),
    path('cartdep/<int:pk>', views.cartdep, name='cartdep'),
    path('cadastrar_socio/', views.cadastrar_socio, name='cadastrar_socio'),
    path('editar_socio/<int:pk>/', views.editar_socio, name='editar_socio'),
    path('editar_socio_foto/<int:pk>/', views.editar_socio_foto, name='editar_socio_foto'),
    path('capturar_foto/', views.capturar_foto, name='capturar_foto'),
    path('editar_dependente/<int:pk>/', views.editar_dependente, name='editar_dependente'),
    path('excluir_socio/<int:pk>/', views.excluir_socio, name='excluir_socio'),
    path('pagar_taxasocio/<int:pk>/', views.pagar_taxasocio, name='pagar_taxasocio'),
    path('pagar_taxadep/<int:pk>/', views.pagar_taxadep, name='pagar_taxadep'),
]
