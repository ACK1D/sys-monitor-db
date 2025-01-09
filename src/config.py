from pathlib import Path
import sys
import os
from dataclasses import dataclass

@dataclass
class Config:
    """Application configuration."""
    
    @property
    def BASE_PATH(self) -> Path:
        """Determines base path for application files."""
        if getattr(sys, 'frozen', False):
            return Path(os.path.dirname(sys.executable))
        return Path(os.path.dirname(os.path.dirname(__file__)))
    
    @property
    def DB_PATH(self) -> Path:
        """Database file path."""
        return self.BASE_PATH / "data" / "system_data.db"
    
    UPDATE_INTERVAL: int = 1000  # ms
    FONT_STYLE: tuple = ("Chalkboard SE Light", 10)
    TEXT_COLOR: str = "white"
    BG_COLOR: str = "black"
    HOVER_COLOR: str = "#333333" 