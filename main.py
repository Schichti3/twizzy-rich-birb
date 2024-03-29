import pygame
from random import randint, seed
from bird import Bird
from tube import Tube
from button import Button
from time import localtime


#wqhd
#SCREEN_W = 1440
#SCREEN_H = 1440

#hd
#SCREEN_W = 1920
#SCREEN_H = 1080

#original resolution
SCREEN_W = 480
SCREEN_H = 720

mute_all = False

pygame.init()
pygame.display.set_caption("TWIZZY RICH BIRB")
icon = pygame.image.load(".\\Images\\icon.png")
pygame.display.set_icon(icon)
screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
clock = pygame.time.Clock()
pygame.mixer.init()
background_music = pygame.mixer.Sound(".\\Sounds\\yeat_if_we_being_real.mp3")

fail_sound = pygame.mixer.Sound(".\\Sounds\\WHATTHEHELL.mp3")

if mute_all:
    fail_sound.set_volume(0)
else:
    fail_sound.set_volume(0.05)

score_add_sound = pygame.mixer.Sound(".\\Sounds\\scorePlusOne2.mp3")
if mute_all:
    score_add_sound.set_volume(0)
else:
    score_add_sound.set_volume(0.05)

running = True

def fps_visualizer(color):
    font = pygame.font.SysFont("Arial" , 18 , bold = True)
    fps = str(int(clock.get_fps()))
    fps_t = font.render(fps , 1, color)
    screen.blit(fps_t,(0,0))

def number_visualizer(number, color, center_x, center_y):
    font = pygame.font.SysFont("Impact", 50)
    number_rendered = font.render(str(number), 1, color)
    screen.blit(number_rendered, (center_x-int(number_rendered.get_width()/2),center_y-int(number_rendered.get_height()/2)))



ground_image = pygame.image.load(".\\Images\\ground.png").convert_alpha()
ground1 = pygame.transform.scale(ground_image, (SCREEN_W, int(SCREEN_H*0.15)))
ground2 = pygame.transform.scale(ground_image, (SCREEN_W, int(SCREEN_H*0.15)))
ground = [{"surface": ground1, "pos_x": 0}, {"surface": ground2, "pos_x": screen.get_width()}]


stars_image = pygame.image.load(".\\Images\\stars.jpg").convert_alpha()
bg_transformed = False
if stars_image.get_width() < screen.get_width() or stars_image.get_height() < screen.get_height()-ground1.get_height():
    stars_image = pygame.transform.scale(stars_image, (screen.get_width(), screen.get_height()-ground1.get_height()))
    bg_transformed = True


scrolling_speed = 2


def create_tube_pair():
    tube_width = int(screen.get_width()/6.4)
    tube_gap_size = int(screen.get_height()/3.2)
    min_tube_size = int(screen.get_height()/72)
    time_struct = localtime()
    seed(time_struct.tm_hour+time_struct.tm_min+time_struct.tm_sec)
    bottom_tube_height = randint(min_tube_size, screen.get_height()-ground1.get_height()-tube_gap_size-min_tube_size)
    new_tube_bottom = Tube(screen, screen.get_width(), screen.get_height()-ground1.get_height()-bottom_tube_height, tube_width, bottom_tube_height)
    new_tube_top = Tube(screen, screen.get_width(), 0, tube_width, screen.get_height()-tube_gap_size-bottom_tube_height-ground1.get_height())
    tube_pair = (new_tube_bottom, new_tube_top)
    return tube_pair

tube_pairs = []

bird_width = int(screen.get_width()/8) 
bird_height = int(screen.get_height()/14.4) 
b = Bird(screen, int(screen.get_width()/2)-(bird_width/2), int((screen.get_height()-ground1.get_height())/2)-(bird_height/2), bird_width, bird_height)

if mute_all:
    b.jump_sound.set_volume(0)

playing = False
restart_menu = False
start_screen = True

counter = 0
score = 0

def on_restart_button_click():
    global start_screen
    global restart_menu
    global tube_pairs
    global counter
    global score
    
    restart_menu = False
    start_screen = True
    fail_sound.stop()
    if mute_all == False:
        background_music.set_volume(0.05)
    tube_pairs.clear()
    counter = 0
    score = 0
    b.hover()

restart_button = Button(on_restart_button_click, screen, int(screen.get_width()/2), int(screen.get_height()*0.5), 100, 50, text="RESTART")



if mute_all:
    background_music.set_volume(0)
else:
    background_music.set_volume(0.05)
background_music.play(loops=-1)





while running:

    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if restart_menu == False:
                if event.unicode == ' ':
                    if playing == True:
                        b.jump() 
                    elif start_screen == True:
                        start_screen = False
                        playing = True
                        b.jump() 
                if event.unicode == '+':
                    scrolling_speed += 1
                if event.unicode == '-':
                    if scrolling_speed > 2:
                        scrolling_speed -= 1

        if event.type == pygame.MOUSEBUTTONDOWN:
            if restart_menu == False:
                if event.button == 1: #left mousebutton
                    if playing == True:
                        b.jump() 
                    elif start_screen == True:
                        start_screen = False
                        playing = True
                        b.jump() 


    if counter == int(screen.get_width()/4):
        counter = 0
        tube_pairs.append(create_tube_pair())
        if tube_pairs[0][0].x < 0-tube_pairs[0][0].w:
            tube_pairs.pop(0)

    if bg_transformed == True:
        screen.blit(stars_image, (0, 0))
    else:
        screen.blit(stars_image, (-int(stars_image.get_width()*0.33), 0))


    for ground_surface in ground:
        screen.blit(ground_surface["surface"], (ground_surface["pos_x"], screen.get_height()-ground_surface["surface"].get_height()))
        if playing == True or start_screen == True:
            ground_surface["pos_x"] -= scrolling_speed
            if ground_surface["pos_x"] <= -screen.get_width():
                ground_surface["pos_x"] = screen.get_width()


    for tube_pair in tube_pairs:
        tube_pair[0].draw()
        tube_pair[1].draw()
        if playing == True:
            tube_pair[0].x -= scrolling_speed
            tube_pair[1].x -= scrolling_speed


    if playing == True:
        for tube_pair in tube_pairs:
            if pygame.Rect.colliderect(b.rect, tube_pair[0].rect) or pygame.Rect.colliderect(b.rect, tube_pair[1].rect):
                playing = False
                if mute_all == False:
                    background_music.set_volume(0.02)
                b.standby()
                fail_sound.play()
                restart_menu = True

            if b.y+b.h < 0 and b.x+b.w >= tube_pair[1].x and b.x+b.w < tube_pair[1].x+tube_pair[1].w:
                playing = False
                if mute_all == False:
                    background_music.set_volume(0.02)
                b.standby()
                fail_sound.play()
                restart_menu = True

            #add score when passing the middle of the tube with the middle of the bird
            if b.x+b.w/2 >= tube_pair[0].x+tube_pair[0].w/2 and tube_pair[0].tube_scored == False:
                tube_pair[0].tube_scored = True
                score_add_sound.play()
                score += 1
                
        for ground_surface in ground:
            ground_rect = ground_surface["surface"].get_rect(topleft=(ground_surface["pos_x"], screen.get_height()-ground_surface["surface"].get_height()))
            if pygame.Rect.colliderect(b.rect, ground_rect):
                playing = False
                if mute_all == False:
                    background_music.set_volume(0.02)
                b.standby()
                fail_sound.play()
                restart_menu = True
                
    
    b.do_things()
    b.draw()

    if playing == True:
        number_visualizer(score, (51,255,255), screen.get_width()/2, int(screen.get_height()*0.05))

    if restart_menu == True:
        restart_button.draw()
        restart_button.handle_click(events)
        number_visualizer(f"Score: {score}", (51,255,255), screen.get_width()/2, int((screen.get_height()-ground1.get_height())/2))

    fps_visualizer((255,255,255))
    pygame.display.flip()
    clock.tick(60)
    if playing == True:
        counter += 1

pygame.quit()
