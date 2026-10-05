import os
import time
from pathlib import Path
from collections import deque
from PIL import Image, ImageDraw
import pystray
from pystray import MenuItem as item
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from plyer import notification

WATCHED_DIR = Path.home() / "Downloads"

EXTENSION_MAP = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp"],
    "Documents": [".pdf", ".docx", ".doc", ".txt", ".xlsx", ".pptx", ".csv"],
    "Installers": [".exe", ".msi", ".dmg", ".pkg", ".iso"],
    "Archives": [".zip", ".rar", ".7z", ".tar", ".gz"],
    "Audio": [".mp3", ".wav", ".flac", ".aac"],
    "Videos": [".mp4", ".mkv", ".avi", ".mov"],
    "Code": [".py", ".pyw", ".js", ".html", ".css", ".json", ".ahk"]
}

recent_files = deque(maxlen=5)
is_paused = False
global_icon = None

def send_notification(file_name, target_folder):
    """Triggers a native Windows toast notification."""
    try:
        notification.notify(
            title="📁 Downloads Organizer",
            message=f"Moved {file_name} ➔ {target_folder}/",
            app_name="Downloads Organizer",
            timeout=3
        )
    except Exception as e:
        print(f"Notification error: {e}")

def create_icon_image(color="blue"):
    """Generates a folder icon image in memory using Pillow."""
    image = Image.new('RGBA', (64, 64), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    fill_color = (0, 120, 215) if color == "blue" else (160, 160, 160)
    
    draw.rectangle([8, 20, 56, 52], fill=fill_color)
    draw.polygon([(8, 20), (24, 20), (30, 12), (8, 12)], fill=fill_color)
    return image

def toggle_pause(icon, item):
    """Pauses or resumes watching the Downloads directory."""
    global is_paused
    is_paused = not is_paused
    icon.icon = create_icon_image("gray" if is_paused else "blue")
    icon.title = "Downloads Organizer (Paused)" if is_paused else "Downloads Organizer (Active)"
    icon.menu = build_menu()
    icon.update_menu()

def open_downloads(icon, item):
    """Opens the user's Downloads folder in File Explorer."""
    os.startfile(WATCHED_DIR)

def exit_app(icon, item):
    """Stops the file observer and closes the tray icon."""
    observer.stop()
    icon.stop()

class DownloadOrganizerHandler(FileSystemEventHandler):
    def process_file(self, file_path: Path):
        global is_paused, global_icon
        if is_paused:
            return

        if file_path.is_dir() or file_path.suffix.lower() in [".crdownload", ".tmp", ".part", ".py", ".pyw", ""]:
            return

        ext = file_path.suffix.lower()
        target_folder_name = "Others"

        for folder, extensions in EXTENSION_MAP.items():
            if ext in extensions:
                target_folder_name = folder
                break

        dest_dir = WATCHED_DIR / target_folder_name
        dest_dir.mkdir(exist_ok=True)

        target_path = dest_dir / file_path.name

        counter = 1
        while target_path.exists():
            target_path = dest_dir / f"{file_path.stem}_{counter}{file_path.suffix}"
            counter += 1

        for _ in range(5):
            try:
                file_path.rename(target_path)
                log_entry = f"{target_path.name} -> {target_folder_name}/"
                recent_files.appendleft(log_entry)
                
                # Send toast notification
                send_notification(target_path.name, target_folder_name)
                
                # Refresh Pystray menu live with the updated recent files
                if global_icon:
                    global_icon.menu = build_menu()
                    global_icon.update_menu()
                break
            except PermissionError:
                time.sleep(0.5)
            except Exception as e:
                recent_files.appendleft(f"Error: {file_path.name}")
                break

    def on_closed(self, event):
        if not event.is_directory:
            self.process_file(Path(event.src_path))

    def on_moved(self, event):
        if not event.is_directory:
            self.process_file(Path(event.dest_path))

def build_menu():
    """Dynamically constructs a fresh menu instance."""
    recent_items = [item(entry, None, enabled=False) for entry in list(recent_files)]
    if not recent_items:
        recent_items = [item("No files moved yet", None, enabled=False)]

    return pystray.Menu(
        item(lambda text: "Resume Monitoring" if is_paused else "Pause Monitoring", toggle_pause),
        item("Open Downloads Folder", open_downloads),
        pystray.Menu.SEPARATOR,
        item("Recent Files", pystray.Menu(*recent_items)),
        pystray.Menu.SEPARATOR,
        item("Exit", exit_app)
    )

def setup_tray():
    global global_icon
    global_icon = pystray.Icon(
        "DownloadsOrganizer",
        create_icon_image("blue"),
        "Downloads Organizer (Active)",
        build_menu()
    )
    global_icon.run()

if __name__ == "__main__":
    event_handler = DownloadOrganizerHandler()
    observer = Observer()
    observer.schedule(event_handler, str(WATCHED_DIR), recursive=False)
    observer.start()

    setup_tray()
    observer.join()