# Generated by Django 5.0.2 on 2024-08-06 16:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('CarritoApp', '0003_remove_lineapedido_user_remove_pedido_user'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='lineapedido',
            options={'verbose_name': 'línea pedido', 'verbose_name_plural': 'líneas pedidos'},
        ),
        migrations.AlterModelOptions(
            name='pedido',
            options={'ordering': ['created'], 'verbose_name': 'pedido', 'verbose_name_plural': 'pedidos'},
        ),
    ]
