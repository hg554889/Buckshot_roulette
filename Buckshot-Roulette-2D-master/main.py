# main.py
import pygame
import random
from menu import Menu
from game import Game
from arme import Arme
from map import Carte
from cigarettes import Cigarette
from enhanced_bullet import Bullet
from scarecrow import Scarecrow
from grenade import Grenade  # Grenade 클래스 임포트
import os

pygame.init()

fenetre = pygame.display.set_mode((1080, 720))
pygame.display.set_caption("Buckshot Roulette")

BLANC = (255, 255, 255)
ROUGE = (255, 0, 0)
NOIR = (0, 0, 0)

# 배경 이미지 로딩
try:
    background = pygame.image.load(os.path.join('images', 'background.png')).convert()
except pygame.error as e:
    print(f"배경 이미지 로딩 실패: {e}")
    background = pygame.Surface((1080, 720))

police = pygame.font.SysFont("Times New Roman", 20)
jouer_texte = police.render("Play", True, BLANC)
regles_texte = police.render("Rules", True, BLANC)
quitter_texte = police.render("Quit", True, BLANC)

# 클래스 인스턴스 생성:
map = Carte()
menu = Menu()
game = Game()
arme = Arme([3, 3, 3], [])
cigarette1 = Cigarette()  # Player 1의 담배
cigarette2 = Cigarette()  # Player 2의 담배

# 초기화
player_lives = [5, 5]  # 두 플레이어의 초기 생명력
current_player = 0  # 현재 차례인 플레이어 (0: Player 1, 1: Player 2)
game_over = False
in_menu = True  # 메뉴 상태를 관리하는 변수

# 담배의 위치 설정 (각 사각형 영역의 중앙에 배치)
cigarette1_position = (80, 200)  # 왼쪽 사각형 영역 안에 위치
cigarette2_position = (920, 200)  # 오른쪽 사각형 영역 안에 위치

# Scarecrow의 위치 설정
scarecrow1_position = (80, 400)  # Player 1의 Scarecrow 위치
scarecrow2_position = (920, 400)  # Player 2의 Scarecrow 위치

# Scarecrow 객체 생성 및 초기 비활성화
scarecrow1 = Scarecrow(position=scarecrow1_position, size=(80, 80))
scarecrow2 = Scarecrow(position=scarecrow2_position, size=(80, 80))
scarecrow1.active = False
scarecrow2.active = False

# Bullet의 크기를 담배와 동일하게 설정
bullet_size = (cigarette1.image.get_width(), cigarette1.image.get_height())

# 총알 위치 설정 (각 플레이어 앞에 배치)
bullet_positions = [
    (cigarette1_position[0], cigarette1_position[1] + 100),  # Player 1의 Bullet 위치
    (cigarette2_position[0], cigarette2_position[1] + 100)   # Player 2의 Bullet 위치
]

# 지정된 위치와 크기로 총알 생성
bullets = [Bullet(position=pos, size=bullet_size) for pos in bullet_positions]

# 플레이어별 강화 상태 추적
bullet_enhanced = [False, False]  # [Player 1의 강화 상태, Player 2의 강화 상태]

# Scarecrow 보호 상태 플래그
scarecrow_protected = [False, False]  # [Player 1 보호 상태, Player 2 보호 상태]

# 버튼 위치와 크기 설정
shoot_self_button_rect = pygame.Rect(420, 600, 120, 40)
shoot_opponent_button_rect = pygame.Rect(540, 600, 120, 40)

# 버튼 텍스트
shoot_self_text = police.render("Shoot Self", True, BLANC)
shoot_opponent_text = police.render("Shoot Opponent", True, BLANC)

# 뒤로가기 버튼 추가
try:
    retour_button_image = pygame.image.load(os.path.join('images', 'retour.png')).convert_alpha()
except pygame.error as e:
    print(f"뒤로가기 버튼 이미지 로딩 실패: {e}")
    retour_button_image = pygame.Surface((50, 50), pygame.SRCALPHA)

# 원하는 크기로 스케일 조정 (예: 50x50 크기)
retour_button_size = (50, 50)  # 너비와 높이
retour_button_image = pygame.transform.scale(retour_button_image, retour_button_size)

# 버튼의 Rect 업데이트
retour_button_rect = retour_button_image.get_rect()
retour_button_rect.topleft = (20, 620)  # 뒤로가기 버튼 위치

# **Grenade 위치 설정: Scarecrow 바로 아래로 배치**
# Scarecrow 크기가 (80, 80)이라고 가정하고, y 좌표에 10 픽셀 여유 추가
grenade_offset_y = 80 + 10  # Scarecrow 높이 + 여유 공간
grenade1_position = (scarecrow1_position[0], scarecrow1_position[1] + grenade_offset_y)
grenade2_position = (scarecrow2_position[0], scarecrow2_position[1] + grenade_offset_y)
grenade_positions = [
    grenade1_position,  # Player 1의 Grenade 위치
    grenade2_position   # Player 2의 Grenade 위치
]
grenades = [Grenade(position=pos, size=(50, 50)) for pos in grenade_positions]  # Grenade 인스턴스 생성

def est_survole(x, y, largeur, hauteur):
    """
    마우스가 버튼 위에 있는지 확인.
    """
    souris_x, souris_y = pygame.mouse.get_pos()
    return x < souris_x < x + largeur and y < souris_y < y + hauteur

def affiche_vie(fenetre, lives):
    """
    두 플레이어의 생명력을 화면 중앙에 표시.
    """
    police_vie = pygame.font.SysFont("Arial", 24)
    text_p1 = f"Player 1 HP: {lives[0]}"
    text_p2 = f"Player 2 HP: {lives[1]}"

    text_p1_surface = police_vie.render(text_p1, True, BLANC)
    text_p2_surface = police_vie.render(text_p2, True, BLANC)

    fenetre_rect = fenetre.get_rect()
    text_y = 50

    fenetre.blit(text_p1_surface, ((fenetre_rect.width - text_p1_surface.get_width()) // 2, text_y))
    fenetre.blit(text_p2_surface, ((fenetre_rect.width - text_p2_surface.get_width()) // 2, text_y + 30))

def affiche_tour(fenetre, current_player):
    """
    현재 플레이어의 턴을 화면에 표시.
    Player 1의 턴일 경우 왼쪽 위, Player 2의 턴일 경우 오른쪽 위에 표시.
    """
    turn_text = police.render("Your Turn", True, ROUGE)

    if current_player == 0:
        # Player 1의 턴일 때: 왼쪽 위에 표시
        fenetre.blit(turn_text, (20, 20))
    else:
        # Player 2의 턴일 때: 오른쪽 위에 표시
        fenetre.blit(turn_text, (fenetre.get_width() - turn_text.get_width() - 20, 20))

def check_game_over(lives):
    """
    게임 종료 조건 확인. 생명력이 0 이하인 플레이어가 있으면 True와 해당 플레이어 반환.
    """
    for i, life in enumerate(lives):
        if life <= 0:
            return True, i
    return False, -1

def draw_game_over(fenetre, winner):
    """
    게임 종료 화면 표시: 검은 배경 위에 흰색으로 승리 메시지 출력.
    """
    fenetre.fill(NOIR)  # 검은 화면
    police_game_over = pygame.font.SysFont("Arial", 36)
    game_over_text = police_game_over.render(f"{winner} Wins!", True, BLANC)
    fenetre.blit(game_over_text,
                 (fenetre.get_width() // 2 - game_over_text.get_width() // 2,
                  fenetre.get_height() // 2 - game_over_text.get_height() // 2))

def draw_buttons(fenetre, current_player):
    """
    발사 버튼을 화면에 그리기.
    """
    pygame.draw.rect(fenetre, ROUGE if est_survole(*shoot_self_button_rect) else BLANC, shoot_self_button_rect, 2)
    pygame.draw.rect(fenetre, ROUGE if est_survole(*shoot_opponent_button_rect) else BLANC, shoot_opponent_button_rect, 2)

    fenetre.blit(shoot_self_text, (shoot_self_button_rect.x + 10, shoot_self_button_rect.y + 10))
    fenetre.blit(shoot_opponent_text, (shoot_opponent_button_rect.x + 10, shoot_opponent_button_rect.y + 10))

def apply_damage(target_player, damage):
    """
    대상 플레이어에게 데미지를 적용합니다. Scarecrow 보호 상태를 확인합니다.
    """
    if not scarecrow_protected[target_player]:
        player_lives[target_player] = max(0, player_lives[target_player] - damage)
    else:
        print(f"Player {target_player + 1} is protected by Scarecrow!")
        scarecrow_protected[target_player] = False  # 보호 상태 초기화

run = True
while run:
    fenetre.blit(background, (0, 0))

    if in_menu:
        # 메뉴 화면 처리
        if est_survole(490, 475, jouer_texte.get_width(), jouer_texte.get_height()):
            jouer_texte = police.render("Play", True, ROUGE)
        else:
            jouer_texte = police.render("Play", True, BLANC)
        if est_survole(490, 510, regles_texte.get_width(), regles_texte.get_height()):
            regles_texte = police.render("Rules", True, ROUGE)
        else:
            regles_texte = police.render("Rules", True, BLANC)
        if est_survole(480, 545, quitter_texte.get_width(), quitter_texte.get_height()):
            quitter_texte = police.render("Quit", True, ROUGE)
        else:
            quitter_texte = police.render("Quit", True, BLANC)

        fenetre.blit(jouer_texte, (490, 475))
        fenetre.blit(regles_texte, (490, 510))
        fenetre.blit(quitter_texte, (490, 545))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.Rect(490, 475, jouer_texte.get_width(), jouer_texte.get_height()).collidepoint(
                        pygame.mouse.get_pos()):
                    # "Play" 버튼 클릭 시 게임 시작
                    in_menu = False
                    game.playing = True

                    # 게임 시작 시 초기 설정
                    arme.recharge()  # 총알 충전
                    cigarette1.active = True  # Player 1 담배 활성화
                    cigarette2.active = True  # Player 2 담배 활성화
                    scarecrow1.reset()  # Player 1 Scarecrow 활성화
                    scarecrow2.reset()  # Player 2 Scarecrow 활성화

                    # Bullet 아이템 초기화
                    for bullet in bullets:
                        bullet.reset()

                elif pygame.Rect(490, 510, regles_texte.get_width(), regles_texte.get_height()).collidepoint(
                        pygame.mouse.get_pos()):
                    # "Rules" 버튼 클릭 시 규칙 화면 표시
                    menu.flou_playing = True
                    menu.regle_playing = True
                elif pygame.Rect(480, 545, quitter_texte.get_width(), quitter_texte.get_height()).collidepoint(
                        pygame.mouse.get_pos()):
                    # "Quit" 버튼 클릭 시 게임 종료
                    run = False

    elif game.playing and not game_over:
        # 게임 진행 화면
        game.affichage_fond_noir(fenetre)
        map.dessine_table(fenetre)
        map.dessine_emplacement_atout(fenetre, 30, 165, 120, 70)
        map.dessine_emplacement_atout(fenetre, 810, 165, 120, 70)
        map.dessine_emplacement_atout(fenetre, 30, 393, 120, 70)
        map.dessine_emplacement_atout(fenetre, 810, 393, 120, 70)

        arme.affichage_shotgun(fenetre)
        arme.affichage_chargeur(fenetre)
        affiche_vie(fenetre, player_lives)

        # 현재 턴 표시
        affiche_tour(fenetre, current_player)

        # 발사 버튼 그리기
        draw_buttons(fenetre, current_player)

        # 뒤로가기 버튼 표시
        fenetre.blit(retour_button_image, retour_button_rect.topleft)

        # 담배 활성화 상태에 따라 위치에 표시
        if cigarette1.active:
            cigarette1.affiche_cigarette(fenetre, *cigarette1_position)  # Player 1 담배 위치
        if cigarette2.active:
            cigarette2.affiche_cigarette(fenetre, *cigarette2_position)  # Player 2 담배 위치

        # Scarecrow 활성화 상태에 따라 위치에 표시
        if scarecrow1.active:
            scarecrow1.draw(fenetre)  # Player 1 Scarecrow 위치
        if scarecrow2.active:
            scarecrow2.draw(fenetre)  # Player 2 Scarecrow 위치

        # Bullet 아이템 그리기
        for bullet in bullets:
            bullet.draw(fenetre)

        # **Grenade 아이템 그리기**
        for grenade in grenades:
            grenade.draw(fenetre)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                # Bullet 아이템 클릭하여 강화
                for idx, bullet in enumerate(bullets):
                    if bullet.is_clicked(mouse_pos):
                        bullet.enhance()  # 아이템 비활성화
                        bullet_enhanced[current_player] = True  # 현재 플레이어의 강화 상태 설정
                        break  # 한 번에 하나의 아이템만 클릭 가능

                # Scarecrow 아이템 클릭하여 효과 적용
                if scarecrow1.active and current_player == 0:
                    if scarecrow1.click(mouse_pos, current_player, player_lives):
                        scarecrow_protected[1] = True  # Player 2 보호 상태 설정
                elif scarecrow2.active and current_player == 1:
                    if scarecrow2.click(mouse_pos, current_player, player_lives):
                        scarecrow_protected[0] = True  # Player 1 보호 상태 설정

                # 뒤로가기 버튼 클릭 시 메뉴로 이동
                if retour_button_rect.collidepoint(mouse_pos):
                    in_menu = True
                    game.playing = False

                # **Grenade 아이템 클릭하여 효과 적용**
                for grenade in grenades:
                    if grenade.is_clicked(mouse_pos):
                        # 모든 플레이어의 HP를 -1
                        for i in range(len(player_lives)):
                            player_lives[i] = max(0, player_lives[i] - 1)
                        print("Grenade 사용됨: 모든 플레이어의 HP가 1 감소했습니다.")
                        grenade.use()  # Grenade 사용 처리

                        # 게임 종료 확인
                        game_over, loser = check_game_over(player_lives)
                        if game_over:
                            winner = "Player 1" if loser == 1 else "Player 2"
                            break
                        # 턴을 다음 플레이어로 넘김
                        current_player = (current_player + 1) % 2
                        break  # 한 번에 하나의 아이템만 클릭 가능

                # 발사 버튼 클릭 처리
                if shoot_self_button_rect.collidepoint(mouse_pos):
                    # 본인을 발사 대상으로 선택
                    if arme.chargeur:
                        bullet_type = arme.tire()
                        if bullet_type is not None:
                            # 데미지 결정
                            damage = 1  # 기본 데미지
                            if bullet_enhanced[current_player]:
                                damage *= 2  # 강화된 경우 데미지 두 배
                                bullet_enhanced[current_player] = False  # 강화 상태 초기화
                            if bullet_type == 1:
                                # 실탄인 경우 데미지 적용
                                apply_damage(current_player, damage)
                            # 공포탄인 경우 데미지 없음
                            game_over, loser = check_game_over(player_lives)
                            if game_over:
                                winner = "Player 2" if loser == 0 else "Player 1"
                                break
                            current_player = (current_player + 1) % 2

                elif shoot_opponent_button_rect.collidepoint(mouse_pos):
                    # 상대를 발사 대상으로 선택
                    if arme.chargeur:
                        bullet_type = arme.tire()
                        if bullet_type is not None:
                            # 데미지 결정
                            damage = 1  # 기본 데미지
                            if bullet_enhanced[current_player]:
                                damage *= 2  # 강화된 경우 데미지 두 배
                                bullet_enhanced[current_player] = False  # 강화 상태 초기화
                            if bullet_type == 1:
                                # 실탄인 경우 상대에게 데미지 적용
                                opponent = (current_player + 1) % 2
                                apply_damage(opponent, damage)
                            # 공포탄인 경우 데미지 없음
                            game_over, loser = check_game_over(player_lives)
                            if game_over:
                                winner = "Player 1" if loser == 1 else "Player 2"
                                break
                            current_player = (current_player + 1) % 2  # 턴을 상대방에게 넘김

                # Player 1 담배 상호작용 (Player 1의 차례에서만 가능)
                if current_player == 0 and cigarette1.active and pygame.Rect(
                        cigarette1_position[0], cigarette1_position[1],
                        cigarette1.image.get_width(), cigarette1.image.get_height()).collidepoint(
                    mouse_pos):
                    player_lives[0] += 1  # Player 1 생명력 증가
                    cigarette1.active = False  # 담배 사용 후 비활성화

                # Player 2 담배 상호작용 (Player 2의 차례에서만 가능)
                if current_player == 1 and cigarette2.active and pygame.Rect(
                        cigarette2_position[0], cigarette2_position[1],
                        cigarette2.image.get_width(), cigarette2.image.get_height()).collidepoint(
                    mouse_pos):
                    player_lives[1] += 1  # Player 2 생명력 증가
                    cigarette2.active = False  # 담배 사용 후 비활성화

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    # 재장전
                    arme.recharge()

                    # 50% 확률로 담배 다시 활성화
                    cigarette1.active = random.choice([True, False])
                    cigarette2.active = random.choice([True, False])

                    # 50% 확률로 Scarecrow 다시 활성화 및 위치 설정
                    if random.choice([True, False]):
                        scarecrow1.reset(new_position=(0, 0))  # 왼쪽 최상단에 생성
                    else:
                        scarecrow1.active = False

                    if random.choice([True, False]):
                        scarecrow2.reset(new_position=(0, 0))  # 왼쪽 최상단에 생성
                    else:
                        scarecrow2.active = False

                    # Bullet 아이템 다시 활성화
                    for bullet in bullets:
                        if random.choice([True, False]):
                            bullet.reset()

                    # **Grenade 아이템 다시 활성화 (50% 확률)**
                    for grenade in grenades:
                        if not grenade.active and random.choice([True, False]):
                            grenade.active = True

    elif game_over:
        # 게임 종료 화면
        draw_game_over(fenetre, winner)

    if menu.flou_playing:
        menu.flou_bg(fenetre)
    if menu.regle_playing:
        menu.affichage_regle(fenetre)

    pygame.display.update()

pygame.quit()
