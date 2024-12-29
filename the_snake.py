from random import choice, randint
import pygame as pg

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)
TURNS = {
    (pg.K_UP, DOWN): None,
    (pg.K_UP, RIGHT): UP,
    (pg.K_UP, LEFT): UP,
    (pg.K_UP, UP): UP,
    (pg.K_DOWN, UP): None,
    (pg.K_DOWN, DOWN): DOWN,
    (pg.K_DOWN, RIGHT): DOWN,
    (pg.K_DOWN, LEFT): DOWN,
    (pg.K_LEFT, RIGHT): None,
    (pg.K_LEFT, LEFT): LEFT,
    (pg.K_LEFT, UP): LEFT,
    (pg.K_LEFT, DOWN): LEFT,
    (pg.K_RIGHT, LEFT): None,
    (pg.K_RIGHT, RIGHT): RIGHT,
    (pg.K_RIGHT, UP): RIGHT,
    (pg.K_RIGHT, DOWN): RIGHT
}

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (0, 255, 0)

# Цвет отравы
POISON_COLOR = (255, 0, 0)

# Цвет камня
STONE_COLOR = (117, 116, 117)

# Цвет змейки
SNAKE_COLOR = (0, 0, 255)

# Скорость движения змейки:
SPEED = 20

# Минимальный уровень змейки
MIN_LEVEL = 1

# Уровень змеи для врезания
LEVEL_FOR_COLLISION = 4

# Настройка игрового окна:
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pg.display.set_caption('Змейка')

# Клавиша завершения:
QUIT = pg.QUIT

# Настройка времени:
clock = pg.time.Clock()

# Счетчик игр в игровой сессии
game = 0


# Тут опишите все классы игры.
class GameObject:
    """Основной класс всех объектов."""

    def __init__(self):
        self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        self.body_color = None

    def draw(self):
        """Отрисовка игрового поля, для переопределения."""

    def draw_cell(self, position, border_color, obj_color):
        """Отрисовка частей объектов."""
        rect = pg.Rect(position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, obj_color, rect)
        pg.draw.rect(screen, border_color, rect, 1)


class Apple(GameObject):
    """Описание яблока."""

    def __init__(self):
        super().__init__()
        self.body_color = APPLE_COLOR
        self.randomize_position([])

    def randomize_position(self, occupied_positions):
        """Случайно задается место яблока на поле."""
        while True:
            self.position = (randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                             randint(0, GRID_HEIGHT - 1) * GRID_SIZE)
            if self.position not in occupied_positions:
                break

    def draw(self):
        """Отрисовка яблока."""
        self.draw_cell(self.position, BORDER_COLOR, self.body_color)


class Poison(Apple):
    """Описание отравы."""

    def __init__(self):
        super().__init__()
        self.body_color = POISON_COLOR


class Stone(Apple):
    """Описание камня."""

    stones: list = []

    def __init__(self):
        super().__init__()
        self.body_color = STONE_COLOR

    @classmethod
    def reset(cls):
        """Сброс камней."""
        cls.stones = []


class Snake(GameObject):
    """Описание змейки."""

    def __init__(self):
        super().__init__()
        self.reset()
        self.direction = RIGHT
        self.next_direction = None
        self.body_color = SNAKE_COLOR
        self.last = None
        self.can_change_direction = True

    def update_direction(self, next_direction=None):
        """Обновление направления движения змейки."""
        if next_direction and self.can_change_direction:
            self.direction = next_direction
            self.can_change_direction = False
            self.next_direction = None

    def move(self):
        """Обновление позиции змейки."""
        head_x, head_y = self.get_head_position()
        direction_x, direction_y = self.direction
        head_position = (
            (head_x + (direction_x * GRID_SIZE)) % SCREEN_WIDTH,
            (head_y + (direction_y * GRID_SIZE)) % SCREEN_HEIGHT,
        )
        self.positions.insert(0, head_position)
        if len(self.positions) > self.lenght:
            self.last = self.positions.pop()
        self.can_change_direction = True

    def draw(self):
        """Отрисовка змейки."""
        for position in self.positions[:-1]:
            self.draw_cell(position, BORDER_COLOR, self.body_color)

        # Отрисовка головы змейки
        self.draw_cell(self.positions[0], BORDER_COLOR, self.body_color)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pg.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pg.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self):
        """Возвращает позицию головы змейки."""
        return self.positions[0]

    def reset(self):
        """Возвращает змейку в изначальное состояние."""
        self.lenght = 1
        self.max_lenght = 1
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        directions = (UP, DOWN, LEFT, RIGHT)
        self.direction = choice(directions)


def main():
    """Основная логика игры."""
    pg.init()
    apple = Apple()
    snake = Snake()
    poison = Poison()
    with open('records.txt', 'w', encoding='utf-8') as f:
        f.write('Ваши очки за игровую сессию:\n')
    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.draw()
        apple.draw()
        poison.draw()
        snake.update_direction(snake.next_direction)
        snake.move()
        occupied_positions = set(snake.positions)
        occupied_positions.add(apple.position)
        occupied_positions.add(poison.position)
        if snake.positions[0] == apple.position:
            snake.lenght += 1
            snake.max_lenght += 1
            apple.randomize_position(occupied_positions)
            # После каждого съеденного яблока идет добавление камня
            stone = Stone()
            stone.randomize_position(occupied_positions)
            Stone.stones.append(stone)
            stone.draw()
        if snake.positions[0] == poison.position:
            snake.lenght -= 1
            del_end = snake.positions.pop()
            del_end_rect = pg.Rect(del_end, (GRID_SIZE, GRID_SIZE))
            pg.draw.rect(screen, BOARD_BACKGROUND_COLOR, del_end_rect)
            poison.randomize_position(occupied_positions)
        if (
            (snake.lenght >= LEVEL_FOR_COLLISION and snake.positions[0]
             in snake.positions[1:snake.lenght])
            or (snake.lenght < MIN_LEVEL)
            or any(snake.positions[0] == stone.position for stone
                   in Stone.stones)
        ):
            records(snake.lenght, snake.max_lenght)
            screen.fill(BOARD_BACKGROUND_COLOR)
            snake.reset()
            apple.randomize_position(occupied_positions)
            poison.randomize_position(occupied_positions)
            Stone.reset()
        pg.display.update()


def records(len, max_len):
    """Запись рекордов за игровую сессию."""
    global game
    game += 1
    with open("records.txt", 'a', encoding='utf-8') as file:
        file.write(f'Игра № {game}. Результат: {len}.'
                   f' Максимальная длина была: {max_len}\n')


def handle_keys(game_object):
    """Функция обработки действий пользователя."""
    for event in pg.event.get():
        if event.type == QUIT:
            records(game_object.lenght, game_object.max_lenght)
            pg.quit()
            raise SystemExit
        elif event.type == pg.KEYDOWN:
            game_object.update_direction(
                TURNS.get((event.key, game_object.direction),
                          game_object.direction))


if __name__ == '__main__':
    main()
