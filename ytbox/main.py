import argparse
from rich.prompt import IntPrompt
from ytbox.dependencies import ensure_dependencies
from ytbox.video import (
    download_video_menu,
    show_video_information
)
from ytbox.playlist import (
    download_playlist_menu,
    show_playlist_information
)
from ytbox.application import (
    show_menu,
    update,
    settings
)
from ytbox.history import show_history
from ytbox.ui import (
    show_info,
    show_error,
    show_success
)
import ytbox.dependencies as _deps
_deps.set_logger(show_info, show_success, show_error)

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
    from ytbox.config import init_dirs
    init_dirs()
    
    while True:
        try:
            show_menu()

            choice = IntPrompt.ask("[bold cyan]Choose an option[/bold cyan]")

            if choice == 1:
                download_video_menu()

            elif choice == 2:
                download_playlist_menu()

            elif choice == 3:
                show_video_information()

            elif choice == 4:
                show_playlist_information()

            elif choice == 5:
                settings()

            elif choice == 6:
                update()

            elif choice == 7:
                show_history()

            elif choice == 8:
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
