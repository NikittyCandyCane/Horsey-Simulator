
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
jumping = False

playing_start_time = None
initial_obstacle_wait = 5000 


obstacles = []
last_obstacle_time = 0
obstacle_spawn_delay = 2000  # ms

HORSE_POS_AFTER_SHRINK = (170,455)
HORSE_WALK_LOOP_COUNT = 0

START_BTN_POS = (630,175)
EXIT_BTN_POS = (630,425)

HORSE_SCALE = {
     'scale': 8,
     'delay': 30,
     'last_update': 0
}

HORSE_X = -30
HORSE_Y = 130


show_start_text = True
horse_y_pos_shrink = 455
horse_x_pos_shrink = 170
y_velocity = 0
jump_strength = 30  # how high the horse jumps
gravity = 2.3        # how fast the horse falls back down
ground_level = 455  # the normal horse y position

color_stage = 0
color_count = 0
color_change = 11.8

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

# Load original unscaled
horse_still_original = pygame.image.load('/Users/nicolezhang/MyCode/Horse animations basic/tile001.png')

# Set Icon and Caption
pygame.display.set_caption('Horsey Simulator')
pygame.display.set_icon(horse_still_original)

# Make scaled versions for menu and animation
horse_still = pygame.transform.scale_by(horse_still_original, 8)
horse_still_for_scaling = pygame.transform.scale_by(horse_still_original, HORSE_SCALE['scale'])

obstacle_images = [
    '/Users/nicolezhang/MyCode/Obstacles/log.png',
    '/Users/nicolezhang/MyCode/Obstacles/rock.png'
]

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

horse_jump = []
for i in range(14):
     i = f"{i:02}"
     img_horse_jump = pygame.transform.scale_by(pygame.image.load(f'/Users/nicolezhang/MyCode/Horse animation jump/jump{i}.png'), 3)
     horse_jump.append(img_horse_jump)

horse_canter = []
for i in range(27,35):
     img_horse_canter = pygame.transform.scale_by(pygame.image.load(f'/Users/nicolezhang/MyCode/Horse animations basic/tile0{i}.png'), 3)
     horse_canter.append(img_horse_canter)

horse_walk = []
for i in range(18,26):
     img_horse_walk = pygame.transform.scale_by(pygame.image.load(f'/Users/nicolezhang/MyCode/Horse animations basic/tile0{i}.png'), 3)
     horse_walk.append(img_horse_walk)

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
    "frames": horse_walk,       # List of images
    "index": 0,                       # Current frame index
    "last_update": 0,                # When it last changed frames
    "delay": 150,                    # How often it updates (in ms)
    "pos": (horse_x_pos_shrink, horse_y_pos_shrink)                 # Where to draw the image
}

horse_jump_anim = {
    "frames": horse_jump,       # List of images
    "index": 3,                       # Current frame index
    "last_update": 0,                # When it last changed frames
    "delay": 100,                    # How often it updates (in ms)
    "pos": [horse_x_pos_shrink, 455],               # Where to draw the image
    "jump_delay": 30,
    "jump_last_update": 0
}

horse_canter_anim = {
    "frames": horse_canter,       # List of images
    "index": 0,                       # Current frame index
    "last_update": 0,                # When it last changed frames
    "delay": 100,                    # How often it updates (in ms)
    "pos": (horse_x_pos_shrink, horse_y_pos_shrink)                # Where to draw the image
}

horse_gallop_anim = {
    "frames": horse_tail_swish,       # List of images
    "index": 0,                       # Current frame index
    "last_update": 0,                # When it last changed frames
    "delay": 200,                    # How often it updates (in ms)
    "pos": (horse_x_pos_shrink, horse_y_pos_shrink)                 # Where to draw the image
}

parallax_bg_anim = {
    "frames": parallax_bg,       # List of images
    "index": 0,                       # Current frame index
    "last_update": 0,                # When it last changed frames
    "delay": 80,                    # How often it updates (in ms)
    "pos": (0, 0)                 # Where to draw the image
}

pygame.mixer.music.load("Royale High Campus 3 Music - Castle Dorms (Flowering & Tidalglow).mp3")
pygame.mixer.music.set_volume(0.4)
pygame.mixer.music.play(-1)

# Obstacle Class
class Obstacle:
    def __init__(self, image, x, y, speed):
        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale_by(self.image, 0.3)
        self.rect = self.image.get_rect(midbottom=(x, y))
        self.speed = speed

    def update(self):
        self.rect.x -= self.speed

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def is_off_screen(self):
        return self.rect.right < 0

# Functions

def update_animation(anim):
    global current_anim
    global idle_delay_set_yet

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

        horse_still_for_scaling = pygame.transform.scale_by(horse_still_original, HORSE_SCALE['scale'])

    # Get scaled size
    scaled_width = horse_still_for_scaling.get_width()
    scaled_height = horse_still_for_scaling.get_height()

    # Get original image size (for positioning math)
    original_width = horse_still.get_width()
    original_height = horse_still.get_height()

    # Find original bottom Y and center X
    original_bottom_y = HORSE_Y + original_height
    original_center_x = HORSE_X + original_width // 2

    # Now calculate new top-left position for blit
    blit_x = original_center_x - scaled_width // 2
    blit_y = original_bottom_y - scaled_height
    screen.blit(horse_still_for_scaling, (blit_x, blit_y))

    if HORSE_SCALE['scale'] < 4:
            print(blit_x,blit_y)


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
         global HORSE_WALK_LOOP_COUNT
         global obstacles, last_obstacle_time, obstacle_spawn_delay
         global jumping, horse_y_pos_shrink, horse_x_pos_shrink
         global color_count
         global color_change
         global color_stage
         screen.blit(parallax_bg[0], (0,0))
         if HORSE_SCALE['scale'] > 3:
          shrink_horse()
         else:
             if HORSE_WALK_LOOP_COUNT < 120:
                HORSE_WALK_LOOP_COUNT += 1
                parallax_bg_anim['delay'] -= 0.5
                horse_walk_anim['delay'] -= 0.5
                update_animation(parallax_bg_anim)
                update_animation(horse_walk_anim)
             else:
                 update_animation(parallax_bg_anim)
                 if jumping:
                    update_animation(horse_jump_anim)
                 else:
                    update_animation(horse_canter_anim)
                # === Handle obstacle generation ===
                 current_time = pygame.time.get_ticks()

                 # Only spawn obstacles after waiting initial delay from when playing started
                 if playing_start_time is not None and (current_time - playing_start_time) > initial_obstacle_wait:
                     if current_time - last_obstacle_time > obstacle_spawn_delay:
                         img = random.choice(obstacle_images)
                         y = 650
                         speed = 16.7
                         x = screen.get_width() + 100  # Start off-screen to the right
                         obstacles.append(Obstacle(img, x, y, speed))
                         last_obstacle_time = current_time

                
                 # === Move and draw obstacles ===
                 for obstacle in obstacles[:]:
                     obstacle.update()
                     obstacle.draw(screen)
 
                     # Remove if it goes off screen (so list doesn't grow forever)
                     if obstacle.is_off_screen():
                         obstacles.remove(obstacle)
                    
                 if show_start_text:
                     #font = pygame.font.SysFont(None, 48)
                     #text_surface = font.render("Press Space to Start", True, (255, 255, 255))
                     #text_rect = text_surface.get_rect(center=(screen.get_width()//2, 300))
                     #screen.blit(text_surface, text_rect)

                     text_color = (168, 50, 50)
                    
                     if color_count <= 10:
                        if color_stage == 0:
                            text_color = (text_color[0], text_color[1] + color_change, text_color[2])
                            color_count += 1
                        elif color_stage == 1:
                            text_color = (text_color[0] - color_change, text_color[1], text_color[2])
                            color_count += 1
                        elif color_stage == 2:
                            text_color = (text_color[0], text_color[1], text_color[2] + color_change)
                            color_count += 1
                        elif color_stage == 3:
                            text_color = (text_color[0], text_color[1] - color_change, text_color[2])
                            color_count += 1
                        elif color_stage == 4:
                            text_color = (text_color[0] + color_change, text_color[1], text_color[2])
                            color_count += 1
                        elif color_stage == 5:
                            text_color = (text_color[0], text_color[1], text_color[2] - color_change)
                            color_count += 1
                        elif color_stage == 6:
                            color_stage = 0
                     else:
                        color_stage += 1
                        color_count = 0

                     text_displayed = pygame.font.Font('Supermario.ttf', 60).render(str('PRESS SPACE TO START'), True, text_color)
                     screen.blit(text_displayed, (200, 300))

                 # Update vertical movement
                 if jumping:
                    global y_velocity
                    current_time = pygame.time.get_ticks()

                    if current_time - horse_jump_anim["jump_last_update"] >= horse_jump_anim["jump_delay"]:
                        horse_jump_anim["jump_last_update"] = current_time
                        y_velocity -= gravity
                        horse_jump_anim['pos'][1] -= y_velocity
                        print('pos:', horse_jump_anim['pos'][1], 'velocity:', y_velocity, 'ground_level:', ground_level)
                        # If horse lands back down
                        if horse_jump_anim['pos'][1] >= ground_level:
                            horse_jump_anim['pos'][1] = ground_level
                            jumping = False
                            horse_jump_anim["index"] = 3
                    


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
                playing_start_time = pygame.time.get_ticks()  # record start time here
            if exit_btn_rect.collidepoint(pygame.mouse.get_pos()):
                pygame.mixer.quit()
                pygame.quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_status == 'playing' and not jumping:
                jumping = True
                y_velocity = jump_strength  # give it upward force
                show_start_text = False



    if start_btn_rect.collidepoint(pygame.mouse.get_pos()) or exit_btn_rect.collidepoint(pygame.mouse.get_pos()):
        if soundplayed == False and game_status == 'menu':
            pygame.mixer.Sound.play(btn_hover_sound)
            soundplayed = True            
    else:
         soundplayed = False
    clock.tick(60)
    update_screen(game_status)