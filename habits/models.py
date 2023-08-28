from django.db import models

from users.models import NULLABLE, User


class Habit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='пользователь')
    location = models.CharField(max_length=255, verbose_name='место')
    time = models.DateTimeField(verbose_name='время')
    action = models.CharField(max_length=255, verbose_name='действие')
    is_enjoyable = models.BooleanField(default=False, verbose_name='признак приятной привычки')
    related_habit = models.ForeignKey('Habit', on_delete=models.SET_NULL, verbose_name='связанная привычка', **NULLABLE)
    periodicity = models.IntegerField(default=1, verbose_name='периодичность')
    reward = models.CharField(max_length=255, verbose_name='вознаграждение', **NULLABLE)
    execution_time = models.IntegerField(verbose_name='время на выполнение', **NULLABLE)
    is_public = models.BooleanField(default=True, verbose_name='Is public')

    class Meta:
        verbose_name = 'привычка'
        verbose_name_plural = 'привычки'

    def __str__(self):
        return f'я буду {self.action} в {self.time.time()} в {self.location}'
