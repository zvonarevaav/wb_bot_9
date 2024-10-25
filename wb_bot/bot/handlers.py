import asyncio  # Импортируем asyncio
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from bot.scheduler import ReminderBot
from bot.buttons import create_reminder_button, create_time_unit_buttons
from bot.data import user_data
from aiogram import types
import logging

# Логирование
logging.basicConfig(level=logging.INFO)

# Приветственное сообщение с персонализацией
async def send_welcome(message: types.Message):
    user_name = message.from_user.first_name or "пользователь"
    logging.info(f"Приветствие для пользователя {message.from_user.id} ({user_name})")
    welcome_text = (
        f"Привет, {user_name}! Я бот для установки напоминаний.\n"
        "Чтобы создать напоминание, нажми на кнопку ниже и следуй инструкциям."
    )
    await message.answer(welcome_text, reply_markup=create_reminder_button())

# Обработка кнопки "Создать напоминание"
async def create_reminder_handler(callback_query: types.CallbackQuery):
    logging.info(f"Пользователь {callback_query.from_user.id} нажал кнопку 'Создать напоминание'")

    # Обязательно добавляем данные о пользователе
    user_data[callback_query.from_user.id] = {"step": "waiting_for_task"}

    await callback_query.message.answer("Введите задачу:")
    logging.info(f"user_data после выбора кнопки: {user_data}")
    await callback_query.answer()

# Обработка ввода задачи
async def handle_task_message(message: types.Message, reminder_bot: ReminderBot):
    if message.from_user.id not in user_data:
        logging.warning(f"Пользователь {message.from_user.id} не зарегистрирован для ввода задачи")
        return

    if user_data[message.from_user.id].get("step") != "waiting_for_task":
        await message.answer("Для начала создайте задачу.")
        return

    task = message.text
    user_data[message.from_user.id]["task"] = task
    user_data[message.from_user.id]["step"] = "waiting_for_time_unit"

    logging.info(f"Пользователь {message.from_user.id} ввел задачу: {task}")
    logging.info(f"user_data после ввода задачи: {user_data}")

    await message.answer("Выберите единицу времени (минуты, часы, дни, недели, месяцы):", reply_markup=create_time_unit_buttons())

# Обработка выбора единицы времени
async def time_unit_handler(callback_query: types.CallbackQuery):
    if callback_query.from_user.id not in user_data:
        logging.warning(f"Пользователь {callback_query.from_user.id} не зарегистрирован для выбора единицы времени")
        return

    if user_data[callback_query.from_user.id].get("step") != "waiting_for_time_unit":
        await callback_query.message.answer("Сначала введите задачу.")
        return

    unit = callback_query.data
    user_data[callback_query.from_user.id]["unit"] = unit
    user_data[callback_query.from_user.id]["step"] = "waiting_for_time_amount"

    logging.info(f"Пользователь {callback_query.from_user.id} выбрал единицу времени: {unit}")
    logging.info(f"user_data после выбора единицы времени: {user_data}")
    await callback_query.message.answer(f"Введите количество {unit}:")
    await callback_query.answer()

# Обработка ввода времени
async def handle_time_message(message: types.Message, reminder_bot: ReminderBot):
    if message.from_user.id not in user_data:
        logging.error(f"Пользователь {message.from_user.id} не найден в user_data")
        return

    # Проверка состояния пользователя
    if user_data[message.from_user.id].get("step") != "waiting_for_time_amount":
        await message.answer("Пожалуйста, сначала выберите единицу времени.")
        return

    try:
        # Попытка преобразовать ввод в число
        amount = int(message.text)
        if amount <= 0:
            raise ValueError
    except ValueError:
        await message.answer("Введите корректное число.")
        return

    # Получаем задачу и единицу времени
    task = user_data[message.from_user.id]["task"]
    unit = user_data[message.from_user.id]["unit"]

    logging.info(f"Пользователь {message.from_user.id} вводит время для задачи: {task}, количество: {amount} {unit}")

    # Устанавливаем напоминание
    await reminder_bot.set_reminder(message, task, amount, unit)

    # Очищаем данные пользователя
    del user_data[message.from_user.id]

# Обертка для передачи reminder_bot
def create_task_handler(handler_func, reminder_bot):
    async def wrapper(message: types.Message):
        logging.info(f"Вызов обработчика для пользователя {message.from_user.id}")
        await handler_func(message, reminder_bot)
    return wrapper

# Регистрация всех обработчиков
def register_handlers(dp: Dispatcher, bot: Bot, scheduler: AsyncIOScheduler, session):
    reminder_bot = ReminderBot(bot, scheduler, session)

    dp.message.register(send_welcome, Command("start"))
    dp.callback_query.register(create_reminder_handler, lambda c: c.data == 'create_reminder')
    dp.callback_query.register(time_unit_handler, lambda c: c.data in ['min', 'h', 'd', 'w', 'mo'])

    dp.message.register(
        create_task_handler(handle_task_message, reminder_bot),
        lambda m: user_data.get(m.from_user.id) and user_data[m.from_user.id].get("step") == "waiting_for_task"
    )
    dp.message.register(
        create_task_handler(handle_time_message, reminder_bot),
        lambda m: user_data.get(m.from_user.id) and user_data[m.from_user.id].get("step") == "waiting_for_time_amount"
    )

