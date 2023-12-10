import pygame
import sys
import random
from fsm import FSM
import math
import time

class SkiJumpGame:
    WIDTH, HEIGHT = 800, 600
    FPS = 60
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    PLAYER_WIDTH = 50
    PLAYER_HEIGHT = 50
    INITIAL_VELOCITY = 5
    START, TOP_OF_JUMP, GOING_DOWN_JUMP, JUMP_CALCULATOR, GAME_OVER, JUMPING, JUMP_CALCULATED = "s", 'j', "g", "c", "o", "ju", "jd"

    def init_fsm(self):
            #input, current state, action, new state
            self.fsm.add_transition("space_bar", self.START, None, self.GOING_DOWN_JUMP)
            self.fsm.add_transition("space_bar", self.GOING_DOWN_JUMP, None, self.GOING_DOWN_JUMP)
            self.fsm.add_transition("reached_bottom", self.GOING_DOWN_JUMP, self.jump_measuring, self.JUMP_CALCULATOR)

            self.fsm.add_transition("space_bar", self.JUMP_CALCULATOR, self.calc_jump, self.JUMP_CALCULATED)
            self.fsm.add_transition("space_bar", self.JUMP_CALCULATED, None, self.JUMP_CALCULATED)

            self.fsm.add_transition("space_bar", self.JUMPING, None, self.JUMPING)
            self.fsm.add_transition("space_bar", self.GAME_OVER, None, self.TOP_OF_JUMP)
            
            self.fsm.add_transition("end_of_jump", self.JUMP_CALCULATOR, self.jump, self.JUMPING)
            self.fsm.add_transition("end_of_jump", self.JUMP_CALCULATED, self.jump, self.JUMPING)
            
            self.fsm.add_transition("landed", self.JUMPING, None, self.GAME_OVER)

            self.fsm.add_transition("space_bar", self.GAME_OVER, self.restart, self.START)
            
            

    def __init__(self):
        # Initialize Pygame
        pygame.init()

        # Player variables
        self.player_x = 0
        self.player_y = 0
        self.jump_height = 0
        self.jump_speed = 5
        self.hasflipped = False
        self.time_since_reaching_bottom = 0
        self.timing_percent = 0

        self.velocity_x = self.INITIAL_VELOCITY * math.cos(math.radians(50))
        self.velocity_y = self.INITIAL_VELOCITY * math.sin(math.radians(50))

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
        
        # Jump image
        self.jump_image = pygame.image.load("assets/ski_bg.jpg")
        self.skier_image = pygame.transform.scale(self.skier_image, (self.PLAYER_WIDTH, self.PLAYER_HEIGHT))
        self.jump_image = pygame.transform.scale(self.jump_image, (self.WIDTH, self.HEIGHT))
       


    def display_text(self, text, color, y_offset=0):
        text_surface = self.font.render(text, True, color)
        text_rect = text_surface.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 2 + y_offset))
        self.screen.blit(text_surface, text_rect)

    #These functions are: What changes when the game moves into this state?
    def start_game(self):

         #NEED TO FIGURE OUT IF I ALSO NEED A SEPARATE RESTART_GAME FUCTION OR THIS WORKS FOR BOTH
        #put up start screen with play button and rules
        pass

    def begin_jump(self):
        pass

    #when player reaches bottom of the jump, this function gets performed once
    def jump_measuring(self):
        self.velocity_y *= -0.3  # Change direction
        time_since_reaching_bottom = time.time()
        
    def jump(self):
        #use jump percent to change y velolcity to move down
        #jump percent will be a usable number by now
        if self.timing_percent == 0:
            self.velocity_x=0
            self.velocity_y = 4
        else:
            self.velocity_x = 3
            self.velocity_y = 2.2/self.timing_percent

    def game_over(self):
        pass

    def calc_jump(self):
        self.timing_percent = ((self.player_x * 6.25 / self.WIDTH) - (41/16))/(27/16)
        #TODO: find what decay I need to set to reach the very end, then multiply that by timing_percent
        pass

    def restart(self):
        self.player_x=0
        self.player_y = 0
        self.velocity_x = self.INITIAL_VELOCITY * math.cos(math.radians(50))
        self.velocity_y = self.INITIAL_VELOCITY * math.sin(math.radians(50))
        self.timing_percent = 0


    def run(self):

        while True:
            # user input based state changes go here
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        #start screen --> top of jump
                        self.fsm.process("space_bar")
                    elif event.key == pygame.K_SPACE and self.fsm.current_state == self.JUMP_CALCULATOR:
                        self.fsm.process("hit_jump")
                    elif event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
            self.update()
            self.draw()

            # Update display
            pygame.display.flip()

            # Cap the frame rate
            self.clock.tick(self.FPS)

    def update(self):
        #calculation / computer based state changes go here


        if self.fsm.current_state == self.GOING_DOWN_JUMP:
            self.player_x += self.velocity_x
            self.player_y += self.velocity_y

            #flips to jump measure when skier reaches minimum of jump
            if self.player_x > self.WIDTH *10/26 :
                #going down jump --> jump calculator
                self.fsm.process("reached_bottom")
        #check if player jumped and just landed
        if self.fsm.current_state == self.JUMPING:
            self.player_x += self.velocity_x
            self.player_y += self.velocity_y
            if self.player_y > self.HEIGHT * 0.75:
                self.fsm.process("landed")
        elif self.fsm.current_state == self.JUMP_CALCULATOR or self.fsm.current_state == self.JUMP_CALCULATED:
            self.player_x += self.velocity_x
            self.player_y += self.velocity_y
            if self.player_x > self.WIDTH * (4.25/6.25): 
                #jump calculator --> game over
                self.fsm.process("end_of_jump")


    def draw(self):
        # Draw background
        self.screen.fill(self.WHITE)
        if self.fsm.current_state != self.START or self.fsm.current_state != self.GAME_OVER:
            # Draw jump image
            self.screen.blit(self.jump_image, (0, 0))

            # Draw skier
            self.screen.blit(self.skier_image, (self.player_x, self.player_y))


        # Display game state-specific text
        if self.fsm.current_state == self.START:
            self.display_text("Welcome to Ski Jump", self.RED, y_offset= self.WIDTH/-20)
            self.display_text("Press SPACE to Start", self.RED)
        elif self.fsm.current_state == self.GAME_OVER:
            self.display_text("Score: " + str(int(self.timing_percent *100)), self.RED, y_offset= self.WIDTH/-20)
            self.display_text("Press SPACE to Play Again", self.RED)
        else:
            self.display_text("Ski Jump", self.RED, y_offset= self.WIDTH*-0.3)

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