import yt_dlp
from rich.prompt import IntPrompt
from ytbox.config import get_ytdlp_options
from rich.progress import (
    Progress,
    TextColumn,
    BarColumn,
    TaskProgressColumn,
    DownloadColumn,
    TransferSpeedColumn,
    TimeRemainingColumn
)

progress = Progress(
    TextColumn("[bold cyan]{task.description}"),
    BarColumn(),
    TaskProgressColumn(),
    DownloadColumn(),
    TransferSpeedColumn(),
    TimeRemainingColumn(),
)

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

def choose_from_menu(items, prompt, display_fn, error_fn):
    display_fn(items)

    while True:
        choice = IntPrompt.ask(f"[bold cyan]{prompt}[/bold cyan]")

        if 1 <= choice <= len(items):
            return items[choice - 1]

        error_fn("Invalid choice. Try again.")

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

def truncate_title(title, max_length=40):
    if title is None:
        return "Downloading..."

    if len(title) <= max_length:
        return title

    return title[:max_length - 1].rstrip() + "…"

def progress_hook(data, task_map=None):
    if not task_map:
        return

    info = data.get("info_dict", {})
    format_id = info.get("format_id")

    task_id = task_map.get(format_id)

    if task_id is None:
        return

    if data["status"] == "downloading":
        downloaded = data.get("downloaded_bytes", 0)
        total = data.get("total_bytes") or data.get("total_bytes_estimate")

        update_progress(
            task_id,
            downloaded,
            total
        )

    elif data["status"] == "finished":
        downloaded = data.get("downloaded_bytes", 0)
        total = data.get("total_bytes") or downloaded

        update_progress(
            task_id,
            downloaded,
            total
        )

def make_playlist_progress_hook(overall_task_id=None):
    task_map = {}
    finished_videos = set()

    def hook(data):
        info = data.get("info_dict", {})
        video_id  = info.get("id", "unknown")
        format_id = info.get("format_id", "0")
        key = f"{video_id}-{format_id}"

        if key not in task_map:
            title = truncate_title(info.get("title"))
            vcodec = info.get("vcodec")
            acodec = info.get("acodec")

            if vcodec and vcodec != "none":
                stream_label = "Video"
            elif acodec and acodec != "none":
                stream_label = "Audio"
            else:
                stream_label = "Stream"

            total = data.get("total_bytes") or data.get("total_bytes_estimate")
            task_map[key] = add_progress_task(f"{title} | {stream_label}", total=total)

        task_id = task_map[key]

        if data["status"] == "downloading":
            downloaded = data.get("downloaded_bytes", 0)
            total = data.get("total_bytes") or data.get("total_bytes_estimate")
            update_progress(task_id, downloaded, total)

        elif data["status"] == "finished":
            downloaded = data.get("downloaded_bytes", 0)
            total = data.get("total_bytes") or downloaded
            update_progress(task_id, downloaded, total)

            if overall_task_id is not None and video_id not in finished_videos:
                finished_videos.add(video_id)
                progress.advance(overall_task_id, 1)

    return hook

def start_progress():
    progress.start()

def stop_progress():
    progress.stop()

def update_progress(task_id, downloaded, total=None):
    if total:
        progress.update(
            task_id,
            completed=downloaded,
            total=total
        )
    else:
        progress.update(
            task_id,
            completed=downloaded
        )

def add_progress_task(description, total=None):
    task_id = progress.add_task(
        description,
        total=total
    )

    progress.refresh()

    return task_id

def set_progress_total(task_id, total):
    progress.update(
        task_id,
        total=total
    )

def reset_progress():
    for task in progress.tasks:
        progress.remove_task(task.id)

def finish_progress():
    progress.stop()
    for task in progress.tasks:
        progress.remove_task(task.id)
