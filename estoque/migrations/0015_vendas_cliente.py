# Generated by Django 5.0.7 on 2024-07-28 17:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('estoque', '0014_remove_mensagem_lida'),
    ]

    operations = [
        migrations.AddField(
            model_name='vendas',
            name='cliente',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='estoque.cliente'),
        ),
    ]