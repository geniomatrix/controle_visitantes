# Generated by Django 4.2.8 on 2024-02-05 18:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('socio', '0017_dependentes_registro_socio_registro'),
    ]

    operations = [
        migrations.AlterField(
            model_name='socio',
            name='registro',
            field=models.CharField(max_length=20, null=True, verbose_name='Numero da Matricula'),
        ),
    ]
