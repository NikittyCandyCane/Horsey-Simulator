
# Import libraries
import pygame
import time
import random
from random import choice

# Initialize pygame and sound mixer
pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((1200, 750))

# Set variables that are used later
game_status = 'menu'
soundplayed = False
time_since_last_idle = 0
time_until_next_idle = random.randint(3000,8000)
current_anim = "idle"
idle_delay_set_yet = False
clock = pygame.time.Clock()

START_BTN_POS = (630,175)
EXIT_BTN_POS = (630,425)

HORSE_SCALE = {
     'scale': 8,
     'delay': 30,
     'last_update': 0
}

HORSE_X = -30
HORSE_Y = 130

#UNPACK TUPLES
(START_BTN_POS_X, START_BTN_POS_Y) = (START_BTN_POS)
(EXIT_BTN_POS_X, EXIT_BTN_POS_Y) = (EXIT_BTN_POS)

# Load Images and sounds
start_btn = pygame.image.load('image start button.png')
exit_btn = pygame.image.load('image finish button.png')

btn_hover_sound = pygame.mixer.Sound('sound button click.mp3')

start_btn = pygame.transform.scale_by(start_btn, 0.8)
exit_btn = pygame.transform.scale_by(exit_btn, 0.8)

# Create rectangles for collision detection
start_btn_rect = pygame.Rect(START_BTN_POS_X, START_BTN_POS_Y, 448*0.8, 170*0.8)
exit_btn_rect = pygame.Rect(EXIT_BTN_POS_X, EXIT_BTN_POS_Y, 445*0.8, 168*0.8)

# Set Icon and Caption
pygame.display.set_caption('Horsey Simulator')

# Load original unscaled
horse_still_original = pygame.image.load('/Users/nicolezhang/MyCode/Horse animations basic/tile001.png')

# Make scaled versions for menu and animation
horse_still = pygame.transform.scale_by(horse_still_original, 8)
horse_still_for_scaling = pygame.transform.scale_by(horse_still_original, HORSE_SCALE['scale'])

# horse_tail_swish = [pygame.image.load('tile000.png'), pygame.image.load('tile001.png'), pygame.image.load('tile002.png'), pygame.image.load('tile003.png'), pygame.image.load('tile004.png'), pygame.image.load('tile05.png'), pygame.image.load('tile006.png'), pygame.image.load('tile007.png'), pygame.image.load('tile008.png'), pygame.image.load('tile009.png')]
# horse_graze = [pygame.image.load('tile0010.png'), pygame.image.load('tile011.png'), pygame.image.load('tile012.png'), pygame.image.load('tile013.png'), pygame.image.load('tile014.png'), pygame.image.load('tile015.png'), pygame.image.load('tile016.png')]
# horse_walk = [pygame.image.load('tile018.png'), pygame.image.load('tile019.png'), pygame.image.load('tile020.png'), pygame.image.load('tile021.png'), pygame.image.load('tile022.png'), pygame.image.load('tile023.png'), pygame.image.load('tile024.png'), pygame.image.load('tile025.png'), pygame.image.load('tile026.png')]
# horse_canter = [pygame.image.load('tile027.png'), pygame.image.load('tile028.png'), pygame.image.load('tile029.png'), pygame.image.load('tile030.png'), pygame.image.load('tile031.png'), pygame.image.load('tile032.png'), pygame.image.load('tile033.png'), pygame.image.load('tile034.png')]
# horse_gallop = [pygame.image.load('tile036.png'), pygame.image.load('tile037.png'), pygame.image.load('tile038.png'), pygame.image.load('tile039.png'), pygame.image.load('tile040.png'), pygame.image.load('tile041.png')]
# horse_jump = [pygame.image.load('jump00.png'), pygame.image.load('jump01.png'), pygame.image.load('jump02.png'), pygame.image.load('jump03.png'), pygame.image.load('jump04.png'), pygame.image.load('jump05.png'), pygame.image.load('jump06.png'), pygame.image.load('jump07.png'), pygame.image.load('jump08.png'), pygame.image.load('jump09.png'), pygame.image.load('jump10.png'), pygame.image.load('jump11.png'), pygame.image.load('jump12.png'), pygame.image.load('jump13.png'), pygame.image.load('jump14.png')]

horse_tail_swish = []
for i in range(0,9):
     img_horse_tail_swish = pygame.transform.scale_by(pygame.image.load(f'/Users/nicolezhang/MyCode/Horse animations basic/tile00{i}.png'), (HORSE_SCALE["scale"]))
     horse_tail_swish.append(img_horse_tail_swish)

horse_graze = []
for i in range(10,17):
     img_horse_graze = pygame.transform.scale_by(pygame.image.load(f'/Users/nicolezhang/MyCode/Horse animations basic/tile0{i}.png'), (HORSE_SCALE['scale']))
     horse_graze.append(img_horse_graze)

parallax_bg = []
for i in range(320):
     i = f"{i:03}"
     img_parallax_bg = pygame.transform.scale_by(pygame.image.load(f'/Users/nicolezhang/MyCode/Parallax background/frame_{i}_delay-0.05s.gif'), (1.39))
     parallax_bg.append(img_parallax_bg)

# Animation Dictionaries
horse_tail_anim = {
    "frames": horse_tail_swish,       # List of images
    "index": 0,                       # Current frame index
    "last_update": 0,                # When it last changed frames
    "delay": 200,                    # How often it updates (in ms)
    "pos": (HORSE_X, HORSE_Y)                 # Where to draw the image
}

horse_graze_anim = {
    "frames": horse_graze,       # List of images
    "index": 0,                       # Current frame index
    "last_update": 0,                # When it last changed frames
    "delay": 350,                    # How often it updates (in ms)
    "pos": (HORSE_X, HORSE_Y)                 # Where to draw the image
}

horse_walk_anim = {
    "frames": horse_tail_swish,       # List of images
    "index": 0,                       # Current frame index
    "last_update": 0,                # When it last changed frames
    "delay": 200,                    # How often it updates (in ms)
    "pos": (HORSE_X, HORSE_Y)                 # Where to draw the image
}

horse_jump_anim = {
    "frames": horse_tail_swish,       # List of images
    "index": 0,                       # Current frame index
    "last_update": 0,                # When it last changed frames
    "delay": 200,                    # How often it updates (in ms)
    "pos": (HORSE_X, HORSE_Y)                 # Where to draw the image
}

horse_canter_anim = {
    "frames": horse_tail_swish,       # List of images
    "index": 0,                       # Current frame index
    "last_update": 0,                # When it last changed frames
    "delay": 200,                    # How often it updates (in ms)
    "pos": (HORSE_X, HORSE_Y)                 # Where to draw the image
}

horse_gallop_anim = {
    "frames": horse_tail_swish,       # List of images
    "index": 0,                       # Current frame index
    "last_update": 0,                # When it last changed frames
    "delay": 200,                    # How often it updates (in ms)
    "pos": (HORSE_X, HORSE_Y)                 # Where to draw the image
}

parallax_bg_anim = {
    "frames": parallax_bg,       # List of images
    "index": 0,                       # Current frame index
    "last_update": 0,                # When it last changed frames
    "delay": 30,                    # How often it updates (in ms)
    "pos": (0, 0)                 # Where to draw the image
}

pygame.mixer.music.load("Royale High Campus 3 Music - Castle Dorms (Flowering & Tidalglow).mp3")
pygame.mixer.music.set_volume(0.4)
pygame.mixer.music.play(-1)

# Functions

def update_animation(anim):
    global current_anim
    global idle_delay_set_yet
    global idle_delay

    current_time = pygame.time.get_ticks()

    if current_time - anim["last_update"] >= anim["delay"]:
        anim["last_update"] = current_time
        anim["index"] = (anim["index"] + 1) % len(anim["frames"])
        if anim['index'] == 0:
            current_anim = 'idle'
            
    # Blit the current frame (after fixing index logic)
    #anim["frames"][anim["index"]] = pygame.transform.scale_by(anim["frames"][anim["index"]], (HORSE_SCALE['scale']))
    screen.blit(anim["frames"][anim["index"]], anim["pos"])

def shrink_horse():
    global horse_still_for_scaling
    current_time = pygame.time.get_ticks()

    if current_time - HORSE_SCALE['last_update'] >= HORSE_SCALE['delay']:
        HORSE_SCALE['last_update'] = current_time
        HORSE_SCALE['scale'] -= 0.5

        if HORSE_SCALE['scale'] < 2.1:
            HORSE_SCALE['scale'] = 2.1

        # Rescale the original image, not the already scaled one
        horse_still_for_scaling = pygame.transform.scale_by(horse_still_original, HORSE_SCALE['scale'])

    # Original image dimensions
    orig_width, orig_height = horse_still_original.get_size()

    # New scaled image dimensions
    new_width, new_height = horse_still_for_scaling.get_size()

    # Calculate the original center position of the horse on the screen
    center_x = HORSE_X + orig_width // 2
    center_y = HORSE_Y + orig_height // 2

    # Calculate new top-left so scaled image stays centered on original center
    new_x = center_x - new_width // 2
    new_y = center_y - new_height // 2

    # Draw the scaled horse at the new position
    screen.blit(horse_still_for_scaling, (new_x, new_y))

    print(f"Scale: {HORSE_SCALE['scale']}")
    print(f"Original size: {orig_width}x{orig_height}")
    print(f"Scaled size: {new_width}x{new_height}")
    print(f"Center: ({center_x}, {center_y})")
    print(f"Blitting at: ({new_x}, {new_y})")

def update_screen(game_status):
    if game_status == 'menu':
            global time_since_last_idle
            global time_until_next_idle
            global current_anim

            #global frame_horse_tail_swish
            screen.blit(parallax_bg[0], (0,0))

            # screen.blit(horse,(-30,200))
            screen.blit(start_btn,(630,175))
            screen.blit(exit_btn,(630,425))
            current_time = pygame.time.get_ticks()
            if current_time - time_since_last_idle >= time_until_next_idle:
                    current_anim = choice(["tail", "graze"])
                    time_since_last_idle = current_time
                    time_until_next_idle = random.randint(3000,8000)
            if current_anim == "idle":
                screen.blit(horse_still, (HORSE_X, HORSE_Y))
            elif current_anim == "graze":
                update_animation(horse_graze_anim)
            elif current_anim == "tail":
                update_animation(horse_tail_anim)
            pygame.display.update()

    elif game_status == 'playing':
         screen.blit(parallax_bg[0], (0,0))
         if HORSE_SCALE['scale'] > 2:
          shrink_horse()
         pygame.display.update()

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.mixer.quit()
            pygame.quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if start_btn_rect.collidepoint(pygame.mouse.get_pos()):
                game_status = 'playing'
    if start_btn_rect.collidepoint(pygame.mouse.get_pos()) or exit_btn_rect.collidepoint(pygame.mouse.get_pos()):
        if soundplayed == False:
            pygame.mixer.Sound.play(btn_hover_sound)
            soundplayed = True
            
    else:
         soundplayed = False
    clock.tick(60)
    update_screen(game_status)