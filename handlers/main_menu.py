from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
from .report import start_report
from .check import start_check
from i18n_helpers import generate_i18n_object

async def handle_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    i18n = generate_i18n_object(update)
    text = update.message.text
    if text == i18n.translate("report_scammer"):
        return await start_report(update, context, "scammers")
    elif text == i18n.translate("report_trust"):
        return await start_report(update, context, "trusted")
    elif text == i18n.translate("check_user"):
        return await start_check(update, context)
    elif text == i18n.translate("request_deletion"):
        await update.message.reply_text(i18n.translate("enter_id_and_reason"))
        return ConversationHandler.END