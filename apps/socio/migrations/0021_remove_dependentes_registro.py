# Generated by Django 4.2.8 on 2024-02-05 19:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('socio', '0020_dependentes_cpf_socio_cpf_alter_socio_registro'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dependentes',
            name='registro',
        ),
    ]
