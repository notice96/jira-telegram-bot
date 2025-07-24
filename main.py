from fastapi import FastAPI, Request
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
import asyncio
import uvicorn
import os

# === НАСТРОЙКИ ===

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher(bot)
app = FastAPI()

# === ПОЛЯ ИЗ JIRA ===
FIELD_PROJECT_NAME = "customfield_10324"
FIELD_EXECUTOR = "customfield_10388"
FIELD_PAYMENT = "customfield_10389"
FIELD_START_DATE = "customfield_10015"
FIELD_DEADLINE = "customfield_10322"

# === HELPER ===
def format_message(data: dict) -> str:
    fields = data.get("issue", {}).get("fields", {})
    key = data.get("issue", {}).get("key", "?")
    url = f"https://top-x-team-team.atlassian.net/browse/{key}"

    project_name = fields.get(FIELD_PROJECT_NAME, "Без названия")
    executor = fields.get(FIELD_EXECUTOR, "Не назначен")
    payment = fields.get(FIELD_PAYMENT, "?")
    start_date = fields.get(FIELD_START_DATE, "?")
    deadline = fields.get(FIELD_DEADLINE, "?")
    status = fields.get("status", {}).get("name", "Без статуса")

    status_emojis = {
        "ВЗЯТ В РАБОТУ": "🟢",
        "ВЕРСТКА": "🟡",
        "ТЕСТИРОВАНИЕ": "🔵",
        "ВЫПОЛНЕНО": "✅",
        "ОТМЕНЕНО": "❌"
    }
    status_emoji = status_emojis.get(status.upper(), "🔘")

    return (
        f"📢 Новый проект!\n"
        f"🔹 Название: {project_name}\n"
        f"👨‍💻 Исполнитель: {executor}\n"
        f"🗓 Начало: {start_date}\n"
        f"⏳ Дедлайн: {deadline}\n"
        f"💰 Оплата: {payment} ₽\n"
        f"📎 {url}\n"
        f"Статус: {status_emoji} {status}"
    )

@app.post("/jira/webhook")
async def receive_webhook(request: Request):
    payload = await request.json()
    message = format_message(payload)
    await bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message, parse_mode=ParseMode.HTML)
    return {"status": "ok"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=int(os.getenv("PORT", 8000)))
