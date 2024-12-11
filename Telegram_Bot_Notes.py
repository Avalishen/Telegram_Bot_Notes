"""
RUS
Автор кода Avalishen
Данный код бота для Telegram написан на версии Aiogram 3.13
База Данных MySQL
Бот представляет собой что-то вроде блокнота в котором есть разделение на user_id
Пользователи могут добавить в боте 3 вида записей
1) Обычный текст команда add_records и попросить бота выдать информацию обратно командой get_records
2) Ссылка в виде гиперссылки команда add_links и попросить бота выдать информацию обратно командой get_links
3) Код add_code который будет помечаться в Telegram как код и попросить бота выдать информацию обратно командой get_code

ENG
Code author Avalishen
This bot code for Telegram is written on Aiogram version 3.13
MySQL database
The bot is something like a notepad in which there is a division by user_id
Users can add 3 types of records in the bot
1) Plain text add_records command and ask the bot to give information back with the get_records command
2) Link in the form of a hyperlink add_links command and ask the bot to give information back with the get_links command
3) Code add_code which will be marked in Telegram as a code and ask the bot to give information back with the get_code command
"""


import asyncio
import sys
import logging
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
import mysql.connector


TOKEN = "BOT_TOKEN"#токен бота
dp = Dispatcher()
logging.basicConfig(level=logging.INFO)
AUTHORIZED_USER_ID = 569360925 #ID пользователя которому доступна команда
DB = mysql.connector.connect(
                    host = "",
                    port = ,
                    user = "",
                    password = "",
                    database = "")
print(DB)


class AddDataState(StatesGroup):
    records = State()
    links = State()
    code = State()
    waiting_for_url = State()
    waiting_for_name = State()
    waiting_for_code = State()
    waiting_for_code_name = State()


def add_users(user_id, user_name):
    cursor = DB.cursor()
    try:
        query = """
                    INSERT INTO users (user_id, user_name)
                    VALUES (%s, %s)
                    ON DUPLICATE KEY UPDATE
                        user_name = VALUES(user_name)
                """
        evidence = (user_id, user_name)
        cursor.execute(query, evidence)
        DB.commit()
        print("Данные успешно добавлены!")
    except mysql.connector.Error as e:
        print(f"Ошибка при добавлении записи: {e}")
    finally:
        cursor.close()


def add_records(records, user_name, user_id):
    cursor = DB.cursor()
    try:
        query = "INSERT INTO save_records (records, user_name, user_id) VALUES (%s, %s, %s)"
        evidence = (records, user_name, user_id,)
        cursor.execute(query, evidence)
        DB.commit()
        print("Данные успешно добавлены!")
    except mysql.connector.Error as e:
        print(f"Ошибка при добавлении записи: {e}")
    finally:
        cursor.close()


def add_links(links, user_name, user_id):
    cursor = DB.cursor()
    try:
        query = "INSERT INTO save_links (links, user_name, user_id) VALUES (%s, %s, %s)"
        evidence = (links, user_name, user_id,)
        cursor.execute(query, evidence)
        DB.commit()
        print("Данные успешно добавлены!")
    except mysql.connector.Error as e:
        print(f"Ошибка при добавлении Ссылки: {e}")
    finally:
        cursor.close()


def add_code(code, user_name, user_id):
    cursor = DB.cursor()
    try:
        query = "INSERT INTO save_code (code, user_name, user_id) VALUES (%s, %s, %s)"
        evidence = (code, user_name, user_id)
        cursor.execute(query, evidence)
        DB.commit()
        print("Данные успешно добавлены!")
    except mysql.connector.Error as e:
        print(f"Ошибка при добавлении Кода: {e}")
    finally:
        cursor.close()


def get_records(user_id):
    cursor = DB.cursor()
    save_records = []
    try:
        query = "SELECT records, user_name, date_time FROM save_records WHERE user_id = (%s)"
        evidence = (user_id,)
        cursor.execute(query, evidence)
        save_records = cursor.fetchall()
        DB.commit()
        print("Данные успешно отправлены!")
    except mysql.connector.Error as e:
        print(f"Ошибка при отправке Записи: {e}")
    finally:
        cursor.close()
    return save_records


def get_links(user_id):
    cursor = DB.cursor()
    save_links = []
    try:
        query = "SELECT links, user_name, date_time FROM save_links WHERE user_id = (%s)"
        evidence = (user_id,)
        cursor.execute(query, evidence)
        save_links = cursor.fetchall()
        DB.commit()
        print("Ссылки успешно отправлены!")
    except mysql.connector.Error as e:
        print(f"Ошибка при отправке Ссылок: {e}")
    finally:
        cursor.close()
    return save_links


def get_code(user_id):
    cursor = DB.cursor()
    save_code = []
    try:
        query = "SELECT code, user_name, date_time FROM save_code WHERE user_id = (%s)"
        evidence = (user_id,)
        cursor.execute(query, evidence)
        save_code = cursor.fetchall()
        DB.commit()
        print("Код успешно отправлен!")
    except mysql.connector.Error as e:
        print(f"Ошибка при отправке Кода: {e}")
    finally:
        cursor.close()
    return save_code


@dp.message(Command("start"))
async def start_command(message: Message):
    user_id = message.from_user.id
    user_name = message.from_user.username or "Без имени"
    try:
        add_users(user_id, user_name)
        await message.answer(f"Добро пожаловать, {user_name}!\nВведите /list чтобы увидеть весь список команд")
    except Exception as e:
        await message.answer(f"Ошибка при регистрации: {e}")


@dp.message(Command("list"))
async def list_command(message: Message):
    await message.answer("Вот все команды к которым у вас есть доступ! \n"
                         "✅/add_records - добавить информацию в Записи \n"
                         "✅/add_links - добавить информацию в Ссылки \n"
                         "✅/add_code - добавить информацию в Коды \n"
                         "✅/get_records - получить информацию о ваших Записях \n"
                         "✅/get_links - получить информацию о ваших Ссылках \n"
                         "✅/get_code - получить информацию о ваших сохранённых Кодах")


@dp.message(Command("add_records"))
async def add_records_command(message: Message, state: FSMContext):
    await message.answer("Введите данные которые хотели бы сохранить в базе!")
    await state.update_data(user_id=message.from_user.id, user_name=message.from_user.username or "Не указан")
    await state.set_state(AddDataState.records)


@dp.message(AddDataState.records)
async def process_records_text(message: Message, state: FSMContext):
    data = await state.get_data()
    user_id = data.get("user_id")
    user_name = data.get("user_name")
    records_text = message.text

    try:
        add_records(records_text, user_name, user_id)
        await message.answer("Данные успешно сохранены в колонке Записи.")
    except Exception as e:
        await message.answer(f"Ошибка при добавлении записи: {e}")
    finally:
        await state.clear()


@dp.message(Command("add_links"))
async def add_links_command(message: Message, state: FSMContext):
    await message.answer("Укажите ссылку (URL):")
    await state.update_data(user_id=message.from_user.id, user_name=message.from_user.username or "Не указан")
    await state.set_state(AddDataState.waiting_for_url)


@dp.message(AddDataState.waiting_for_url)
async def process_url(message: Message, state: FSMContext):
    url = message.text.strip()
    if not url.startswith("http://") and not url.startswith("https://"):
        await message.answer("Пожалуйста, укажите корректный URL (начинается с http:// или https://).")
        return
    await state.update_data(url=url)
    await message.answer("Укажите название для ссылки:")
    await state.set_state(AddDataState.waiting_for_name)


@dp.message(AddDataState.waiting_for_name)
async def process_name(message: Message, state: FSMContext):
    data = await state.get_data()
    user_name = data.get("user_name")
    user_id = data.get("user_id")
    name = message.text.strip()
    url = data["url"]
    hyperlink = f'<a href="{url}">{name}</a>'
    try:
        add_links(hyperlink, user_name, user_id,)
        await message.answer(f"Ссылка сохранена: {hyperlink}", parse_mode="HTML")
    except Exception as e:
        await message.answer(f"Ошибка при сохранении ссылки: {e}")
    await state.clear()


@dp.message(Command("add_code"))
async def add_code_command(message: Message, state: FSMContext):
    await message.answer("Отправьте код который хотели бы сохранить:")
    await state.update_data(user_id=message.from_user.id, user_name=message.from_user.username or "Не указан")
    await state.set_state(AddDataState.waiting_for_code)


@dp.message(AddDataState.waiting_for_code)
async def process_code(message: Message, state: FSMContext):
    code = message.text.strip()
    if code.startswith("```") and code.endswith("```"):
        await message.answer("Пожалуйста, отправьте код в формате ```Code Example```.")
        return
    await state.update_data(code=code)
    await message.answer("Теперь введите название для вашего кода через #:")
    await state.set_state(AddDataState.waiting_for_code_name)


@dp.message(AddDataState.waiting_for_code_name)
async def receive_name(message: Message, state: FSMContext):
    data = await state.get_data()
    user_name = data.get("user_name")
    user_id = data.get("user_id")
    name = message.text.strip()
    code = data["code"]
    hypercode = f'{name}\n{code}\n'
    try:
        add_code(hypercode, user_name, user_id)
        await message.answer(f"✅Ваш Код успешно сохранён: \n```{hypercode}```", parse_mode="MarkdownV2")
    except Exception as e:
        await message.answer(f"Ошибка при сохранении кода: {e}")
    finally:
        await state.clear()


@dp.message(Command("get_records"))
async def get_column_values_records(message: Message):
    user_id = message.from_user.id
    data = get_records(user_id,)
    if not data:
        await message.answer("Будьте внимательны. У вас пока нет сохраненных Записей ⚠️⚠️⚠️")
        return

    response = "Вот ваши сохраненные Записи:\n\n"
    for records, user_name, date_time in get_records(user_id):
        response += f"👤Автор: {user_name}👤\n⛔Добавлено: {date_time}⛔\n✅Запись: {records}\n\n"
    await message.answer(response)


@dp.message(Command("get_links"))
async def get_column_values_links(message: Message):
    user_id = message.from_user.id
    data = get_links(user_id,)
    if not data:
        await message.answer("Будьте внимательны. У вас пока нет сохраненных Ссылок ⚠️⚠️⚠️")
        return

    response =  "Вот ваши сохраненные Ссылки:\n\n"
    for links, user_name, date_time in get_links(user_id):
        response += f"👤Автор: {user_name}👤\n⛔Добавлено: {date_time}⛔\n✅Запись: {links}\n\n"
    await message.answer(response)


@dp.message(Command("get_code"))
async def get_column_values_code(message: Message):
    user_id = message.from_user.id
    data = get_code(user_id)
    if not data:
        await message.answer("Будьте внимательны. У вас пока нет сохраненных Кодов ⚠️⚠️⚠️")
        return

    def escape_markdown_v2(text):
        reserved_characters = r"_*[]()~`>#+-=|{}.!"
        for char in reserved_characters:
            text = text.replace(char, f"\\{char}")
        return text

    response = "Вот ваши сохраненные Коды:\n\n"
    for code, user_name, date_time in data:
        safe_code = escape_markdown_v2(code)
        safe_user_name = escape_markdown_v2(user_name)
        safe_date_time = escape_markdown_v2(str(date_time))

        response += (
            f"👤*Автор*: {safe_user_name}👤\n"
            f"⛔*Добавлено*: {safe_date_time}⛔\n"
            f"✅*Ваша Запись*:"
            f"\n```python\n{safe_code}\n```\n\n"
        )

    try:
        await message.answer(response, parse_mode="MarkdownV2")
    except Exception as e:
        print(f"Ошибка при отправке сообщения: {e}")
        await message.answer("Возникла ошибка при отправке данных. Проверьте содержимое базы данных.")




async def main():
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
