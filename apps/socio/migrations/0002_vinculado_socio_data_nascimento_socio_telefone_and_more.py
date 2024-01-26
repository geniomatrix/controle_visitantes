# Generated by Django 4.2.8 on 2024-01-18 02:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('socio', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Vinculado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('data_nascimento', models.DateField()),
            ],
        ),
        migrations.AddField(
            model_name='socio',
            name='data_nascimento',
            field=models.DateField(default='2024-01-17'),
        ),
        migrations.AddField(
            model_name='socio',
            name='telefone',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='socio',
            name='email',
            field=models.EmailField(max_length=254, unique=True),
        ),
        migrations.DeleteModel(
            name='Dependente',
        ),
        migrations.AddField(
            model_name='vinculado',
            name='socio',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vinculados', to='socio.socio'),
        ),
    ]