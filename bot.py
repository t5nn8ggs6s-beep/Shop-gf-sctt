from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

from config import TOKEN, ADMIN_ID, WALLET, SUPPORT
import db
import keyboards

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

db.init_db()

# ================= СТАРТ =================
@dp.message_handler(commands=["start"])
async def start(msg: types.Message):
    db.add_user(msg.from_user.id)

    await msg.answer(
        "🔐 NO VPNNiffy — Премиум VPN\n\n"
        "🚀 Быстрый и стабильный доступ\n"
        "🔒 Без ограничений\n\n"
        "Выберите действие:",
        reply_markup=keyboards.main_menu()
    )

# ================= КУПИТЬ =================
@dp.message_handler(lambda m: m.text == "💎 Купить VPN")
async def buy(msg: types.Message):

    await msg.answer(
        "💎 ПОКУПКА VPN\n\n"
        "📅 7 дней — 5 USDT\n"
        "📅 30 дней — 10 USDT\n\n"
        "💰 Оплата: TON / USDT\n\n"
        f"📥 Кошелёк:\n{WALLET}\n\n"
        "⚠️ После оплаты нажмите кнопку ниже",
        reply_markup=keyboards.pay_kb()
    )

# ================= Я ОПЛАТИЛ =================
@dp.callback_query_handler(lambda c: c.data == "paid")
async def paid(call: types.CallbackQuery):

    db.add_payment(call.from_user.id)

    await call.message.answer("⏳ Заявка отправлена, ожидайте подтверждения")

    await bot.send_message(
        ADMIN_ID,
        f"💰 Новая оплата\n\n👤 {call.from_user.id}\n\nПроверь перевод"
    )

# ================= ПОДДЕРЖКА =================
@dp.message_handler(lambda m: m.text == "👨‍💻 Поддержка")
async def support(msg: types.Message):
    await msg.answer(f"👨‍💻 Поддержка: {SUPPORT}")

# ================= АДМИН =================
@dp.message_handler(commands=["admin"])
async def admin(msg: types.Message):
    if msg.from_user.id == ADMIN_ID:
        await msg.answer("👑 Админ панель", reply_markup=keyboards.admin_menu())

# ---------- СТАТИСТИКА ----------
@dp.message_handler(lambda m: m.text == "📊 Статистика")
async def stats(msg: types.Message):
    if msg.from_user.id != ADMIN_ID:
        return

    users = db.get_users()
    await msg.answer(f"📊 Пользователей: {len(users)}")

# ---------- РАССЫЛКА ----------
broadcast = {}

@dp.message_handler(lambda m: m.text == "📨 Рассылка")
async def broadcast_start(msg: types.Message):
    if msg.from_user.id == ADMIN_ID:
        broadcast[msg.from_user.id] = True
        await msg.answer("✉️ Отправь текст")

@dp.message_handler()
async def broadcast_send(msg: types.Message):

    if broadcast.get(msg.from_user.id):
        broadcast[msg.from_user.id] = False

        users = db.get_users()

        for u in users:
            try:
                await bot.send_message(u[0], msg.text)
            except:
                pass

        await msg.answer("✅ Рассылка завершена")

# ================= ВЫДАЧА =================
@dp.message_handler(commands=["give"])
async def give(msg: types.Message):
    if msg.from_user.id != ADMIN_ID:
        return

    try:
        user_id = int(msg.get_args())

        await bot.send_message(
            user_id,
            "✅ Оплата подтверждена!\n\n"
            "🔐 VPN доступ активирован\n\n"
            "📱 Скачайте VPNIFY\n"
            "Подключитесь 🚀"
        )

    except:
        await msg.answer("Используй: /give user_id")

# ================= ЗАПУСК =================
executor.start_polling(dp)
