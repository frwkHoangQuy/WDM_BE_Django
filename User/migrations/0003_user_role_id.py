# Generated by Django 4.1 on 2024-05-15 20:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0002_permission_role_rolepermission_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='role_id',
            field=models.UUIDField(default=0),
        ),
    ]