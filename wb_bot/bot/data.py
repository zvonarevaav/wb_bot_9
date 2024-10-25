import json
import os

# Глобальная переменная для хранения данных пользователей
user_data = {}

# Путь к файлу, в котором сохраняются данные
DATA_FILE = "user_data.json"

def load_user_data():
    """
    Загрузка данных пользователей из файла (если файл существует).
    """
    global user_data
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r') as file:
                user_data = json.load(file)
                print("Данные пользователей загружены.")
        except Exception as e:
            print(f"Ошибка при загрузке данных пользователей: {e}")

def save_user_data():
    """
    Сохранение данных пользователей в файл.
    """
    try:
        with open(DATA_FILE, 'w') as file:
            json.dump(user_data, file, indent=4)
            print("Данные пользователей сохранены.")
    except Exception as e:
        print(f"Ошибка при сохранении данных пользователей: {e}")

# Функция для добавления данных пользователя
def add_user(user_id, data):
    user_data[user_id] = data
    save_user_data()

# Функция для удаления данных пользователя
def remove_user(user_id):
    if user_id in user_data:
        del user_data[user_id]
        save_user_data()

# Загрузка данных при старте программы
load_user_data()
