from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from datetime import datetime
import os
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

# Получаем параметры для подключения к базе данных
DATABASE_URL = os.getenv("DATABASE_URL")

# Создаем базовый класс для всех моделей
Base = declarative_base()


# Определяем модель User
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)

    # Отношение с напоминаниями
    reminders = relationship("Reminder", back_populates="user")


# Определяем модель Reminder (напоминание)
class Reminder(Base):
    __tablename__ = 'reminders'
    id = Column(Integer, primary_key=True)
    task = Column(String, nullable=False)
    time = Column(DateTime, nullable=False)
    repeat = Column(Boolean, default=False)

    # Внешний ключ на таблицу users
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", back_populates="reminders")


# Создаем движок базы данных и сессию
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
