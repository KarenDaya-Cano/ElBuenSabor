# Generated by Django 5.0.2 on 2024-05-23 01:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ElBuenSaborApp', '0005_alter_adicion_updated_alter_producto_updated'),
    ]

    operations = [
        migrations.AlterField(
            model_name='adicion',
            name='precio',
            field=models.IntegerField(max_length=10),
        ),
        migrations.AlterField(
            model_name='producto',
            name='precio',
            field=models.IntegerField(max_length=50),
        ),
    ]
