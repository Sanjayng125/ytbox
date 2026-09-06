from ytbox.dependencies import get_ffmpeg_path, get_deno_path
from pathlib import Path
import json

BASE_DIR = Path(__file__).resolve().parent
CONFIG_FILE = BASE_DIR / "config.json"
DEFAULT_DOWNLOAD_DIR = BASE_DIR / "downloads"


def load_config():
    if not CONFIG_FILE.exists():
        return {}

    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except (OSError, json.JSONDecodeError):
        return {}


def save_config(config):
    try:
        with open(CONFIG_FILE, "w", encoding="utf-8") as file:
            json.dump(config, file, indent=4)
    except OSError as e:
        raise RuntimeError("Could not save configuration.") from e


def get_saved_download_dir():
    config = load_config()
    path = config.get("download_dir")

    if not path:
        return DEFAULT_DOWNLOAD_DIR

    return Path(path).expanduser()


DOWNLOAD_DIR = get_saved_download_dir()

def init_dirs():
    DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)

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
        
    config = load_config()
    config["download_dir"] = str(new_path)
    save_config(config)

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
