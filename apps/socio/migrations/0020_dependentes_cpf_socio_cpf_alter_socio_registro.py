# Generated by Django 4.2.8 on 2024-02-05 19:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('socio', '0019_alter_dependentes_registro'),
    ]

    operations = [
        migrations.AddField(
            model_name='dependentes',
            name='cpf',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='socio',
            name='cpf',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='socio',
            name='registro',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Numero da Matricula no caso de servidor publico'),
        ),
    ]
