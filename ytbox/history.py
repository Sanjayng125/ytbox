import json
from datetime import datetime
from ytbox.json_utils import write_json_atomic
from ytbox.ui import show_history_table, show_history_menu, show_success, show_error
from ytbox.paths import get_base_dir

HISTORY_FILE = get_base_dir() / "data" / "history.json"
MAX_HISTORY_ENTRIES = 200

def save_download(title, url, download_type):
    entry = {
        "title": title,
        "url": url,
        "type": download_type,
        "downloaded_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }

    history = get_history()

    history.append(entry)

    if len(history) > MAX_HISTORY_ENTRIES:
        history = history[-MAX_HISTORY_ENTRIES:]

    write_json_atomic(HISTORY_FILE, history)


def get_history():
    if not HISTORY_FILE.exists():
        return []

    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        write_json_atomic(HISTORY_FILE, [])
        return []


def show_history():
    while True:
        history = get_history()

        show_history_table(history)
        show_history_menu()

        try:
            choice = input("Choose an option: ").strip()

            if choice == "1":
                clear_history()
                show_success("History cleared.")
                return

            elif choice == "2":
                return

            else:
                show_error("Invalid option. Try again.")
        except KeyboardInterrupt:
            print()
            return


def clear_history():
    write_json_atomic(HISTORY_FILE, [])
