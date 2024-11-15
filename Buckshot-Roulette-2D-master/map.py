import pygame


class Carte:

    def __init__(self):
        self.cord_millieu_atout = []

    def dessine_table(self, fenetre):
        # Dessine la table de jeu
        pygame.draw.rect(fenetre, (111, 63, 77), ((0, 145), (1080, 420)), 0)
        pygame.draw.line(fenetre, (255, 255, 255), (540, 145), (540, 563), 3)
        pygame.draw.circle(fenetre, (255, 255, 255), (540, 355), 210, 3)
        pygame.draw.rect(fenetre, (192, 192, 192), ((487, 565), (106, 35)), 0)

    def dessine_emplacement_atout(self, fenetre, cord_x, cord_y, largeur, hauteur):
        # Dessine 8 emplacements pour les cartes
        espacement = 1  # Espacement entre les cartes
        cord_y_reset = cord_y - (2 * (hauteur + espacement))
        for i in range(4):
            if i <= 1:
                pygame.draw.rect(fenetre, (255, 255, 255), (cord_x, cord_y + (i * (hauteur + espacement)), largeur, hauteur), 1)
            else:
                cord_x += largeur + 1
                pygame.draw.rect(fenetre, (255, 255, 255), (cord_x, cord_y_reset + (i * (hauteur + espacement)), largeur, hauteur), 1)
                cord_x -= largeur + 1

