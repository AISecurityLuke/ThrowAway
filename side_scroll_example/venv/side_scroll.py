import pygame
import sys
#########################
# UNFINISHED FRAMEWORK ##
#######
# Constants for screen dimensions and game speed
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # Create a basic visual representation of the player using a colored rectangle.
        self.image = pygame.Surface((50, 50))
        self.image.fill((0, 128, 255))  # A blue shade for the player.
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = 5  # Pixels per update cycle.

    def update(self, keys_pressed):
        # Move left if the left arrow key is pressed.
        if keys_pressed[pygame.K_LEFT]:
            self.rect.x -= self.speed
        # Move right if the right arrow key is pressed.
        if keys_pressed[pygame.K_RIGHT]:
            self.rect.x += self.speed
        # Additional actions like jumping can be added here.
        # For example: if keys_pressed[pygame.K_SPACE]: implement jump logic.

class Level:
    def __init__(self):
        # Initialize the level by creating the player and grouping sprites.
        self.player = Player(100, SCREEN_HEIGHT - 100)  # Starting position near bottom left.
        self.all_sprites = pygame.sprite.Group(self.player)
        # Placeholder for additional sprite groups (enemies, obstacles, etc.).
        self.scroll_x = 0  # Tracks horizontal scrolling offset.

    def update(self):
        # Process keyboard input for all sprites.
        keys_pressed = pygame.key.get_pressed()
        self.all_sprites.update(keys_pressed)

        # Horizontal scrolling logic:
        # If the player moves beyond 70% of the screen's width on the right, scroll left.
        if self.player.rect.right > SCREEN_WIDTH * 0.7:
            self.scroll_x = self.player.rect.right - SCREEN_WIDTH * 0.7
            self.player.rect.right = SCREEN_WIDTH * 0.7  # Keep player within the threshold.
        # If the player moves beyond 30% of the screen's width on the left, scroll right.
        elif self.player.rect.left < SCREEN_WIDTH * 0.3:
            self.scroll_x = self.player.rect.left - SCREEN_WIDTH * 0.3
            self.player.rect.left = SCREEN_WIDTH * 0.3
        else:
            self.scroll_x = 0

        # The scroll_x value can later be used to shift other level elements or backgrounds.

    def draw(self, surface):
        # Draw the background using a greenish color as a placeholder.
        surface.fill((34, 139, 34))
        # Draw all sprites onto the provided surface.
        self.all_sprites.draw(surface)
        # Additional drawing (UI elements, platforms, etc.) can be added here.

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Sidescrolling RPG Roguelike Skeleton")
    clock = pygame.time.Clock()

    level = Level()

    running = True
    # Main game loop.
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        level.update()
        level.draw(screen)
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
