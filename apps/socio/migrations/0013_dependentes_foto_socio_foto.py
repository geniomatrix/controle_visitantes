# Generated by Django 4.2.8 on 2024-01-23 00:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('socio', '0012_alter_dependentes_validade'),
    ]

    operations = [
        migrations.AddField(
            model_name='dependentes',
            name='foto',
            field=models.ImageField(blank=True, null=True, upload_to='dependentes_fotos/'),
        ),
        migrations.AddField(
            model_name='socio',
            name='foto',
            field=models.ImageField(blank=True, null=True, upload_to='socios_fotos/'),
        ),
    ]
