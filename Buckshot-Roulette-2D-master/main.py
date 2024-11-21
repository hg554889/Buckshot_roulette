import pygame
import random
from menu import Menu
from game import Game
from arme import Arme
from map import Carte
from cigarettes import Cigarette
# from card_1 import Card1
# from card_2 import Card2
# from card_3 import Card3a

pygame.init()

fenetre = pygame.display.set_mode((1080, 720))
pygame.display.set_caption("Buckshot Roulette")

BLANC = (255, 255, 255)
ROUGE = (255, 0, 0)
NOIR = (0, 0, 0)

background = pygame.image.load("./images/background.png")
police = pygame.font.SysFont("Times New Roman", 20)
jouer_texte = police.render("Play", 1, BLANC)
regles_texte = police.render("Rules", 1, BLANC)
quitter_texte = police.render("Quit", 1, BLANC)

# Créez une instance des différentes classes:
map = Carte()
menu = Menu()
game = Game()
arme = Arme([3, 3, 3], [])
cigarette1 = Cigarette()  # Player 1의 담배
cigarette2 = Cigarette()  # Player 2의 담배

# 초기화
player_lives = [3, 3]  # 두 플레이어의 초기 생명력
current_player = 0  # 현재 차례인 플레이어 (0: Player 1, 1: Player 2)
game_over = False
in_menu = True  # 메뉴 상태를 관리하는 변수
cigarette1_active = False  # Player 1의 담배 활성화 상태
cigarette2_active = False  # Player 2의 담배 활성화 상태

# 담배의 위치 설정 (각 사각형 영역의 중앙에 배치)
cigarette1_position = (80, 200)  # 왼쪽 사각형 영역 안에 위치
cigarette2_position = (920, 200)  # 오른쪽 사각형 영역 안에 위치

# 버튼 위치와 크기 설정
shoot_self_button_rect = pygame.Rect(420, 600, 120, 40)
shoot_opponent_button_rect = pygame.Rect(540, 600, 120, 40)

# 버튼 텍스트
shoot_self_text = police.render("Shoot Self", True, BLANC)
shoot_opponent_text = police.render("Shoot Opponent", True, BLANC)

# 뒤로가기 버튼 추가
retour_button_image = pygame.image.load("./images/retour.png")

# 원하는 크기로 스케일 조정 (예: 50x50 크기)
retour_button_size = (50, 50)  # 너비와 높이
retour_button_image = pygame.transform.scale(retour_button_image, retour_button_size)

# 버튼의 Rect 업데이트
retour_button_rect = retour_button_image.get_rect()
retour_button_rect.topleft = (20, 620)  # 뒤로가기 버튼 위치


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
    police = pygame.font.SysFont("Arial", 24)
    text_p1 = f"Player 1 HP: {lives[0]}"
    text_p2 = f"Player 2 HP: {lives[1]}"

    text_p1_surface = police.render(text_p1, True, BLANC)
    text_p2_surface = police.render(text_p2, True, BLANC)

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
    police = pygame.font.SysFont("Arial", 36)
    game_over_text = police.render(f"{winner} Wins!", True, BLANC)
    fenetre.blit(game_over_text,
                 (fenetre.get_width() // 2 - game_over_text.get_width() // 2,
                  fenetre.get_height() // 2 - game_over_text.get_height() // 2))


# 버튼 그리기 함수
def draw_buttons(fenetre, current_player):
    """
    발사 버튼을 화면에 그리기.
    """
    pygame.draw.rect(fenetre, ROUGE if est_survole(*shoot_self_button_rect) else BLANC, shoot_self_button_rect, 2)
    pygame.draw.rect(fenetre, ROUGE if est_survole(*shoot_opponent_button_rect) else BLANC, shoot_opponent_button_rect, 2)

    fenetre.blit(shoot_self_text, (shoot_self_button_rect.x + 10, shoot_self_button_rect.y + 10))
    fenetre.blit(shoot_opponent_text, (shoot_opponent_button_rect.x + 10, shoot_opponent_button_rect.y + 10))


run = True
while run:
    fenetre.blit(background, (0, 0))

    if in_menu:
        # 메뉴 화면 처리
        if est_survole(490, 475, jouer_texte.get_width(), jouer_texte.get_height()):
            jouer_texte = police.render("Play", 1, ROUGE)
        else:
            jouer_texte = police.render("Play", 1, BLANC)
        if est_survole(490, 510, regles_texte.get_width(), regles_texte.get_height()):
            regles_texte = police.render("Rules", 1, ROUGE)
        else:
            regles_texte = police.render("Rules", 1, BLANC)
        if est_survole(480, 545, quitter_texte.get_width(), quitter_texte.get_height()):
            quitter_texte = police.render("Quit", 1, ROUGE)
        else:
            quitter_texte = police.render("Quit", 1, BLANC)

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
                    cigarette1_active = True  # Player 1 담배 활성화
                    cigarette2_active = True  # Player 2 담배 활성화
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
        arme.affichage_chargeur()
        affiche_vie(fenetre, player_lives)

        # 현재 턴 표시
        affiche_tour(fenetre, current_player)

        # 발사 버튼 그리기
        draw_buttons(fenetre, current_player)

        # 뒤로가기 버튼 표시
        fenetre.blit(retour_button_image, retour_button_rect.topleft)

        # 담배 활성화 상태에 따라 위치에 표시
        if cigarette1_active:
            cigarette1.affiche_cigarette(fenetre, *cigarette1_position)  # Player 1 담배 위치
        if cigarette2_active:
            cigarette2.affiche_cigarette(fenetre, *cigarette2_position)  # Player 2 담배 위치

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if retour_button_rect.collidepoint(pygame.mouse.get_pos()):
                    # 뒤로가기 버튼 클릭 시 메뉴로 이동
                    in_menu = True
                    game.playing = False
                elif shoot_self_button_rect.collidepoint(pygame.mouse.get_pos()):
                    # 본인을 발사 대상으로 선택
                    if arme.chargeur:
                        success, player_lives[current_player] = arme.tire_self(player_lives[current_player])
                        game_over, loser = check_game_over(player_lives)
                        if game_over:
                            winner = "Player 2" if loser == 0 else "Player 1"
                            break
                        current_player = (current_player + 1) % 2
                elif shoot_opponent_button_rect.collidepoint(pygame.mouse.get_pos()):
                    # 상대를 발사 대상으로 선택
                    if arme.chargeur:
                        success, player_lives[(current_player + 1) % 2] = arme.tire_opponent(
                            player_lives[(current_player + 1) % 2])
                        game_over, loser = check_game_over(player_lives)
                        if game_over:
                            winner = "Player 2" if loser == 0 else "Player 1"
                            break
                        current_player = (current_player + 1) % 2
                # Player 1 담배와 상호작용
                if cigarette1_active and pygame.Rect(cigarette1_position[0], cigarette1_position[1],
                                                     cigarette1.image.get_width(),
                                                     cigarette1.image.get_height()).collidepoint(
                    pygame.mouse.get_pos()):
                    player_lives[0] += 1  # Player 1 생명력 증가
                    cigarette1_active = False  # 담배 사용 후 비활성화

                # Player 2 담배와 상호작용
                if cigarette2_active and pygame.Rect(cigarette2_position[0], cigarette2_position[1],
                                                     cigarette2.image.get_width(),
                                                     cigarette2.image.get_height()).collidepoint(
                    pygame.mouse.get_pos()):
                    player_lives[1] += 1  # Player 2 생명력 증가
                    cigarette2_active = False  # 담배 사용 후 비활성화
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    # 재장전
                    arme.recharge()

                    # 50% 확률로 담배 다시 활성화
                    cigarette1_active = random.choice([True, False])
                    cigarette2_active = random.choice([True, False])

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if shoot_self_button_rect.collidepoint(pygame.mouse.get_pos()):
                    # 본인을 발사 대상으로 선택
                    if arme.chargeur:
                        success, player_lives[current_player] = arme.tire_self(player_lives[current_player])
                        game_over, loser = check_game_over(player_lives)
                        if game_over:
                            winner = "Player 2" if loser == 0 else "Player 1"
                            break
                        current_player = (current_player + 1) % 2
                elif shoot_opponent_button_rect.collidepoint(pygame.mouse.get_pos()):
                    # 상대를 발사 대상으로 선택
                    if arme.chargeur:
                        success, player_lives[(current_player + 1) % 2] = arme.tire_opponent(player_lives[(current_player + 1) % 2])
                        game_over, loser = check_game_over(player_lives)
                        if game_over:
                            winner = "Player 2" if loser == 0 else "Player 1"
                            break
                        current_player = (current_player + 1) % 2

    elif game_over:
        # 게임 종료 화면
        draw_game_over(fenetre, winner)

    if menu.flou_playing:
        menu.flou_bg(fenetre)
    if menu.regle_playing:
        menu.affichage_regle(fenetre)

    pygame.display.update()

pygame.quit()
