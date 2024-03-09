from django.contrib import admin

from .models import Socio, Dependentes

class SocioAdmin(admin.ModelAdmin):
    search_fields = ['nome', 'email', 'tpsocio']  # Lista de campos pelos quais deseja realizar a busca

class DependAdmin(admin.ModelAdmin):
    search_fields = ['nome', 'tpsocio']  # Lista de campos pelos quais deseja realizar a busca

admin.site.register(Socio,SocioAdmin)
admin.site.register(Dependentes,DependAdmin)

