from datetime import timedelta, datetime
from apscheduler.triggers.date import DateTrigger
from apscheduler.triggers.interval import IntervalTrigger
import logging
from bot.models import User, Reminder


class ReminderBot:
    def __init__(self, bot, scheduler, session):
        self.bot = bot
        self.scheduler = scheduler
        self.session = session

    async def set_reminder(self, message, task, amount, unit, repeat=False):
        # Определяем правильный интервал времени
        delta = self._parse_time_unit(amount, unit)
        reminder_time = datetime.now() + delta

        logging.info(f"Устанавливаем напоминание на: {reminder_time}")

        # Проверяем, существует ли пользователь в базе данных
        user_id = message.from_user.id
        username = message.from_user.first_name
        user = self.session.query(User).filter_by(id=user_id).first()

        if not user:
            # Если пользователя нет, создаем его
            user = User(id=user_id, username=username)
            self.session.add(user)
            self.session.commit()
            logging.info(f"Пользователь {username} (ID: {user_id}) добавлен в базу данных.")

        # Добавляем напоминание в планировщик и базу данных
        try:
            if repeat:
                # Повторяющееся напоминание
                trigger = IntervalTrigger(**{self._get_interval_key(unit): amount})
                self.scheduler.add_job(
                    self.send_reminder_async,
                    trigger,
                    args=[message.chat.id, task],
                    id=f"reminder_{message.chat.id}_{task}_repeat"
                )
                await message.answer(f"Задача '{task}' создана и будет повторяться каждые {amount} {self._format_unit(unit, amount)}.")
            else:
                # Одноразовое напоминание
                self.scheduler.add_job(
                    self.send_reminder_async,
                    DateTrigger(run_date=reminder_time),
                    args=[message.chat.id, task],
                    id=f"reminder_{message.chat.id}_{task}"
                )
                await message.answer(f"Задача '{task}' создана и напоминание установлено через {amount} {self._format_unit(unit, amount)}.")

            # Сохраняем напоминание в базе данных
            reminder = Reminder(task=task, time=reminder_time, repeat=repeat, user_id=user_id)
            self.session.add(reminder)
            self.session.commit()

            logging.info(f"Напоминание установлено на задачу: {task}, время: {reminder_time}")
        except Exception as e:
            logging.error(f"Ошибка при добавлении задачи в планировщик или базу данных: {e}")

    async def send_reminder_async(self, chat_id, task):
        try:
            logging.info(f"Отправка напоминания. Задача: {task}, чат: {chat_id}")
            await self.bot.send_message(chat_id, f"Напоминание о задаче: '{task}'")
        except Exception as e:
            logging.error(f"Ошибка при отправке напоминания: {e}")

    def get_active_reminders(self, user_id):
        """Возвращает все активные напоминания для данного пользователя."""
        return self.session.query(Reminder).filter_by(user_id=user_id).all()

    def delete_reminder(self, user_id, task):
        """Удаляет напоминание по имени задачи."""
        reminder = self.session.query(Reminder).filter_by(user_id=user_id, task=task).first()
        if reminder:
            self.session.delete(reminder)
            self.session.commit()

            # Удаляем задачу из планировщика
            try:
                self.scheduler.remove_job(f"reminder_{user_id}_{task}")
                self.scheduler.remove_job(f"reminder_{user_id}_{task}_repeat")
            except Exception as e:
                logging.error(f"Ошибка при удалении задачи: {e}")
            return True
        return False

    def _parse_time_unit(self, amount, unit):
        logging.info(f"Парсинг времени: {amount} {unit}")
        if unit == 'min':
            return timedelta(minutes=amount)
        elif unit == 'h':
            return timedelta(hours=amount)
        elif unit == 'd':
            return timedelta(days=amount)
        elif unit == 'w':
            return timedelta(weeks=amount)
        elif unit == 'mo':
            return timedelta(days=amount * 30)  # Условный месяц
        else:
            return timedelta(minutes=amount)

    def _get_interval_key(self, unit):
        """Возвращает ключ для IntervalTrigger в зависимости от единицы времени."""
        if unit == 'min':
            return 'minutes'
        elif unit == 'h':
            return 'hours'
        elif unit == 'd':
            return 'days'
        elif unit == 'w':
            return 'weeks'
        else:
            raise ValueError(f"Недопустимая единица времени: {unit}")

    def _format_unit(self, unit, amount):
        """Форматирует единицу времени для отображения в сообщении."""
        if unit == 'min':
            return 'минуту' if amount == 1 else 'минут'
        elif unit == 'h':
            return 'час' if amount == 1 else 'часов'
        elif unit == 'd':
            return 'день' if amount == 1 else 'дней'
        elif unit == 'w':
            return 'неделю' if amount == 1 else 'недель'
        elif unit == 'mo':
            return 'месяц' if amount == 1 else 'месяцев'
        else:
            return unit
