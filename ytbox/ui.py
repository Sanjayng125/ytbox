from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from ytbox.utils import format_number, format_duration, format_date, format_live_status

console = Console()

def show_main_menu():
    menu = (
        "[bold cyan]1.[/bold cyan] Download video\n"
        "[bold cyan]2.[/bold cyan] Download playlist\n"
        "[bold cyan]3.[/bold cyan] Video information\n"
        "[bold cyan]4.[/bold cyan] Playlist information\n"
        "[bold cyan]5.[/bold cyan] Settings\n"
        "[bold cyan]6.[/bold cyan] Update\n"
        "[bold cyan]7.[/bold cyan] Download history\n"
        "[bold cyan]8.[/bold cyan] Exit"
    )

    console.print(
        Panel(
            menu,
            title="[bold green]YTBox[/bold green]",
            border_style="cyan",
            padding=(1,2),
            expand=False
        )
    )

def show_title(title):
    console.print()
    console.print(f"[bold cyan]{title}[/bold cyan]")
    console.print()


def show_success(message):
    console.print(f"[bold green]✓ {message}[/bold green]")


def show_error(message):
    console.print(f"[bold red]✗ {message}[/bold red]")


def show_info(message):
    console.print(f"[bold yellow]• {message}[/bold yellow]")
    
def show_download_mode_menu():
    menu = (
        "[bold cyan]1.[/bold cyan] Video + Audio\n"
        "[bold cyan]2.[/bold cyan] Video only\n"
        "[bold cyan]3.[/bold cyan] Audio only"
    )

    console.print(
        Panel(
            menu,
            title="[bold green]Download Mode[/bold green]",
            border_style="cyan",
            padding=(1,2),
            expand=False
        )
    )

def show_quality_menu(qualities):
    table = Table(
        title="Available Qualities",
        border_style="cyan"
    )

    table.add_column("Option", style="cyan")
    table.add_column("Quality", style="green")
    table.add_column("Format")
    table.add_column("Resolution")
    table.add_column("FPS")
    table.add_column("Progress")

    for index, item in enumerate(qualities, start=1):
        format_info = item["format"]

        progress_note = (
            "[yellow]no live progress bar[/yellow]"
            if format_info.get("is_hls")
            else "[green]✓[/green]"
        )

        table.add_row(
            str(index),
            f"{item['quality']}p",
            format_info["ext"].upper(),
            f"{format_info['width']}x{format_info['height']}",
            f"{format_info['fps']}fps",
            progress_note
        )

    console.print(table)

def show_audio_menu(audio_formats):
    table = Table(
        title="Available Audio",
        border_style="cyan"
    )

    table.add_column("Option", style="cyan")
    table.add_column("Bitrate", style="green")
    table.add_column("Format")
    table.add_column("Codec")

    for index, item in enumerate(audio_formats, start=1):
        format_info = item["format"]

        table.add_row(
            str(index),
            f"{item['quality']:.0f} kbps",
            format_info["ext"].upper(),
            format_info["acodec"]
        )

    console.print(table)

def show_playlist_quality_menu():
    table = Table(
        title="Select Video Quality",
        border_style="cyan"
    )

    table.add_column("Option", style="cyan")
    table.add_column("Resolution", style="green")

    qualities = [
        ("1", "144p"),
        ("2", "240p"),
        ("3", "360p"),
        ("4", "480p"),
        ("5", "720p"),
        ("6", "1080p"),
        ("7", "1440p (2K)"),
        ("8", "2160p (4K)"),
        ("9", "Cancel"),
    ]

    for option, quality in qualities:
        table.add_row(option, quality)

    console.print(
        "[dim]YTBox will select the best available quality up to your chosen resolution.[/dim]"
    )
    console.print(table)


def show_playlist_audio_quality_menu():
    table = Table(
        title="Select Audio Quality",
        border_style="cyan"
    )

    table.add_column("Option", style="cyan")
    table.add_column("Bitrate", style="green")

    qualities = [
        ("1", "320 kbps"),
        ("2", "256 kbps"),
        ("3", "192 kbps"),
        ("4", "128 kbps"),
        ("5", "96 kbps"),
        ("6", "Cancel"),
    ]

    for option, quality in qualities:
        table.add_row(option, quality)

    console.print(table)

def show_video_information_panel(info, video_formats, audio_formats):
    table = Table(
        title="Video Information",
        border_style="cyan",
        show_header=False
    )

    table.add_column("Property", style="cyan")
    table.add_column("Value", style="white")

    table.add_row("Title", info.get("title") or "Unknown")
    table.add_row("Channel", info.get("channel") or "Unknown")
    table.add_row(
        "Subscribers",
        format_number(info.get("channel_follower_count"))
    )
    table.add_row("Duration", format_duration(info.get("duration")))
    table.add_row("Views", format_number(info.get("view_count")))
    table.add_row("Likes", format_number(info.get("like_count")))
    table.add_row("Comments", format_number(info.get("comment_count")))
    table.add_row("Uploaded", format_date(info.get("upload_date")))
    table.add_row(
        "Category",
        ", ".join(info.get("categories") or []) or "Unknown"
    )
    table.add_row("Language", info.get("language") or "Unknown")
    table.add_row("Age limit", str(info.get("age_limit") or "None"))
    table.add_row(
        "Live status",
        format_live_status(info.get("live_status"))
    )
    table.add_row(
        "Thumbnail",
        "Available" if info.get("thumbnail") else "None"
    )
    table.add_row(
        "Tags",
        ", ".join(info.get("tags") or []) or "None"
    )
    table.add_row(
        "Description",
        "Available" if info.get("description") else "None"
    )
    table.add_row(
        "Available video",
        ", ".join(
            f"{format_info['height']}p"
            for format_info in video_formats
        ) or "None"
    )
    table.add_row(
        "Available audio",
        ", ".join(
            f"{format_info['abr']:.0f} kbps"
            for format_info in audio_formats
        ) or "None"
    )

    console.print(table)

def show_playlist_information_panel(title, channel, total_videos, total_duration, entries):
    table = Table(
        title="Playlist Information",
        border_style="cyan",
        show_header=False
    )

    table.add_column("Property", style="cyan")
    table.add_column("Value", style="white")

    table.add_row("Title", title)
    table.add_row("Channel", channel)
    table.add_row("Videos", str(total_videos))

    if total_duration:
        table.add_row("Duration", format_duration(total_duration))
    else:
        table.add_row("Duration", "Unknown")

    console.print(table)

    videos_table = Table(
        title="Videos",
        border_style="cyan"
    )

    videos_table.add_column("#", style="cyan", width=4)
    videos_table.add_column("Title", style="green")
    videos_table.add_column("URL")

    for index, entry in enumerate(entries, start=1):
        videos_table.add_row(
            str(index),
            entry.get("title", "Unknown"),
            entry.get("url", "Unknown")
        )

    console.print(videos_table)

def show_settings_menu():
    menu = (
        "[bold cyan]1.[/bold cyan] Download location\n"
        "[bold cyan]2.[/bold cyan] Back"
    )

    console.print(
        Panel(
            menu,
            title="[bold green]Settings[/bold green]",
            border_style="cyan",
            padding=(1,2),
            expand=False
        )
    )


def show_download_location(path):
    console.print(
        Panel(
            str(path),
            title="[bold green]Current Download Location[/bold green]",
            border_style="cyan",
            padding=(1,2),
            expand=False
        )
    )

def show_playlist_download_info(title, video_count):
    table = Table(
        title="Playlist",
        border_style="cyan",
        show_header=False
    )

    table.add_column("Property", style="cyan")
    table.add_column("Value", style="white")

    table.add_row("Title", title)
    table.add_row("Videos", str(video_count))

    console.print(table)


def show_playlist_download_options():
    table = Table(
        title="Download Options",
        border_style="cyan"
    )

    table.add_column("Option", style="cyan")
    table.add_column("Mode", style="green")

    table.add_row("1", "Video + Audio")
    table.add_row("2", "Audio only")
    table.add_row("3", "Cancel")

    console.print(table)


def show_playlist_quality_options(mode):
    table = Table(
        title=f"{mode} Quality",
        border_style="cyan"
    )

    table.add_column("Option", style="cyan")
    table.add_column("Choice", style="green")

    table.add_row("1", "Best quality")
    table.add_row("2", "Select quality")
    table.add_row("3", "Cancel")

    console.print(table)

def show_history_table(history):
    if not history:
        console.print(
            Panel(
                "No download history.",
                title="[bold green]Download History[/bold green]",
                border_style="cyan",
                padding=(0,2),
                expand=False
            )
        )
        return

    table = Table(
        title="Download History",
        border_style="cyan",
        show_lines=True,
        row_styles=["", "dim"],
    )
    
    table.add_column("#", style="cyan", width=4, justify="right")
    table.add_column("Title", style="green")
    table.add_column("Type")
    table.add_column("Downloaded")
    table.add_column("URL")

    for index, entry in enumerate(history, start=1):
        table.add_row(
            str(index),
            entry.get("title", "Unknown"),
            entry.get("type", "Unknown"),
            entry.get("downloaded_at", "Unknown"),
            entry.get("url", "Unknown")
        )

    console.print(table)


def show_history_menu():
    table = Table(
        title="History Options",
        border_style="cyan"
    )

    table.add_column("Option", style="cyan")
    table.add_column("Action", style="green")

    table.add_row("1", "Clear history")
    table.add_row("2", "Back")

    console.print(table)

def show_update_status_table(results):
    table = Table(title="Dependency Status", border_style="cyan")
    table.add_column("Dependency", style="cyan")
    table.add_column("Installed",  style="white")
    table.add_column("Latest",     style="white")
    table.add_column("Status",     style="white")

    for dep in results:
        installed = dep["installed"] or "[dim]unknown[/dim]"
        latest    = dep["latest_display"] or "[dim]unknown[/dim]"

        if dep["needs_update"] is None:
            status = "[dim]could not check[/dim]"
        elif dep["needs_update"]:
            status = "[bold yellow]update available[/bold yellow]"
        else:
            status = "[bold green]up to date ✓[/bold green]"

        table.add_row(dep["name"], installed, latest, status)

    console.print(table)
