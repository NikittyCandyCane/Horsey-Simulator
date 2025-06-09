
# Import libraries
import pygame
import time
import random
from random import choice

# Initialize pygame and sound mixer
pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((1200,750))

# Set variables that are used later
game_status = 'menu'
soundplayed = False
time_since_last_idle = 0
time_until_next_idle = random.randint(3000,8000)
current_anim = "idle"
idle_delay_set_yet = False

START_BTN_POS = (630,175)
EXIT_BTN_POS = (630,425)

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

# Animation Lists
horse_still = pygame.transform.scale_by(pygame.image.load('/Users/nicolezhang/MyCode/Horse animations basic/tile001.png'), (8))
# horse_tail_swish = [pygame.image.load('tile000.png'), pygame.image.load('tile001.png'), pygame.image.load('tile002.png'), pygame.image.load('tile003.png'), pygame.image.load('tile004.png'), pygame.image.load('tile05.png'), pygame.image.load('tile006.png'), pygame.image.load('tile007.png'), pygame.image.load('tile008.png'), pygame.image.load('tile009.png')]
# horse_graze = [pygame.image.load('tile0010.png'), pygame.image.load('tile011.png'), pygame.image.load('tile012.png'), pygame.image.load('tile013.png'), pygame.image.load('tile014.png'), pygame.image.load('tile015.png'), pygame.image.load('tile016.png')]
# horse_walk = [pygame.image.load('tile018.png'), pygame.image.load('tile019.png'), pygame.image.load('tile020.png'), pygame.image.load('tile021.png'), pygame.image.load('tile022.png'), pygame.image.load('tile023.png'), pygame.image.load('tile024.png'), pygame.image.load('tile025.png'), pygame.image.load('tile026.png')]
# horse_canter = [pygame.image.load('tile027.png'), pygame.image.load('tile028.png'), pygame.image.load('tile029.png'), pygame.image.load('tile030.png'), pygame.image.load('tile031.png'), pygame.image.load('tile032.png'), pygame.image.load('tile033.png'), pygame.image.load('tile034.png')]
# horse_gallop = [pygame.image.load('tile036.png'), pygame.image.load('tile037.png'), pygame.image.load('tile038.png'), pygame.image.load('tile039.png'), pygame.image.load('tile040.png'), pygame.image.load('tile041.png')]
# horse_jump = [pygame.image.load('jump00.png'), pygame.image.load('jump01.png'), pygame.image.load('jump02.png'), pygame.image.load('jump03.png'), pygame.image.load('jump04.png'), pygame.image.load('jump05.png'), pygame.image.load('jump06.png'), pygame.image.load('jump07.png'), pygame.image.load('jump08.png'), pygame.image.load('jump09.png'), pygame.image.load('jump10.png'), pygame.image.load('jump11.png'), pygame.image.load('jump12.png'), pygame.image.load('jump13.png'), pygame.image.load('jump14.png')]

horse_tail_swish = []
for i in range(0,9):
     img_horse_tail_swish = pygame.transform.scale_by(pygame.image.load(f'/Users/nicolezhang/MyCode/Horse animations basic/tile00{i}.png'), (8))
     horse_tail_swish.append(img_horse_tail_swish)

horse_graze = []
for i in range(10,17):
     img_horse_graze = pygame.transform.scale_by(pygame.image.load(f'/Users/nicolezhang/MyCode/Horse animations basic/tile0{i}.png'), (8))
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
    screen.blit(anim["frames"][anim["index"]], anim["pos"])

def update_screen(game_status):
    if game_status == 'menu':
            global time_since_last_idle
            global time_until_next_idle
            global current_anim
            #global frame_horse_tail_swish
            screen.fill((255,255,255))
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
            

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.mixer.quit()
            pygame.quit()
    if start_btn_rect.collidepoint(pygame.mouse.get_pos()) or exit_btn_rect.collidepoint(pygame.mouse.get_pos()):
        if soundplayed == False:
            pygame.mixer.Sound.play(btn_hover_sound)
            soundplayed = True
    else:
         soundplayed = False
    update_screen(game_status)