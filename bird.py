import pygame
from random import randint

class Bird:
    def __init__(self, screen, x, y, w, h):
        self.screen = screen
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.jumper_color = (255,0,0)
        self.dead_color = (111,0,120)
        self.current_color = self.jumper_color

        self.velocity = 0
        self.max_velocity = 12

        #behaviour flags
        self.falling = False
        self.jumping = False
        self.hovering = True
        if randint(0,1) == 0:
            self.hover_speed = 0.25
            self.hover_limit = 10
        else:
            self.hover_speed = -0.25
            self.hover_limit = -10
        self.initial_y = self.y

        self.rect = pygame.Rect(0,0,0,0) #
        self.picture_alive = pygame.image.load(".\\Images\\yeat_2093.jpg").convert_alpha()
        self.picture_alive = pygame.transform.scale(self.picture_alive, (w, h))
        self.picture_dead = pygame.image.load(".\\Images\\yeat_2093_dead.jpg").convert_alpha()
        self.picture_dead = pygame.transform.scale(self.picture_dead, (w, h))

        self.displayed_picture = self.picture_alive

        self.jump_sound = pygame.mixer.Sound(".\\Sounds\\bird_jump.mp3")
        self.jump_sound.set_volume(0.1)


    def draw(self):
        #self.rect = pygame.draw.rect(self.screen, self.current_color, (self.x, self.y, self.w, self.h)) 
        self.rect = self.screen.blit(self.displayed_picture, (self.x, self.y))

    def do_things(self):
        if self.falling == True:
            if self.velocity < self.max_velocity:
                self.velocity += 1
            self.y = self.y + self.velocity

        elif self.jumping == True:
            if self.velocity < 0:
                self.y = self.y + self.velocity
                self.velocity += 1
            else:
               self.jumping = False
               self.falling = True

        elif self.hovering == True:
                self.y -= self.hover_speed
                if self.y == self.initial_y-self.hover_limit:
                    self.hover_speed = -self.hover_speed
                    self.hover_limit = -self.hover_limit

    def jump(self):
        self.hovering = False
        self.falling = False
        self.jumping = True   
        self.current_color = self.jumper_color
        self.displayed_picture = self.picture_alive
        self.velocity = -self.max_velocity 
        #self.jump_sound.stop() 
        self.jump_sound.play() 

    
    def hover(self):
        self.falling = False
        self.jumping = False
        self.hovering = True
        self.current_color = self.jumper_color
        self.displayed_picture = self.picture_alive
        self.y = self.initial_y
        

    def standby(self):
        self.falling = False
        self.jumping = False
        self.hovering = False
        self.displayed_picture = self.picture_dead
        self.current_color = self.dead_color