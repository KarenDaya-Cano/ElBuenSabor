# Generated by Django 5.0.2 on 2024-05-21 16:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ElBuenSaborApp', '0004_adicion_delete_adiciones'),
    ]

    operations = [
        migrations.AlterField(
            model_name='adicion',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='producto',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
