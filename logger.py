import pygame as pg
import logging
from logging.handlers import RotatingFileHandler

# Logger class that handles both file/console logging and in-game UI display
class GameLogger:
    def __init__(self, max_lines=10):
        self.logger = self._setup_logger()                  # Setup file + console logging
        self.display = GameLogDisplay(max_lines)           # In-game log panel

    # Configure Python logging with file rotation and console output
    def _setup_logger(self):
        logger = logging.getLogger("GameLogger")
        logger.setLevel(logging.DEBUG)

        # Log to file with rotation
        handler = RotatingFileHandler("game_logs.txt", maxBytes=10 * 1024, backupCount=3)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        # Also print to console
        console = logging.StreamHandler()
        console.setFormatter(formatter)
        logger.addHandler(console)

        return logger

    # Log to file/console and optionally show on-screen
    def log(self, message, type):
        formatted = f"{type.upper()}: {message}"
        self.display.add_log(formatted)  # Add to visual in-game log

        # Log based on type
        if type == 'info':
            self.logger.info(message)
        elif type == 'warning':
            self.logger.warning(message)
        elif type == 'error':
            self.logger.error(message)


# Class to visually display game logs in the game window
class GameLogDisplay:
    def __init__(self, max_lines=10):
        self.max_lines = max_lines
        self.logs = []
        self.visible = False  # Visibility can be toggled

    def toggle(self):
        self.visible = not self.visible

    def add_log(self, message):
        self.logs.append(message)
        if len(self.logs) > self.max_lines:
            self.logs.pop(0)  # Keep only the most recent messages

    # Render the logs to a section of the screen
    def draw(self, surface, font, x, y, width):
        if not self.visible:
            return

        log_surface = pg.Surface((width, self.max_lines * 22 + 10))
        log_surface.set_alpha(180)  # Semi-transparent background
        log_surface.fill((0, 0, 0))  # Black background

        # Draw each log line
        for i, line in enumerate(self.logs):
            text_surface = font.render(line, True, (255, 255, 255))
            log_surface.blit(text_surface, (5, 5 + i * 22))

        surface.blit(log_surface, (x, y))


# Global logger instance to be imported and used across the project
game_logger = GameLogger()
