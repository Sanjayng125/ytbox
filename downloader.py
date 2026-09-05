import config
from ui import (
    show_download_mode_menu,
    show_error
)

def choose_download_mode():
    show_download_mode_menu()

    while True:
        choice = input("Choose mode: ")

        if choice in ("1", "2", "3"):
            return choice

        show_error("Invalid choice. Try again.")
        

def cleanup_partial_downloads():
    config.DOWNLOAD_DIR.mkdir(exist_ok=True)

    temporary_extensions = (
        ".part",
        ".ytdl",
        ".part-Frag",
    )

    for path in config.DOWNLOAD_DIR.rglob("*"):
        if path.is_file() and path.name.endswith(temporary_extensions):
            try:
                path.unlink()
            except OSError:
                pass

