# Generated by Django 4.2.8 on 2024-01-19 17:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('socio', '0009_alter_socio_data_nascimento'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dependentes',
            name='socio',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dependentes', to='socio.socio'),
        ),
    ]