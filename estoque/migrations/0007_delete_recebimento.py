# Generated by Django 5.0 on 2024-07-13 18:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('estoque', '0006_cliente_recebimento'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Recebimento',
        ),
    ]
