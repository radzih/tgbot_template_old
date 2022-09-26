from django.db import models

class TelegramUser(models.Model):
    class Meta:
        verbose_name = 'Telegram User'
        verbose_name_plural = 'Telegram Users'
        db_table = 'telegram_user'

    id = models.AutoField(primary_key=True)
    telegram_id = models.BigIntegerField(unique=True)
    full_name = models.CharField(max_length=255)
    join_time = models.DateTimeField(auto_now_add=True)