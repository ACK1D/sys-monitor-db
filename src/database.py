import sqlite3
from pathlib import Path
import logging
from datetime import datetime

class Database:
    def __init__(self, db_path: Path):
        self.db_path = db_path
        self.db_path.parent.mkdir(mode=0o777, exist_ok=True)
        self.logger = logging.getLogger("SystemMonitor.Database")
        self.conn = None
        
    def connect(self):
        """Устанавливает соединение с БД."""
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.create_table()
        except sqlite3.Error as e:
            self.logger.error(f"Ошибка подключения к БД: {e}")
            raise
            
    def create_table(self):
        """Создает таблицу в БД."""
        try:
            with self.conn:
                self.conn.execute("""
                    CREATE TABLE IF NOT EXISTS system_data (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        timestamp TEXT,
                        cpu_usage REAL,
                        ram_usage REAL,
                        disk_usage REAL
                    )
                """)
        except sqlite3.Error as e:
            self.logger.error(f"Ошибка создания таблицы: {e}")
            raise
            
    def save_data(self, cpu: float, ram: float, disk: float):
        """Сохраняет данные в БД."""
        try:
            with self.conn:
                self.conn.execute(
                    """
                    INSERT INTO system_data (timestamp, cpu_usage, ram_usage, disk_usage)
                    VALUES (datetime('now', 'localtime'), ?, ?, ?)
                    """,
                    (cpu, ram, disk),
                )
        except sqlite3.Error as e:
            self.logger.error(f"Ошибка сохранения данных: {e}")
            raise
            
    def close(self):
        """Закрывает соединение с БД."""
        if self.conn:
            self.conn.close() 