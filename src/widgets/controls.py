import pygame

KEYS = {
    pygame.K_LEFT: "left", pygame.K_a: "left",
    pygame.K_RIGHT: "right", pygame.K_d: "right",
    pygame.K_UP: "up", pygame.K_w: "up",
    pygame.K_DOWN: "down", pygame.K_s: "down",
}


class Controls:
    """Обрабатывает ввод."""

    def __init__(self, board):
        """Сохраняет модель."""
        self.board = board
        self.state = "playing"

    def handle(self, event):
        """Обрабатывает одно событие."""
        if event.type != pygame.KEYDOWN:
            return
        if event.key == pygame.K_r:
            self.board.reset()
            self.state = "playing"
            return
        if self.state != "playing":
            return
        direction = KEYS.get(event.key)
        if direction:
            self.board.move(direction)
            self._update_state()

    def _update_state(self):
        """Пересчитывает победу/поражение."""
        if self.board.is_won():
            self.state = "won"
        elif not self.board.can_move():
            self.state = "lost"
