# Generated by Django 4.1 on 2024-05-17 18:58

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("User", "0002_remove_rolepermission_unique_role_permission_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="user",
            old_name="role_id",
            new_name="role",
        ),
    ]
