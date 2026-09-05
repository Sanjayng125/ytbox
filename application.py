import config
from dependencies import (
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
from ui import (
    show_main_menu,
    show_title,
    show_success,
    show_error,
    show_info,
    show_settings_menu,
    show_download_location
)

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

def update():
    try:
        print()
        show_info("Checking for updates...")

        installed_ytdlp = get_ytdlp_version()
        latest_ytdlp = get_latest_ytdlp_version()

        installed_ffmpeg = get_ffmpeg_build_date()
        latest_ffmpeg = get_latest_ffmpeg_version()
        
        installed_deno = get_deno_version()
        latest_deno = get_latest_deno_version()

        ytdlp_update = is_ytdlp_update_available(
            installed_ytdlp,
            latest_ytdlp
        )
        ffmpeg_update = is_ffmpeg_update_available(
            installed_ffmpeg,
            latest_ffmpeg
        )
        deno_update = is_deno_update_available(
            installed_deno,
            latest_deno
        )

        print()

        if installed_ytdlp and latest_ytdlp:
            if ytdlp_update:
                show_info(f"yt-dlp:  Update available ({installed_ytdlp} -> {latest_ytdlp})")
            else:
                show_success(f"yt-dlp:  Up to date ({installed_ytdlp})")
        else:
            show_error("yt-dlp:  Could not check")

        if installed_ffmpeg and latest_ffmpeg:
            latest_ffmpeg_date = latest_ffmpeg[:10].replace("-", "")

            if ffmpeg_update:
                show_info(f"FFmpeg:  Update available ({installed_ffmpeg} -> {latest_ffmpeg_date})")
            else:
                show_success(f"FFmpeg:  Up to date ({installed_ffmpeg})")
        else:
            show_error("FFmpeg:  Could not check")

        if installed_deno and latest_deno:
            latest_deno_version = latest_deno.lstrip("v")

            if deno_update:
                show_info(f"Deno:    Update available ({installed_deno} -> {latest_deno_version})")
            else:
                show_success(f"Deno:    Up to date ({installed_deno})")
        else:
            show_error("Deno:    Could not check")
        
        if not ytdlp_update and not ffmpeg_update and not deno_update:
            print()
            show_success("Everything is up to date.")
            return

        print()
        choice = input("Update now? (y/n): ").strip().lower()

        if choice != "y":
            show_info("Update cancelled.")
            return

        if ytdlp_update:
            print()
            show_info("Updating yt-dlp...")

            if update_ytdlp():
                show_success("yt-dlp updated successfully.")
            else:
                show_error("yt-dlp update failed.")

        if ffmpeg_update:
            print()
            show_info("Updating FFmpeg...")

            if update_ffmpeg():
                show_success("FFmpeg updated successfully.")
            else:
                show_error("FFmpeg update failed.")

        if deno_update:
            print()
            show_info("Updating Deno...")

            if update_deno():
                show_success("Deno updated successfully.")
            else:
                show_error("Deno update failed.")
        
        print()
        show_success("Update successful.")

    except KeyboardInterrupt:
        show_info("\nUpdate cancelled.")
        return
