import yt_dlp
import ytbox.config as config
from ytbox.config import get_ytdlp_options
from ytbox.utils import (
    progress_hook,
    truncate_title,
    start_progress,
    add_progress_task,
    finish_progress,
    choose_from_menu
)
from pathlib import Path
from ytbox.history import save_download
from ytbox.ui import (
    show_audio_menu,
    show_error
)

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
    
    item = choose_from_menu(
        audio_formats,
        prompt="Choose audio: ",
        display_fn=show_audio_menu,
        error_fn=show_error,
    )
    return item["format"]

# ------------------------------------------------ Downloads ------------------------------------------------

def download_audio_only(info, audio_format):
    config.DOWNLOAD_DIR.mkdir(exist_ok=True)

    format_id = audio_format["format_id"]

    options = {
        "format": format_id,
        "outtmpl": str(config.DOWNLOAD_DIR / "%(title)s.%(ext)s"),
        **get_ytdlp_options()
    }
    
    title = truncate_title(info.get("title", "Downloading..."))
    audio_size = audio_format.get("filesize") or audio_format.get("filesize_approx")

    start_progress()

    audio_task_id = add_progress_task(f"{title} | Audio", total=audio_size)

    task_map = {
        format_id: audio_task_id,
    }

    options["progress_hooks"] = [
        lambda data: progress_hook(data, task_map=task_map)
    ]

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
    finally:
        finish_progress()
