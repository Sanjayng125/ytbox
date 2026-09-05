import json
from pathlib import Path
from datetime import datetime
from ui import show_history_table, show_history_menu, show_success, show_error

HISTORY_FILE = Path(__file__).resolve().parent / "history.json"


def save_download(title, url, download_type):
    entry = {
        "title": title,
        "url": url,
        "type": download_type,
        "downloaded_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }

    history = []

    if HISTORY_FILE.exists():
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                history = json.load(f)
        except json.decoder.JSONDecodeError:
            history = []

    history.append(entry)

    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=4)


def get_history():
    if not HISTORY_FILE.exists():
        return []

    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.decoder.JSONDecodeError:
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
                json.dump([], f, indent=4)
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
            return
        
def clear_history():
    if HISTORY_FILE.exists():
        HISTORY_FILE.unlink()

