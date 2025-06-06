
# Import libraries
import pygame
import time
from random import randint

# Initialize pygame and sound mixer
pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((1200,750))

# Set variables that are used later
game_status = 'menu'
soundplayed = False

START_BTN_POS = 630,175
EXIT_BTN_POS = 630,425

# Load Images and sounds
start_btn = pygame.image.load('image start button.png')
exit_btn = pygame.image.load('image finish button.png')

btn_hover_sound = pygame.mixer.Sound('sound button click.mp3')

start_btn = pygame.transform.scale_by(start_btn, 0.8)
exit_btn = pygame.transform.scale_by(exit_btn, 0.8)

# Create rectangles for collision detection
start_btn_rect = pygame.Rect(START_BTN_POS, 448*0.8, 170*0.8)
exit_btn_rect = pygame.Rect(EXIT_BTN_POS, 445*0.8, 168*0.8)

# Set Icon and Caption
pygame.display.set_caption('Horsey Simulator')

# Animation Lists
horse = pygame.transform.scale_by(pygame.image.load('/Users/nicolezhang/MyCode/Horse animations basic/tile000.png'), (8))
# horse_tail_swish = [pygame.image.load('tile000.png'), pygame.image.load('tile001.png'), pygame.image.load('tile002.png'), pygame.image.load('tile003.png'), pygame.image.load('tile004.png'), pygame.image.load('tile05.png'), pygame.image.load('tile006.png'), pygame.image.load('tile007.png'), pygame.image.load('tile008.png'), pygame.image.load('tile009.png')]
# horse_graze = [pygame.image.load('tile0010.png'), pygame.image.load('tile011.png'), pygame.image.load('tile012.png'), pygame.image.load('tile013.png'), pygame.image.load('tile014.png'), pygame.image.load('tile015.png'), pygame.image.load('tile016.png')]
# horse_walk = [pygame.image.load('tile018.png'), pygame.image.load('tile019.png'), pygame.image.load('tile020.png'), pygame.image.load('tile021.png'), pygame.image.load('tile022.png'), pygame.image.load('tile023.png'), pygame.image.load('tile024.png'), pygame.image.load('tile025.png'), pygame.image.load('tile026.png')]
# horse_canter = [pygame.image.load('tile027.png'), pygame.image.load('tile028.png'), pygame.image.load('tile029.png'), pygame.image.load('tile030.png'), pygame.image.load('tile031.png'), pygame.image.load('tile032.png'), pygame.image.load('tile033.png'), pygame.image.load('tile034.png')]
# horse_gallop = [pygame.image.load('tile036.png'), pygame.image.load('tile037.png'), pygame.image.load('tile038.png'), pygame.image.load('tile039.png'), pygame.image.load('tile040.png'), pygame.image.load('tile041.png')]
# horse_jump = [pygame.image.load('jump00.png'), pygame.image.load('jump01.png'), pygame.image.load('jump02.png'), pygame.image.load('jump03.png'), pygame.image.load('jump04.png'), pygame.image.load('jump05.png'), pygame.image.load('jump06.png'), pygame.image.load('jump07.png'), pygame.image.load('jump08.png'), pygame.image.load('jump09.png'), pygame.image.load('jump10.png'), pygame.image.load('jump11.png'), pygame.image.load('jump12.png'), pygame.image.load('jump13.png'), pygame.image.load('jump14.png')]

frame_horse_tail_swish = 1
horse_tail_swish = []
for i in range(0,10):
     img_horse_tail_swish = pygame.transform.scale_by(pygame.image.load(f'/Users/nicolezhang/MyCode/Horse animations basic/tile00{i}.png'), (8))
     horse_tail_swish.append(img_horse_tail_swish)

# Functions

def wait(time):
     # Makes pygame.time.wait easier to understand and makes it take in
     # seconds instead of milliseconds
     pygame.time.wait(time)

def update_screen(game_status):
    if game_status == 'menu':
            global frame_horse_tail_swish
            screen.fill((255,255,255))
            # screen.blit(horse,(-30,200))
            screen.blit(start_btn,(630,175))
            screen.blit(exit_btn,(630,425))
            screen.blit(horse_tail_swish[frame_horse_tail_swish], (-30,50))
            frame_horse_tail_swish += 1
            if frame_horse_tail_swish == 9:
               frame_horse_tail_swish = 1
            #wait(200)
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