import pygame
from .models.board import Board
from .renderers.renderer import Renderer
from .widgets.controls import Controls


class App:
    """Главное приложение."""

    def __init__(self, width: int = 480, height: int = 600,
                 fps: int = 60):
        """Инициализирует pygame и компоненты."""
        pygame.init()
        self.width, self.height, self.fps = width, height, fps
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("2048")
        self.clock = pygame.time.Clock()
        self.board = Board()
        self.controls = Controls(self.board)
        self.renderer = Renderer(self.screen)
        self.best = 0
        self.running = True

    def run(self):
        """Главный цикл."""
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                else:
                    self.controls.handle(event)
            self.best = max(self.best, self.board.score)
            self.renderer.draw(self.board, self.best, self.controls.state)
            pygame.display.flip()
            self.clock.tick(self.fps)
        pygame.quit()
