from aiogram import Bot
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from fastapi import FastAPI, Request
import os

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

bot = Bot(
    token=TELEGRAM_BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)

app = FastAPI()

@app.post("/jira/webhook")
async def jira_webhook(request: Request):
    data = await request.json()

    issue = data.get("issue", {})
    fields = issue.get("fields", {})

    название = fields.get("customfield_10324", "—")
    дата_начала = fields.get("customfield_10015", "—")
    дедлайн = fields.get("customfield_10322", "—")
    оплата = fields.get("customfield_10389", "—")
    исполнитель = fields.get("customfield_10388", "—")
    статус = fields.get("status", {}).get("name", "—")
    issue_key = issue.get("key", "")
    ссылка = f"https://top-x-team-team.atlassian.net/browse/{issue_key}"

    # Определим иконку по статусу
    статус_иконка = "🟢"
    if "СДАНО" in статус.upper():
        статус_иконка = "✅"
    elif "ОТКЛОНЕНО" in статус.upper():
        статус_иконка = "🔴"
    elif "В ОЖИДАНИИ" in статус.upper():
        статус_иконка = "🟡"

    text = (
        "📢 <b>Новый проект!</b>\n"
        f"🔹 <b>Название:</b> {название}\n"
        f"👨‍💻 <b>Исполнитель:</b> {исполнитель}\n"
        f"💰 <b>Оплата:</b> {оплата} $\n"
        f"🗓 <b>Начало:</b> {дата_начала}\n"
        f"⏳ <b>Дедлайн:</b> {дедлайн}\n"
        f"📎 <a href='{ссылка}'>Ссылка на задачу</a>\n\n"
        f"{статус_иконка} <b>Статус:</b> {статус}"
    )

    await bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=text)

    return {"ok": True}
