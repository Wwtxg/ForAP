import pygame

from settings import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    CAMERA_FOLLOW_OFFSET,
)


class Camera:
    def __init__(self):
        self.x = 0
        self.y = 0

    def update(self, player):
        target_y = (
            player.rect.centery
            - CAMERA_FOLLOW_OFFSET
        )

        # Camera only moves upward.
        if target_y < self.y:
            self.y = target_y

    def apply(self, rect):
        return pygame.Rect(
            rect.x - self.x,
            rect.y - self.y,
            rect.width,
            rect.height
        )

    def draw_background(self, screen):
        screen.fill((25, 25, 35))