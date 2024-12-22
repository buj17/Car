import os.path
from enum import Enum

import pygame

pygame.init()
_size = _width, _height = 600, 95
_main_screen = pygame.display.set_mode(_size)


def load_image(filename: str | os.PathLike, colorkey=None) -> pygame.Surface:
    fullname = os.path.join('data', filename)
    if not os.path.isfile(fullname):
        pass
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


class Way(Enum):
    Right = 0
    Left = 1


class Car(pygame.sprite.Sprite):
    car_image = load_image('Car.png')
    inverted_car_image = pygame.transform.flip(car_image, True, False)

    def __init__(self, *groups):
        super().__init__(*groups)
        self.image = Car.car_image
        self.rect = self.image.get_rect()
        self.x = self.y = 0
        self.car_velocity = 120
        self.car_way = Way.Right

    def change_way(self):
        self.car_way = {Way.Right: Way.Left, Way.Left: Way.Right}[self.car_way]
        self.image = {Car.car_image: Car.inverted_car_image, Car.inverted_car_image: Car.car_image}[self.image]

    def move(self, fps: int):
        displacement = self.car_velocity / fps

        if self.car_way == Way.Right:
            self.x += displacement
        elif self.car_way == Way.Left:
            self.x -= displacement

        self.rect.x = self.x

        if self.x + self.rect.width >= _width or self.rect.x < 0:
            self.change_way()


class MainWindow:
    def __init__(self):
        self.fps = 60
        self.size = _size
        self.screen = _main_screen
        self.main_sprite_group = pygame.sprite.Group()
        self.car = Car(self.main_sprite_group)

    @property
    def width(self):
        return self.size[0]

    @property
    def height(self):
        return self.size[1]

    def run(self):
        clock = pygame.time.Clock()
        running = True

        while running:
            self.screen.fill(pygame.Color('white'))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.car.move(self.fps)

            self.main_sprite_group.draw(self.screen)
            self.main_sprite_group.update()

            pygame.display.flip()
            clock.tick(self.fps)
        pygame.quit()


if __name__ == '__main__':
    window = MainWindow()
    window.run()
