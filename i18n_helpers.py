from i18n import I18n

def get_locale(update):
    return I18n.get_user_locale(update)

def generate_i18n_object(update):
    user_locale = get_locale(update)
    return I18n(locale=user_locale)

def localized_start(update, context, start):
    i18n = generate_i18n_object(update)
    start(update, context, i18n)

def localized_handle_main_menu(update, context, handle_main_menu):
    i18n = generate_i18n_object(update)
    handle_main_menu(update, context, i18n)