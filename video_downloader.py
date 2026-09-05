import yt_dlp
import config
from config import get_ytdlp_options
from dependencies import get_ffmpeg_path
from utils import (
    truncate_title,
    progress_hook,
    start_progress,
    stop_progress,
    reset_progress,
    add_progress_task
)
from pathlib import Path
from history import save_download
from ui import (
    show_quality_menu,
    show_info,
    show_error
)

def get_video_info(url):
    options = {
        **get_ytdlp_options()
    }

    try:
        with yt_dlp.YoutubeDL(options) as ydl:
            info = ydl.extract_info(url, download=False)

        if not info.get("formats"):
            raise RuntimeError("The URL does not point to a downloadable video.")

        return info

    except yt_dlp.utils.DownloadError as e:
        raise RuntimeError("Could not retrieve this video.") from e


def get_video_qualities(info):
    qualities = []

    for format in info["formats"]:
        if format.get("vcodec") == "none":
            continue

        height = format.get("height")

        if height is None:
            continue

        is_hls = "m3u8" in (format.get("protocol") or "")

        qualities.append({
            "format_id": format.get("format_id"),
            "height": height,
            "width": format.get("width"),
            "ext": format.get("ext"),
            "fps": format.get("fps"),
            "vcodec": format.get("vcodec"),
            "filesize": format.get("filesize"),
            "filesize_approx": format.get("filesize_approx"),
            "is_hls": is_hls,
        })

    return qualities


def get_best_video_formats(info):
    formats = get_video_qualities(info)

    codec_priority = {
        "avc1": 3,
        "av01": 2,
        "vp09": 1,
        "vp9": 1
    }

    best_formats = {}

    for format in formats:
        height = format["height"]

        codec = format["vcodec"].lower()

        if codec.startswith("avc1"):
            priority = codec_priority["avc1"]
        elif codec.startswith("av01"):
            priority = codec_priority["av01"]
        elif codec.startswith("vp09") or codec.startswith("vp9"):
            priority = codec_priority["vp09"]
        else:
            priority = 0

        bitrate = format.get("vbr") or 0

        score = (priority, bitrate)

        if height not in best_formats:
            best_formats[height] = (score, format)
            continue

        current_score, _ = best_formats[height]

        if score > current_score:
            best_formats[height] = (score, format)

    return sorted(
        [item[1] for item in best_formats.values()],
        key=lambda x: x["height"]
    )


def get_video_format(info, quality):
    formats = get_best_video_formats(info)

    if not formats:
        return None

    selected = None

    for format in formats:
        if format["height"] <= quality:
            selected = format

    if selected is None:
        selected = formats[0]

    return selected

def get_available_qualities(info):
    formats = get_best_video_formats(info)

    return [
        {
            "quality": format["height"],
            "format": format,
        }
        for format in formats
    ]


def choose_quality(qualities):
    if not qualities:
        raise RuntimeError("No suitable video formats found.")

    show_quality_menu(qualities)

    while True:
        choice = input("Choose quality: ")

        if choice.isdigit():
            choice = int(choice)

            if 1 <= choice <= len(qualities):
                return qualities[choice - 1]["format"]

        show_error("Invalid choice. Try again.")
        
# ------------------------------------------------ Downloads ------------------------------------------------

def download_video(info, video_format, audio_format):
    ffmpeg_path = get_ffmpeg_path()

    if ffmpeg_path is None:
        raise RuntimeError(
            "FFmpeg is required to merge video and audio, but it was not found."
        )

    config.DOWNLOAD_DIR.mkdir(exist_ok=True)

    video_id = video_format["format_id"]
    audio_id = audio_format["format_id"]

    options = {
        "format": f"{video_id}+{audio_id}",
        "outtmpl": str(config.DOWNLOAD_DIR / "%(title)s.%(ext)s"),
        "merge_output_format": "mp4",
        **get_ytdlp_options()
    }

    title = truncate_title(info.get("title", "Downloading..."))

    video_size = video_format.get("filesize") or video_format.get("filesize_approx")
    audio_size = audio_format.get("filesize") or audio_format.get("filesize_approx")

    start_progress()

    video_task_id = add_progress_task(f"{title} | Video", total=video_size)
    audio_task_id = add_progress_task(f"{title} | Audio", total=audio_size)

    task_map = {
        video_id: video_task_id,
        audio_id: audio_task_id,
    }

    options["progress_hooks"] = [
        lambda data: progress_hook(data, task_map=task_map)
    ]

    try:
        with yt_dlp.YoutubeDL(options) as ydl:
            show_info("Selected format:", options["format"])

            try:
                ydl.download([info["webpage_url"]])
            finally:
                stop_progress()
                reset_progress()

            filename = ydl.prepare_filename(info)

        save_download(
            info["title"],
            info["webpage_url"],
            "Video + Audio"
        )

        return Path(filename).with_suffix(".mp4")

    except yt_dlp.utils.DownloadError as e:
        stop_progress()
        reset_progress()
        raise RuntimeError(
            "Download failed. Check your internet connection or try again."
        ) from e
    except KeyboardInterrupt:
        stop_progress()
        reset_progress()
        raise


def download_video_only(info, video_format):
    config.DOWNLOAD_DIR.mkdir(exist_ok=True)

    format_id = video_format["format_id"]

    options = {
        "format": format_id,
        "outtmpl": str(config.DOWNLOAD_DIR / "%(title)s.%(ext)s"),
        **get_ytdlp_options()
    }

    title = truncate_title(info.get("title", "Downloading..."))
    video_size = video_format.get("filesize") or video_format.get("filesize_approx")

    start_progress()

    video_task_id = add_progress_task(f"{title} | Video", total=video_size)

    task_map = {
        format_id: video_task_id,
    }

    options["progress_hooks"] = [
        lambda data: progress_hook(data, task_map=task_map)
    ]

    try:
        with yt_dlp.YoutubeDL(options) as ydl:
            try:
                ydl.download([info["webpage_url"]])
            finally:
                stop_progress()
                reset_progress()

            filename = ydl.prepare_filename(info)

        save_download(
            info["title"],
            info["webpage_url"],
            "Video only"
        )

        return Path(filename).with_suffix(".mp4")

    except yt_dlp.utils.DownloadError as e:
        stop_progress()
        reset_progress()
        raise RuntimeError(
            "Download failed. Check your internet connection or try again."
        ) from e
    except KeyboardInterrupt:
        stop_progress()
        reset_progress()
        raise