import random
from typing import List

SIZE = 4


class Board:
    """Поле 4×4. 0 — пустая клетка."""

    def __init__(self):
        """Создаёт пустое поле с двумя плитками."""
        self.cells: List[List[int]] = [[0] * SIZE for _ in range(SIZE)]
        self.score = 0
        self.add_random_tile()
        self.add_random_tile()

    def add_random_tile(self):
        """Ставит 2 (90%) или 4 (10%) в случайную пустую клетку."""
        empty = [(r, c) for r in range(SIZE) for c in range(SIZE)
                 if self.cells[r][c] == 0]
        if not empty:
            return
        r, c = random.choice(empty)
        self.cells[r][c] = 2 if random.random() < 0.9 else 4

    @staticmethod
    def _slide_left(row):
        """Сдвигает строку влево, сливая пары."""
        nonzero = [x for x in row if x]           # убрать нули
        result: List[int] = []
        gained = 0
        i = 0
        while i < len(nonzero):
            if i + 1 < len(nonzero) and nonzero[i] == nonzero[i + 1]:
                v = nonzero[i] * 2
                result.append(v)
                gained += v
                i += 2
            else:
                result.append(nonzero[i])
                i += 1
        result += [0] * (SIZE - len(result))
        return result, gained

    @staticmethod
    def _rotate(m):
        """Поворот на 90° по часовой."""
        return [list(row) for row in zip(*m[::-1])]

    def move(self, direction):
        """Ход в направлении left/right/up/down."""
        before = [row[:] for row in self.cells]

        # Поворачиваем так, чтобы нужное направление стало "влево".
        # - left: ничего не делаем (0 поворотов)
        # - up: 3 поворота по часовой (это равносильно 1 повороту против
        # часовой)
        # - right: 2 поворота по часовой (180 градусов)
        # - down: 1 поворот по часовой
        turns = {"left": 0, "up": 3, "right": 2, "down": 1}

        if direction not in turns:
            raise ValueError(f"bad direction: {direction}")

        n = turns[direction]

        # 1. Поворачиваем
        for _ in range(n):
            self.cells = self._rotate(self.cells)

        # 2. Сдвигаем влево
        gained = 0
        for r in range(SIZE):
            self.cells[r], g = self._slide_left(self.cells[r])
            gained += g

        # 3. Возвращаем обратно (делаем 4-n поворотов, чтобы в сумме было 4,
        # т.е. полный круг)
        for _ in range((4 - n) % 4):
            self.cells = self._rotate(self.cells)

        # 4. Если поле изменилось, начисляем очки и добавляем плитку
        if self.cells != before:
            self.score += gained
            self.add_random_tile()
            return True
        return False

    def can_move(self):
        """Есть ли хоть один возможный ход."""
        for r in range(SIZE):
            for c in range(SIZE):
                if self.cells[r][c] == 0:
                    return True
                if c + 1 < SIZE and self.cells[r][c] == self.cells[r][c + 1]:
                    return True
                if r + 1 < SIZE and self.cells[r][c] == self.cells[r + 1][c]:
                    return True
        return False

    def is_won(self):
        """Есть ли плитка 2048."""
        return any(2048 in row for row in self.cells)

    def reset(self):
        """Сбрасывает поле."""
        self.cells = [[0] * SIZE for _ in range(SIZE)]
        self.score = 0
        self.add_random_tile()
        self.add_random_tile()
