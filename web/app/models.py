from django.db import models

class TelegramUser(models.Model):
    class Meta:
        verbose_name = 'Telegram User'
        verbose_name_plural = 'Telegram Users'
        db_table = 'telegram_user'

    telegram_id = models.BigIntegerField(unique=True, primary_key=True)
    full_name = models.CharField(max_length=255)
    join_time = models.DateTimeField(auto_now_add=True)
    language = models.CharField(
        max_length=2,
        default='en',
        choices=(
            ('en', 'English'),
            ('ua', 'Українська'),
        )
    )
    
    def __str__(self):
        return f'{self.full_name} ({self.telegram_id})'

    def dict(self):
        return {
            'telegram_id': self.telegram_id,
            'full_name': self.full_name,
            'join_time': self.join_time,
            'language': self.language,
        }
        
class SupportRequest(models.Model):
    class Meta:
        verbose_name = 'Support Request'
        verbose_name_plural = 'Support Requests'
        db_table = 'support_request'
    
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(TelegramUser, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.user} at {self.time}'
    
    def dict(self):
        return {
            'id': self.id,
            'user_id': self.user.telegram_id,
            'created_time': self.created_time,
        }
