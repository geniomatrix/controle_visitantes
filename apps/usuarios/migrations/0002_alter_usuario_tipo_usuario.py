# Generated by Django 4.2.8 on 2023-12-26 18:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='tipo_usuario',
            field=models.CharField(choices=[('P', 'Porteiro'), ('S', 'Sócio')], default='P', max_length=1, verbose_name='Tipo de usuário'),
        ),
    ]
