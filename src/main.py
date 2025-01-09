import time
import psutil
import tkinter as tk
import customtkinter as ctk
from .logger import setup_logger
from .config import Config
from .database import Database
from .translations import TRANSLATIONS

class SystemMonitorApp:
    """
    Main application class for system resource monitoring.
    Provides GUI interface and database recording functionality.
    """
    
    def __init__(self, root):
        self.logger = setup_logger()
        self.config = Config()
        self.current_lang = 'ru'
        
        self.db = Database(self.config.DB_PATH)
        self.db.connect()
        
        self.root = root
        self.setup_window()
        self.setup_ui()
        self.update_data()
        
    def setup_window(self):
        """Configure main application window."""
        self.logger.info("Initializing main window")
        self.root.title("System Monitor")
        self.root.geometry("400x300")
        self.root.configure(bg=self.config.BG_COLOR)
        
        self.main_frame = ctk.CTkFrame(
            self.root,
            corner_radius=20,
            fg_color=self.config.BG_COLOR,
            border_color=self.config.TEXT_COLOR,
            border_width=1
        )
        self.main_frame.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.8)
        
    def setup_ui(self):
        """Configure UI elements."""
        self.logger.info("Setting up UI elements")
        
        self.title_label = tk.Label(
            self.main_frame,
            text=TRANSLATIONS[self.current_lang]['title'],
            font=self.config.FONT_STYLE,
            fg=self.config.TEXT_COLOR,
            bg=self.config.BG_COLOR,
        )
        self.title_label.pack(pady=10, anchor='w', padx=20)

        for label_name in ['cpu', 'ram', 'disk']:
            setattr(self, f"{label_name}_label", tk.Label(
                self.main_frame,
                text=f"{TRANSLATIONS[self.current_lang][label_name]}: --%",
                font=self.config.FONT_STYLE,
                fg=self.config.TEXT_COLOR,
                bg=self.config.BG_COLOR,
            ))
            getattr(self, f"{label_name}_label").pack(pady=0, anchor='w', padx=20)

        self.record_button = ctk.CTkButton(
            self.main_frame,
            text=TRANSLATIONS[self.current_lang]['start_recording'],
            command=self.toggle_recording,
            font=self.config.FONT_STYLE,
            fg_color=self.config.BG_COLOR,
            bg_color=self.config.BG_COLOR,
            border_color=self.config.TEXT_COLOR,
            border_width=2,
            corner_radius=10,
            hover_color=self.config.HOVER_COLOR,
            text_color=self.config.TEXT_COLOR,
            height=40,
        )
        self.record_button.pack(pady=(50, 0))

        self.timer_label = tk.Label(
            self.main_frame,
            font=self.config.FONT_STYLE,
            fg=self.config.TEXT_COLOR,
            bg=self.config.BG_COLOR,
        )
        self.timer_label.pack(pady=5)

        self.lang_button = ctk.CTkButton(
            self.main_frame,
            text=TRANSLATIONS[self.current_lang]['switch_lang'],
            command=self.toggle_language,
            font=self.config.FONT_STYLE,
            fg_color=self.config.BG_COLOR,
            bg_color=self.config.BG_COLOR,
            border_color=self.config.TEXT_COLOR,
            border_width=2,
            corner_radius=10,
            hover_color=self.config.HOVER_COLOR,
            text_color=self.config.TEXT_COLOR,
            width=40,
            height=30,
        )
        self.lang_button.place(relx=0.85, rely=0.05)

        self.recording = False
        self.start_time = None

    def update_data(self):
        """Update system information in the interface."""
        try:
            cpu = psutil.cpu_percent(interval=None)
            ram = psutil.virtual_memory()
            disk = psutil.disk_usage('/')

            texts = TRANSLATIONS[self.current_lang]
            self._update_system_labels(cpu, ram, disk, texts)

            if self.recording:
                self.db.save_data(cpu, ram.percent, disk.percent)

            self.root.after(self.config.UPDATE_INTERVAL, self.update_data)
        except Exception as e:
            self.logger.error(f"Error updating data: {e}")
            raise

    def _update_system_labels(self, cpu, ram, disk, texts):
        """Update system information labels."""
        self.cpu_label.config(text=f"{texts['cpu']}: {cpu}%")
        
        ram_free = ram.available // (1024 * 1024)
        ram_total = ram.total // (1024 * 1024)
        self.ram_label.config(text=f"{texts['ram']}: {ram_free}{texts['mb']}/{ram_total}{texts['mb']}")
        
        disk_free = disk.free // (1024 * 1024 * 1024)
        disk_total = disk.total // (1024 * 1024 * 1024)
        self.disk_label.config(text=f"{texts['disk']}: {disk_free}{texts['gb']}/{disk_total}{texts['gb']}")
        
    def toggle_recording(self):
        """Toggle database recording state."""
        if self.recording:
            self.stop_recording()
        else:
            self.start_recording()

    def start_recording(self):
        """Start recording system data to database."""
        try:
            self.logger.info("Starting data recording")
            self.recording = True
            self.start_time = time.time()
            self.record_button.configure(
                text=TRANSLATIONS[self.current_lang]['stop_recording']
            )
            self.update_timer()
        except Exception as e:
            self.logger.error(f"Error starting recording: {e}")
            raise

    def stop_recording(self):
        """Stop recording system data to database."""
        try:
            self.logger.info("Stopping data recording")
            self.recording = False
            self.record_button.configure(
                text=TRANSLATIONS[self.current_lang]['start_recording']
            )
            self.timer_label.config(text="")
        except Exception as e:
            self.logger.error(f"Error stopping recording: {e}")
            raise

    def update_timer(self):
        """Update recording timer display."""
        if self.recording:
            try:
                elapsed_time = int(time.time() - self.start_time)
                self.timer_label.config(
                    text=f"{elapsed_time} {TRANSLATIONS[self.current_lang]['recording_time']}"
                )
                self.root.after(1000, self.update_timer)
            except Exception as e:
                self.logger.error(f"Error updating timer: {e}")
                raise

    def toggle_language(self):
        """Toggle interface language between Russian and English."""
        try:
            self.logger.info(f"Switching language from {self.current_lang}")
            self.current_lang = 'en' if self.current_lang == 'ru' else 'ru'
            texts = TRANSLATIONS[self.current_lang]
            
            self.title_label.config(text=texts['title'])
            self.record_button.configure(
                text=texts['stop_recording'] if self.recording else texts['start_recording']
            )
            self.lang_button.configure(text=texts['switch_lang'])
            
            if self.recording and hasattr(self, 'start_time'):
                elapsed_time = int(time.time() - self.start_time)
                self.timer_label.config(text=f"{elapsed_time} {texts['recording_time']}")
            else:
                self.timer_label.config(text="")
        except Exception as e:
            self.logger.error(f"Error switching language: {e}")
            raise

    def on_close(self):
        """Close database connection and destroy window."""
        try:
            self.logger.info("Closing application")
            self.db.close()
            self.root.destroy()
        except Exception as e:
            self.logger.error(f"Error closing application: {e}")
            raise 