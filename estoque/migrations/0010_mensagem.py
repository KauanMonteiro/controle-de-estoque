# Generated by Django 5.0 on 2024-07-18 16:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('estoque', '0009_produto_preco_alter_cliente_documento_and_more'),
        ('usuario', '0003_alter_usuario_email'),
    ]

    operations = [
        migrations.CreateModel(
            name='Mensagem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=100)),
                ('aviso', models.TextField()),
                ('data_de_criacao', models.DateTimeField(auto_now_add=True)),
                ('tipo_destino', models.CharField(choices=[('todos', 'Para todos os usuários'), ('destinatarios', 'Para destinatários específicos')], default='destinatarios', max_length=20)),
                ('destinatarios', models.ManyToManyField(blank=True, related_name='mensagens_enviadas', to='usuario.usuario')),
                ('remetente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mensagens_recebidas', to='usuario.usuario')),
            ],
        ),
    ]