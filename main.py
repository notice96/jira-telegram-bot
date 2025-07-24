import os
from fastapi import FastAPI, Request
from aiogram import Bot
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

app = FastAPI()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

bot = Bot(token=TELEGRAM_BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

@app.post("/jira/webhook")
async def jira_webhook(request: Request):
    data = await request.json()

    issue = data.get("issue", {})
    fields = issue.get("fields", {})
    key = issue.get("key", "—")
    summary = fields.get("customfield_10324", "—")  # Название
    start_date = fields.get("customfield_10015", "—")
    deadline = fields.get("customfield_10322", "—")
    payment = fields.get("customfield_10389", "—")
    assignee = fields.get("customfield_10388", "—")
    status = fields.get("status", {}).get("name", "—")
    url = f"https://top-x-team-team.atlassian.net/browse/{key}"

    # Цветной кружок по статусу
    status_upper = status.upper()
    if "ВЫПОЛНЕНО" in status_upper:
        status_icon = "✅"
    elif "ТЕСТИРОВАНИЕ" in status_upper:
        status_icon = "🟡"
    elif "ВЕРСТКА" in status_upper:
        status_icon = "🟠"
    elif "ВЗЯТ В РАБОТУ" in status_upper:
        status_icon = "🟢"
    else:
        status_icon = "⚪️"

    text = (
        "📢 <b>Новый проект!</b> \n"
        f"🔹 <b>Название:</b> {summary}\n"
        f"👨‍💻 <b>Исполнитель:</b> {assignee}\n"
        f"💰 <b>Оплата:</b> {payment} $\n"
        f"🗓 <b>Начало:</b> {start_date}\n"
        f"⏳ <b>Дедлайн:</b> {deadline}\n"
        f"📎 <a href='{url}'>Ссылка на задачу</a>\n\n"
        f"{status_icon} <b>Статус:</b> {status}"
    )

    await bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=text)
    return {"ok": True}
