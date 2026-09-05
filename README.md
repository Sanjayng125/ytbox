# YTBox

A friendly, interactive command-line wrapper around [yt-dlp](https://github.com/yt-dlp/yt-dlp) for downloading YouTube videos, playlists, and audio — with live progress bars, quality menus, download history, and automatic dependency management. No manual FFmpeg setup required.

## Features

- Download videos — pick video quality and audio bitrate separately, or grab video/audio only
- Download playlists — best quality or a capped resolution, video or audio-only
- Live progress bars for every stream, powered by Rich
- Video & playlist info — views, likes, duration, available formats, and more, without downloading
- Download history — every download logged locally, browsable and clearable
- Configurable download location, saved between sessions
- One-command updates for yt-dlp, FFmpeg, and Deno
- Zero manual setup — FFmpeg and Deno are detected or auto-downloaded on first run
- Cross-platform — Windows (x64/ARM64), Linux (x64/ARM64), and macOS (Intel/Apple Silicon)

## Installation

### Requirements

- Python 3.10 or newer

### Install with pip

```bash
git clone https://github.com/Sanjayng125/ytbox.git
cd ytbox
pip install .
```

Then run it from anywhere:

```bash
ytbox
```

### Recommended: install with pipx

Keeps YTBox isolated from your other Python projects while still exposing the `ytbox` command globally:

```bash
pipx install .
```

### For development

If you're modifying the code and want changes to take effect immediately:

```bash
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -e .
```

## Usage

Just run:

```bash
ytbox
```

...and follow the interactive menu. On first run, YTBox will automatically detect or download FFmpeg and Deno into a local `bin/` folder — no manual installation needed.

Check for updates to yt-dlp, FFmpeg, and Deno at any time:

```bash
ytbox update
```

## How it works

- Video/audio extraction & downloading is handled by yt-dlp.
- FFmpeg merges separate video/audio streams and converts audio formats.
- Deno is used by yt-dlp to solve YouTube's JS-based playback challenges when needed (optional — skipped automatically on platforms without an official Deno build).
- Dependencies are downloaded into a local `bin/` folder next to the app the first time they're needed, and can be updated later via the in-app Update menu.

## Platform support

| Platform | Architecture          | Status                                                             |
| -------- | --------------------- | ------------------------------------------------------------------ |
| Windows  | x64                   | Fully supported                                                    |
| Windows  | ARM64                 | Supported (FFmpeg only — Deno has no official ARM64 Windows build) |
| Linux    | x64 / ARM64           | Fully supported                                                    |
| macOS    | Intel / Apple Silicon | Supported                                                          |

> Note: On some platforms, certain video resolutions are only available via HLS streaming. These download correctly but won't show a live progress bar (the bar will jump straight to 100% when done) — this is a limitation of how FFmpeg handles HLS downloads internally, not a bug. The quality menu flags these options for you upfront.

## Configuration

Download location and other settings are saved to `config.json` in the project directory and persist between runs. Change it anytime via Settings in the main menu.

## Download history

Every completed download is logged to `history.json`, viewable and clearable from the Download history menu.

## Contributing

Issues and pull requests are welcome. If you run into a bug, please include:

- Your OS and architecture
- The exact steps to reproduce
- Any error output

## License

MIT

## Disclaimer

YTBox is a personal-use tool for downloading content you have the right to download. Respect copyright law and the terms of service of the platforms you use it with.
