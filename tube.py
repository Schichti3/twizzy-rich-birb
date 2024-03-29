import pygame


class Tube:
    def __init__(self, screen, x, y, w, h):
        self.screen = screen
        self.x = x
        self.y = y
        self.w = w
        self.h = h

        self.rect = pygame.Rect(0,0,0,0) #placeholder
        self.picture = pygame.image.load(".\\Images\\100_dollar.jpg")
        self.picture = pygame.transform.scale(self.picture, (self.w, self.h))

        self.tube_scored = False

    def draw(self):
        self.rect = self.screen.blit(self.picture, (self.x, self.y))
        #self.rect = pygame.draw.rect(self.screen, (255,255,0),(self.x, self.y, self.w, self.h)) 

