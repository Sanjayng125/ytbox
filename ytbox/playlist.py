from ytbox.playlist_downloader import (
    get_playlist_info,
    download_playlist,
    download_playlist_audio,
    choose_playlist_quality,
    choose_playlist_audio_quality
)
from ytbox.utils import get_playlist_duration
from ytbox.downloader import cleanup_partial_downloads
from ytbox.ui import (
    show_playlist_information_panel,
    show_playlist_download_info,
    show_playlist_download_options,
    show_playlist_quality_options,
    show_error,
    show_info,
)
from rich.status import Status
from rich.console import Console
from rich.prompt import Prompt, IntPrompt
from rich.panel import Panel
console = Console()

def show_playlist_information():
    url = Prompt.ask("[bold cyan]Enter Playlist URL[/bold cyan]").strip()

    if not url:
        show_info("Please enter a playlist URL.")
        return

    try:
        with Status("[bold yellow]Extracting Playlist Information…[/bold yellow]", console=console):
            info = get_playlist_info(url)

        title = info.get("title", "Unknown")
        channel = info.get("uploader", "Unknown")
        entries = info.get("entries") or []

        total_videos = len(entries)

        total_duration = get_playlist_duration(info)

        show_playlist_information_panel(
            title,
            channel,
            total_videos,
            total_duration,
            entries
        )

    except RuntimeError as e:
        console.print(Panel(f"[bold red]✗ {e}[/bold red]", border_style="red", padding=(0,2), expand=False))

def _video_flow(url, info):
    show_playlist_quality_options("Video")
    quality_choice = IntPrompt.ask("[bold cyan]Choose an option[/bold cyan]")

    if quality_choice == 3:
        return
    elif quality_choice == 1:
        try:
            show_info("Downloading...")
            
            download_playlist(url, info=info)
        except KeyboardInterrupt:
            cleanup_partial_downloads()
            show_info("\nDownload cancelled.")
    elif quality_choice == 2:
        quality = choose_playlist_quality()
        if quality is None:
            return
        try:
            show_info("Downloading...")
            
            download_playlist(url, quality, info)
        except KeyboardInterrupt:
            cleanup_partial_downloads()
            show_info("\nDownload cancelled.")
    else:
        show_error("Invalid option.")


def _audio_flow(url, info):
    show_playlist_quality_options("Audio")
    quality_choice = IntPrompt.ask("[bold cyan]Choose an option[/bold cyan]")

    if quality_choice == 3:
        return
    elif quality_choice == 1:
        try:
            show_info("Downloading...")
            
            download_playlist_audio(url, info=info)
        except KeyboardInterrupt:
            cleanup_partial_downloads()
            show_info("\nDownload cancelled.")
    elif quality_choice == 2:
        quality = choose_playlist_audio_quality()
        if quality is None:
            return
        try:
            show_info("Downloading...")
            
            download_playlist_audio(url, quality, info)
        except KeyboardInterrupt:
            cleanup_partial_downloads()
            show_info("\nDownload cancelled.")
    else:
        show_error("Invalid option.")

def download_playlist_menu():
    url = Prompt.ask("[bold cyan]Enter Playlist URL[/bold cyan]").strip()

    if not url:
        show_info("Please enter a playlist URL.")
        return

    try:
        with Status("[bold yellow]Extracting Playlist Information…[/bold yellow]", console=console):
            info = get_playlist_info(url)

        title = info.get("title", "Unknown")
        entries = info.get("entries") or []

        show_playlist_download_info(title, len(entries))

        show_playlist_download_options()
        choice = IntPrompt.ask("[bold cyan]Choose an option[/bold cyan]")

        if choice == 1:
            _video_flow(url, info)
        elif choice == 2:
            _audio_flow(url, info)
        elif choice == 3:
            return
        else:
            show_error("Invalid option.")

    except RuntimeError as e:
        console.print(Panel(f"[bold red]✗ {e}[/bold red]", border_style="red", padding=(0,2), expand=False))


