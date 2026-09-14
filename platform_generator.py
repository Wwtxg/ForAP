import random

from platform import Platform

from settings import (
    PLATFORM_WIDTH,
    PLATFORM_HEIGHT,
    MIN_PLATFORM_VERTICAL_DISTANCE,
    MAX_PLATFORM_VERTICAL_DISTANCE,
    MAX_PLATFORM_HORIZONTAL_DISTANCE,
    INITIAL_PLATFORM_COUNT,
    PLATFORMS_AHEAD,
    PLATFORM_CLEANUP_DISTANCE,
    SCREEN_WIDTH,
)


class PlatformGenerator:
    def __init__(self):
        self.platforms = []

        self.generate_initial_platforms()

    def generate_initial_platforms(self):
        start_x = (SCREEN_WIDTH - PLATFORM_WIDTH) // 2
        start_y = 500

        first_platform = Platform(
            start_x,
            start_y,
            PLATFORM_WIDTH,
            PLATFORM_HEIGHT
        )

        self.platforms.append(first_platform)

        for _ in range(INITIAL_PLATFORM_COUNT - 1):
            self.generate_next_platform()

    def generate_next_platform(self):
        previous_platform = self.platforms[-1]

        previous_x = previous_platform.rect.x
        previous_y = previous_platform.rect.y

        horizontal_offset = random.randint(
            -MAX_PLATFORM_HORIZONTAL_DISTANCE,
            MAX_PLATFORM_HORIZONTAL_DISTANCE
        )

        vertical_distance = random.randint(
            MIN_PLATFORM_VERTICAL_DISTANCE,
            MAX_PLATFORM_VERTICAL_DISTANCE
        )

        new_x = previous_x + horizontal_offset
        new_y = previous_y - vertical_distance

        # Keep platform inside the world horizontally.
        new_x = max(
            0,
            min(
                new_x,
                SCREEN_WIDTH - PLATFORM_WIDTH
            )
        )

        platform = Platform(
            new_x,
            new_y,
            PLATFORM_WIDTH,
            PLATFORM_HEIGHT
        )

        self.platforms.append(platform)

    def update(self, player):
        self.generate_platforms_ahead(player)
        self.remove_old_platforms(player)

    def generate_platforms_ahead(self, player):
        highest_platform_y = min(
            platform.rect.y
            for platform in self.platforms
        )

        target_y = player.rect.y - (
            PLATFORMS_AHEAD * MAX_PLATFORM_VERTICAL_DISTANCE
        )

        while highest_platform_y > target_y:
            self.generate_next_platform()

            highest_platform_y = min(
                platform.rect.y
                for platform in self.platforms
            )

    def remove_old_platforms(self, player):
        minimum_y = (
            player.rect.y
            + PLATFORM_CLEANUP_DISTANCE
        )

        self.platforms = [
            platform
            for platform in self.platforms
            if platform.rect.y < minimum_y
        ]

    def get_platforms(self):
        return self.platforms

    def draw(self, screen, camera):
        for platform in self.platforms:
            platform.draw(screen, camera)