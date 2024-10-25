from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# Кнопка для создания напоминания
def create_reminder_button():
    reminder_button = InlineKeyboardButton(text="📝 Создать напоминание", callback_data="create_reminder")
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [reminder_button]  # Оставлена только кнопка для создания напоминания
    ])
    return keyboard

# Кнопки для выбора единицы времени
def create_time_unit_buttons():
    min_button = InlineKeyboardButton(text="⏱ Минуты", callback_data="min")
    hour_button = InlineKeyboardButton(text="🕒 Часы", callback_data="h")
    day_button = InlineKeyboardButton(text="📅 Дни", callback_data="d")
    week_button = InlineKeyboardButton(text="📆 Недели", callback_data="w")
    month_button = InlineKeyboardButton(text="🗓 Месяц", callback_data="mo")

    # Удалены кнопки "Повторять" и "Удалить"
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [min_button, hour_button],  # Первая строка с двумя кнопками
        [day_button, week_button],  # Вторая строка с двумя кнопками
        [month_button]  # Третья строка с кнопкой "Месяц"
    ])
    return keyboard
