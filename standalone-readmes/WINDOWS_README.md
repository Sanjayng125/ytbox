# YTBox Standalone

## Quick Start

1. Extract this folder anywhere
2. Run `ytbox.exe`
3. Follow the interactive menu

## Folders

- **bin/** — FFmpeg and Deno binaries (auto-downloaded on first run if missing)
- **data/** — your config and download history (auto-created on first run)
- **downloads/** — default location for saved videos (change in Settings menu)
- **\_internal/** — bundled application files required for YTBox to run; do not delete or modify

## First Run

YTBox will automatically download FFmpeg and Deno if needed. This may take a minute or two. You only need to do this once.

## Settings

Change your download location anytime:

1. Run `ytbox.exe`
2. Select "Settings" from the menu
3. Pick "Download location"

## Update Dependencies

Check for updates to yt-dlp, FFmpeg, and Deno:

1. Run `ytbox.exe`
2. Select "Update" from the menu

## Troubleshooting

**FFmpeg/Deno won't download?**

- Check your internet connection
- Try running `ytbox.exe` again
- If it still fails, download manually:
  - [FFmpeg](https://github.com/BtbN/FFmpeg-Builds/releases/latest)
  - [Deno](https://github.com/denoland/deno/releases/latest)
- Place `ffmpeg.exe` and `deno.exe` in the `bin/` folder next to `ytbox.exe`

**"ytbox.exe is not recognized"?**

- You need to extract the entire folder first
- Don't just run the exe from the zip file
- Extract to a permanent location (Desktop, Documents, etc.)

## For more help

Visit: https://github.com/Sanjayng125/ytbox

## License

MIT
