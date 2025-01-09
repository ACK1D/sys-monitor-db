import tkinter as tk
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.main import SystemMonitorApp
from src.logger import setup_logger

def main():
    """Application entry point."""
    try:
        root = tk.Tk()
        app = SystemMonitorApp(root)
        root.protocol("WM_DELETE_WINDOW", app.on_close)
        root.mainloop()
    except Exception as e:
        logger = setup_logger()
        logger.error(f"Critical error: {e}")
        raise

if __name__ == "__main__":
    main() 