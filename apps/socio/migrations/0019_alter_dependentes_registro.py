# Generated by Django 4.2.8 on 2024-02-05 19:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('socio', '0018_alter_socio_registro'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dependentes',
            name='registro',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
