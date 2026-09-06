# YTBox

A friendly, interactive command-line wrapper around [yt-dlp](https://github.com/yt-dlp/yt-dlp) for downloading YouTube videos, playlists, and audio — with live progress bars, quality menus, download history, and automatic dependency management. No manual FFmpeg setup required.

## Features

- **Download videos** — pick video quality and audio bitrate separately, or grab video/audio only
- **Download playlists** — best quality or a capped resolution, video or audio-only
- **Live progress bars** for every stream, powered by [Rich](https://rich.readthedocs.io/)
- **Video & playlist info** — views, likes, duration, available formats, and more, without downloading
- **Download history** — every download logged locally, browsable and clearable
- **Configurable download location**, saved between sessions
- **One-command updates** for yt-dlp, FFmpeg, and Deno
- **Zero manual setup** — FFmpeg and Deno are detected or auto-downloaded on first run
- **Cross-platform** — Windows (x64), Linux (x64/ARM64), and macOS (Intel/Apple Silicon)

## Installation

### Option 1: Standalone executable (recommended for users)

Download the latest release from [GitHub Releases](https://github.com/Sanjayng125/ytbox/releases):

- **Windows**: `ytbox-windows.zip` — extract and run `ytbox.exe`
- **Linux**: `ytbox-linux.zip` — extract, run `chmod +x ytbox`, then `./ytbox`

On first run, YTBox automatically downloads FFmpeg and Deno if needed — no manual setup required.

### Option 2: Install from source with pip

**Requirements**: Python 3.10+

```bash
git clone https://github.com/Sanjayng125/ytbox.git
cd ytbox
pip install .
```

Then run from anywhere:

```bash
ytbox
```

### Option 3: Install with pipx (isolated, recommended for developers)

Keeps YTBox isolated from your other Python projects:

```bash
git clone https://github.com/Sanjayng125/ytbox.git
cd ytbox
pipx install .
```

Then:

```bash
ytbox
```

### Option 4: Development mode

If you're modifying the code:

```bash
git clone https://github.com/Sanjayng125/ytbox.git
cd ytbox
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -e .
ytbox
```

## Usage

Just run:

```bash
ytbox
```

Follow the interactive menu to download videos, playlists, or view information.

Check for updates to yt-dlp, FFmpeg, and Deno:

```bash
ytbox update
```

## How it works

- **yt-dlp** extracts video/audio metadata and downloads streams
- **FFmpeg** merges separate video/audio streams and converts audio formats (MP3, etc.)
- **Deno** (optional) helps yt-dlp bypass YouTube's JS-based playback challenges; auto-skipped on platforms without an official build
- **Dependencies** are downloaded into a local `bin/` folder next to the app on first run, and can be updated anytime via the Update menu

## Platform support

| Platform | Architecture  | Status                           |
| -------- | ------------- | -------------------------------- |
| Windows  | x64           | ✓ Fully supported                |
| Windows  | ARM64         | ⚠ FFmpeg only (Deno unavailable) |
| Linux    | x64           | ✓ Fully supported                |
| Linux    | ARM64         | ✓ Fully supported                |
| macOS    | Intel (x64)   | ✓ Fully supported                |
| macOS    | Apple Silicon | ✓ Fully supported                |

> **Note on HLS streams**: Some video resolutions are only available via HLS streaming. These download correctly but won't show a live progress bar (it jumps to 100% when done) — this is a limitation of how FFmpeg handles HLS internally, not a bug. The quality menu flags these with "no live progress bar" so you know upfront.

## Configuration

Download location and other settings are saved to `data/config.json` and persist between runs. Change them anytime via **Settings** in the main menu.

## Download history

Every completed download is logged to `data/history.json`, viewable and clearable from the **Download history** menu.

## Building standalone executables

If you want to build your own standalones:

```bash
pip install pyinstaller
pyinstaller \
  --onedir \
  --name ytbox \
  --hidden-import yt_dlp.extractor \
  --collect-submodules yt_dlp \
  ytbox/main.py
```

Then grab `bin/` and `data/` from the repo and copy them next to the exe:

```bash
# Windows (PowerShell)
Copy-Item -Recurse bin dist\ytbox\bin
New-Item -ItemType Directory -Force dist\ytbox\data

# Linux/macOS
cp -r bin dist/ytbox/bin
mkdir -p dist/ytbox/data
```

The result in `dist/ytbox/` is your portable distributable.

## Contributing

Issues and pull requests are welcome. If you run into a bug, please include:

- Your OS and architecture
- The exact steps to reproduce
- Any error output

## License

MIT

## Disclaimer

YTBox is a personal-use tool for downloading content you have the right to download. Respect copyright law and the terms of service of the platforms you use it with.
