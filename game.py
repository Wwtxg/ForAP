import pygame

from player import Player
from platform_generator import PlatformGenerator
from camera import Camera

from settings import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    FPS,
    GAME_OVER_TITLE,
    GAME_OVER_BUTTON,
    GAME_OVER_TITLE_SIZE,
    GAME_OVER_BUTTON_SIZE,
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
        self.game_over = False

        self.camera = Camera()

        self.platform_generator = PlatformGenerator()

        self.create_player()

        # Fonts
        self.title_font = pygame.font.Font(
            None,
            GAME_OVER_TITLE_SIZE
        )

        self.button_font = pygame.font.Font(
            None,
            GAME_OVER_BUTTON_SIZE
        )

        self.resume_button = pygame.Rect(
            SCREEN_WIDTH // 2 - 100,
            SCREEN_HEIGHT // 2 + 50,
            200,
            60
        )

    def create_player(self):
        starting_platform = (
            self.platform_generator
            .get_platforms()[0]
        )

        self.player = Player(
            starting_platform.rect.centerx - 15,
            starting_platform.rect.top - 40
        )

    def restart_game(self):
        self.camera = Camera()

        self.platform_generator = PlatformGenerator()

        self.create_player()

        self.game_over = False

    def run(self):
        while self.running:
            self.handle_events()

            if not self.game_over:
                self.update()

            self.draw()

            self.clock.tick(FPS)

        pygame.quit()

    def handle_events(self):
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                self.running = False

            if self.game_over:

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.restart_game()

                    if event.key == pygame.K_ESCAPE:
                        self.running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if self.resume_button.collidepoint(
                            event.pos
                        ):
                            self.restart_game()

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

        self.check_player_death()

    def check_player_death(self):
        # World-space bottom of the visible screen.
        screen_bottom = (
            self.camera.y + SCREEN_HEIGHT
        )

        # Player has fallen below the screen.
        if self.player.rect.top > screen_bottom:
            self.game_over = True

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

        if self.game_over:
            self.draw_game_over()

        pygame.display.flip()

    def draw_game_over(self):
        # Dark overlay
        overlay = pygame.Surface(
            (SCREEN_WIDTH, SCREEN_HEIGHT)
        )

        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))

        self.screen.blit(
            overlay,
            (0, 0)
        )

        # GAME OVER text
        title_surface = self.title_font.render(
            GAME_OVER_TITLE,
            True,
            (255, 255, 255)
        )

        title_rect = title_surface.get_rect(
            center=(
                SCREEN_WIDTH // 2,
                SCREEN_HEIGHT // 2 - 50
            )
        )

        self.screen.blit(
            title_surface,
            title_rect
        )

        # Button
        pygame.draw.rect(
            self.screen,
            (80, 180, 80),
            self.resume_button
        )

        pygame.draw.rect(
            self.screen,
            (255, 255, 255),
            self.resume_button,
            2
        )

        # RESUME text
        button_surface = self.button_font.render(
            GAME_OVER_BUTTON,
            True,
            (255, 255, 255)
        )

        button_rect = button_surface.get_rect(
            center=self.resume_button.center
        )

        self.screen.blit(
            button_surface,
            button_rect
        )