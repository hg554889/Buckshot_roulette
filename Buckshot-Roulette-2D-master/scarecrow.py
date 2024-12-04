import pygame
import os

class Scarecrow:
    def __init__(self, position=(0, 0), size=(80, 80)):
        self.position = position
        self.size = size

        # 절대 경로로 이미지 로딩
        current_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(current_dir, 'images', 'blanche.png')

        try:
            self.image = pygame.image.load(image_path).convert_alpha()
            self.image = pygame.transform.scale(self.image, self.size)
            print(f"Scarecrow 이미지 로딩 성공: {image_path}")
        except pygame.error as e:
            print(f"Scarecrow 이미지 로딩 실패: {image_path}")
            print(f"에러 메시지: {e}")
            # 기본적으로 투명한 Surface 생성
            self.image = pygame.Surface(self.size, pygame.SRCALPHA)

        self.rect = self.image.get_rect()
        self.rect.topleft = self.position
        self.active = False  # 초기에는 비활성화 상태

    def draw(self, screen):
        """아이템을 화면에 그립니다."""
        if self.active:
            screen.blit(self.image, self.rect)

    def click(self, mouse_pos, current_player, player_lives):
        """아이템이 클릭되었는지 확인하고, 클릭 시 사라짐과 효과를 적용."""
        if self.active and self.rect.collidepoint(mouse_pos):
            self.apply_effect(current_player, player_lives)  # 아이템 효과 적용
            self.active = False  # 아이템을 비활성화
            return True
        return False

    def apply_effect(self, current_player, player_lives):
        """Scarecrow 아이템의 효과를 적용."""
        if current_player == 0:
            # Player 1이 클릭한 경우: Player 2의 피해 무효화
            print("Player 1 activated Scarecrow!")
            # 실제 보호는 main 코드에서 처리
        elif current_player == 1:
            # Player 2가 클릭한 경우: Player 1의 피해 무효화
            print("Player 2 activated Scarecrow!")
            # 실제 보호는 main 코드에서 처리

    def reset(self, new_position=None):
        """아이템을 다시 활성화 상태로 설정하고 위치를 변경할 수 있습니다."""
        if new_position:
            self.position = new_position
            self.rect.topleft = self.position
        self.active = True
