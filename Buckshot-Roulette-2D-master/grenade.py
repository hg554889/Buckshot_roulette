import pygame
import os


class Grenade:
    def __init__(self, position=(0, 0), size=(50, 50)):
        try:
            self.image = pygame.image.load(os.path.join('images', 'fond_noir.png')).convert_alpha()
        except pygame.error as e:
            print(f"Grenade 이미지 로딩 실패: {e}")
            # Create a placeholder surface if the image fails to load
            self.image = pygame.Surface(size, pygame.SRCALPHA)
            pygame.draw.circle(self.image, (255, 0, 0), (size[0]//2, size[1]//2), size[0]//2)
        self.image = pygame.transform.scale(self.image, size)
        self.rect = self.image.get_rect(topleft=position)
        self.active = True

    def draw(self, fenetre):
        if self.active:
            fenetre.blit(self.image, self.rect.topleft)

    def is_clicked(self, pos):
        return self.active and self.rect.collidepoint(pos)

    def use(self):
        self.active = False
        # The effect will be handled in the main loop
