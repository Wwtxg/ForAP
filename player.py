import pygame

from settings import (
    PLAYER_WIDTH,
    PLAYER_HEIGHT,
    PLAYER_SPEED,
    PLAYER_JUMP_STRENGTH,
    GRAVITY,
)


class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(
            x,
            y,
            PLAYER_WIDTH,
            PLAYER_HEIGHT
        )

        self.velocity_x = 0
        self.velocity_y = 0

        self.on_ground = False

    def handle_input(self):
        keys = pygame.key.get_pressed()

        self.velocity_x = 0

        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.velocity_x = -PLAYER_SPEED

        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.velocity_x = PLAYER_SPEED

        if (
            keys[pygame.K_SPACE]
            or keys[pygame.K_w]
            or keys[pygame.K_UP]
        ):
            self.jump()

    def jump(self):
        if self.on_ground:
            self.velocity_y = -PLAYER_JUMP_STRENGTH
            self.on_ground = False

    def update(self, platforms):
        self.handle_input()

        self.apply_horizontal_movement()

        self.apply_gravity()

        self.apply_vertical_movement(platforms)

    def apply_horizontal_movement(self):
        self.rect.x += self.velocity_x

    def apply_gravity(self):
        self.velocity_y += GRAVITY

    def apply_vertical_movement(self, platforms):
        previous_bottom = self.rect.bottom

        self.rect.y += int(self.velocity_y)

        self.on_ground = False

        if self.velocity_y >= 0:
            for platform in platforms:
                if self.rect.colliderect(platform.rect):
                    if previous_bottom <= platform.rect.top:
                        self.rect.bottom = platform.rect.top
                        self.velocity_y = 0
                        self.on_ground = True
                        break

    def draw(self, screen, camera):
        screen_rect = camera.apply(self.rect)

        pygame.draw.rect(
            screen,
            (220, 70, 70),
            screen_rect
        )