import os
import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F, Router
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Получаем токен и ID админа из переменных окружения
API_TOKEN = os.getenv("7916354605:AAF5Dh9KBN1-8sRTc8pIpq67U6T8fkDJkxA")
ADMIN_ID = os.getenv("893382104")

# Настройка логгера
logging.basicConfig(level=logging.INFO)

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher()
router = Router()
dp.include_router(router)

# Главное меню
main_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Узнать о приложении", callback_data="about_app")],
    [InlineKeyboardButton(text="Подробнее о франшизе", callback_data="about_franchise")],
    [InlineKeyboardButton(text="Оставить заявку", callback_data="send_request")]
])

# Стартовое сообщение
@router.message(CommandStart())
async def start_handler(message: types.Message):
    text = (
        "👋 Привет! \n\n"
        "Если тебя интересует пассивный заработок, желание работать на себя, "
        "финансовая независимость и запуск своего дела с минимальными рисками — "
        "ты по адресу. Франшиза Good Day — лучший вариант.\n\n"
        "Нажми «Старт», чтобы узнать подробнее."
    )
    await message.answer(text, reply_markup=InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Старт", callback_data="intro")]
    ]))

# Введение
@router.callback_query(F.data == "intro")
async def intro(callback: types.CallbackQuery):
    await callback.message.answer(
        "📱 Good Day — это проект с множеством направлений, объединённых мобильным приложением. "
        "Смартфон — спутник каждого, и мы используем это преимущество."
    )
    await callback.message.answer("⬇ Меню:", reply_markup=main_menu)
    await callback.answer()

# Кнопка "Узнать о приложении"
@router.callback_query(F.data == "about_app")
async def about_app(callback: types.CallbackQuery):
    await callback.message.answer(
        "📱 В приложении Good Day:\n"
        "• Скидки и акции в городе\n"
        "• Реклама для бизнесов\n"
        "• Удобный поиск и фильтры\n\n"
        "🔥 Идеально подходит для пользователей и предпринимателей.",
        reply_markup=main_menu
    )
    await callback.answer()

# Кнопка "О франшизе"
@router.callback_query(F.data == "about_franchise")
async def about_franchise(callback: types.CallbackQuery):
    await callback.message.answer(
        "💼 Франшиза Good Day — это:\n"
        "• Минимальные риски\n"
        "• Эксклюзивность в регионе\n"
        "• Готовый IT-продукт\n"
        "• Поддержка, обучение и маркетинг\n\n"
        "Ты зарабатываешь на подключении бизнеса к рекламным пакетам.\n"
        "Мы помогаем тебе на каждом этапе запуска.",
        reply_markup=main_menu
    )
    await callback.answer()

# Кнопка "Оставить заявку"
@router.callback_query(F.data == "send_request")
async def send_request(callback: types.CallbackQuery):
    user = callback.from_user
    text = (
        f"📬 Новая заявка!\n\n"
        f"Имя: {user.full_name}\n"
        f"Юзернейм: @{user.username if user.username else 'нет'}\n"
        f"ID: {user.id}"
    )
    if ADMIN_ID:
        await bot.send_message(chat_id=int(ADMIN_ID), text=text)
    await callback.message.answer("✅ Заявка отправлена! Мы свяжемся с тобой в ближайшее время.")
    await callback.answer()

# Запуск бота
async def main():
    print("Бот запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
