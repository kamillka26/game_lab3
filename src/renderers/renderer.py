import pygame
from ..models.board import Board

BG = (250, 248, 239)
BOARD_BG = (187, 173, 160)
DARK = (119, 110, 101)
LIGHT = (249, 246, 242)
COLORS = {
    0: (205, 193, 180), 2: (238, 228, 218), 4: (237, 224, 200),
    8: (242, 177, 121), 16: (245, 149, 99), 32: (246, 124, 95),
    64: (246, 94, 59), 128: (237, 207, 114), 256: (237, 204, 97),
    512: (237, 200, 80), 1024: (237, 197, 63), 2048: (237, 194, 46),
}


class Renderer:
    """Рисует поле и счёт."""

    def __init__(self, screen):
        """Считает геометрию поля."""
        self.screen = screen
        self.gap = 12
        self.tile = 100
        self.x0 = 30
        self.y0 = 120
        self.font_big = pygame.font.SysFont("Arial", 40, bold=True)
        self.font_sm = pygame.font.SysFont("Arial", 22, bold=True)

    def draw(self, board, best, state):
        """Полная отрисовка кадра."""
        self.screen.fill(BG)
        self._header(board.score, best)
        self._grid(board)
        if state != "playing":
            self._overlay(state)

    def _header(self, score, best):
        """Рисует заголовок и счёт."""
        title = self.font_big.render("2048", True, DARK)
        self.screen.blit(title, (30, 20))
        s = self.font_sm.render(f"Score: {score}", True, DARK)
        b = self.font_sm.render(f"Best: {best}", True, DARK)
        self.screen.blit(s, (300, 30))
        self.screen.blit(b, (300, 60))

    def _grid(self, board):
        """Рисует фон и плитки."""
        size = self.tile * 4 + self.gap * 5
        pygame.draw.rect(self.screen, BOARD_BG,
                         (self.x0, self.y0, size, size), border_radius=8)
        for r in range(4):
            for c in range(4):
                value = board.cells[r][c]
                x = self.x0 + self.gap + c * (self.tile + self.gap)
                y = self.y0 + self.gap + r * (self.tile + self.gap)
                pygame.draw.rect(self.screen, COLORS.get(value, (60, 58, 50)),
                                 (x, y, self.tile, self.tile),
                                 border_radius=6)
                if value:
                    color = LIGHT if value >= 8 else DARK
                    t = self.font_big.render(str(value), True, color)
                    rect = t.get_rect(center=(x + self.tile // 2,
                                              y + self.tile // 2))
                    self.screen.blit(t, rect)

    def _overlay(self, state):
        """Полупрозрачный оверлей победы/поражения."""
        layer = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        layer.fill((238, 228, 218, 200))
        self.screen.blit(layer, (0, 0))
        msg = "You win!" if state == "won" else "Game over!"
        t = self.font_big.render(msg, True, DARK)
        rect = t.get_rect(center=(self.screen.get_width() // 2, 60))
        self.screen.blit(t, rect)
        hint = self.font_sm.render("R — restart", True, DARK)
        self.screen.blit(hint, hint.get_rect(
            center=(self.screen.get_width() // 2, 100)))
