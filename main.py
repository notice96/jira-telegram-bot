import os
from fastapi import FastAPI, Request
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from dotenv import load_dotenv

# Загружаем переменные из .env
load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

bot = Bot(
    token=TELEGRAM_BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher()
app = FastAPI()

@app.post("/jira/webhook")
async def jira_webhook(request: Request):
    data = await request.json()

    issue = data.get("issue", {})
    fields = issue.get("fields", {})

    name = fields.get("customfield_10324", "—")
    start_date = fields.get("customfield_10015", "—")
    deadline = fields.get("customfield_10322", "—")
    payment = fields.get("customfield_10389", "—")
    assignee = fields.get("customfield_10388", "—")
    status = fields.get("status", {}).get("name", "—")

    text = (
        "📢 <b>Новый проект!</b>\n"
        f"🔹 <b>Название:</b> {название}\n"
        f"👨‍💻 <b>Исполнитель:</b> {исполнитель}\n"
        f"🗓 <b>Начало:</b> {дата_начала}\n"
        f"⏳ <b>Дедлайн:</b> {дедлайн}\n"
        f"💰 <b>Оплата:</b> {оплата} $\n"
        f"📎 <a href='{ссылка}'>Открыть задачу в Jira</a>\n"
        f"Статус: 🟢 <b>{статус}</b>"
    )

    await bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=text)
    return {"ok": True}
