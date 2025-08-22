
from django.contrib import admin
from django.urls import include,path

from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static



from apps.dashboard import views
from dashboard.views import index
from visitantes.views import (
    registrar_visitante, informacoes_visitante, finalizar_visita,buscar_visitante,identificacao
)

urlpatterns = [
    path("admin/", admin.site.urls),
    
    #path("login/", auth_views.LoginView.as_view(
     #   template_name="login.html"
      #  ),
       # name="login"
    #),
    path('accounts/', include('apps.usuarios.urls')),  # Incluindo as URLs do app 'usuarios'

    # URLs para resetar a senha
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'), 

    path("logout/", auth_views.LogoutView.as_view(
        template_name="logout.html"
        ),
        name="logout"
    ),
    path("socios/", include('socio.urls')),
    path("", index, name="index"),
    path("registrar-visitante/", registrar_visitante, name="registrar_visitante"),
    path("visitantes/<int:id>/", informacoes_visitante, name="informacoes_visitante"),
    path("visitantes/<int:id>/finalizar-visita/", finalizar_visita, name="finalizar_visita"),
    path("buscar/", buscar_visitante, name="buscar_visitante"),
 
    #path("listad/", lista_dependentes, name="lista_dependentes"),
    #path("cart/", identificacao, name="carteirinha"),
    
    
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
