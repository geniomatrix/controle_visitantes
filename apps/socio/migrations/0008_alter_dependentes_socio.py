# Generated by Django 4.2.8 on 2024-01-19 03:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('socio', '0007_remove_dependentes_dependente'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dependentes',
            name='socio',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='socio.socio'),
        ),
    ]
