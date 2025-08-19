from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from database import init_db, add_booking, get_bookings, delete_booking, get_booking_by_datetime
from scheduler import start_scheduler
from config import TELEGRAM_TOKEN, ADMIN_CHAT_ID

init_db()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Я бот для записи на тренировки.\n"
        "Клиенты могут записываться через тренера."
    )

async def book(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if str(update.message.from_user.id) != ADMIN_CHAT_ID:
        await update.message.reply_text("❌ Доступ запрещён. Только тренер может записывать клиентов.")
        return
    
    try:
        parts = update.message.text.split()
        if len(parts) != 5:
            raise ValueError()
            
        _, date, time, name, chat_id = parts
        add_booking(date, time, name, int(chat_id))
        
        try:
            await context.bot.send_message(
                chat_id=int(chat_id),
                text=f"✅ Вы записаны на тренировку {date} в {time}"
            )
        except:
            pass
            
        await update.message.reply_text(f"✅ Клиент {name} записан на {date} в {time}")
        
    except Exception as e:
        await update.message.reply_text(
            "❌ Ошибка формата. Используйте:\n"
            "/book ГГГГ-ММ-ДД ЧЧ:ММ Имя_клиента ChatID_клиента\n"
            "Пример: /book 2024-04-15 18:00 Иван 123456789"
        )

async def show_schedule(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if str(update.message.from_user.id) != ADMIN_CHAT_ID:
        await update.message.reply_text("❌ Доступ запрещён.")
        return
        
    bookings = get_bookings()
    if not bookings:
        await update.message.reply_text("📅 Расписание пусто.")
        return
        
    msg = "📅 Текущее расписание:\n\n"
    for b in bookings:
        msg += f"• {b[1]} в {b[2]} — {b[3]}\n"
    
    await update.message.reply_text(msg)

async def delete(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if str(update.message.from_user.id) != ADMIN_CHAT_ID:
        await update.message.reply_text("❌ Доступ запрещён.")
        return
    
    try:
        parts = update.message.text.split()
        if len(parts) != 3:
            raise ValueError()
            
        _, date, time = parts
        
        booking = get_booking_by_datetime(date, time)
        if not booking:
            await update.message.reply_text("❌ Запись не найдена.")
            return
            
        delete_booking(date, time)
        
        try:
            await context.bot.send_message(
                chat_id=booking[4],
                text=f"❌ Ваша тренировка {date} в {time} была отменена."
            )
        except:
            pass
            
        await update.message.reply_text(f"✅ Запись на {date} в {time} удалена.")
        
    except:
        await update.message.reply_text(
            "❌ Ошибка формата. Используйте:\n"
            "/delete ГГГГ-ММ-ДД ЧЧ:ММ\n"
            "Пример: /delete 2024-04-15 18:00"
        )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = (
        "🤖 Команды бота:\n\n"
        "📌 /start - Приветствие\n"
        "📌 /book ДАТА ВРЕМЯ ИМЯ CHAT_ID - Записать клиента (только для тренера)\n"
        "📌 /schedule - Показать расписание (только для тренера)\n"
        "📌 /delete ДАТА ВРЕМЯ - Удалить запись (только для тренера)\n"
        "📌 /help - Помощь"
    )
    await update.message.reply_text(help_text)

def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("book", book))
    app.add_handler(CommandHandler("schedule", show_schedule))
    app.add_handler(CommandHandler("delete", delete))
    app.add_handler(CommandHandler("help", help_command))

    start_scheduler()

    print("Бот запущен...")
    app.run_polling()

if __name__ == '__main__':
    main()
