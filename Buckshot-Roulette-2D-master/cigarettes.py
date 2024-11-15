import pygame
import random


class Cigarette:

    def __init__(self):
        self.image = pygame.image.load("./images/cigarette.png")
        
    def fumer(self, vie_joueur):
        X_aleatoire = random.randint(0, 2)
        vie_joueur[X_aleatoire] += 1
        return vie_joueur
    
    def affiche_cigarette(self, fenetre, x, y):
        """
        담배를 지정된 위치에 표시
        """
        fenetre.blit(self.image, (x, y))
