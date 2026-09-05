import yt_dlp
from config import get_ytdlp_options, DOWNLOAD_DIR
from utils import (
    make_playlist_progress_hook,
    start_progress,
    stop_progress,
    reset_progress
)
from history import save_download
from ui import (
    show_playlist_quality_menu,
    show_playlist_audio_quality_menu
)

def is_playlist(info):
    return info.get("_type") == "playlist"
    
def get_playlist_info(url):
    options = get_ytdlp_options()
    options["extract_flat"] = True

    try:
        with yt_dlp.YoutubeDL(options) as ydl:
            info = ydl.extract_info(url, download=False)

        if info.get("_type") != "playlist":
            raise RuntimeError("The URL does not point to a playlist.")

        return info

    except Exception as e:
        raise RuntimeError(f"Could not get playlist information: {e}")

        
def choose_playlist_quality():
    show_playlist_quality_menu()

    choices = {
        "1": 144,
        "2": 240,
        "3": 360,
        "4": 480,
        "5": 720,
        "6": 1080,
        "7": 1440,
        "8": 2160,
    }

    while True:
        choice = input("Choose an option: ").strip()

        if choice == "9":
            return None

        if choice in choices:
            return choices[choice]

        print("Invalid option. Try again.")
        
def choose_playlist_audio_quality():
    show_playlist_audio_quality_menu()

    choices = {
        "1": "320",
        "2": "256",
        "3": "192",
        "4": "128",
        "5": "96",
    }

    while True:
        choice = input("Choose an option: ").strip()

        if choice == "6":
            return None

        if choice in choices:
            return choices[choice]

        print("Invalid option. Try again.")

def download_playlist(url, quality=None, info=None):
    if info is None:
        info = get_playlist_info(url)

    playlist_title = info.get("title", "Playlist")
    playlist_id = info.get("id", "unknown")

    playlist_dir = DOWNLOAD_DIR / f"{playlist_title}-[{playlist_id}]"
    playlist_dir.mkdir(parents=True, exist_ok=True)

    options = get_ytdlp_options()

    options["progress_hooks"] = [make_playlist_progress_hook()]

    if quality:
        options["format"] = (
            f"bestvideo[height<=?{quality}]+bestaudio/"
            f"best[height<=?{quality}]/best"
        )
    else:
        options["format"] = "bv*+ba/b"

    options["merge_output_format"] = "mp4"
    options["outtmpl"] = str(
        playlist_dir / "%(playlist_index)02d-%(title)s-[%(id)s].%(ext)s"
    )

    start_progress()

    try:
        with yt_dlp.YoutubeDL(options) as ydl:
            ydl.download([url])

        save_download(
            playlist_title,
            url,
            "Playlist - Video + Audio"
        )

    except KeyboardInterrupt:
        raise

    except Exception as e:
        raise RuntimeError(
            f"Could not download playlist: {e}"
        )

    finally:
        stop_progress()
        reset_progress()


def download_playlist_audio(url, quality=None, info=None):
    if info is None:
        info = get_playlist_info(url)

    playlist_title = info.get("title", "Playlist")
    playlist_id = info.get("id", "unknown")

    playlist_dir = DOWNLOAD_DIR / f"{playlist_title}-[{playlist_id}]"
    playlist_dir.mkdir(parents=True, exist_ok=True)

    options = get_ytdlp_options()

    options["progress_hooks"] = [make_playlist_progress_hook()]

    options["format"] = "bestaudio/best"
    options["outtmpl"] = str(
        playlist_dir / "%(playlist_index)02d-%(title)s-[%(id)s].%(ext)s"
    )

    options["postprocessors"] = [
        {
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": quality or "192",
        }
    ]

    start_progress()

    try:
        with yt_dlp.YoutubeDL(options) as ydl:
            ydl.download([url])

        save_download(
            playlist_title,
            url,
            "Playlist - Audio only"
        )

    except KeyboardInterrupt:
        raise

    except Exception as e:
        raise RuntimeError(
            f"Could not download playlist audio: {e}"
        )

    finally:
        stop_progress()
        reset_progress()

        
# if __name__ == "__main__":
#     download_playlist_audio("https://youtube.com/playlist?list=PLDZn36KwauCU&si=n2AGU-ETFR-QZMbZ", "320")
