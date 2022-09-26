# Generated by Django 4.1.1 on 2022-09-26 12:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TelegramUser',
            fields=[
                ('telegram_id', models.BigIntegerField(primary_key=True, serialize=False, unique=True)),
                ('full_name', models.CharField(max_length=255)),
                ('join_time', models.DateTimeField(auto_now_add=True)),
                ('language', models.CharField(choices=[('en', 'English'), ('ua', 'Українська')], default='en', max_length=2)),
            ],
            options={
                'verbose_name': 'Telegram User',
                'verbose_name_plural': 'Telegram Users',
                'db_table': 'telegram_user',
            },
        ),
        migrations.CreateModel(
            name='SupportRequest',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('message', models.TextField()),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.telegramuser')),
            ],
            options={
                'verbose_name': 'Support Request',
                'verbose_name_plural': 'Support Requests',
                'db_table': 'support_request',
            },
        ),
    ]