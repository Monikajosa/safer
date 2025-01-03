import json
from telegram import KeyboardButton, ReplyKeyboardMarkup
from i18n_helpers import generate_i18n_object

def load_data():
    try:
        with open('reported_users.json', 'r') as f:
            data = json.load(f)
            if isinstance(data, dict):  # Sicherstellen, dass die Daten ein Dictionary sind
                return data
            else:
                print("DEBUG: Daten sind nicht im erwarteten Format:", data)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print("DEBUG: Fehler beim Laden der Daten:", e)  # Debug-Ausgabe
    return {"scammers": {}, "trusted": {}}  # Standardwert zurückgeben

def save_data(reported_users):
    try:
        with open('reported_users.json', 'w') as f:
            json.dump(reported_users, f, indent=4)
            print("DEBUG: Daten gespeichert:", reported_users)  # Debug-Ausgabe
    except Exception as e:
        print("DEBUG: Fehler beim Speichern der Daten:", e)  # Debug-Ausgabe

def get_main_keyboard(i18n):
    keyboard = [
        [KeyboardButton(i18n.translate("report_scammer")), KeyboardButton(i18n.translate("report_trust"))],
        [KeyboardButton(i18n.translate("check_user"))],
        [KeyboardButton(i18n.translate("request_deletion"))]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

def escape_markdown(text):
    """Escapes markdown special characters."""
    escape_chars = r"\_*[]()~`>#+-=|{}.!"
    return ''.join(f'\\{char}' if char in escape_chars else char for char in text)