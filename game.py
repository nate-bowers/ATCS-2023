import pygame
import sys
import random
from fsm import FSM
import math

class SkiJumpGame:
    def __init__(self):
        # Initialize Pygame
        pygame.init()

        # Constants
        self.WIDTH, self.HEIGHT = 800, 600
        self.FPS = 60
        self.WHITE = (255, 255, 255)
        self.RED = (255, 0, 0)

        # Player variables
        self.player_width = 50
        self.player_height = 50
        self.player_x = 0
        self.player_y = 0
        self.jumping = True
        self.jump_height = 0
        self.jump_speed = 5
        self.jump_target = random.randint(400, 800)  # Randomize the jump target
        self.hasflipped = False

        self.initial_velocity = 5
        self.velocity_x = self.initial_velocity * math.cos(math.radians(35))
        self.velocity_y = self.initial_velocity * math.sin(math.radians(35))

        # Game states
        self.START = 0
        self.PLAYING = 1
        self.GAME_OVER = 2
        self.current_state = self.START

        # Initialize screen
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Ski Jump Game")
        self.clock = pygame.time.Clock()

        # Fonts
        self.font = pygame.font.Font(None, 36)

        # Skier image
        self.skier_image = pygame.image.load("assets/skier.png")
        self.skier_image = pygame.transform.scale(self.skier_image, (self.player_width, self.player_height))

        # Jump image
        self.jump_image = pygame.image.load("assets/jump.png")
        self.jump_image = pygame.transform.scale(self.jump_image, (self.WIDTH, self.HEIGHT))

    def display_text(self, text, color, y_offset=0):
        text_surface = self.font.render(text, True, color)
        text_rect = text_surface.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 2 + y_offset))
        self.screen.blit(text_surface, text_rect)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and self.current_state == self.START:
                    self.current_state = self.PLAYING
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and self.current_state == self.GAME_OVER:
                    self.current_state = self.PLAYING
                    self.jump_target = random.randint(200, 400)
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

            self.update()
            self.draw()

            # Update display
            pygame.display.flip()

            # Cap the frame rate
            self.clock.tick(self.FPS)

    def update(self):
        if self.current_state == self.PLAYING:
            if self.jumping:
                self.player_x += self.velocity_x
                self.player_y += self.velocity_y

                # Check if skier crossed half the screen
                if self.player_x > self.WIDTH / 2 and self.hasflipped == False:
                    self.velocity_y *= -1  # Change direction
                    self.hasflipped = True

                self.jump_height += self.jump_speed
                if self.jump_height >= self.jump_target:
                    self.jumping = False
                    self.jump_height = 0
                    self.current_state = self.GAME_OVER
        elif self.current_state == self.GAME_OVER:
            if self.jumping:
                self.jumping = False
                self.jump_height = 0

    def draw(self):
        # Draw background
        self.screen.fill(self.WHITE)

        # Draw jump image
        self.screen.blit(self.jump_image, (0, 0))

        # Draw skier
        self.screen.blit(self.skier_image, (self.player_x, self.player_y))

        # Display game state-specific text
        if self.current_state == self.START:
            self.display_text("Press SPACE to Start", self.RED)
        elif self.current_state == self.GAME_OVER:
            self.display_text("Game Over. Press SPACE to Play Again", self.RED)

    def reset_game(self):
        self.player_x = self.WIDTH - self.player_width
        self.player_y = 0
        self.jumping = True
        self.jump_height = 0
        self.jump_target = random.randint(200, 400)
        self.velocity_x = self.initial_velocity * math.cos(math.radians(35))
        self.velocity_y = self.initial_velocity * math.sin(math.radians(35))
        self.current_state = self.PLAYING

# Create an instance of the SkiJumpGame class and run the game
game = SkiJumpGame()
game.run()