import ytbox.config as config
from ytbox.dependencies import (
    get_ytdlp_version,
    get_latest_ytdlp_version,
    get_ffmpeg_build_date,
    get_latest_ffmpeg_version,
    get_deno_version,
    get_latest_deno_version,
    is_ytdlp_update_available,
    is_ffmpeg_update_available,
    is_deno_update_available,
    update_ytdlp,
    update_ffmpeg,
    update_deno
)
from ytbox.ui import (
    show_main_menu,
    show_success,
    show_error,
    show_info,
    show_settings_menu,
    show_download_location,
    show_update_status_table
)
from rich.status import Status
from rich.console import Console
console = Console()

def show_menu():
    show_main_menu()

def settings():
    try:
        while True:
            show_settings_menu()

            choice = input("Choose an option: ")

            if choice == "1":
                show_download_location(config.DOWNLOAD_DIR)

                new_path = input(
                    "Enter new download location: "
                ).strip()

                if not new_path:
                    show_info("Location unchanged.")
                    continue

                try:
                    config.set_download_dir(new_path)
                except RuntimeError as e:
                    print()
                    print(f"Error: {e}")
                    continue

                show_success("Download location updated!")
                show_download_location(config.DOWNLOAD_DIR)

            elif choice == "2":
                return

            else:
                show_error("Invalid choice. Try again.")

    except KeyboardInterrupt:
        show_info("\nCancelled.")
        return

def _check_updates():
    with Status("[bold yellow]Checking for updates…[/bold yellow]", console=console):
        installed_ytdlp  = get_ytdlp_version()
        latest_ytdlp     = get_latest_ytdlp_version()
        installed_ffmpeg = get_ffmpeg_build_date()
        latest_ffmpeg    = get_latest_ffmpeg_version()
        installed_deno   = get_deno_version()
        latest_deno      = get_latest_deno_version()

    return [
        {
            "name": "yt-dlp",
            "installed": installed_ytdlp,
            "latest": latest_ytdlp,
            "latest_display": latest_ytdlp,
            "needs_update": is_ytdlp_update_available(installed_ytdlp, latest_ytdlp),
            "updater": update_ytdlp,
        },
        {
            "name": "FFmpeg",
            "installed": installed_ffmpeg,
            "latest": latest_ffmpeg,
            "latest_display": latest_ffmpeg[:10].replace("-", "") if latest_ffmpeg else None,
            "needs_update": is_ffmpeg_update_available(installed_ffmpeg, latest_ffmpeg),
            "updater": update_ffmpeg,
        },
        {
            "name": "Deno",
            "installed": installed_deno,
            "latest": latest_deno,
            "latest_display": latest_deno.lstrip("v") if latest_deno else None,
            "needs_update": is_deno_update_available(installed_deno, latest_deno),
            "updater": update_deno,
        },
    ]


def _apply_updates(results):
    for dep in results:
        if not dep["needs_update"]:
            continue
        print()
        show_info(f"Updating {dep['name']}...")
        if dep["updater"]():
            show_success(f"{dep['name']} updated successfully.")
        else:
            show_error(f"{dep['name']} update failed.")


def update():
    try:
        print()
        results = _check_updates()

        show_update_status_table(results)

        pending = [r for r in results if r["needs_update"]]

        if not pending:
            print()
            show_success("Everything is up to date.")
            return

        print()
        choice = input("Update now? (y/n): ").strip().lower()

        if choice != "y":
            show_info("Update cancelled.")
            return

        _apply_updates(results)

        print()
        show_success("Update complete.")

    except KeyboardInterrupt:
        show_info("\nUpdate cancelled.")
        return
