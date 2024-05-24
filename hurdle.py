import pygame
import pygame.mixer
import random
import sys

# Initialize Pygame
pygame.init()

# Initialize Pygame Mixer
pygame.mixer.init()

# Constants
WIDTH, HEIGHT = 1000, 400
GROUND_HEIGHT = HEIGHT - 80
FPS = 60
GRAVITY = 0.6
JUMP_SPEED = -12
INITIAL_HURDLE_SPEED = 5
SPEED_INCREMENT = 0.05
MIN_HURDLE_DISTANCE_START = 300
MIN_HURDLE_DISTANCE_MIN = 100
SCORE_INCREMENT = 1000
DISTANCE_DECREASE = 20
MAX_HURDLES_PER_FRAME = 2

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hurdle Game")

# Load and scale images
person_img = pygame.image.load('person.gif')
person_img = pygame.transform.scale(person_img, (50, 80))  # Resize person image
hurdle_img = pygame.image.load('hurdle.png')
hurdle_img = pygame.transform.scale(hurdle_img, (50, 50))  # Resize hurdle image
background_img = pygame.image.load('trackAndField.jpg')
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))
game_over_background_img = pygame.image.load('gameOver.jpg')
game_over_background_img = pygame.transform.scale(game_over_background_img, (WIDTH, HEIGHT))

# Load sound files
start_music = pygame.mixer.Sound('start.mp3')
bg_music = pygame.mixer.Sound('bgMusic.mp3')
game_over_sound = pygame.mixer.Sound('gameover.mp3')

# Function to display start screen
def show_start_screen():
    font_large = pygame.font.Font(None, 144)
    font_small = pygame.font.Font(None, 36)

    # Load a different background image for the start screen
    start_background_img = pygame.image.load('starting.jpg')
    start_background_img = pygame.transform.scale(start_background_img, (WIDTH, HEIGHT))

    running = True
    player_name = ""
    input_box = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 3 + 170, 300, 30)
    start_button_rect = pygame.Rect(WIDTH // 2 - 60, HEIGHT // 3 + 220, 120, 40)

    # Play start music
    start_music.play()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if player_name.strip() != "":
                        running = False  # Start game
                elif event.key == pygame.K_BACKSPACE:
                    player_name = player_name[:-1]
                else:
                    player_name += event.unicode
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Start game if mouse button is pressed
                if start_button_rect.collidepoint(event.pos):
                    if player_name.strip() != "":
                        running = False

        screen.blit(start_background_img, (0, 0))

        # Render game title
        start_text = font_large.render("HURDLE GAME", True, WHITE)
        start_rect = start_text.get_rect(center=(WIDTH // 2, HEIGHT // 6))

        outline_positions = [(-2, -2), (2, -2), (-2, 2), (2, 2)]
        for pos in outline_positions:
            screen.blit(start_text, (start_rect.x + pos[0], start_rect.y + pos[1]))

        # Render the original text in white
        screen.blit(start_text, start_rect)

        # Render instructions with white font color and black background
        instruction_text1 = font_small.render("   Instructions:   ", True, WHITE)
        instruction_rect1 = instruction_text1.get_rect(center=(WIDTH // 2, HEIGHT // 3))
        pygame.draw.rect(screen, BLACK, instruction_rect1)  # Black background
        screen.blit(instruction_text1, instruction_rect1)

        instruction_text2 = font_small.render("Press SPACE BAR to jump over hurdles.", True, WHITE)
        instruction_rect2 = instruction_text2.get_rect(center=(WIDTH // 2, HEIGHT // 3 + 40))
        screen.blit(instruction_text2, instruction_rect2)

        instruction_text3 = font_small.render("Avoid collision with hurdles to continue.", True, WHITE)
        instruction_rect3 = instruction_text3.get_rect(center=(WIDTH // 2, HEIGHT // 3 + 80))
        screen.blit(instruction_text3, instruction_rect3)

        # Render input prompt and input box below the instructions
        input_prompt = font_small.render("Enter Your Name:", True, WHITE)
        input_prompt_rect = input_prompt.get_rect(center=(WIDTH // 2, HEIGHT // 3 + 140))
        screen.blit(input_prompt, input_prompt_rect)

        pygame.draw.rect(screen, WHITE, input_box)
        font_input = pygame.font.Font(None, 24)
        input_text_surface = font_input.render(player_name, True, BLACK)
        input_text_x = input_box.x + input_box.width / 2 - input_text_surface.get_width() / 2
        screen.blit(input_text_surface, (input_text_x, input_box.y + 5))


        # Render start button with black font color and green background
        start_button_text = font_small.render("   START", True, BLACK)  # Use black font color
        pygame.draw.rect(screen, GREEN, start_button_rect)
        screen.blit(start_button_text, start_button_rect)

        pygame.display.flip()

    return player_name

# Define the Person class
class Person:
    def __init__(self):
        self.width, self.height = person_img.get_size()
        self.x = 50
        self.y = GROUND_HEIGHT - self.height
        self.vel_y = 0
        self.is_jumping = False

    def jump(self):
        if not self.is_jumping:
            self.vel_y = JUMP_SPEED
            self.is_jumping = True

    def update(self):
        self.y += self.vel_y
        self.vel_y += GRAVITY
        if self.y >= GROUND_HEIGHT - self.height:
            self.y = GROUND_HEIGHT - self.height
            self.vel_y = 0
            self.is_jumping = False

    def draw(self):
        screen.blit(person_img, (self.x, self.y))

# Define the Hurdle class
class Hurdle:
    def __init__(self, x, speed):
        self.width, self.height = hurdle_img.get_size()
        self.x = x
        self.y = GROUND_HEIGHT - self.height
        self.vel_x = speed

    def update(self):
        self.x -= self.vel_x

    def draw(self):
        screen.blit(hurdle_img, (self.x, self.y))

# Generate hurdles
def generate_hurdles(last_hurdle_x, score):
    hurdles = []
    max_distance = max(MIN_HURDLE_DISTANCE_MIN, MIN_HURDLE_DISTANCE_START - (score // SCORE_INCREMENT) * DISTANCE_DECREASE)
    
    num_hurdles = min(MAX_HURDLES_PER_FRAME, 1 + score // SCORE_INCREMENT)
    
    for _ in range(num_hurdles):
        distance = random.randint(max_distance // 2, max_distance)
        new_hurdle_x = last_hurdle_x + distance
        new_hurdle = Hurdle(new_hurdle_x, INITIAL_HURDLE_SPEED + (score // SCORE_INCREMENT) * SPEED_INCREMENT)
        hurdles.append(new_hurdle)
        last_hurdle_x = new_hurdle_x + distance
    
    return hurdles, last_hurdle_x

# Main game function
def main():
    person = Person()
    hurdles = []
    next_hurdle_x = WIDTH
    score = 0
    highest_score = 0  # Initialize the highest score

    font_large = pygame.font.Font(None, 72)
    font_bold_large = pygame.font.Font(None, 144)
    font_small = pygame.font.Font(None, 36)
    font_color = (255, 255, 255)
    clock = pygame.time.Clock()
    game_over = False

    # Get player's name from the start screen
    player_name = show_start_screen()

    # Stop start music
    start_music.stop()

    # Play background music
    bg_music.play(-1)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if not game_over:
                        person.jump()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if game_over:
                    # Check if the retry button is clicked
                    retry_rect = pygame.Rect(WIDTH // 2 - 50, HEIGHT // 2 + 90, 100, 40)
                    if retry_rect.collidepoint(event.pos):
                        game_over = False
                        person = Person()
                        hurdles = []
                        next_hurdle_x = WIDTH
                        score = 0
                        # Stop game over sound
                        game_over_sound.stop()
                        # Play background music
                        bg_music.play(-1)
                    # Check if the quit button is clicked
                    quit_rect = pygame.Rect(WIDTH // 2 - 50, HEIGHT // 2 + 150, 100, 40)
                    if quit_rect.collidepoint(event.pos):
                        pygame.quit()
                        sys.exit()

        if not game_over:
            person.update()

            new_hurdles, next_hurdle_x = generate_hurdles(next_hurdle_x, score)
            hurdles.extend(new_hurdles)

        # Render the main background
        if game_over:
            screen.blit(game_over_background_img, (0, 0))
        else:
            screen.blit(background_img, (0, 0))

        for hurdle in hurdles:
            if not game_over:
                hurdle.update()
            hurdle.draw()

            if hurdle.x < -50:
                hurdles.remove(hurdle)
                if not game_over:
                    score += 100  # Increment score when hurdle is passed

            hurdle_rect = pygame.Rect(hurdle.x, hurdle.y, hurdle.width, hurdle.height)
            person_rect = pygame.Rect(person.x, person.y, person.width, person.height)
            if person_rect.colliderect(hurdle_rect):
                game_over = True
                highest_score = max(highest_score, score)  # Update highest score

        person.draw()

        score_text = font_large.render(f"Score: {score}", True, font_color)
        text_rect = score_text.get_rect(center=(WIDTH // 2, 40))
        screen.blit(score_text, text_rect)

        player_name_text = font_small.render(f"Player: {player_name}", True, font_color)
        player_name_rect = player_name_text.get_rect(center=(WIDTH // 2, 80))
        screen.blit(player_name_text, player_name_rect)

        if game_over:
            # Stop background music
            bg_music.stop()

            # Play game over sound
            game_over_sound.play()

            # Render game over text
            game_over_text = font_bold_large.render(" Game Over! ", True, font_color)
            game_over_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 3 + 50))
            pygame.draw.rect(screen, RED, game_over_rect)
            screen.blit(game_over_text, game_over_rect)

            # Render highest score text
            highest_score_text = font_small.render(f" Highest Score: {highest_score} ", True, font_color)
            highest_score_rect = highest_score_text.get_rect(center=(WIDTH // 2, HEIGHT // 3 + 120))
            pygame.draw.rect(screen, BLUE, highest_score_rect.inflate(10, 10))
            screen.blit(highest_score_text, highest_score_rect)

            # Render retry button
            retry_text = font_small.render("     Retry     ", True, BLACK)
            retry_rect = retry_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 100))
            pygame.draw.rect(screen, GREEN, retry_rect)
            screen.blit(retry_text, retry_rect)

            # Render quit button
            quit_text = font_small.render("     Quit     ", True, WHITE)
            quit_rect = quit_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 160))
            pygame.draw.rect(screen, RED, quit_rect)
            screen.blit(quit_text, quit_rect)

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
0