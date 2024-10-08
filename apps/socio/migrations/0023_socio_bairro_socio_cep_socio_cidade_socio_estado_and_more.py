# Generated by Django 4.2.8 on 2024-02-07 14:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('socio', '0022_dependentes_ativo_socio_ativo_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='socio',
            name='bairro',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='socio',
            name='cep',
            field=models.CharField(blank=True, max_length=9, null=True),
        ),
        migrations.AddField(
            model_name='socio',
            name='cidade',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='socio',
            name='estado',
            field=models.CharField(blank=True, max_length=2, null=True),
        ),
        migrations.AddField(
            model_name='socio',
            name='logradouro',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='AV/Rua'),
        ),
    ]
