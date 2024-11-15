import pygame


class Game:

    def __init__(self):
        self.playing = False
        self.table = pygame.image.load("./images/table.png")
        self.fond_noir = pygame.image.load("./images/fond_noir.png")
        self.fond_noir = pygame.transform.scale(self.fond_noir, (1080, 720))
        

    def affichage_table(self, fenetre):
        if self.playing:
            fenetre.blit(self.table, (-110, 50))

    def affichage_fond_noir(self, fenetre):
        if self.playing:
            fenetre.blit(self.fond_noir, (0, 0))
