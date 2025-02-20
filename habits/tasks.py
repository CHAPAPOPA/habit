from datetime import datetime

import pytz
from celery import shared_task
from dateutil.relativedelta import relativedelta

from config import settings
from habits.models import Habit
from habits.services import send_message


@shared_task
def send_reminder():
    """
    Периодическая задача для напоминания о том, в какое время
    и какие привычки необходимо выполнять.
    """
    current_date_time = datetime.now(pytz.timezone(settings.TIME_ZONE))
    habits = Habit.objects.filter(time__lte=current_date_time)

    for habit in habits:
        text = (
            f'Итс тайм! Выполни "{habit.behavior}" в локации {habit.location} '
            f'и получи {habit.award if habit.award else (habit.related_habit if habit.related_habit
                                                         else "хорошее настроение")}!'
        )

        chat_id = habit.owner.tg_chat_id
        send_message(text, chat_id)
        habit.time = habit.time + relativedelta(days=habit.frequency)
        habit.save()
