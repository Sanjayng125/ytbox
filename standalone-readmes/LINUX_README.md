# YTBox Standalone

## Quick Start

1. Extract this folder anywhere
2. Make the binary executable: `chmod +x ytbox`
3. Run: `./ytbox`
4. Follow the interactive menu

## Folders

- **bin/** — FFmpeg and Deno binaries (auto-downloaded on first run if missing)
- **data/** — your config and download history (auto-created on first run)
- **downloads/** — default location for saved videos (change in Settings menu)
- **\_internal/** — bundled application files required for YTBox to run; do not delete or modify

## First Run

YTBox will automatically download FFmpeg and Deno if needed. This may take a minute or two. You only need to do this once.

## Settings

Change your download location anytime:

1. Run `./ytbox`
2. Select "Settings" from the menu
3. Pick "Download location"

## Update Dependencies

Check for updates to yt-dlp, FFmpeg, and Deno:

1. Run `./ytbox`
2. Select "Update" from the menu

## Make it accessible globally (optional)

Add to your PATH:

```bash
sudo mv . /opt/ytbox
sudo ln -s /opt/ytbox/ytbox /usr/local/bin/ytbox
ytbox  # now works from anywhere
```

Or add to ~/.bashrc:

```bash
export PATH="$HOME/path/to/ytbox:$PATH"
```

## Troubleshooting

**"Permission denied"?**

- Run: `chmod +x ytbox`

**FFmpeg/Deno won't download?**

- Check your internet connection
- Try running `./ytbox` again
- If it still fails, download manually:
  - [FFmpeg](https://github.com/BtbN/FFmpeg-Builds/releases/latest)
  - [Deno](https://github.com/denoland/deno/releases/latest)
- Place `ffmpeg` and `deno` in the `bin/` folder next to the `ytbox` binary

## For more help

Visit: https://github.com/Sanjayng125/ytbox

## License

MIT
EOF
