from telegram import Update, KeyboardButton, ReplyKeyboardMarkup, KeyboardButtonRequestUser
from telegram.ext import ContextTypes, ConversationHandler
from .utils import load_data, get_main_keyboard, escape_markdown
from i18n_helpers import generate_i18n_object

CHECKING_LIST = range(1)

async def start_check(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    i18n = generate_i18n_object(update)
    button = KeyboardButton(
        text=i18n.translate("select_user"),
        request_user=KeyboardButtonRequestUser(
            request_id=1,
            user_is_bot=False,
            user_is_premium=None
        )
    )
    reply_markup = ReplyKeyboardMarkup([[button]], one_time_keyboard=True)
    await update.message.reply_text(
        i18n.translate("please_select_user_to_check"),
        reply_markup=reply_markup
    )
    return CHECKING_LIST

async def check_user(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    i18n = generate_i18n_object(update)
    user_shared = update.message.user_shared
    if user_shared:
        selected_user_id = user_shared.user_id
        print(f"DEBUG: Überprüfe Benutzer-ID: {selected_user_id}")  # Debug-Ausgabe

        reported_users = load_data()  # Daten neu laden
        print(f"DEBUG: Geladene Daten: {reported_users}")  # Debug-Ausgabe

        if str(selected_user_id) in reported_users["scammers"]:
            user_data = reported_users["scammers"][str(selected_user_id)]
            print(f"DEBUG: Benutzer gefunden in Scammerliste: {user_data}")  # Debug-Ausgabe
            message = (
                f"__**⚠️ {i18n.translate('scammer_list')} ⚠️**__\n\n"
                f"**ID:** {escape_markdown(str(selected_user_id))}\n"
                f"**{i18n.translate('full_name')}:** {escape_markdown(user_data.get('full_name', i18n.translate('unknown')))}\n"
                f"**{i18n.translate('username')}:** {escape_markdown(user_data.get('username', i18n.translate('not_available')))}\n"
                f"**{i18n.translate('reason')}:** {escape_markdown(user_data['reason'])}\n"
                f"**{i18n.translate('reported_on')}:** {escape_markdown(user_data.get('first_reported_at', i18n.translate('unknown')).split('T')[0])}\n"
                f"**{i18n.translate('last_reported_on')}:** {escape_markdown(user_data.get('last_reported_at', i18n.translate('unknown')).split('T')[0])}\n"
                f"**{i18n.translate('total_reports')}:** {user_data['count']}\n"
            )
            await update.message.reply_text(message, parse_mode='MarkdownV2', reply_markup=get_main_keyboard())
        elif str(selected_user_id) in reported_users["trusted"]:
            user_data = reported_users["trusted"][str(selected_user_id)]
            print(f"DEBUG: Benutzer gefunden in Trustliste: {user_data}")  # Debug-Ausgabe
            message = (
                f"__**✅ {i18n.translate('trust_list')} ✅**__\n"
                f"**ID:** {escape_markdown(str(selected_user_id))}\n"
                f"**{i18n.translate('full_name')}:** {escape_markdown(user_data.get('full_name', i18n.translate('unknown')))}\n"
                f"**{i18n.translate('username')}:** {escape_markdown(user_data.get('username', i18n.translate('not_available')))}\n"
                f"**{i18n.translate('reason')}:** {escape_markdown(user_data['reason'])}\n"
                f"**{i18n.translate('reported_on')}:** {escape_markdown(user_data.get('first_reported_at', i18n.translate('unknown')).split('T')[0])}\n"
                f"**{i18n.translate('last_reported_on')}:** {escape_markdown(user_data.get('last_reported_at', i18n.translate('unknown')).split('T')[0])}\n"
                f"**{i18n.translate('total_reports')}:** {user_data['count']}\n"
            )
            await update.message.reply_text(message, parse_mode='MarkdownV2', reply_markup=get_main_keyboard())
        else:
            print(f"DEBUG: Benutzer nicht in Listen gefunden")  # Debug-Ausgabe
            await update.message.reply_text(
                i18n.translate("user_not_found_in_lists"),
                reply_markup=get_main_keyboard()
            )
        return ConversationHandler.END
    else:
        await update.message.reply_text(
            i18n.translate("no_user_selected_retry"),
            reply_markup=get_main_keyboard()
        )
        return ConversationHandler.END