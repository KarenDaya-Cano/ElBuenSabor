# Generated by Django 5.0.2 on 2024-07-11 16:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ElBuenSaborApp', '0008_alter_adicion_precio'),
    ]

    operations = [
        migrations.CreateModel(
            name='Venta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateTimeField()),
                ('producto', models.CharField(max_length=100)),
                ('cantidad', models.IntegerField()),
                ('precio_unitario', models.DecimalField(decimal_places=2, max_digits=10)),
                ('total', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
    ]