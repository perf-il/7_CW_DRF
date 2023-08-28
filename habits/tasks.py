from datetime import datetime, timedelta

from celery import shared_task


from habits.models import Habit
from users.models import User
from habits.services import send_message_bot


@shared_task
def check_habits():
    """Проверка привычек пользователя и отправка сообщения в ТГ"""
    all_habits = Habit.objects.all()

    for habit in all_habits:

        if habit.time.date() == datetime.now().date():
            if habit.time.time() <= datetime.now().time():
                user = User.objects.get(pk=habit.user.pk)
                chat_id = user.tg_user_id
                if chat_id:
                    send_message_bot(chat_id, text=habit)
                    habit.time += timedelta(days=habit.periodicity)
                    habit.save()
