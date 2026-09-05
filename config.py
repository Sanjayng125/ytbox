from dependencies import get_ffmpeg_path, get_deno_path
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DOWNLOAD_DIR = BASE_DIR / "downloads"

def set_download_dir(path):
    global DOWNLOAD_DIR

    new_path = Path(path).expanduser().resolve()

    if new_path.exists() and not new_path.is_dir():
        raise RuntimeError("The selected path is not a directory.")

    try:
        new_path.mkdir(parents=True, exist_ok=True)
    except OSError as e:
        raise RuntimeError(
            "Could not create or access the selected directory."
        ) from e

    DOWNLOAD_DIR = new_path

def get_ytdlp_options():
    deno_path = get_deno_path()

    options = {
        "quiet": True,
        "no_warnings": True,
        "hls_prefer_native": False,
        "noprogress": True,
        "restrictfilenames": True,
    }

    if deno_path:
        options["js_runtimes"] = {
            "deno": {
                "path": str(deno_path)
            }
        }
        
    ffmpeg_path = get_ffmpeg_path()

    if ffmpeg_path:
        options["ffmpeg_location"] = str(ffmpeg_path)

    return options
