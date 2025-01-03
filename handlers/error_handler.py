import logging
from telegram import Update
from telegram.ext import ContextTypes
from telegram.error import TimedOut
from i18n_helpers import generate_i18n_object

logger = logging.getLogger(__name__)

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    i18n = generate_i18n_object(update)
    try:
        logger.error(msg=i18n.translate("exception_while_handling_update"), exc_info=context.error)
        await update.message.reply_text(i18n.translate("unexpected_error_occurred"))
    except TimedOut:
        logger.error(i18n.translate("request_timed_out_retrying"))
        # Hier können Sie Logik hinzufügen, um die Anfrage erneut zu senden oder andere Maßnahmen zu ergreifen.