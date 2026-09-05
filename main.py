from dependencies import ensure_dependencies
from video import (
    download_video_menu,
    show_video_information
)
from playlist import (
    download_playlist_menu,
    show_playlist_information
)
from application import (
    show_menu,
    update,
    settings
)
from history import show_history
import argparse
from ui import (
    show_info,
    show_error
)

try:
    ensure_dependencies()
except RuntimeError as e:
    print(f"Error: {e}")
    raise SystemExit

def parse_arguments():
    parser = argparse.ArgumentParser(
        prog="ytbox",
        description="A friendly yt-dlp wrapper."
    )

    parser.add_argument(
        "command",
        nargs="?",
        choices=["update"],
        help="Command to run."
    )

    return parser.parse_args()

def interactive_mode():
    while True:
        try:
            show_menu()

            choice = input("Choose an option: ")

            if choice == "1":
                download_video_menu()

            elif choice == "2":
                download_playlist_menu()

            elif choice == "3":
                show_video_information()

            elif choice == "4":
                show_playlist_information()

            elif choice == "5":
                settings()

            elif choice == "6":
                update()

            elif choice == "7":
                show_history()

            elif choice == "8":
                show_info("Goodbye!")
                break

            else:
                show_error("Invalid option. Try again.")

        except KeyboardInterrupt:
            show_info("\nGoodbye!")
            break

def cli_entry():
    args = parse_arguments()

    if args.command == "update":
        update()
    else:
        interactive_mode()

if __name__ == "__main__":
    cli_entry()

# if __name__ == "__main__":
#     args = parse_arguments()

#     if args.command == "update":
#         update()
#     else:
#         interactive_mode()
