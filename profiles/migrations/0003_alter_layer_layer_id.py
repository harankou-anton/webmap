# Generated by Django 4.2.1 on 2023-06-17 19:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0002_alter_layeraccess_access_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='layer',
            name='layer_id',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
    ]
