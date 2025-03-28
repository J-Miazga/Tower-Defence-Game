import pygame as pg
import logging
from logging.handlers import RotatingFileHandler


class GameLogger:
    def __init__(self, max_lines=10):
        self.logger = self._setup_logger()
        self.display = GameLogDisplay(max_lines)

    def _setup_logger(self):
        logger = logging.getLogger("GameLogger")
        logger.setLevel(logging.DEBUG)

        handler = RotatingFileHandler("game_logs.txt", maxBytes=10 * 1024, backupCount=3)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        console = logging.StreamHandler()
        console.setFormatter(formatter)
        logger.addHandler(console)

        return logger

    def log(self, message, type):
        formatted = f"{type.upper()}: {message}"
        self.display.add_log(formatted)

        if type == 'info':
            self.logger.info(message)
        elif type == 'warning':
            self.logger.warning(message)
        elif type == 'error':
            self.logger.error(message)


class GameLogDisplay:
    def __init__(self, max_lines=10):
        self.max_lines = max_lines
        self.logs = []
        self.visible = False

    def toggle(self):
        self.visible = not self.visible

    def add_log(self, message):
        self.logs.append(message)
        if len(self.logs) > self.max_lines:
            self.logs.pop(0)

    def draw(self, surface, font, x, y, width):
        if not self.visible:
            return
        log_surface = pg.Surface((width, self.max_lines * 22 + 10))
        log_surface.set_alpha(180)
        log_surface.fill((0, 0, 0))
        for i, line in enumerate(self.logs):
            text_surface = font.render(line, True, (255, 255, 255))
            log_surface.blit(text_surface, (5, 5 + i * 22))
        surface.blit(log_surface, (x, y))
        
game_logger = GameLogger()

