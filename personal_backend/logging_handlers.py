import os
from datetime import datetime
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path

class DailyDirectoryLogHandler(TimedRotatingFileHandler):
    """
    Custom logging handler that creates daily subdirectories for logs
    in the format YYYY-MM-DD/filename.log
    """
    
    def __init__(self, filename, *args, **kwargs):
        self.base_dir = Path(filename).parent
        self.base_filename = Path(filename).name
        # Ensure the base directory exists
        self.base_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize with the current date's path
        current_path = self._get_current_path()
        
        # Initialize parent class with the current day's path
        super().__init__(current_path, *args, **kwargs)

    def _get_current_path(self):
        """Get the current day's log directory and create it if needed"""
        current_date = datetime.now().strftime('%Y-%m-%d')
        daily_dir = self.base_dir / current_date
        daily_dir.mkdir(exist_ok=True)
        return str(daily_dir / self.base_filename)

    def doRollover(self):
        """Override doRollover to handle directory creation and path updates"""
        # Close current file if it's open
        if self.stream:
            self.stream.close()
            self.stream = None

        # Update the base filename to the new day's path
        self.baseFilename = self._get_current_path()

        # Create new file
        if not self.delay:
            self.stream = self._open() 