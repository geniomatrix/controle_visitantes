# Generated by Django 4.2.8 on 2024-01-22 20:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('socio', '0011_dependentes_dtexame_fin_dependentes_dtexame_ini_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dependentes',
            name='validade',
            field=models.DateField(blank=True, null=True, verbose_name='Validade da Filiacao'),
        ),
    ]