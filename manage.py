#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

from django.contrib import admin
class CustomAdminSite(admin.AdminSite):
    site_header = 'Controle de Visitantes'

# Registrar a instância personalizada
custom_admin_site = CustomAdminSite(name='custom_admin')

# Substituir a instância padrão do site admin pela personalizada
admin.site = custom_admin_site

# Registrar seus modelos aqui
def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'controle_visitantes.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()