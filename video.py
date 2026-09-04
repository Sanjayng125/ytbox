from downloader import (
    choose_download_mode,
    cleanup_partial_downloads
)
from utils import (
    get_format_summary
)
from video_downloader import (
    choose_quality,
    get_video_info,
    get_available_qualities,
    download_video,
    download_video_only
)
from audio_downloader import (
    choose_audio,
    get_available_audio,
    download_audio_only
)
from ui import show_video_information_panel

def show_video_information():
    try:
        url = input("Enter YouTube URL: ")

        try:
            info = get_video_info(url)
        except RuntimeError as e:
            print()
            print(f"Error: {e}")
            return

        video_formats, audio_formats = get_format_summary(info)

        show_video_information_panel(
            info,
            video_formats,
            audio_formats
        )

    except KeyboardInterrupt:
        print("\nCancelled.")
        return

def download_video_menu():
    try:
        url = input("Enter YouTube URL: ")

        try:
            info = get_video_info(url)
        except RuntimeError as e:
            print()
            print(f"Error: {e}")
            return

        mode = choose_download_mode()

        if mode == "1":
            qualities = get_available_qualities(info)
            video_format = choose_quality(qualities)

            audio_formats = get_available_audio(info)
            audio_format = choose_audio(audio_formats)

            print()
            print("Downloading...")

            output_path = download_video(
                info,
                video_format,
                audio_format
            )

        elif mode == "2":
            qualities = get_available_qualities(info)
            video_format = choose_quality(qualities)

            print()
            print("Downloading...")

            output_path = download_video_only(
                info,
                video_format
            )

        elif mode == "3":
            audio_formats = get_available_audio(info)
            audio_format = choose_audio(audio_formats)

            print()
            print("Downloading...")

            output_path = download_audio_only(
                info,
                audio_format
            )

        print()
        print("Download complete!")
        print("Saved to:", output_path)

    except KeyboardInterrupt:
        cleanup_partial_downloads()
        print("\nDownload cancelled.")
        return

    except RuntimeError as e:
        print()
        print(f"Error: {e}")
        return