# Generated by Django 4.2.8 on 2024-01-18 18:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('socio', '0002_vinculado_socio_data_nascimento_socio_telefone_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='socio',
            name='tpsocio',
            field=models.CharField(choices=[('II', 'Servidor Publico'), ('VI', 'Particular')], default='ESPOSA(o)', max_length=50, verbose_name='Tipo de Socio'),
        ),
        migrations.AddField(
            model_name='vinculado',
            name='dependente',
            field=models.CharField(max_length=194, null=True, verbose_name='Dependente'),
        ),
        migrations.AddField(
            model_name='vinculado',
            name='filiacao',
            field=models.CharField(choices=[('ESPOSA(o)', 'Esposa(o)'), ('FILHO(a)', 'Filho(a)'), ('NETO(a)', 'Neto(a)')], default='ESPOSA(o)', max_length=50, verbose_name='Filiacao'),
        ),
        migrations.AddField(
            model_name='vinculado',
            name='validade',
            field=models.DateField(blank=True, null=True, verbose_name='Validade'),
        ),
    ]
