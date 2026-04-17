import pygame
import sys
import random
import os

# Init
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()

WIDTH, HEIGHT = 1200, 675
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Modi")

clock = pygame.time.Clock()
font = pygame.font.Font(None, 50)

# Load images
bird_img = pygame.image.load("assets/bird.png")
bg_img = pygame.image.load("assets/bg.png")

bg_img = pygame.transform.scale(bg_img, (WIDTH, HEIGHT))
bird_img = pygame.transform.scale(bird_img, (150, 100))

# Sounds
pygame.mixer.music.load("assets/bg_music.mp3")
pygame.mixer.music.set_volume(0.5)
hit_sound = pygame.mixer.Sound("assets/hit.wav")

# Pipes
pipe_images = []
for file in os.listdir("assets"):
    if "pipe" in file.lower():
        img = pygame.image.load(f"assets/{file}")
        img = pygame.transform.scale(img, (156, 354))
        pipe_images.append(img)

# Bird
bird_x = 150
bird_y = HEIGHT // 2
bird_velocity = 0
gravity = 0.7

# Pipes
pipes = []
pipe_gap = 350

# Score
score = 0
high_score = 0

# Load high score
if os.path.exists("highscore.txt"):
    with open("highscore.txt", "r") as f:
        high_score = int(f.read())

game_active = False

def save_high_score():
    with open("highscore.txt", "w") as f:
        f.write(str(high_score))

def create_pipe():
    pipe_img = random.choice(pipe_images)
    gap_y = random.randint(200, HEIGHT - 200)

    top = pipe_img.get_rect(midbottom=(WIDTH + 150, gap_y - pipe_gap // 2))
    bottom = pipe_img.get_rect(midtop=(WIDTH + 150, gap_y + pipe_gap // 2))

    return [pipe_img, top, bottom, False]

def reset_game():
    global bird_y, bird_velocity, pipes, score
    bird_y = HEIGHT // 2
    bird_velocity = 0
    pipes = [create_pipe()]
    score = 0

pipes.append(create_pipe())

while True:
    screen.blit(bg_img, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            save_high_score()
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if game_active:
                    bird_velocity = -12
                else:
                    game_active = True
                    reset_game()
                    pygame.mixer.music.play(-1)

    if game_active:
        # Bird physics
        bird_velocity += gravity
        bird_y += bird_velocity

        # Bird rotation animation
        rotated_bird = pygame.transform.rotate(bird_img, -bird_velocity * 3)
        bird_rect = rotated_bird.get_rect(center=(bird_x, bird_y))
        screen.blit(rotated_bird, bird_rect.topleft)

        # Pipes
        for pipe in pipes:
            pipe_img, top_rect, bottom_rect, scored = pipe

            top_rect.x -= 4
            bottom_rect.x -= 4

            flipped = pygame.transform.flip(pipe_img, False, True)

            screen.blit(flipped, top_rect)
            screen.blit(pipe_img, bottom_rect)

        # Spawn pipes
        if pipes[-1][1].x < WIDTH - 400:
            pipes.append(create_pipe())

        # Collision
        for pipe in pipes:
            _, top_rect, bottom_rect, _ = pipe

            if bird_rect.colliderect(top_rect) or bird_rect.colliderect(bottom_rect):
                hit_sound.play()
                pygame.mixer.music.stop()
                game_active = False

        # Boundaries
        if bird_y > HEIGHT or bird_y < 0:
            hit_sound.play()
            pygame.mixer.music.stop()
            game_active = False

        # Score
        for pipe in pipes:
            if pipe[1].x < bird_x and not pipe[3]:
                score += 1
                pipe[3] = True

        # High score update
        if score > high_score:
            high_score = score

        # Display score
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        high_text = font.render(f"High Score: {high_score}", True, (255, 255, 0))

        screen.blit(score_text, (20, 20))
        screen.blit(high_text, (20, 70))

    else:
        title = font.render("Press SPACE to Start", True, (255, 255, 255))
        score_text = font.render(f"Score: {score}", True, (255, 255, 0))
        high_text = font.render(f"High Score: {high_score}", True, (255, 255, 255))

        screen.blit(title, (WIDTH // 2 - 220, HEIGHT // 2 - 60))
        screen.blit(score_text, (WIDTH // 2 - 80, HEIGHT // 2))
        screen.blit(high_text, (WIDTH // 2 - 120, HEIGHT // 2 + 60))

    pygame.display.update()
    clock.tick(60)