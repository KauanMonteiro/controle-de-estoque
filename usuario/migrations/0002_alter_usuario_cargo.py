# Generated by Django 5.0 on 2024-07-17 12:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuario', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='cargo',
            field=models.CharField(choices=[('Admin', 'Administrador'), ('GestorEstoque', 'Gerente de Estoque'), ('AnalistaFinanceiro', 'Analista Financeiro')], max_length=18),
        ),
    ]
