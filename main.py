"""
🤖 FIB BOT - Исправленная версия для Render
С правильным UTC временем и keep-alive
"""

import requests
import json
import time
import os
from datetime import datetime
import schedule
import threading
import logging
from dotenv import load_dotenv
from flask import Flask, jsonify
from threading import Thread

# ===================== FLASK ДЛЯ RENDER =====================
app = Flask(__name__)

@app.route('/')
def home():
    return "🤖 Bot работает! Время UTC, keep-alive каждые 14 мин"


def get_job_name(job):
    func_name = job.job_func.__name__
    if "str" in func_name: return "STR"
    if "atf" in func_name: return "ATF"
    if "fpb" in func_name: return "FPB"
    if "cid" in func_name: return "CID"
    if "keep" in func_name: return "Keep-alive"
    return "Unknown"

@app.route('/health')
def health():
    return jsonify({
        "status": "ok",
        "time_utc": datetime.utcnow().strftime("%H:%M:%S"),
        "time_msk": (datetime.utcnow().hour + 3) % 24,
        "next_messages": get_next_messages()
    })

def get_next_messages():
    jobs = list(schedule.get_jobs())
    if not jobs:
        return "Нет задач"
    next_job = min(jobs, key=lambda x: x.next_run)
    return f"Следующее: {get_job_name(next_job)} в {next_job.next_run.strftime('%H:%M UTC')}"

# ===================== ЗАГРУЗКА КОНФИГА =====================
load_dotenv()

WEBHOOK_URL = os.getenv("WEBHOOK_URL", "https://discord.com/api/webhooks/1467255626240495740/Nk1PW-RU2f3ORjQd4Hmy-Jgc_1NZtw4Z2lXakfgbHjDb5ezziVgvGi75tsdriOdP7DfG")

ROLES = {
    "FIB": os.getenv("ROLE_FIB", "1242210100584910858"),
    "STR": os.getenv("ROLE_STR", "1389060594161942558"),
    "ATF": os.getenv("ROLE_ATF", "1242213554761764995"),
    "FPB": os.getenv("ROLE_FPB", "1242216678507417741"),
    "CID": os.getenv("ROLE_CID", "1242214655733141514"),
}

CHANNELS = {
    "APPLICATIONS_STR": os.getenv("CHANNEL_APPLICATIONS_STR", "1263503399442317342"),
    "APPLICATIONS_ATF": os.getenv("CHANNEL_APPLICATIONS_ATF", "1263503451640299662"),
    "APPLICATIONS_FPB": os.getenv("CHANNEL_APPLICATIONS_FPB", "1263503533710246062"),
    "APPLICATIONS_CID": os.getenv("CHANNEL_APPLICATIONS_CID", "1263503558813286420"),
    "SERVER_ID": os.getenv("SERVER_ID", "714752380616441878")
}

# ===================== ВАЖНО: ВРЕМЯ В UTC =====================
# Москва UTC+3: вычитаем 3 часа
SCHEDULES = {
    "str": ["08:30"],    # МСК: 11:30
    "atf": ["10:00"],   # МСК: 13:00
    "fpb": ["11:30"],    # МСК: 14:30
    "cid": ["13:00"]    # МСК: 16:00
}

# ===================== ТЕКСТЫ СООБЩЕНИЙ =====================
MESSAGES = {
    "str": {
        "name": "Selection, Training and Regulation",
        "content": """**Приветствую, уважаемые сотрудники** {FIB} 

🌟 **Отдел STR открывает свои двери для самых амбициозных и преданных делу!** Готовы ли вы стать частью команды мечты?

**Что вас ждет:**

💰 **Быстрый взлет по карьерной лестнице:** Ваши усилия будут мгновенно замечены и щедро вознаграждены!
🤝 **Дружный коллектив:** Забудьте об интригах и склоках — у нас царит атмосфера взаимопомощи и поддержки!
🏞️ **Работа в удовольствие:** Забудьте о скучных буднях, вас ждут захватывающие приключения на благо штата!
🌊 **Полный доступ к ресурсам:** В вашем распоряжении будет водный транспорт департамента, чтобы вы могли оперативно реагировать на любые вызовы!

**Что требуется от вас:**

🧠 **Знание законов штата:** Будьте готовы применять свои знания на практике!
🚗 **Водительское удостоверение:** Без него никуда!
🎤 **Четкая речь:** Важно уметь доносить свои мысли до окружающим.
♾️ **Готовность к обучению:** Мир не стоит на месте, и мы тоже! Развивайтесь вместе с нами!

**Ваша миссия:**

🎣 **Проведение обучения академии Федерального Бюро**
📜 **Ведение дисциплинарного надзора внутри Федерального Бюро**
🚨 **Задержание нарушителей:** Преступность не пройдет!

**Не упустите свой шанс стать частью легендарного отдела {STR}!** 
🎯 **Подайте заявку прямо сейчас в канале:** {APPLICATIONS_STR}

По всем вопросам обращайтесь к руководству отдела <@&1389060880968192020>**""",
        "roles": ["FIB", "STR"],
        "channels": ["APPLICATIONS_STR"]
    },
    "atf": {
        "name": "Anti-Terror Force",
        "content": """**Уважаемые сотрудники** {FIB}
🔹 **Набор в отдел ATF открыт!** 🔹

Если ты обладаешь 3 порядковым рангом и действительно готов работать, а не просто числиться в списке — у тебя есть шанс стать частью элиты.

{ATF} — это не просто подразделение. Это команда, действующая в самых сложных и ответственных ситуациях. Мы принимаем только тех, кто готов брать на себя ответственность, не боится трудностей и всегда действует в интересах службы.

**Требования для вступления:**

🔹 Минимум 3 порядковый ранг
🔹 Осознанное желание работать и развиваться в составе ATF
🔹 Дисциплина, пунктуальность, соблюдение субординации
🔹 Готовность действовать в команде и по уставу

**Что даёт служба в ATF:**

🔺 Работа на передовой
🔺 Тактические операции
🔺 Возможность карьерного роста внутри элитного подразделения
🔺 Поддержка сплочённого коллектива

**Не упустите свой шанс стать частью легендарного отдела** {ATF}! 
🎯 **Подайте заявку прямо сейчас в канале:** {APPLICATIONS_ATF}

**Хочешь стать частью лучших? Пиши!!!!**

По всем вопросам обращайтесь к руководству отдела <@&966268913170141194>""",
        "roles": ["FIB", "ATF"],
        "channels": ["APPLICATIONS_ATF"]
    },
    "fpb": {
        "name": "Federal Patrol Bureau",
        "content": """**Уважаемые сотрудники бюро** {FIB}
хотим сообщить что проходит **Набор в отдел: Federal Patrol Bureau** ({FPB}),!

Мы занимаемся патрулями, помогаем людям освоиться
и влиться в жизнь отдела!

**Требования для работы:**
- Знание основ УАК, Закон о "FIB", Закон о "Юрисдикции"
- Активность на тренировках и различных мероприятиях
- Желание развиваться вместе с отделом

**Что вы получите от нас:**
- Приятный коллектив, который всегда составит компанию
- Добрый старший состав, протягивающий руку помощи
- Красивая и приятная глазу форма

**С нетерпением ждём твоей заявки!**
🎯 **Подать заявку можно в канале:** {APPLICATIONS_FPB}

По всем вопросам обращайтесь к руководству отдела <@&1106939082313039922>""",
        "roles": ["FIB", "FPB"],
        "channels": ["APPLICATIONS_FPB"]
    },
    "cid": {
        "name": "Criminal Investigation Division",
        "content": """**Внимание {FIB} !**

📚 **Отдел {CID} открывает набор!** Вопрос в том, хватит ли у вас Желания, т.к. у нас вы не будете сидеть без дела! 

Наш отдел построен на командной работе и только от вас будет зависеть как выглядит FIB для общества.

**Что мы вам предлагаем:**

• 🪶 **Лёгкую Систему повышения**
• 📣 **Возможность бороться с преступностью**
• 💸 **Хорошие премии за работу**
• 📈 **Тесную команду профессионалов, которые станут твоей опорой**

**Что требуется от вас?**

• Желание Работать на благо фракции
• (По возможности) иметь Опыт работы в схожих отделах
• Уделять работе время 

По всем вопросам обращайтесь к руководству отдела <@&966269084129951784>""",
        "roles": ["FIB", "CID"],
        "channels": ["APPLICATIONS_CID"]
    }
}

# ===================== ЛОГГИРОВАНИЕ =====================
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s UTC - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# ===================== ФУНКЦИИ =====================
def format_role_mention(role_key):
    return f"<@&{ROLES.get(role_key, role_key)}>" if role_key in ROLES else f"@{role_key}"

def format_channel_mention(channel_key):
    return f"<#{CHANNELS.get(channel_key, channel_key)}>" if channel_key in CHANNELS else f"#{channel_key}"

def prepare_message(message_key):
    msg_data = MESSAGES.get(message_key)
    if not msg_data:
        return ""
    
    content = msg_data["content"]
    for role in msg_data.get("roles", []):
        content = content.replace(f"{{{role}}}", format_role_mention(role))
    for channel in msg_data.get("channels", []):
        content = content.replace(f"{{{channel}}}", format_channel_mention(channel))
    
    return content

def send_webhook(content, username="FIB Bot"):
    if not WEBHOOK_URL:
        logger.error("❌ Нет WEBHOOK_URL")
        return False
    
    data = {
        "content": content,
        "username": username,
        "avatar_url": os.getenv("BOT_AVATAR", "https://imgur.com/a/70K4fGM")
    }
    
    try:
        response = requests.post(WEBHOOK_URL, json=data, timeout=10)
        if response.status_code in [200, 204]:
            logger.info(f"✅ Отправлено: {username}")
            return True
        else:
            logger.error(f"❌ Ошибка {response.status_code}")
            return False
    except Exception as e:
        logger.error(f"❌ Ошибка сети: {e}")
        return False

def send_rd():
    content = prepare_message("str")
    return send_webhook(content, "Selection, Training and Regulation")

def send_seb():
    content = prepare_message("atf")
    return send_webhook(content, "Anti-Terror Force")

def send_pb():
    content = prepare_message("fpb")
    return send_webhook(content, "Federal Patrol Bureau")

def send_rdb():
    content = prepare_message("cid")
    return send_webhook(content, "Criminal Investigation Division")

# ===================== KEEP-ALIVE ДЛЯ RENDER =====================
def keep_alive_ping():
    """ВАЖНО: Предотвращаем сон Render"""
    logger.info("🔄 Keep-alive: бот активен")

# ===================== НАСТРОЙКА РАСПИСАНИЯ =====================
def setup_schedule():
    schedule.clear()
    
    # ВАЖНО: Keep-alive каждые 14 минут (меньше 15!)
    schedule.every(5).minutes.do(keep_alive_ping)
    
    # РАСПИСАНИЕ В UTC!
    # STR
    for t in SCHEDULES["str"]:
        schedule.every().day.at(t).do(send_rd)
        logger.info(f"📅 STR в {t} UTC ({int(t[:2])+3}:{t[3:]} МСК)")
    
    # ATF
    for t in SCHEDULES["atf"]:
        schedule.every().day.at(t).do(send_seb)
        logger.info(f"📅 ATF в {t} UTC ({int(t[:2])+3}:{t[3:]} МСК)")
    
    # FPB
    for t in SCHEDULES["fpb"]:
        schedule.every().day.at(t).do(send_pb)
        logger.info(f"📅 FPB в {t} UTC ({int(t[:2])+3}:{t[3:]} МСК)")
    
    # CID
    for t in SCHEDULES["cid"]:
        schedule.every().day.at(t).do(send_rdb)
        logger.info(f"📅 CID в {t} UTC ({int(t[:2])+3}:{t[3:]} МСК)")
    
    logger.info(f"✅ Расписание настроено. Задач: {len(schedule.get_jobs())}")


# ===================== ОСНОВНОЙ ПЛАНИРОВЩИК =====================
def run_scheduler():
    """Основной цикл бота"""
    logger.info("🚀 FIB Bot запущен (UTC время)")
    
    # Настраиваем расписание
    setup_schedule()
    
    # Отправляем тестовое сообщение
    send_webhook("🤖 FIB Bot перезапущен с правильным UTC временем", "Система")
    
    # Основной цикл
    while True:
        try:
            schedule.run_pending()
            time.sleep(30)  # 58 секунд
            
            # Лог каждый час
            if datetime.now().minute == 0:
                logger.info(f"⏰ Текущее время UTC: {datetime.utcnow().strftime('%H:%M')}")
                
        except KeyboardInterrupt:
            break
        except Exception as e:
            logger.error(f"❌ Ошибка: {e}")
            time.sleep(60)

# ===================== ЗАПУСК FLASK =====================
def run_flask_server():
    """Запускаем Flask сервер для Render"""
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False)

# ===================== ГЛАВНЫЙ ЗАПУСК =====================
if __name__ == "__main__":
    # Запускаем Flask в отдельном потоке
    flask_thread = Thread(target=run_flask_server, daemon=True)
    flask_thread.start()
    
    # Даем Flask время запуститься
    time.sleep(3)
    
    # Запускаем бота
    try:
        run_scheduler()
    except Exception as e:
        logger.error(f"💀 Критическая ошибка: {e}")





