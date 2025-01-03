import logging
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ConversationHandler
from config import TOKEN, SUPPORT_GROUP_ID, OWNER_ID
from handlers import start, handle_main_menu, user_selected, check_user, handle_update_choice, receive_full_name, receive_username, receive_reason, cancel, handle_support_message, error_handler, delete_user
from handlers import SELECTING_USER, WAITING_FOR_FULL_NAME, WAITING_FOR_USERNAME, WAITING_FOR_REASON, UPDATING_USER, WAITING_FOR_DELETION_INFO, CHECKING_LIST
from handlers.deletion_request import request_deletion, receive_deletion_info, deletion_conv_handler
from handlers.utils import get_main_keyboard
from i18n_helpers import localized_start, localized_handle_main_menu

# Logging konfigurieren
logging.basicConfig(format='%(asctime)s - %(name)s - %(levellevel)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Timeout-Wert
TIMEOUT = 60  # Timeout-Wert in Sekunden

def main() -> None:
    global support_message_mapping, deletion_requests
    support_message_mapping = {}
    deletion_requests = {}

    application = Application.builder().token(TOKEN).build()

    i18n = I18n(locale='en')  # Default locale for regex patterns
    report_conv_handler = ConversationHandler(
        entry_points=[
            MessageHandler(filters.Regex(f'^{i18n.translate("report_scammer")}|{i18n.translate("report_trust")}$'), lambda update, context: localized_handle_main_menu(update, context, handle_main_menu))
        ],
        states={
            SELECTING_USER: [MessageHandler(filters.StatusUpdate.USER_SHARED, user_selected)],
            UPDATING_USER: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_update_choice)],
            WAITING_FOR_FULL_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_full_name)],
            WAITING_FOR_USERNAME: [
                MessageHandler(filters.TEXT & ~filters.COMMAND | filters.Regex(f'^{i18n.translate("skip")}$'), receive_username)],
            WAITING_FOR_REASON: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_reason)]
        },
        fallbacks=[CommandHandler("cancel", cancel)]
    )

    check_list_conv_handler = ConversationHandler(
        entry_points=[
            MessageHandler(filters.Regex(f'^{i18n.translate("check_user")}$'), lambda update, context: localized_handle_main_menu(update, context, handle_main_menu))
        ],
        states={
            CHECKING_LIST: [MessageHandler(filters.StatusUpdate.USER_SHARED, check_user)]
        },
        fallbacks=[CommandHandler("cancel", cancel)]
    )

    application.add_handler(CommandHandler("start", lambda update, context: localized_start(update, context, start)))
    application.add_handler(report_conv_handler)
    application.add_handler(check_list_conv_handler)
    application.add_handler(deletion_conv_handler)
    application.add_handler(MessageHandler(filters.ALL & ~filters.COMMAND, handle_support_message))
    application.add_handler(CommandHandler("del", delete_user))

    # Register the error handler
    application.add_error_handler(error_handler)

    application.run_polling()

if __name__ == '__main__':
    main()