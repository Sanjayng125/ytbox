import yt_dlp
from config import get_ytdlp_options
import re

def format_duration(seconds):
    if seconds is None:
        return "Unknown"

    minutes, seconds = divmod(int(seconds), 60)
    hours, minutes = divmod(minutes, 60)

    if hours:
        return f"{hours}:{minutes:02}:{seconds:02}"

    return f"{minutes}:{seconds:02}"

def format_number(number):
    if number is None:
        return "Unknown"

    if number >= 1_000_000:
        return f"{number / 1_000_000:.1f}M"

    if number >= 1_000:
        return f"{number / 1_000:.1f}K"

    return str(number)

def format_date(date):
    if not date:
        return "Unknown"

    return f"{date[:4]}-{date[4:6]}-{date[6:]}"

def format_live_status(status):
    if status == "is_live":
        return "Live"

    if status == "was_live":
        return "Ended live stream"

    if status == "not_live":
        return "Not live"

    return "Unknown"

def get_format_summary(info):
    formats = info.get("formats", [])

    video_formats = []
    audio_formats = []

    for format in formats:
        vcodec = format.get("vcodec")
        acodec = format.get("acodec")

        # Video-only formats
        if vcodec != "none" and format.get("height"):
            video_formats.append(format)

        # Audio-only formats with a bitrate
        elif acodec != "none" and vcodec == "none" and format.get("abr"):
            audio_formats.append(format)

    # Keep only one video format per resolution
    best_video = {}

    for format in video_formats:
        height = format["height"]

        if height not in best_video:
            best_video[height] = format
            continue

        current = best_video[height]

        # Prefer H.264 when available
        if format.get("vcodec", "").lower().startswith("avc1"):
            if not current.get("vcodec", "").lower().startswith("avc1"):
                best_video[height] = format

    video_formats = sorted(
        best_video.values(),
        key=lambda format: format["height"]
    )

    # Highest bitrate first for audio
    audio_formats = sorted(
        audio_formats,
        key=lambda format: format["abr"],
        reverse=True
    )

    return video_formats, audio_formats

def get_playlist_duration(info):
    total = 0

    for entry in info.get("entries") or []:
        duration = entry.get("duration")

        if duration is not None:
            total += duration

    return total if total > 0 else None

def get_url_type(url):
    options = get_ytdlp_options()
    options["extract_flat"] = True

    try:
        with yt_dlp.YoutubeDL(options) as ydl:
            info = ydl.extract_info(url, download=False)

        return info.get("_type")

    except Exception as e:
        raise RuntimeError(f"Could not analyze URL: {e}")
    

def progress_hook(data):
    info = data.get("info_dict", {})

    title = info.get("title", "Unknown")
    playlist_index = info.get("playlist_index")
    playlist_count = info.get("n_entries")

    if playlist_index and playlist_count:
        position = f"[{playlist_index}/{playlist_count}] "
    else:
        position = ""

    if len(title) > 40:
        title = title[:37] + "..."

    if info.get("vcodec") != "none":
        stream = "Video"
    elif info.get("acodec") != "none":
        stream = "Audio"
    else:
        stream = "Unknown"

    if data["status"] == "downloading":

        downloaded = data.get("downloaded_bytes", 0)
        total = data.get("total_bytes") or data.get("total_bytes_estimate")

        downloaded_str = f"{downloaded / 1024 / 1024:.1f}MiB"

        if total:
            total_str = f"{total / 1024 / 1024:.1f}MiB"
            size = f"{downloaded_str}/{total_str}"
        else:
            size = f"{downloaded_str}/?"

        print(
            "\r" + " " * 140 + "\r",
            end=""
        )

        print(
            f"{position}"
            f"{title:<40} | "
            f"{stream:<5} | "
            f"{size:>18} | "
            f"{data.get('_percent_str', '?'):>6} | "
            f"{data.get('_speed_str', '?'):>10} | "
            f"ETA {data.get('_eta_str', '?')}",
            end="",
            flush=True
        )

    elif data["status"] == "finished":

        print(
            "\r" + " " * 140 + "\r",
            end=""
        )

        print(
            f"{position}"
            f"{title:<40} | "
            f"{stream:<5} | "
            "100.0% | Finished"
        )

