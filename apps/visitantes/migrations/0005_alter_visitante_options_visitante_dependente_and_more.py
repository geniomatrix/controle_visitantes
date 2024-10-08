# Generated by Django 4.2.8 on 2024-01-18 02:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('visitantes', '0004_alter_visitante_morador_responsavel_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='visitante',
            options={'verbose_name': 'Sócios', 'verbose_name_plural': 'Sócios'},
        ),
        migrations.AddField(
            model_name='visitante',
            name='dependente',
            field=models.CharField(max_length=194, null=True, verbose_name='Dependente'),
        ),
        migrations.AddField(
            model_name='visitante',
            name='filiacao',
            field=models.CharField(choices=[('ESPOSA(o)', 'Esposa(o)'), ('FILHO(a)', 'Filho(a)'), ('NETO(a)', 'Neto(a)')], default='ESPOSA(o)', max_length=50, verbose_name='Filiacao'),
        ),
        migrations.AddField(
            model_name='visitante',
            name='tpsocio',
            field=models.CharField(max_length=50, null=True, verbose_name='Tipo de Socio'),
        ),
        migrations.AddField(
            model_name='visitante',
            name='validade',
            field=models.DateField(blank=True, null=True, verbose_name='Validade'),
        ),
        migrations.AlterField(
            model_name='visitante',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='visitante',
            name='numero_casa',
            field=models.PositiveBigIntegerField(verbose_name='Número do Quiosque a ser Visitada'),
        ),
    ]
