import logging
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ContextTypes
from handlers.utils import get_main_keyboard, load_data
from i18n_helpers import generate_i18n_object

logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    i18n = generate_i18n_object(update)
    reported_users = load_data()
    total_reports = sum(user_data['count'] for list_type in reported_users for user_data in reported_users[list_type].values())
    await update.message.reply_text(
        i18n.translate("welcome_message").format(total_reports=total_reports),
        reply_markup=get_main_keyboard(i18n)
    )