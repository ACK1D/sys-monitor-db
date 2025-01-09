import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
import sys
import os

def setup_logger():
    """Configure application logging."""
    if getattr(sys, 'frozen', False):
        base_path = Path(os.path.dirname(sys.executable))
    else:
        base_path = Path(os.path.dirname(os.path.dirname(__file__)))
    
    log_dir = base_path / "logs"
    log_dir.mkdir(mode=0o777, exist_ok=True)
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            RotatingFileHandler(
                log_dir / "app.log",
                maxBytes=1024*1024,  # 1MB limit
                backupCount=3,
                encoding='utf-8'
            ),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger("SystemMonitor") 