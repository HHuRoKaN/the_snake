from random import choice, randint
import pygame

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

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    """Основной класс всех оюъектов."""

    def __init__(self):
        self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        self.body_color = None

    def draw(self):
        """Отрисовка игрового поля, для переопределения."""
        pass


class Apple(GameObject):
    """Описание яблока."""

    def __init__(self):
        super().__init__()
        self.body_color = APPLE_COLOR
        self.position = self.randomize_position(self.position)

    def randomize_position(self, occupied_positions):
        """Случайно задается место яблока на поле."""
        while True:
            self.position = (randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                             randint(0, GRID_HEIGHT - 1) * GRID_SIZE)
            if self.position not in occupied_positions:
                return self.position

    def draw(self):
        """Отрисовка яблока."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


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
        self.lenght = 1
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = RIGHT
        self.next_direction = None
        self.body_color = SNAKE_COLOR
        self.last = None

    def update_direction(self):
        """Обновление направления движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Обновление позиции змейки."""
        head_position = self.get_head_position()
        head_position = (
            (head_position[0] + self.direction[0] * GRID_SIZE),
            (head_position[1] + self.direction[1] * GRID_SIZE))
        if head_position[0] >= SCREEN_WIDTH:
            head_position = (0, head_position[1])
        elif head_position[0] < 0:
            head_position = (SCREEN_WIDTH - GRID_SIZE, head_position[1])
        if head_position[1] >= SCREEN_HEIGHT:
            head_position = (head_position[0], 0)
        elif head_position[1] < 0:
            head_position = (head_position[0], SCREEN_HEIGHT - GRID_SIZE)
        self.positions.insert(0, head_position)
        if len(self.positions) > self.lenght:
            self.last = self.positions.pop()

    def draw(self):
        """Отрисовка змейки."""
        for position in self.positions[:-1]:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self):
        """Возвращает позицию головы змейки."""
        # В задании просили указать этот метод, но по сути он и не нужен
        # ту же команду можно вставить вместо вызова самой функции, но так
        # описали задание, поэтому и оставил его.
        return self.positions[0]

    def reset(self):
        """Возвращает змейку в изначальное состояние."""
        self.lenght = 1
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        directions = (UP, DOWN, LEFT, RIGHT)
        self.direction = choice(directions)


def main():
    """Основная логика игры."""
    # Инициализация PyGame:
    pygame.init()
    # Тут нужно создать экземпляры классов.
    apple = Apple()
    snake = Snake()
    poison = Poison()
    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.draw()
        apple.draw()
        poison.draw()
        # Тут опишите основную логику игры.
        snake.update_direction()
        snake.move()
        # Добавление всех занятых позиций
        occupied_positions = set(snake.positions)
        occupied_positions.add(apple.position)
        occupied_positions.add(poison.position)
        if snake.positions[0] == apple.position:
            snake.lenght += 1
            apple.randomize_position(occupied_positions)
            # После каждого съеденного яблока идет добавление камня
            stone = Stone()
            stone.randomize_position(occupied_positions)
            Stone.stones.append(stone)
            stone.draw()
        if snake.positions[0] == poison.position:
            snake.lenght -= 1
            del_end = snake.positions.pop()
            del_end_rect = pygame.Rect(del_end, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, del_end_rect)
            poison.randomize_position(occupied_positions)
        if (
            (snake.lenght > 3 and snake.positions[0]
             in snake.positions[1:snake.lenght])
            or (snake.lenght < 1)
            or any(snake.positions[0] == stone.position for stone
                   in Stone.stones)
        ):
            screen.fill(BOARD_BACKGROUND_COLOR)
            snake.reset()
            apple.randomize_position(occupied_positions)
            poison.randomize_position(occupied_positions)
            Stone.reset()
        pygame.display.update()


def handle_keys(game_object):
    """Функция обработки действий пользователя."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


if __name__ == '__main__':
    main()
