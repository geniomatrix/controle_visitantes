# Generated by Django 4.2.8 on 2024-01-25 00:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('socio', '0015_alter_dependentes_foto_alter_socio_foto'),
    ]

    operations = [
        migrations.AddField(
            model_name='dependentes',
            name='nrcart',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='socio',
            name='nrcart',
            field=models.CharField(max_length=20, null=True),
        ),
    ]