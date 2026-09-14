import pygame

from player import Player
from platform_generator import PlatformGenerator
from camera import Camera

from settings import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    FPS,
)


class Game:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode(
            (SCREEN_WIDTH, SCREEN_HEIGHT)
        )

        pygame.display.set_caption("Platform Jumper")

        self.clock = pygame.time.Clock()

        self.running = True

        self.camera = Camera()

        self.platform_generator = PlatformGenerator()

        starting_platform = (
            self.platform_generator
            .get_platforms()[0]
        )

        self.player = Player(
            starting_platform.rect.centerx - 15,
            starting_platform.rect.top - 40
        )

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()

            self.clock.tick(FPS)

        pygame.quit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def update(self):
        platforms = (
            self.platform_generator
            .get_platforms()
        )

        self.player.update(platforms)

        self.platform_generator.update(
            self.player
        )

        self.camera.update(
            self.player
        )

    def draw(self):
        self.camera.draw_background(
            self.screen
        )

        self.platform_generator.draw(
            self.screen,
            self.camera
        )

        self.player.draw(
            self.screen,
            self.camera
        )

        pygame.display.flip()