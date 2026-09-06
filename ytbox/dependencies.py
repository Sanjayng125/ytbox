from pathlib import Path
import shutil
import urllib.request
import urllib.error
import zipfile
import tarfile
import platform
import subprocess
import sys
import stat
from packaging.version import Version
import json

def _default_info(msg):
    print(f"• {msg}")

def _default_success(msg):
    print(f"✓ {msg}")

def _default_error(msg):
    import sys
    print(f"✗ {msg}", file=sys.stderr)

_log_info    = _default_info
_log_success = _default_success
_log_error   = _default_error

def set_logger(info_fn, success_fn, error_fn):
    global _log_info, _log_success, _log_error
    _log_info    = info_fn
    _log_success = success_fn
    _log_error   = error_fn

SYSTEM = platform.system()
ARCH = platform.machine()

def _get_base_dir():
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent
    return Path(__file__).resolve().parent.parent

BASE_DIR = _get_base_dir()
BIN_DIR = BASE_DIR / "bin"

if SYSTEM == "Windows":

    if ARCH == "AMD64":
        FFMPEG_URL = (
            "https://github.com/BtbN/FFmpeg-Builds/releases/latest/download/"
            "ffmpeg-master-latest-win64-gpl.zip"
        )

        DENO_URL = (
            "https://github.com/denoland/deno/releases/latest/download/"
            "deno-x86_64-pc-windows-msvc.zip"
        )

    elif ARCH == "ARM64":
        raise RuntimeError("Windows ARM64 support is not implemented yet.")

    else:
        raise RuntimeError(f"Unsupported Windows architecture: {ARCH}")

    FFMPEG_PATH = BIN_DIR / "ffmpeg.exe"
    DENO_PATH = BIN_DIR / "deno.exe"
    FFMPEG_ARCHIVE_FORMAT = "zip"

elif SYSTEM == "Linux":

    if ARCH in ("x86_64", "AMD64"):
        FFMPEG_URL = (
            "https://github.com/BtbN/FFmpeg-Builds/releases/latest/download/"
            "ffmpeg-master-latest-linux64-gpl.tar.xz"
        )

        DENO_URL = (
            "https://github.com/denoland/deno/releases/latest/download/"
            "deno-x86_64-unknown-linux-gnu.zip"
        )

    elif ARCH in ("aarch64", "arm64", "ARM64"):
        FFMPEG_URL = (
            "https://github.com/BtbN/FFmpeg-Builds/releases/latest/download/"
            "ffmpeg-master-latest-linuxarm64-gpl.tar.xz"
        )

        DENO_URL = (
            "https://github.com/denoland/deno/releases/latest/download/"
            "deno-aarch64-unknown-linux-gnu.zip"
        )

    else:
        raise RuntimeError(f"Unsupported Linux architecture: {ARCH}")

    FFMPEG_PATH = BIN_DIR / "ffmpeg"
    DENO_PATH = BIN_DIR / "deno"
    FFMPEG_ARCHIVE_FORMAT = "tar.xz"

elif SYSTEM == "Darwin":
    raise RuntimeError("macOS support is not implemented yet.")

else:
    raise RuntimeError(f"Unsupported operating system: {SYSTEM}")


def _make_executable(path):
    if SYSTEM == "Windows":
        return

    current_mode = path.stat().st_mode
    path.chmod(current_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)


def _extract_ffmpeg_binary(archive_path, destination_path):
    if FFMPEG_ARCHIVE_FORMAT == "zip":
        with zipfile.ZipFile(archive_path, "r") as archive:
            for file in archive.namelist():
                if file.endswith("/bin/ffmpeg.exe") or file.endswith("/bin/ffmpeg"):
                    with archive.open(file) as source:
                        with open(destination_path, "wb") as target:
                            target.write(source.read())
                    break

    elif FFMPEG_ARCHIVE_FORMAT == "tar.xz":
        with tarfile.open(archive_path, "r:xz") as archive:
            for member in archive.getmembers():
                if member.name.endswith("/bin/ffmpeg"):
                    source = archive.extractfile(member)

                    if source is None:
                        continue

                    with open(destination_path, "wb") as target:
                        target.write(source.read())
                    break

    else:
        raise RuntimeError(f"Unsupported FFmpeg archive format: {FFMPEG_ARCHIVE_FORMAT}")

    _make_executable(destination_path)


def check_dependencies():
    ffmpeg = get_ffmpeg_path()
    deno = get_deno_path()

    return {
        "ffmpeg": ffmpeg,
        "deno": deno
    }

def ensure_dependencies():
    dependencies = check_dependencies()

    installers = {
        "ffmpeg": install_ffmpeg,
        "deno": install_deno
    }

    try:
        for name, path in dependencies.items():
            if path is None:
                _log_error(f"{name.upper()} not found.")
                dependencies[name] = installers[name]()

    except KeyboardInterrupt:
        for file in (BIN_DIR / f"ffmpeg.{FFMPEG_ARCHIVE_FORMAT}", BIN_DIR / "deno.zip"):
            if file.exists():
                try:
                    file.unlink()
                except OSError:
                    pass

        _log_info("\nDependency installation cancelled.")
        raise SystemExit

    except (urllib.error.URLError, OSError, zipfile.BadZipFile, tarfile.TarError) as e:
        for file in (BIN_DIR / f"ffmpeg.{FFMPEG_ARCHIVE_FORMAT}", BIN_DIR / "deno.zip"):
            if file.exists():
                try:
                    file.unlink()
                except OSError:
                    pass

        print()
        _log_error(f"Dependency installation failed: {e}")
        raise SystemExit

    return dependencies

def get_ffmpeg_path():
    if FFMPEG_PATH.exists():
        return FFMPEG_PATH

    system_ffmpeg = shutil.which("ffmpeg")

    if system_ffmpeg:
        return Path(system_ffmpeg)

    return None


def install_ffmpeg():
    BIN_DIR.mkdir(exist_ok=True)

    archive_path = BIN_DIR / f"ffmpeg.{FFMPEG_ARCHIVE_FORMAT}"

    _log_info("Downloading FFmpeg...")

    urllib.request.urlretrieve(FFMPEG_URL, archive_path)

    _log_info("Extracting FFmpeg...")

    _extract_ffmpeg_binary(archive_path, FFMPEG_PATH)

    archive_path.unlink()

    if not FFMPEG_PATH.exists():
        raise RuntimeError("Could not find the ffmpeg binary in the downloaded archive.")

    _log_success("FFmpeg installed successfully.")

    return FFMPEG_PATH

def get_deno_path():
    if DENO_PATH.exists():
        return DENO_PATH

    system_deno = shutil.which("deno")

    if system_deno:
        return Path(system_deno)

    return None

def install_deno():
    BIN_DIR.mkdir(exist_ok=True)

    zip_path = BIN_DIR / "deno.zip"

    _log_info("Downloading Deno...")

    urllib.request.urlretrieve(DENO_URL, zip_path)

    _log_info("Extracting Deno...")

    with zipfile.ZipFile(zip_path, "r") as archive:
        with archive.open(DENO_PATH.name) as source:
            with open(DENO_PATH, "wb") as target:
                target.write(source.read())

    zip_path.unlink()

    _make_executable(DENO_PATH)

    if not DENO_PATH.exists():
        raise RuntimeError("Could not find the deno binary in the downloaded archive.")

    _log_success("Deno installed successfully.")

    return DENO_PATH

# ------------------------------------------------- Update -------------------------------------------------

# ------------------------------------------------- yt-dlp -------------------------------------------------

def get_ytdlp_version():
    try:
        result = subprocess.run(
            [sys.executable, "-m", "yt_dlp", "--version"],
            capture_output=True,
            text=True
        )

        return result.stdout.strip()
    except (subprocess.SubprocessError, OSError):
        _log_error("yt-dlp version fetch failed!.")
        return None

def get_latest_ytdlp_version():
    result = subprocess.run(
        [sys.executable, "-m", "pip", "index", "versions", "yt-dlp"],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        return None

    for line in result.stdout.splitlines():
        if line.startswith("Available versions:"):
            versions = line.split(":", 1)[1].strip()
            return versions.split(",")[0].strip()

    return None

def is_ytdlp_update_available(installed=None, latest=None):
    if installed is None:
        installed = get_ytdlp_version()

    if latest is None:
        latest = get_latest_ytdlp_version()

    if not installed or not latest:
        return None

    return Version(latest) > Version(installed)

def update_ytdlp():
    result = subprocess.run(
        [sys.executable, "-m", "pip", "install", "--upgrade", "yt-dlp"],
        text=True
    )

    return result.returncode == 0

# ------------------------------------------------- ffmpeg -------------------------------------------------

def get_ffmpeg_version():
    ffmpeg_path = get_ffmpeg_path()

    if ffmpeg_path is None:
        return None

    result = subprocess.run(
        [str(ffmpeg_path), "-version"],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        return None

    first_line = result.stdout.splitlines()[0]

    return first_line.split()[2]

def get_latest_ffmpeg_version():
    url = "https://api.github.com/repos/BtbN/FFmpeg-Builds/releases/latest"

    try:
        with urllib.request.urlopen(url) as response:
            data = json.load(response)

        name = data.get("name", "")

        if "Latest Auto-Build (" not in name:
            return None

        return name.split("(")[1].split(")")[0]

    except (urllib.error.URLError, json.JSONDecodeError):
        return None
    

def get_ffmpeg_build_date():
    version = get_ffmpeg_version()

    if version is None:
        return None

    return version[-8:]

def is_ffmpeg_update_available(installed=None, latest=None):
    if installed is None:
        installed = get_ffmpeg_build_date()

    if latest is None:
        latest = get_latest_ffmpeg_version()

    if not installed or not latest:
        return None

    latest_date = latest[:10].replace("-", "")

    return latest_date > installed

def update_ffmpeg():
    BIN_DIR.mkdir(exist_ok=True)

    archive_path = BIN_DIR / f"ffmpeg.{FFMPEG_ARCHIVE_FORMAT}"

    try:
        _log_info("Downloading FFmpeg...")

        urllib.request.urlretrieve(FFMPEG_URL, archive_path)

        _log_info("Extracting FFmpeg...")

        _extract_ffmpeg_binary(archive_path, FFMPEG_PATH)

        if not FFMPEG_PATH.exists():
            return False

        return True

    finally:
        if archive_path.exists():
            archive_path.unlink()


# ------------------------------------------------- deno -------------------------------------------------            

def get_deno_version():
    deno_path = get_deno_path()

    if deno_path is None:
        return None

    result = subprocess.run(
        [str(deno_path), "--version"],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        return None

    for line in result.stdout.splitlines():
        if line.startswith("deno "):
            return line.split()[1]

    return None

def get_latest_deno_version():
    url = "https://api.github.com/repos/denoland/deno/releases/latest"

    try:
        with urllib.request.urlopen(url) as response:
            data = json.load(response)

        return data.get("tag_name")

    except (urllib.error.URLError, json.JSONDecodeError):
        return None
    
def is_deno_update_available(installed=None, latest=None):
    if installed is None:
        installed = get_deno_version()

    if latest is None:
        latest = get_latest_deno_version()

    if not installed or not latest:
        return None

    latest = latest.lstrip("v")

    return Version(latest) > Version(installed)

def update_deno():
    BIN_DIR.mkdir(exist_ok=True)

    zip_path = BIN_DIR / "deno.zip"

    try:
        _log_info("Downloading Deno...")

        urllib.request.urlretrieve(DENO_URL, zip_path)

        _log_info("Extracting Deno...")

        with zipfile.ZipFile(zip_path, "r") as archive:
            with archive.open(DENO_PATH.name) as source:
                with open(DENO_PATH, "wb") as target:
                    target.write(source.read())

        _make_executable(DENO_PATH)

        return DENO_PATH.exists()

    finally:
        if zip_path.exists():
            zip_path.unlink()

