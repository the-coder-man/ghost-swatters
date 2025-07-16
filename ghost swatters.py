# ghost swatters game
# A simple game where you swat ghosts using hand motion detection with OpenCV and Pygame.
# The game uses your computer's webcam to detect hand movements and swat ghosts that appear on the screen.
# The player earns points by swatting ghosts, and the game ends when a ghost reaches the bottom of the screen.
import cv2
import pygame
import random
import sys


# Initialize Pygame and basic setup
pygame.init()
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Ghost Swatters")
clock = pygame.time.Clock()

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)

# Initialize sound
pygame.mixer.init()
pygame.mixer.music.load("muisc/halloween-248129.mp3")
pygame.mixer.music.play(loops=-1)
pygame.mixer.music.set_volume(0.7)

# Load assets
player_img = pygame.Surface((50, 50))
player_img.fill(white)
ghost_img = pygame.Surface((40, 40))
ghost_img.fill(red)

# Font
pygame.font.init()
font = pygame.font.SysFont(None, 36)

def draw_text(text, x, y):
    img = font.render(text, True, white)
    screen.blit(img, (x, y))

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)
        self.image = player_img
        self.rect = self.image.get_rect(center=(width // 2, height - 60))
        self.last_valid_hand_x = self.rect.centerx / width  # track last valid hand position

    def update(self, *args, **kwargs):
        hand_x = kwargs.get('hand_x', None)
        if hand_x is not None:
            self.last_valid_hand_x = hand_x
        self.rect.centerx = int(hand_x * width)
        self.rect.clamp_ip(screen.get_rect())
# ghost class
class Ghost(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)
        self.image = pygame.image.load("assets/ghost-156969_1280.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.rect = self.image.get_rect(center=(random.randint(20, width - 20), -20))
        self.speed = random.randint(3, 7)
    def update(self, *args, **kwargs):
        self.rect.y += self.speed
        if self.rect.top > height:
            global game_over
            game_over = True

# Initialize sprites
player = Player()
player_group = pygame.sprite.Group()
player_group.add(player)
ghosts = pygame.sprite.Group()

# Initialize webcam and motion detection
cap = cv2.VideoCapture(1)
bg_subtractor = cv2.createBackgroundSubtractorMOG2(history=50, varThreshold=25)
hand_x_history = []  # For smoothing
last_known_hand_x = 0.5  # Start in the middle

# Game state variables
game_over = False
spawn_timer = 0
score = 0

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN and game_over:
            game_over = False
            ghosts.empty()
            player.rect.center = (width // 2, height - 60)
            score = 0
            spawn_timer = 0
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                cap.release()
                pygame.quit()
                sys.exit()
        if event.type == pygame.QUIT:
            cap.release()
            pygame.quit()
            sys.exit()

    ret, frame = cap.read()
    clock.tick(30)
    if not ret:
        print("Failed to grab frame")
        continue

    frame = cv2.flip(frame, 1)
    frame_resized = cv2.resize(frame, (width, height))
    gray = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2GRAY)
    fg_mask = bg_subtractor.apply(gray)
    _, thresh = cv2.threshold(fg_mask, 200, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    hand_x = None
    if contours:
        largest_contour = max(contours, key=cv2.contourArea)
        if cv2.contourArea(largest_contour) > 1000:
            x, y, w, h = cv2.boundingRect(largest_contour)
            raw_hand_x = x + w // 2
            hand_x_normalized = raw_hand_x / width
            player_group.update(hand_x=hand_x_normalized)
            # Smooth it
            hand_x_history.append(hand_x_normalized)
            if len(hand_x_history) > 5:
                hand_x_history.pop(0)
            hand_x = sum(hand_x_history) / len(hand_x_history)
   

    # Create a surface for the frame
    frame_surface = pygame.surfarray.make_surface(cv2.cvtColor(frame_resized, cv2.COLOR_BGR2RGB))
    screen.fill(black)
    screen.blit(frame_surface, (0, 0))
    # Draw the player and ghosts
    if hand_x is None:
        hand_x = width // 2 / width
    if contours:
        largest_contour = max(contours, key=cv2.contourArea)
        if cv2.contourArea(largest_contour) > 1000:
            x, y, w, h = cv2.boundingRect(largest_contour)
            raw_hand_x = x + w // 2
            hand_x_normalized = raw_hand_x / width
            player_group.update(hand_x=hand_x_normalized)
            # Smooth it
            hand_x_history.append(hand_x_normalized)
            if len(hand_x_history) > 5:
                hand_x_history.pop(0)
            hand_x = sum(hand_x_history) / len(hand_x_history)
            last_known_hand_x = hand_x


        screen.fill(black)
        screen.blit(frame_surface, (0, 0))

        if not game_over:
            player_group.update(hand_x=last_known_hand_x)
            player_group.draw(screen)

            
            spawn_timer += 1
            if spawn_timer > 30:
                ghosts.add(Ghost())
                spawn_timer = 0


                # Update and draw ghosts
            ghosts.update()
            ghosts.draw(screen)

            if hand_x is not None:
                collided_ghosts = pygame.sprite.spritecollide(player, ghosts, dokill=True)
                for ghost in collided_ghosts:
                    score += 1

            draw_text(f"Score: {score}", 10, 10)
        else:
            draw_text("GAME OVER", width // 2 - 80, height // 2 - 20)
            draw_text("Press any key to restart", width // 2 - 120, height // 2 + 20)
            draw_text(f"Final Score: {score}", width // 2 - 80, height // 2 + 60)

        pygame.display.flip()
        clock.tick(30)