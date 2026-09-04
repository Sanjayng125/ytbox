import json
from pathlib import Path
from datetime import datetime

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

        print("\nDownload History")
        print("----------------")

        if not history:
            print("No download history.\n")
        else:
            for index, entry in enumerate(history, start=1):
                print(f"{index}. {entry['title']}")
                print(f"   Type: {entry['type']}")
                print(f"   Downloaded: {entry.get('downloaded_at', 'Unknown')}")
                print(f"   URL: {entry['url']}")
                print()

        print("1. Clear history")
        print("2. Back")

        try:
            choice = input("Choose an option: ").strip()

            if choice == "1":
                clear_history()
                print("History cleared.")
                return

            elif choice == "2":
                return

            else:
                print("Invalid option. Try again.")
        except KeyboardInterrupt:
            return
        
def clear_history():
    if HISTORY_FILE.exists():
        HISTORY_FILE.unlink()

