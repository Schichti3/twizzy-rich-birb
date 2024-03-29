import pygame


class Button:

    def __init__(self, on_click_function, screen, center_x, center_y, w, h, text="Click me!"):
        self.screen = screen
        self.center_x = center_x
        self.center_y = center_y
        self.w = w
        self.h = h

        self.surface = pygame.Surface((w, h))
        self.rect = pygame.Rect(center_x-int(w/2), center_y-int(h/2), w, h)
        self.__font = pygame.font.Font(None, 24)
        self.text = self.__font.render(text, True, (0,0,0))
        self.text_rect = self.text.get_rect(center=(w/2, h/2))

        self.mouse_hovering_above = False

        self.on_click_function = on_click_function


    def handle_click(self, even_list):
        for event in even_list:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.rect.collidepoint(event.pos):
                    self.on_click_function()


    def draw(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.mouse_hovering_above = True
            pygame.draw.rect(self.surface, (51,255,255), (1, 1, 148, 48))
        else:
            self.mouse_hovering_above = False
            pygame.draw.rect(self.surface, (0, 0, 0), (0, 0, 150, 50))
            pygame.draw.rect(self.surface, (255, 255, 255), (1, 1, 148, 48))
            pygame.draw.rect(self.surface, (0, 0, 0), (1, 1, 148, 1), 2)
            pygame.draw.rect(self.surface, (0, 100, 0), (1, 48, 148, 10), 2)

        self.surface.blit(self.text, self.text_rect)
        self.screen.blit(self.surface, (self.rect.x, self.rect.y))
