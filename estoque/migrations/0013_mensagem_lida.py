# Generated by Django 5.0 on 2024-07-25 14:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('estoque', '0012_remove_mensagem_lida'),
    ]

    operations = [
        migrations.AddField(
            model_name='mensagem',
            name='lida',
            field=models.BooleanField(default=False),
        ),
    ]
