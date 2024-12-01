import pygame

class Bullet:
    def __init__(self, position=(0, 0), size=(40, 40)):
        self.position = position  # Bullet 아이템의 위치
        self.size = size  # Bullet 아이템의 크기
        self.image = pygame.image.load('./images/rouge.png')  # Bullet 아이템 이미지 로드
        self.image = pygame.transform.scale(self.image, self.size)  # 이미지 크기 조정
        self.rect = self.image.get_rect()
        self.rect.topleft = self.position
        self.active = True  # Bullet 아이템의 활성화 상태

    def enhance(self):
        """
        Bullet 아이템을 사용하여 플레이어의 다음 공격을 강화하고, 아이템을 비활성화합니다.
        """
        self.active = False  # 아이템을 사용한 후 비활성화

    def draw(self, fenetre):
        if self.active:
            fenetre.blit(self.image, self.position)
            # 디버깅을 위해 경계선을 그리고 싶다면 아래 주석을 해제하세요.
            # pygame.draw.rect(fenetre, (0, 255, 0), self.rect, 1)

    def is_clicked(self, mouse_pos):
        """
        Bullet 아이템이 클릭되었는지 확인합니다.
        """
        return self.active and self.rect.collidepoint(mouse_pos)

    def reset(self):
        """
        Bullet 아이템의 상태를 초기화합니다.
        """
        self.active = True  # 아이템을 다시 활성화
