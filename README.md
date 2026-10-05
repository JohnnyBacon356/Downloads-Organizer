#Downloads Organizer 
Downloads Organizer is a  lightweight, automated Windows background service that automatically monitors your Downloads directory and organizes incoming files into designated subfolders by file type. It runs discreetly in the system tray with desktop notifications, pause/resume controls, and auto-run on Windows startup.

Features:

Automated File Categorization: Instantly moves downloaded files into sub-directories (`Images`, `Documents`, `Installers`, `Archives`, `Audio`, `Videos`, `Code`, ect) based on extension.
System Tray Control: Easily pause/resume file monitoring or exit the application via the system tray icon.
Desktop Toast Notifications: Displays Windows toast notifications whenever a file is organized.
Recent Files History: View up to 5 recently organized files directly from the system tray menu.
Conflict Resolution: Automatically handles file naming collisions by appending incremental numbers (e.g., `file_1.png`).
Download Safety: Ignores partial or temporary download files (e.g., `.crdownload`, `.tmp`, `.part`) until downloads complete.
Startup Integration: Script/batch utility to easily add the organizer to the Windows Startup folder.

Requirements

Operating System: Windows 10 or later
Python:** Python 3.8+ (must be added to system `PATH`).

Installation

1. Clone or Download this repository to your preferred directory.
2. Automated Setup (Recommended):**
   - Double-click setup.bat.
   - This script will install required dependencies from requirements.txt and create a shortcut in your Windows Startup folder so it runs every time you log in.

3. Manual Setup:
   If you prefer to install dependencies manually, run:
   pip install -r requirements.txt
