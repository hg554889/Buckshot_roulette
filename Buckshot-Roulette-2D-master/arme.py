import pygame
import random
import math

fenetre = pygame.display.set_mode((1080, 720))


class Arme:

    def __init__(self, vie_joueur, chargeur):
        self.shotgun = pygame.image.load("./images/shotgun.png")
        self.shotgun = pygame.transform.scale(self.shotgun, (170, 50))
        self.blanche = pygame.image.load("./images/blanche.png")
        self.blanche = pygame.transform.scale(self.blanche, (69, 45))
        self.blanche = pygame.transform.rotate(self.blanche, 90)
        self.rouge = pygame.image.load("./images/rouge.png")
        self.rouge = pygame.transform.scale(self.rouge, (69, 45))
        self.rouge = pygame.transform.rotate(self.rouge, 90)
        self.vie_joueur = list(vie_joueur)
        self.chargeur = chargeur

    def recharge(self):
        if len(self.chargeur) == 0 or 0 in self.vie_joueur:
            self.chargeur = []
            capacite_chargeur = random.randint(2, 8)
            if capacite_chargeur == 2:
                nb_balles_rouges = 1
            else:
                nb_balles_rouges = random.uniform(capacite_chargeur / 4, float(capacite_chargeur // 2))
            print("nb: ", nb_balles_rouges, math.ceil(nb_balles_rouges))
            self.chargeur = self.chargeur + [1] * math.ceil(nb_balles_rouges) + [0] * (capacite_chargeur - math.ceil(nb_balles_rouges))
            random.shuffle(self.chargeur)
            print(self.chargeur)
        return self.chargeur
    
    def tire(self, cible):
        if self.chargeur:  # 충전된 총알이 있으면 발사
            bullet = self.chargeur.pop(-1)
            self.vie_joueur[cible] -= bullet
        return self.chargeur, self.vie_joueur

    def affichage_balle(self, fenetre, cord, couleur):
        pygame.draw.rect(fenetre, couleur, (cord, (8, 25)), 0)
        pygame.draw.rect(fenetre, (0, 0, 0), ((cord[0], cord[-1] - 8), (8, 8)), 0)

    def affichage_shotgun(self, fenetre):
        fenetre.blit(self.shotgun, (455, 330))

    def affichage_chargeur(self):
        pos_x_b = 492
        pos_x_r = 492 + (12 * self.chargeur.count(0)) + 5
        nb_balles_blanche = self.chargeur.count(0) 
        for i in range(len(self.chargeur)):
            if i <= nb_balles_blanche - 1:
                self.affichage_balle(fenetre, (pos_x_b, 574), (255, 255, 255))
                pos_x_b += 12
            else:
                self.affichage_balle(fenetre, (pos_x_r, 574), (255, 0, 0))
                pos_x_r += 12

    def tire_self(self, life):
        """
        현재 플레이어 본인을 발사.
        """
        if self.chargeur:
            damage = 1  # 한 번 발사 시 입히는 피해량
            self.chargeur.pop()  # 탄창에서 총알 하나 제거
            life = max(0, life - damage)
            return True, life
        return False, life

    def tire_opponent(self, opponent_life):
        """
        상대 플레이어를 발사.
        """
        if self.chargeur:
            damage = 1
            self.chargeur.pop()
            opponent_life = max(0, opponent_life - damage)
            return True, opponent_life
        return False, opponent_life
