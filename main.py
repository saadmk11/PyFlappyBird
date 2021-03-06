import random
import sys

import pygame


class FlappyBirdGame:
    """Implementation of The Flappy Bird Game Using Python"""

    # pygame needs to be initialized 
    # before any method of the pygame module can be used
    pygame.init()

    # This handles the framerate of the game
    CLOCK = pygame.time.Clock()
    
    # Game Font to display Score
    GAME_FONT = pygame.font.Font('assets/font.ttf', 40)
    
    # Game screen Height and Weight
    SCREEN_HEIGHT = 1024
    SCREEN_WIDTH = 576

    # Floor Height on The Screen
    FLOOR_HEIGHT = 900

    # The main Game Screen
    GAME_SCREEN = pygame.display.set_mode(
        (SCREEN_WIDTH, SCREEN_HEIGHT)
    )

    # Background of the Game
    BACKGROUND_SURFACE = pygame.transform.scale2x(
        pygame.image.load('assets/background-day.png').convert()
    )
    # Floor of the Game
    FLOOR_SURFACE = pygame.transform.scale2x(
        pygame.image.load('assets/base.png').convert()
    )
    # Bird
    BIRD_SURFACE = pygame.transform.scale2x(
        pygame.image.load('assets/redbird-midflap.png').convert_alpha()
    )
    # Pipe
    PIPE_SURFACE = pygame.transform.scale2x(
        pygame.image.load('assets/pipe-red.png').convert()
    )
    # Game over screen
    GAME_OVER_SURFACE = pygame.transform.scale2x(
        pygame.image.load('assets/message.png').convert_alpha()
    )
    # Position the Game over Surface on Center using rectangle
    GAME_OVER_RECT = GAME_OVER_SURFACE.get_rect(
        center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    )
    
    # Pipe Heights that will be chosen randomly
    PIPE_HEIGHT_CHOICES = [400, 600, 800]

    # Speed at which the bird will fall
    GRAVITY = 0.22

    # Create an event that will be used in the timer
    # to spawn pipes on the screen
    SPAWN_PIPE = pygame.USEREVENT
    # Speed at which the pipes will spawn
    PIPE_SPEED = 1400  # milliseconds
    # timer used to spawn pipes
    pygame.time.set_timer(SPAWN_PIPE, PIPE_SPEED)

    def __init__(self):
        # State of the Game (running or game over)
        self.active = True
        # Score of the player
        self.score = 0
        # Used to change position of the bird (Jump/Fall)
        self.bird_movement = 0
        # List of spawned pipes
        self.pipe_list = []
        # Used to keep the floor moving
        self.floor_x_position = 0
        self.score_lock = False
        # Create rectangle around the bird to easily detect collision
        self.bird_rect = self.BIRD_SURFACE.get_rect(
            center=(100, self.SCREEN_HEIGHT / 2)
        )

    def create_pipe(self):
        """Create top and bottom pipe and add to the pipe list"""
        # Randomly Select a pipe height
        random_pipe_position = random.choice(self.PIPE_HEIGHT_CHOICES)
        # Create Bottom Pipe
        bottom_pipe = self.PIPE_SURFACE.get_rect(
            midtop=(700, random_pipe_position)
        )
        # Create Top Pipe
        top_pipe = self.PIPE_SURFACE.get_rect(
            midbottom=(700, random_pipe_position - 300)
        )
        # Add created pipes to the pipe list
        self.pipe_list.extend([bottom_pipe, top_pipe])

    def move_pipes(self):
        """Moves pipes on the screen"""
        # # move pipes x center by -5
        for pipe in self.pipe_list:
            pipe.centerx -= 5

            # keep pipes only if the right is > -50 (Outside of the screen)
            if not pipe.right > -50:
                self.pipe_list.remove(pipe)

    def draw_pipes(self):
        """Draw pipes on the screen"""
        for pipe in self.pipe_list:
            # top pipe
            if pipe.bottom >= self.SCREEN_HEIGHT:
                self.GAME_SCREEN.blit(self.PIPE_SURFACE, pipe)
            else:
                # bottom pipe (Flip the pipe position)
                flip_pipe = pygame.transform.flip(
                    self.PIPE_SURFACE, False, True
                )
                self.GAME_SCREEN.blit(flip_pipe, pipe)

    def draw_floor(self):
        """Draw moving floor on the screen"""
        if self.floor_x_position <= -self.SCREEN_WIDTH:
            # Reset floor_x_position if its <= screen width
            self.floor_x_position = 0
        else:
            self.floor_x_position -= 1
        
        # Add two floor surfaces together
        # and move them by -1 on each display update
        self.GAME_SCREEN.blit(
            self.FLOOR_SURFACE,
            (self.floor_x_position, self.FLOOR_HEIGHT)
        )
        self.GAME_SCREEN.blit(
            self.FLOOR_SURFACE,
            (self.floor_x_position + self.SCREEN_WIDTH, self.FLOOR_HEIGHT)
        )

    def draw_background(self):
        """Draw background on the screen"""
        self.GAME_SCREEN.blit(self.BACKGROUND_SURFACE, (0, 0))

    def draw_game_over_surface(self):
        """Draw game over surface on the screen"""
        self.GAME_SCREEN.blit(
            self.GAME_OVER_SURFACE, self.GAME_OVER_RECT
        )

    def move_bird(self):
        """Move the flappy bird on the screen"""
        # Increase movement by gravity so that the bird falls
        self.bird_movement += self.GRAVITY
        self.bird_rect.centery += self.bird_movement
        # Draw the bird
        self.GAME_SCREEN.blit(self.BIRD_SURFACE, self.bird_rect)

    def check_no_collision(self):
        """Check if the bird collided with any pipe 
        or fallen down or jumped above the screen"""
        for pipe in self.pipe_list:
            # Check if the bird is colliding with any pipe
            if self.bird_rect.colliderect(pipe):
                self.score_lock = False
                return False
        # Check if the bird is outside of the playable screen
        if (
            self.bird_rect.top <= -100 or
            self.bird_rect.bottom >= self.FLOOR_HEIGHT
        ):
            self.score_lock = False
            return False

        return True

    def update_score(self):
        """Update Score of the player"""
        for pipe in self.pipe_list:
            # Check if the bird is between the pipes
            if 95 < pipe.centerx < 105 and not self.score_lock:
                self.score += 1
                self.score_lock = True
            if pipe.centerx < 0:
                self.score_lock = False

    def display_score(self):
        """Display Score of the player on the screen"""
        score_str = (
            str(self.score)
            if self.active
            else f'Your Score: {self.score}'
        )
        # Display score on the top center of the screen
        score_surface = self.GAME_FONT.render(
            score_str, True, (255, 255, 255)
        )
        score_rect = score_surface.get_rect(
            center=(self.SCREEN_WIDTH / 2, 100)
        )
        self.GAME_SCREEN.blit(score_surface, score_rect)

    def reset(self):
        """Reset the game to it's initial state"""
        self.active = True
        self.score = 0
        self.bird_movement = 0
        self.floor_x_position = 0
        self.pipe_list = []
        self.score_lock = False
        self.bird_rect = self.BIRD_SURFACE.get_rect(
            center=(100, self.SCREEN_HEIGHT / 2)
        )

    def start(self):
        """Entry Point to the Game, Game starts when this method is invoked"""
        # Game Event Loop
        while True:
            # Draw Game Background
            self.draw_background()

            # Draw the moving floor
            self.draw_floor()

            for event in pygame.event.get():
                # Exit the game when the cross icon is clicked
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # Space Key Pressed
                if (
                    event.type == pygame.KEYDOWN and
                    event.key == pygame.K_SPACE
                ):
                    # Update the bird movement by -12 to let the bird jump
                    # when pressed space and the game is active/running
                    if self.active:
                        self.bird_movement = -12
                    else:
                        # Reset the game if the game is not running
                        # when space key is pressed
                        self.reset()

                # Spawn a pair of new pipes using the timer event
                if event.type == self.SPAWN_PIPE:
                    self.create_pipe()

            if self.active:
                # keep the bird moving (Jump/Fall) while the game is running
                self.move_bird()
                # Check for collision and set active state
                self.active = self.check_no_collision()

                # keep the pipes moving while the game is running
                self.move_pipes()
                self.draw_pipes()

                # Update player Score
                self.update_score()
                # Display Player Score on the screen
                self.display_score()
            else:
                # Show Game over Screen
                self.draw_game_over_surface()
                # Display Player Score on the screen
                self.display_score()

            # Update the Display
            pygame.display.update()
            # Set refresh rate to 120
            self.CLOCK.tick(120)


if __name__ == '__main__':
    # Initialize and Start the Game when the file runs directly
    game = FlappyBirdGame()
    game.start()
