import pygame
import random  # random number for pipe
import sys  # to exit we use sys.exit

from pygame import mixer


# background Sound


def draw_floor():
    pygame.display.set_caption('Flappy Bird at IUBAT')
    screen.blit(ground, (ground_x, 450))
    screen.blit(ground, (ground_x + 720, 450))  # double the base


def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop=(700, random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midbottom=(700, random_pipe_pos - 200))
    return top_pipe, bottom_pipe


def move_pipe(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    return pipes


def draw_pipe(pipes):
    for pipe in pipes:
        if pipe.bottom >= 1024:
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe, pipe)


def remove_pipes(pipes):
    for pipe in pipes:
        if pipe.centerx == -600:
            pipes.remove(pipe)
    return pipes


def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            death_sound.play()
            return False

    if bird_rect.top <= -100 or bird_rect.bottom >= 450:
        death_sound.play()
        return False

    return True


# Rotation
def rotate_bird(bird):
    new_bird = pygame.transform.rotozoom(bird, -bird_move * 3, 1)
    return new_bird


# animation
def bird_animation():
    new_bird = bird_frames[bird_index]
    new_bird_rect = new_bird.get_rect(center=(100, bird_rect.centery))
    return new_bird, new_bird_rect


def score_show(game_state):
    if game_state == 'main_game':
        score_surface = game_font.render(str(int(score)), True, (238, 250, 214))
        score_rect = score_surface.get_rect(center=(40, 30))
        screen.blit(score_surface, score_rect)
    if game_state == 'game_over':
        score_surface = game_font.render(f' Score: {(int(score))}', True, (238, 250, 214))
        score_rect = score_surface.get_rect(center=(70, 30))
        screen.blit(score_surface, score_rect)

        high_score_surface = game_font.render(f'High Score:{(int(high_score))}', True, (238, 250, 214))
        high_score_rect = high_score_surface.get_rect(center=(105, 70))
        screen.blit(high_score_surface, high_score_rect)


def update_score(score, high_score):
    if score > high_score:
        high_score = score
    return high_score


pygame.mixer.pre_init(frequency=44100, channels=1, buffer=512)
pygame.init()
screen = pygame.display.set_mode((720, 540))  # screen size and display
clock = pygame.time.Clock()
game_font = pygame.font.Font('04B_19.TTF', 30)

# game variable
gravity = 0.25
bird_move = 0
game_active = True
score = 0
high_score = 0

background = pygame.image.load('gallery/images/background.png').convert()  # we use convert() to speed up display
pygame.mixer.music.load('gallery/sounds/background.mp3')
pygame.mixer.music.play(-1)
# while the game is busy
# screen will stay  and when we click close button screen will close
ground = pygame.image.load('gallery/images/base.png').convert()
ground_x = 0
bird_downflap = pygame.transform.scale2x(pygame.image.load('gallery/images/red_downfall.png').convert_alpha())
bird_midflap = pygame.transform.scale2x(pygame.image.load('gallery/images/red_midfall.png').convert_alpha())
bird_upflap = pygame.transform.scale2x(pygame.image.load('gallery/images/red_up.png').convert_alpha())
bird_frames = [bird_downflap, bird_midflap, bird_upflap]
bird_index = 0
bird_surface = bird_frames[bird_index]
bird_rect = bird_surface.get_rect(center=(250, 150))
BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP, 200)

# bird_surface = pygame.image.load('gallery/images/bird.png').convert_alpha()
# bird_rect = bird_surface.get_rect(center=(250, 150))
pipe_surface = pygame.image.load('gallery/images/pipe.png').convert_alpha()
pipe_list = []
PIPE = pygame.USEREVENT
pygame.time.set_timer(PIPE, 1200)
pipe_height = [200, 300, 400]
game_over_surface = pygame.image.load('gallery/images/message.png').convert_alpha()
game_over_rect = game_over_surface.get_rect(center=(360, 270))
flap_sound = pygame.mixer.Sound('gallery/sounds/wing.wav')
death_sound = pygame.mixer.Sound('gallery/sounds/hit.wav')
score_sound = pygame.mixer.Sound('gallery/sounds/point.wav')
score_sound_count = 100
background_sound = pygame.mixer.Sound('gallery/sounds/background.mp3')

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                flap_sound.play()
                bird_move = 0
                bird_move -= 6.5

            if event.key == pygame.K_SPACE and game_active == False:
                game_active = True
                pipe_list.clear()
                bird_rect.center = (250, 150)
                bird_move = 0
                score = 0

        if event.type == PIPE:
            pipe_list.extend(create_pipe())

        if event.type == BIRDFLAP:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0
            bird_surface, bird_rect = bird_animation()

    screen.blit(background, (0, 0))  # to set the background image in our display if our image is smaller then we

    # need to increase the image size with pygame.transform.scale2x(background) =double ,in my case the image size
    # and the screen size is equal
    if game_active:
        # bird
        bird_move += gravity
        rotated_bird = rotate_bird(bird_surface)
        bird_rect.centery += bird_move
        screen.blit(rotated_bird, bird_rect)
        game_active = check_collision(pipe_list)

        # pipes
        pipe_list = move_pipe(pipe_list)
        pipe_list = remove_pipes(pipe_list)
        draw_pipe(pipe_list)

        score += 0.01
        score_show('main_game')
        score_sound_count -= 1
        if score_sound_count <= 0:
            score_sound.play()
            score_sound_count = 100
    else:
        screen.blit(game_over_surface, game_over_rect)
        high_score = update_score(score, high_score)
        score_show('game_over')
    ground_x -= 1  # moving ground to left
    draw_floor()
    if ground_x <= -720:
        ground_x = 0  # continuous moving ground

    pygame.display.update()
    clock.tick(70)  # control image speed
