# Generated by Django 5.0 on 2024-07-05 16:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('estoque', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='fornecedor',
            name='contato',
            field=models.CharField(default='', max_length=150),
        ),
        migrations.AddField(
            model_name='fornecedor',
            name='descricao',
            field=models.CharField(default='', max_length=190),
        ),
    ]