import pygame


class Menu:

    def __init__(self):
        self.flou_playing = False
        self.retour_playing = False
        self.regle_playing = False
        self.background_flou = pygame.image.load("./images/background_flou.png")
        self.retour = pygame.image.load("./images/retour.png")
        self.regles = pygame.image.load("./images/regles.png")
        self.retour = pygame.transform.scale(self.retour, (100, 100))
        self.retour_rect = self.retour.get_rect()

    def flou_bg(self, fenetre):
        if self.flou_playing:
            fenetre.blit(self.background_flou, (0, 0))

    def bouton_retour(self, fenetre):
        if self.retour_playing:
            fenetre.blit(self.retour, (0, 0))

    def affichage_regle(self, fenetre):
        if self.regle_playing:
            fenetre.blit(self.regles, (150, 80))
