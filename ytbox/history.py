import json
from pathlib import Path
from datetime import datetime
from ytbox.ui import show_history_table, show_history_menu, show_success, show_error
import sys

def _get_base_dir():
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent
    return Path(__file__).resolve().parent.parent

HISTORY_FILE = _get_base_dir() / "data" / "history.json"
MAX_HISTORY_ENTRIES = 200

def _write_history_atomic(history):
    temp_file = HISTORY_FILE.with_suffix(".json.tmp")

    with open(temp_file, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=4)

    temp_file.replace(HISTORY_FILE)  # atomic on both Windows and POSIX


def save_download(title, url, download_type):
    entry = {
        "title": title,
        "url": url,
        "type": download_type,
        "downloaded_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }

    history = get_history()

    if HISTORY_FILE.exists():
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                history = json.load(f)
        except json.decoder.JSONDecodeError:
            history = []

    history.append(entry)

    if len(history) > MAX_HISTORY_ENTRIES:
        history = history[-MAX_HISTORY_ENTRIES:]

    _write_history_atomic(history)


def get_history():
    if not HISTORY_FILE.exists():
        return []

    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        _write_history_atomic([])
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
    _write_history_atomic([])
