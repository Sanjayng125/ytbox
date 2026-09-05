from playlist_downloader import (
    get_playlist_info,
    download_playlist,
    download_playlist_audio,
    choose_playlist_quality,
    choose_playlist_audio_quality
)
from utils import get_playlist_duration
from downloader import cleanup_partial_downloads
from ui import (
    show_playlist_information_panel,
    show_playlist_download_info,
    show_playlist_download_options,
    show_playlist_quality_options,
    show_error,
    show_info,
)

def show_playlist_information():
    url = input("Enter playlist URL: ").strip()

    if not url:
        show_info("Please enter a playlist URL.")
        return

    try:
        info = get_playlist_info(url)

        title = info.get("title", "Unknown")
        channel = info.get("uploader", "Unknown")
        entries = info.get("entries") or []

        total_videos = len(entries)

        total_duration = get_playlist_duration(info)

        show_playlist_information_panel(
            title,
            channel,
            total_videos,
            total_duration,
            entries
        )

    except RuntimeError as e:
        print(f"Error: {e}")


def download_playlist_menu():
    url = input("Enter playlist URL: ").strip()

    if not url:
        show_info("Please enter a playlist URL.")
        return

    try:
        show_info("Extracting Playlist Information...")
        info = get_playlist_info(url)

        title = info.get("title", "Unknown")
        entries = info.get("entries") or []

        show_playlist_download_info(title, len(entries))

        show_playlist_download_options()

        choice = input("Choose an option: ").strip()

        if choice == "3":
            return

        if choice == "1":
            show_playlist_quality_options("Video")

            quality_choice = input("Choose an option: ").strip()

            if quality_choice == "1":
                try:
                    download_playlist(url, info=info)
                except KeyboardInterrupt:
                    cleanup_partial_downloads()
                    show_info("\nDownload cancelled.")
                    return

            elif quality_choice == "2":
                quality = choose_playlist_quality()

                if quality is None:
                    return

                try:
                    download_playlist(url, quality, info)
                except KeyboardInterrupt:
                    cleanup_partial_downloads()
                    show_info("\nDownload cancelled.")
                    return

            elif quality_choice == "3":
                return

            else:
                show_error("Invalid option.")
                return

        elif choice == "2":
            show_playlist_quality_options("Audio")

            quality_choice = input("Choose an option: ").strip()

            if quality_choice == "1":
                try:
                    download_playlist_audio(url, info=info)
                except KeyboardInterrupt:
                    cleanup_partial_downloads()
                    show_info("\nDownload cancelled.")
                    return

            elif quality_choice == "2":
                quality = choose_playlist_audio_quality()

                if quality is None:
                    return

                try:
                    download_playlist_audio(url, quality, info)
                except KeyboardInterrupt:
                    cleanup_partial_downloads()
                    show_info("\nDownload cancelled.")
                    return

            elif quality_choice == "3":
                return

            else:
                show_info("Invalid option.")
                return

        else:
            show_info("Invalid option.")
            return

    except RuntimeError as e:
        print(f"Error: {e}")


