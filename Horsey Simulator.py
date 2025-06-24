
# Import libraries
import pygame
import random
from random import choice

# Initialize pygame and sound mixer
pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((1200, 750))

# Set variables that are used later
game_status = 'menu'          # what is the game status?
soundplayed = False           # has the sound for hovering over the menu buttons played?
time_since_last_idle = 0      # how long since the last idle animation occured?
time_until_next_idle = random.randint(3000,8000)  # how long until the next idle animation occurs?
current_anim = "idle"         # the current animation (only for menu screen)
idle_delay_set_yet = False    # has the idle delay been set yet?
clock = pygame.time.Clock()   # make accessing the time easier
jumping = False               # are they currently jumping?
first_jump = False            # have they taken their first jump yet?
done_walking = False          # are they done the walking animation?
playing_start_time = None     # a snapshot of the time taken after your first jump
initial_obstacle_wait = 5000  # the initial wait after the first jump for obstacles to start spawning
spacebar_pressed = False      # the spacebar does not start off as pressed
spacebar_held = False         # the spacebar does not start off as held
show_masks = False            # should masks be shown? (collision)
show_start_text = True        # should start text be shown?
show_meters_text = True       # should meter tracker text be shown?
horse_y_pos_shrink = 455      # the horse's y position after shrunken
horse_x_pos_shrink = 170      # the horse's x position after shrunken
y_velocity = 0      # the horse's velocity
jump_strength = 70  # how high the horse jumps
GRAVITY = 13        # how fast the horse falls back down
ground_level = 455  # the normal horse y position

# text colour variables
text_color = (168, 50, 50)
color_stage = 0
color_count = 0
color_change = 11.8

# Meters traveled text
meters_traveled = 0
METER_UPDATE_DELAY = 100
blit_meters_text_count = 0
font = pygame.font.SysFont(None, 36)
meters_text = font.render(f"Meters: {int(meters_traveled)}", True, (255, 255, 255))

# Calculate x-position manually
meters_text_x = screen.get_width() - meters_text.get_width() - 20  # 20 px padding from right
meters_text_y = 20  # 20 px from top

# Set obstacles list and time since the last obstacle was created, as well as the spawn delay between obstacles
obstacles = []
last_obstacle_time = 0
OBSTACLE_SPAWN_DELAY = 2000  # ms

#Store horse position aafter shrink, and the amount of times it has went through the walking animation loop
HORSE_POS_AFTER_SHRINK = (170,455)
HORSE_WALK_LOOP_COUNT = 0

#Store constants for the start and exit buttons
START_BTN_POS = (630,175)
EXIT_BTN_POS = (630,425)

# STORE HORSE POSITION FOR MENU SCREEN
HORSE_X = -30
HORSE_Y = 130

#UNPACK TUPLES
(START_BTN_POS_X, START_BTN_POS_Y) = (START_BTN_POS)
(EXIT_BTN_POS_X, EXIT_BTN_POS_Y) = (EXIT_BTN_POS)

# Load Images and sounds
start_btn = pygame.image.load('image start button.png')
exit_btn = pygame.image.load('image finish button.png')

btn_hover_sound = pygame.mixer.Sound('sound button click.mp3')
neigh_sound = pygame.mixer.Sound('neigh.mp3')
crash_sound = pygame.mixer.Sound('crash.mp3')
crash_sound.set_volume(0.15)
neigh_sound.set_volume(0.8)

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

HORSE_SCALE = {
     'scale': 8,
     'delay': 30,
     'last_update': 0
}

# Make scaled versions for menu and animation
horse_still = pygame.transform.scale_by(horse_still_original, 8)
horse_still_for_scaling = pygame.transform.scale_by(horse_still_original, HORSE_SCALE['scale'])

# Images that can be used as obstacles
obstacle_images = [
    '/Users/nicolezhang/MyCode/Obstacles/log.png',
    '/Users/nicolezhang/MyCode/Obstacles/rock.png'
]

# Code frames stored for the future, if I want to add onto the game
# horse_tail_swish = [pygame.image.load('tile000.png'), pygame.image.load('tile001.png'), pygame.image.load('tile002.png'), pygame.image.load('tile003.png'), pygame.image.load('tile004.png'), pygame.image.load('tile05.png'), pygame.image.load('tile006.png'), pygame.image.load('tile007.png'), pygame.image.load('tile008.png'), pygame.image.load('tile009.png')]
# horse_graze = [pygame.image.load('tile0010.png'), pygame.image.load('tile011.png'), pygame.image.load('tile012.png'), pygame.image.load('tile013.png'), pygame.image.load('tile014.png'), pygame.image.load('tile015.png'), pygame.image.load('tile016.png')]
# horse_walk = [pygame.image.load('tile018.png'), pygame.image.load('tile019.png'), pygame.image.load('tile020.png'), pygame.image.load('tile021.png'), pygame.image.load('tile022.png'), pygame.image.load('tile023.png'), pygame.image.load('tile024.png'), pygame.image.load('tile025.png'), pygame.image.load('tile026.png')]
# horse_canter = [pygame.image.load('tile027.png'), pygame.image.load('tile028.png'), pygame.image.load('tile029.png'), pygame.image.load('tile030.png'), pygame.image.load('tile031.png'), pygame.image.load('tile032.png'), pygame.image.load('tile033.png'), pygame.image.load('tile034.png')]
# horse_gallop = [pygame.image.load('tile036.png'), pygame.image.load('tile037.png'), pygame.image.load('tile038.png'), pygame.image.load('tile039.png'), pygame.image.load('tile040.png'), pygame.image.load('tile041.png')]
# horse_jump = [pygame.image.load('jump00.png'), pygame.image.load('jump01.png'), pygame.image.load('jump02.png'), pygame.image.load('jump03.png'), pygame.image.load('jump04.png'), pygame.image.load('jump05.png'), pygame.image.load('jump06.png'), pygame.image.load('jump07.png'), pygame.image.load('jump08.png'), pygame.image.load('jump09.png'), pygame.image.load('jump10.png'), pygame.image.load('jump11.png'), pygame.image.load('jump12.png'), pygame.image.load('jump13.png'), pygame.image.load('jump14.png')]

# I use lists and loops to load in all the images, iterating through each file name and appending it to the list

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
     # make sure theres always 3 digits
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
    "index": 6,                       # Current frame index
    "last_update": 0,                # When it last changed frames
    "delay": 80,                    # How often it updates (in ms)
    "pos": [horse_x_pos_shrink, 455],               # Where to draw the image
    "jump_delay": 40,
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

#Make sure background music is always playing
pygame.mixer.music.load("Royale High Campus 3 Music - Castle Dorms (Flowering & Tidalglow).mp3")
pygame.mixer.music.set_volume(0.4)
#play forever
pygame.mixer.music.play(-1)

# Obstacle Class
class Obstacle:
    # define its own variables
    def __init__(self, image, x, y, speed):
        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale_by(self.image, 0.3)
        self.rect = self.image.get_rect(midbottom=(x, y))
        self.speed = speed
        self.mask = pygame.mask.from_surface(self.image)
        self.mask_image = self.mask.to_surface(setcolor=(255, 0, 0, 150), unsetcolor=(0, 0, 0, 0))
        self.x = x
        self.y = y

    # update the speed
    def update(self):
        self.rect.x -= self.speed

    # blit it onto the screen
    def draw(self, screen):
        screen.blit(self.image, self.rect)
    
    # draw its mask
    def draw_mask(self, screen):
        screen.blit(self.mask_image, self.rect)

    # is it off the screen? returns boolean
    def is_off_screen(self):
        # self.rect.right = x value of the right of the rect
        return self.rect.right < 0

# Functions

def update_animation(anim):
    # PURPOSE: update the animation. if the difference between the time snapshot of the last update and the current time are greater than or equal to the delay time, switch frames and reset
    global current_anim
    global idle_delay_set_yet

    current_time = pygame.time.get_ticks()

    if current_time - anim["last_update"] >= anim["delay"]:
        anim["last_update"] = current_time
        anim["index"] = (anim["index"] + 1) % len(anim["frames"])
        # if the idle animation is completed, make the current animation the still horse
        if anim['index'] == 0:
            current_anim = 'idle'
            
    screen.blit(anim["frames"][anim["index"]], anim["pos"])

def detect_collision():
    # PURPOSE: get & return the horse's mask, and detect collisions with obstacles
    # if the horse is jumping, use the image from the jumping horse. If not, use it from the cantering horse.
    if jumping:
        horse_mask = pygame.mask.from_surface(horse_jump_anim['frames'][horse_jump_anim['index']])
    else:
        horse_mask = pygame.mask.from_surface(horse_canter_anim['frames'][horse_canter_anim['index']])
    mask_image = horse_mask.to_surface(setcolor=(255, 0, 0, 150), unsetcolor=(0, 0, 0, 0))
    
    # for each obstacle, if its mask collides with the horse's mask, end the game
    for obstacle in obstacles:
        if jumping:
            if horse_mask.overlap(obstacle.mask, (obstacle.rect[0] - horse_x_pos_shrink, obstacle.rect[1] - horse_jump_anim['pos'][1])):
                print('collision detected')
                game_lose()
                
        else:
            if horse_mask.overlap(obstacle.mask, (obstacle.rect[0] - horse_x_pos_shrink, obstacle.rect[1] - horse_y_pos_shrink)):
                print('collision detected')
                game_lose()

    return mask_image

def game_lose():
    # PURPOSE: reset variables so that the game is repeatable, and make variables so that the score blits for a little while after loss
    global game_status, show_start_text, first_jump, done_walking, playing_start_time, HORSE_WALK_LOOP_COUNT, meters_traveled, blit_meters_text_count
    pygame.mixer.Sound.play(neigh_sound)
    pygame.mixer.Sound.play(crash_sound)
    game_status = 'menu'
    for obstacle in obstacles:
        obstacles.remove(obstacle)
    show_start_text = True
    first_jump = False
    done_walking = False
    playing_start_time = None
    HORSE_SCALE['scale'] = 8
    HORSE_WALK_LOOP_COUNT = 0
    parallax_bg_anim['delay'] = 80
    horse_walk_anim['delay'] = 150
    meters_traveled = 0
    blit_meters_text_count = 30


def shrink_horse():
    # PURPOSE: after you press start, the horse will shrink. This function is responsible for that.
    global horse_still_for_scaling

    current_time = pygame.time.get_ticks()
    
    # if it has been long enough time, make the horse shrink.
    if current_time - HORSE_SCALE['last_update'] >= HORSE_SCALE['delay']:
        HORSE_SCALE['last_update'] = current_time
        HORSE_SCALE['scale'] -= 0.5

        horse_still_for_scaling = pygame.transform.scale_by(horse_still_original, HORSE_SCALE['scale'])

    # What is the width and height of the current version of the scaled horse?
    scaled_width = horse_still_for_scaling.get_width()
    scaled_height = horse_still_for_scaling.get_height()

    # What is the width and height of the original horse?
    original_width = horse_still.get_width()
    original_height = horse_still.get_height()

    # Gets the bottom y pos of the original horse, as well as  the center x position of the original horse.
    original_bottom_y = HORSE_Y + original_height
    original_center_x = HORSE_X + original_width // 2

    # Based on where we want the horse to show up, we need to find the top left corner of the new image. We can find this by subtracting the dimensions of the scaled horse.
    blit_x = original_center_x - scaled_width // 2
    blit_y = original_bottom_y - scaled_height

    # Blit the new scaled horse!
    screen.blit(horse_still_for_scaling, (blit_x, blit_y))

def update_screen(game_status):
    # PURPOSE: depending on the var "game_status", update the screen
    # meters text variables must be globalled at the top, or else it would be called before assigned
    global meters_traveled, meters_text, meters_text_x, meters_text_y, blit_meters_text_count, show_meters_text, time_since_last_meter_update
    if game_status == 'menu':
            global time_since_last_idle
            global time_until_next_idle
            global current_anim
            global done_walking

            #blit the still frame of parallax_bg
            screen.blit(parallax_bg[0], (0,0))

            # Blit the meters text for a little longer after death. Does this by checking if the difference between current 
            # time and snapshot time are enough, then loops through a couple of times.
            if blit_meters_text_count:
                if show_meters_text:
                        current_time = pygame.time.get_ticks()
                        if current_time - time_since_last_meter_update >= METER_UPDATE_DELAY:
                            time_since_last_meter_update = current_time
                            blit_meters_text_count -= 1
                        screen.blit(meters_text, (meters_text_x, meters_text_y))

            # draw the buttons 
            screen.blit(start_btn,(630,175))
            screen.blit(exit_btn,(630,425))
            current_time = pygame.time.get_ticks()
            # If enough time has gone by, do an idle animation
            if current_time - time_since_last_idle >= time_until_next_idle:
                    current_anim = choice(["tail", "graze"])
                    time_since_last_idle = current_time
                    time_until_next_idle = random.randint(3000,8000)
            # Depending on the random animation chosen, update that animation
            if current_anim == "idle":
                screen.blit(horse_still, (HORSE_X, HORSE_Y))
            elif current_anim == "graze":
                update_animation(horse_graze_anim)
            elif current_anim == "tail":
                update_animation(horse_tail_anim)
            pygame.display.update()

    elif game_status == 'playing':
         # global variables needed in this loop
         global HORSE_WALK_LOOP_COUNT
         global obstacles, last_obstacle_time, OBSTACLE_SPAWN_DELAY
         global jumping, horse_y_pos_shrink, horse_x_pos_shrink
         global color_count, color_change
         global color_stage, text_color
         global spacebar_held
         global y_velocity
         global playing_start_time, show_start_text, first_jump

         # blit the parallax background. This only matters while the horse is shrinking.
         screen.blit(parallax_bg[0], (0,0))

         # if the horse isn't bigger than a scale factor of 3, keep shrinking it
         if HORSE_SCALE['scale'] > 3:
          shrink_horse()
         
         else:
             # if the horse has finished shrinking, start walking. Run the animation 120 times.
             if HORSE_WALK_LOOP_COUNT < 120:
                HORSE_WALK_LOOP_COUNT += 1
                parallax_bg_anim['delay'] -= 0.5
                horse_walk_anim['delay'] -= 0.5
                update_animation(parallax_bg_anim)
                update_animation(horse_walk_anim)
             else:
                 # if the horse has finished walking, start cantering. make this known with var "done_walking".
                 # if the spacebar is held, then make spacebar_held true.
                 spacebar_held = pygame.key.get_pressed()[pygame.K_SPACE]
                 done_walking = True
                 # update the parallax background, and the canter/jump animation, depending on whether the horse is jumping or not.
                 update_animation(parallax_bg_anim)
                 if jumping:
                    update_animation(horse_jump_anim)
                 else:
                    update_animation(horse_canter_anim)
                 # get the horse's mask from detect_collision()
                 mask_image = detect_collision()
                 if show_masks:
                    # make sure it blits at the correct spot
                    if jumping:
                        screen.blit(mask_image, (horse_x_pos_shrink, horse_jump_anim['pos'][1]))
                    else:
                        screen.blit(mask_image, (horse_x_pos_shrink, horse_y_pos_shrink))
                # === Handle obstacle generation ===
                 current_time = pygame.time.get_ticks()

                 # Only spawn obstacles after waiting initial delay from when playing started
                 if playing_start_time is not None and (current_time - playing_start_time) > initial_obstacle_wait:
                     if current_time - last_obstacle_time > OBSTACLE_SPAWN_DELAY:
                         img = random.choice(obstacle_images)   # choose a random image from the list loaded before
                         y = 650
                         speed = 16.7
                         x = screen.get_width() + 100  # Start off-screen to the right
                         obstacles.append(Obstacle(img, x, y, speed))
                         last_obstacle_time = current_time       # the last obstacle created was created NOW!
                
                 # === Move and draw obstacles (and masks if on) ===
                 for obstacle in obstacles[:]:
                     obstacle.update()
                     obstacle.draw(screen)
                     if show_masks:
                        obstacle.draw_mask(screen)
 
                     # Remove if it goes off screen (so list doesn't grow forever and cause lag)
                     if obstacle.is_off_screen():
                         obstacles.remove(obstacle)
                 # if they have pressed the spacebar at least once, then the meters bar should be shown. 
                 # if an amount of time (METER_UPDATE_DELAY) has passed, add more meters to the meter tracker, and update the text, then blit it
                 if playing_start_time is not None:
                    if show_meters_text:
                        current_time = pygame.time.get_ticks()
                        if current_time - time_since_last_meter_update >= METER_UPDATE_DELAY:
                            time_since_last_meter_update = pygame.time.get_ticks()
                            meters_traveled += 1
                            meters_text = font.render(f"Meters: {meters_traveled}", True, (255, 255, 255))
                            meters_text_x = screen.get_width() - meters_text.get_width() - 20
                        screen.blit(meters_text, (meters_text_x, meters_text_y))

                 # if the start text is being shown, scroll through the RGB codes to make the text gradient rainbow.
                 # depending on what RGB code is currently shown, the RGB numbers must change in different stages (color_stage)
                 if show_start_text:
                     
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
                        # when it has finished the color count to 10, reset it
                        color_stage += 1
                        color_count = 0
                     
                     # load the text displayed, as well as its font, then draw it
                     text_displayed = pygame.font.Font('Supermario.ttf', 60).render(str('PRESS SPACE TO START'), True, text_color)
                     screen.blit(text_displayed, (200, 300))
                 
                 # if the spacebar is pressed/held, the game is playing, they arent already jumping, and the walking animation has finished, then jump
                 if (spacebar_pressed or spacebar_held) and game_status == 'playing' and not jumping and done_walking:
                                 jumping = True
                                 # if it has been their first jump, the start text must disappear, and the meter tracker must show
                                 if first_jump == False:
                                     playing_start_time = pygame.time.get_ticks()  # record start time here
                                     first_jump = True
                                     time_since_last_meter_update = pygame.time.get_ticks()
                                 y_velocity = jump_strength  # give it upward force
                                 show_start_text = False

                 # If they are jumping, update the animation for it. Since the jumping animation logic is more complex than the others, 
                 # it cannot be run using the update_animation() func
                 if jumping:
                    
                    current_time = pygame.time.get_ticks()

                    if current_time - horse_jump_anim["jump_last_update"] >= horse_jump_anim["jump_delay"]:
                        horse_jump_anim["jump_last_update"] = current_time
                        y_velocity -= GRAVITY
                        horse_jump_anim['pos'][1] -= y_velocity
                        # If horse lands back down
                        if horse_jump_anim['pos'][1] >= ground_level:
                            horse_jump_anim['pos'][1] = ground_level
                            jumping = False
                            horse_jump_anim["index"] = 6     

         pygame.display.update()

# Main game loop
while True:

    for event in pygame.event.get():
        # if they press the x button, close the game safely
        if event.type == pygame.QUIT:
            pygame.mixer.quit()
            pygame.quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            # if they click on the start button, then start. if they click on the exit button, then close the game.
            if start_btn_rect.collidepoint(pygame.mouse.get_pos()):
                game_status = 'playing'
            if exit_btn_rect.collidepoint(pygame.mouse.get_pos()):
                pygame.mixer.quit()
                pygame.quit()
        # if they press the spacebar, then store that information using spacebar_pressed boolean.
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                spacebar_pressed = True
        else:
            spacebar_pressed = False
    # if the mouse has hovered over a button, then check if a sound has already played, and make sure they are on the menu screen. Play the click! sound.
    if start_btn_rect.collidepoint(pygame.mouse.get_pos()) or exit_btn_rect.collidepoint(pygame.mouse.get_pos()):
        if soundplayed == False and game_status == 'menu':
            pygame.mixer.Sound.play(btn_hover_sound)
            soundplayed = True            
    else:
         soundplayed = False
    
    # make sure the game doesn't lag the computer too much by setting a limit on time.
    clock.tick(60)

    # run the update_screen func.
    update_screen(game_status)

print('hi')