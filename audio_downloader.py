import yt_dlp
from config import get_ytdlp_options, DOWNLOAD_DIR
from utils import progress_hook
from pathlib import Path
from history import save_download
from ui import show_audio_menu

def get_audio_formats(info):
    formats = []

    for format in info["formats"]:
        if format.get("acodec") == "none":
            continue

        if format.get("vcodec") != "none":
            continue

        if format.get("abr") is None:
            continue

        formats.append({
            "format_id": format.get("format_id"),
            "ext": format.get("ext"),
            "acodec": format.get("acodec"),
            "abr": format.get("abr"),
            "filesize": format.get("filesize")
        })

    # Remove duplicate audio entries
    unique_formats = {}

    for format in formats:
        key = (
            format["ext"],
            format["acodec"],
            round(format["abr"])
        )

        if key not in unique_formats:
            unique_formats[key] = format

    return list(unique_formats.values())


def get_best_audio_format(info):
    formats = get_audio_formats(info)

    if not formats:
        return None

    return max(formats, key=lambda x: x["abr"])

def get_available_audio(info):
    formats = get_audio_formats(info)

    formats.sort(
        key=lambda x: x["abr"],
        reverse=True
    )

    return [
        {
            "quality": format["abr"],
            "format": format
        }
        for format in formats
    ]
    
def choose_audio(audio_formats):
    if not audio_formats:
        raise RuntimeError("No suitable audio formats found.")
    
    show_audio_menu(audio_formats)

    while True:
        choice = input("Choose audio: ")

        if choice.isdigit():
            choice = int(choice)

            if 1 <= choice <= len(audio_formats):
                return audio_formats[choice - 1]["format"]

        print("Invalid choice. Try again.")
        
# ------------------------------------------------ Downloads ------------------------------------------------

def download_audio_only(info, audio_format):
    DOWNLOAD_DIR.mkdir(exist_ok=True)

    format_id = audio_format["format_id"]

    options = {
        "format": format_id,
        "outtmpl": str(DOWNLOAD_DIR / "%(title)s.%(ext)s"),
        **get_ytdlp_options()
    }
    
    options["progress_hooks"] = [progress_hook]

    try:
        with yt_dlp.YoutubeDL(options) as ydl:
            ydl.download([info["webpage_url"]])

            filename = ydl.prepare_filename(info)

        save_download(
            info["title"],
            info["webpage_url"],
            "Audio only"
        )

        return Path(filename)

    except yt_dlp.utils.DownloadError as e:
        raise RuntimeError(
            "Download failed. Check your internet connection or try again."
        ) from e
    except KeyboardInterrupt:
        raise
