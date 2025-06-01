
# Import libraries
import pygame
import time
from random import randint

# Initialize pygame and sound mixer
pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((1200,750))

# Load Images and sounds
start_btn = pygame.image.load('image start button.png')
exit_btn = pygame.image.load('image finish button.png')

btn_hover_sound = pygame.mixer.Sound('sound button click.mp3')

start_btn = pygame.transform.scale_by(start_btn, 0.8)
exit_btn = pygame.transform.scale_by(exit_btn, 0.8)

# Create rectangles for collision detection
start_btn_rect = pygame.Rect(400, 175, 448*0.8, 170*0.8)
exit_btn_rect = pygame.Rect(400, 425, 445*0.8, 168*0.8)

# Set variables that are used later
game_status = 'menu'
soundplayed = False

# Functions

def wait(time):
     # Makes pygame.time.wait easier to understand and makes it take in
     # seconds instead of milliseconds
     pygame.time.wait(time*1000)

def update_screen(game_status):
    if game_status == 'menu':
            screen.fill((255,255,255))
            screen.blit(start_btn,(400,175))
            screen.blit(exit_btn,(400,425))
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
    