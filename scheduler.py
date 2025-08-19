from apscheduler.schedulers.background import BackgroundScheduler
from database import get_bookings
import telegram
from config import TELEGRAM_TOKEN
from datetime import datetime, timedelta

bot = telegram.Bot(token=TELEGRAM_TOKEN)

def send_reminders():
    bookings = get_bookings()
    now = datetime.now()
    
    for booking in bookings:
        _, date, time, name, chat_id = booking
        
        try:
            booking_datetime = datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M")
        except ValueError:
            continue
            
        if booking_datetime - timedelta(hours=24) <= now < booking_datetime - timedelta(hours=23):
            try:
                bot.send_message(
                    chat_id=chat_id, 
                    text=f"🔔 Напоминание: у вас тренировка завтра в {time}"
                )
            except:
                pass
                
        elif booking_datetime - timedelta(hours=2) <= now < booking_datetime - timedelta(hours=1):
            try:
                bot.send_message(
                    chat_id=chat_id, 
                    text=f"⏰ Напоминание: у вас тренировка через 2 часа ({time})"
                )
            except:
                pass

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(send_reminders, "interval", minutes=5)
    scheduler.start()
    return scheduler
