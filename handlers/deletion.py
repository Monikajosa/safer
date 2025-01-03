from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
from .utils import save_data, load_data, get_main_keyboard
from i18n_helpers import generate_i18n_object
import logging
import os
from dotenv import load_dotenv

# Laden der Umgebungsvariablen aus der .env Datei
load_dotenv()

OWNER_ID = os.getenv('OWNER_ID')  # Stellen Sie sicher, dass OWNER_ID korrekt geladen wird
logger = logging.getLogger(__name__)

WAITING_FOR_DELETION_INFO = range(1)

async def delete_user(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    i18n = generate_i18n_object(update)
    try:
        user_id = update.effective_user.id
        if str(user_id) != OWNER_ID:
            await update.message.reply_text(i18n.translate("no_permission_for_action"))
            return

        command, user_id_to_delete = update.message.text.split()
        user_id_to_delete = user_id_to_delete.strip()

        # Laden Sie die aktuellen Daten
        reported_users = load_data()
        user_deleted = False

        if user_id_to_delete in reported_users["scammers"]:
            del reported_users["scammers"][user_id_to_delete]
            user_deleted = True

        if user_id_to_delete in reported_users["trusted"]:
            del reported_users["trusted"][user_id_to_delete]
            user_deleted = True

        if user_deleted:
            save_data(reported_users)  # Speichern Sie die aktualisierten Daten
            await update.message.reply_text(i18n.translate("user_deleted_successfully").format(user_id_to_delete=user_id_to_delete))
            logger.info(i18n.translate("log_user_deleted_successfully").format(user_id_to_delete=user_id_to_delete))
        else:
            await update.message.reply_text(i18n.translate("user_id_not_found"))
            logger.info(i18n.translate("log_user_id_not_found").format(user_id_to_delete=user_id_to_delete))
    except ValueError:
        await update.message.reply_text(i18n.translate("invalid_format_use_del"))
        logger.error(i18n.translate("log_invalid_format_for_del"))

async def receive_deletion_info(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    i18n = generate_i18n_object(update)
    user_id_to_delete = update.message.text.strip()
    reported_users = load_data()  # Laden Sie die aktuellen Daten
    user_deleted = False

    if user_id_to_delete in reported_users["scammers"]:
        del reported_users["scammers"][user_id_to_delete]
        user_deleted = True

    if user_id_to_delete in reported_users["trusted"]:
        del reported_users["trusted"][user_id_to_delete]
        user_deleted = True

    if user_deleted:
        save_data(reported_users)  # Speichern Sie die aktualisierten Daten
        await update.message.reply_text(i18n.translate("user_deleted_successfully").format(user_id_to_delete=user_id_to_delete),
                                        reply_markup=get_main_keyboard())
        logger.info(i18n.translate("log_user_deleted_successfully").format(user_id_to_delete=user_id_to_delete))
    else:
        await update.message.reply_text(i18n.translate("user_id_not_found"),
                                        reply_markup=get_main_keyboard())
        logger.info(i18n.translate("log_user_id_not_found").format(user_id_to_delete=user_id_to_delete))
    
    return ConversationHandler.END