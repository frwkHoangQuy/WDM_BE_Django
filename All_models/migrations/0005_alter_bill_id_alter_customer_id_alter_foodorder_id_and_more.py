# Generated by Django 4.1 on 2024-05-20 11:42

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('All_models', '0004_alter_bill_id_alter_customer_id_alter_foodorder_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bill',
            name='id',
            field=models.CharField(default=uuid.UUID('dd2e6be7-7776-434d-955c-4025ce5bd23a'), max_length=191, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='customer',
            name='id',
            field=models.CharField(default='0b7f7e06e71a460898b592d3e87f2fdb', max_length=191, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='foodorder',
            name='id',
            field=models.CharField(default=uuid.UUID('34121f82-ed02-41ae-b93f-b4f350900c3b'), max_length=191, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='lobby',
            name='created_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='lobby',
            name='deleted_at',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AlterField(
            model_name='lobby',
            name='id',
            field=models.CharField(default='47b311c54efa405e83c190d4a52a6d4e', max_length=32, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='lobtype',
            name='id',
            field=models.CharField(default='7b62958fa43643be9645c19a5b90f30c', editable=False, max_length=32, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='serviceorder',
            name='id',
            field=models.CharField(default=uuid.UUID('0fd7b1f5-438e-4d4c-8e5a-2bdbcb6ef920'), max_length=191, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='shift',
            name='id',
            field=models.CharField(default='532f53d0feb54fbab0eb36ba049b5828', max_length=191, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='wedding',
            name='id',
            field=models.CharField(default='b0466c596b5d4c608bf6736e75865bb8', max_length=191, primary_key=True, serialize=False),
        ),
    ]
