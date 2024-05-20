# Generated by Django 4.1 on 2024-05-20 10:10

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.CharField(default='3c366a1abdc144aaa85625940a324f80', max_length=191, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=191)),
                ('phone', models.CharField(max_length=191, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'Customer',
            },
        ),
        migrations.CreateModel(
            name='Lobby',
            fields=[
                ('id', models.CharField(default='7670113e4c4e46c2b819a23069cbea48', max_length=32, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=191)),
            ],
            options={
                'db_table': 'Lobby',
            },
        ),
        migrations.CreateModel(
            name='LobType',
            fields=[
                ('id', models.CharField(default='b827507b33624c48be192ba0ae90295c', editable=False, max_length=32, primary_key=True, serialize=False)),
                ('max_table_count', models.IntegerField()),
                ('min_table_price', models.IntegerField()),
                ('deposit_percent', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('type_name', models.CharField(max_length=191)),
                ('deleted_at', models.DateTimeField(default=None, null=True)),
            ],
            options={
                'db_table': 'LobType',
            },
        ),
        migrations.CreateModel(
            name='Shift',
            fields=[
                ('id', models.CharField(default='cfc7523969ed4dd68eedbbe860fab794', max_length=191, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=191)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(null=True)),
            ],
            options={
                'db_table': 'Shift',
            },
        ),
        migrations.CreateModel(
            name='Wedding',
            fields=[
                ('id', models.CharField(default='6191245184ca4790b07f180956f9ba28', max_length=191, primary_key=True, serialize=False)),
                ('groom', models.CharField(max_length=191)),
                ('bride', models.CharField(max_length=191)),
                ('wedding_date', models.DateTimeField()),
                ('table_count', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('note', models.CharField(blank=True, max_length=191, null=True)),
                ('is_penalty_mode', models.BooleanField(default=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='All_models.customer')),
                ('lobby', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='All_models.lobby')),
                ('shift', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='All_models.shift')),
            ],
            options={
                'db_table': 'Wedding',
            },
        ),
        migrations.CreateModel(
            name='ServiceOrder',
            fields=[
                ('id', models.CharField(default=uuid.UUID('75bb9df6-c877-459a-828f-b83b97e1b218'), max_length=191, primary_key=True, serialize=False)),
                ('service_id', models.CharField(max_length=191)),
                ('service_name', models.CharField(max_length=191)),
                ('service_price', models.IntegerField()),
                ('note', models.CharField(blank=True, max_length=191, null=True)),
                ('count', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('wedding', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='All_models.wedding')),
            ],
            options={
                'db_table': 'ServiceOrder',
            },
        ),
        migrations.AddField(
            model_name='lobby',
            name='lob_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='All_models.lobtype'),
        ),
        migrations.CreateModel(
            name='FoodOrder',
            fields=[
                ('id', models.CharField(default=uuid.UUID('8065c06d-2ff6-4ab3-9c63-6be7bf62e49f'), max_length=191, primary_key=True, serialize=False)),
                ('food_id', models.CharField(max_length=191)),
                ('food_name', models.CharField(max_length=191)),
                ('food_price', models.IntegerField()),
                ('count', models.IntegerField()),
                ('note', models.CharField(blank=True, max_length=191, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('wedding', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='All_models.wedding')),
            ],
            options={
                'db_table': 'FoodOrder',
            },
        ),
        migrations.CreateModel(
            name='Bill',
            fields=[
                ('id', models.CharField(default=uuid.UUID('055dd2d7-87ce-4b31-8755-8922ce39236b'), max_length=191, primary_key=True, serialize=False)),
                ('payment_date', models.DateTimeField()),
                ('service_total_price', models.IntegerField()),
                ('food_total_price', models.IntegerField()),
                ('total_price', models.IntegerField()),
                ('deposit_require', models.IntegerField()),
                ('deposit_amount', models.IntegerField()),
                ('remain_amount', models.IntegerField()),
                ('extra_fee', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('wedding', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='All_models.wedding')),
            ],
            options={
                'db_table': 'Bill',
            },
        ),
    ]
