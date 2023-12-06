import pygame
import sys
import random
from fsm import FSM
import math

class SkiJumpGame:
    WIDTH, HEIGHT = 800, 600
    FPS = 60
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    START, TOP_OF_JUMP, GOING_DOWN_JUMP, JUMP_CALCULATOR, GAME_OVER = "s", 'j', "g", "c", "o", 
    
    def start_game():
        pass
    def begin_jump():
        pass
    def jump_measuring():
        pass
    def game_over():
        pass
    def jump():
        pass

    def init_fsm(self):
            #input, current state, action, new state
            self.fsm.add_transition("start_button", self.START, self.start_game, self.TOP_OF_JUMP)
            self.fsm.add_transition("space_bar", self.TOP_OF_JUMP, self.begin_jump, self.GOING_DOWN_JUMP)
            self.fsm.add_transition("reached_bottom", self.GOING_DOWN_JUMP, self.jump_measuring, self.JUMP_CALCULATOR)
            self.fsm.add_transition("missed_jump", self.JUMP_CALCULATOR, self.game_over, self.GAME_OVER)
            self.fsm.add_transition("hit_jump", self.JUMP_CALCULATOR, self.jump, self.jumping)
            self.fsm.add_transition("landed", self.jumping, self.game_over, self.GAME_OVER)
            self.fsm.add_transition("start_button", self.GAME_OVER, self.start_game, self.TOP_OF_JUMP)

    def __init__(self):
        # Initialize Pygame
        pygame.init()

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
        self.velocity_x = self.initial_velocity * math.cos(math.radians(50))
        self.velocity_y = self.initial_velocity * math.sin(math.radians(50))

        self.fsm = FSM(self.START)
        self.init_fsm()


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
        self.jump_image = pygame.image.load("assets/ski_bg.jpg")
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
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and self.fsm.current_state == self.START:
                    #this might be wrong
                    self.fsm.current_state = self.GOING_DOWN_JUMP
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and self.fsm.current_state == self.GAME_OVER:
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
        if self.fsm.current_state == self.GOING_DOWN_JUMP:
            #this is going_down jump
            if self.jumping:
                self.player_x += self.velocity_x
                self.player_y += self.velocity_y

                # Check if skier crossed half the screen
                #this is jump measure
                if self.player_x > self.WIDTH / 2 and self.hasflipped == False:
                    self.velocity_y *= -1  # Change direction
                    self.hasflipped = True

                self.jump_height += self.jump_speed
                if self.jump_height >= self.jump_target:
                    self.jumping = False
                    self.jump_height = 0
                    self.current_state = self.GAME_OVER
        elif self.fsm.current_state == self.GAME_OVER:
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
        if self.fsm.current_state == self.START:
            self.display_text("Press SPACE to Start", self.RED)
        elif self.fsm.current_state == self.GAME_OVER:
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