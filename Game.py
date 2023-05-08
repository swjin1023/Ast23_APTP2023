import pygame
import random

import player as pl
import Item
import arrow

import variables
import consts

global screen


def game_over():
    """게임 종료 함수"""
    # Game over screen
    game_over_page_font = pygame.font.SysFont(None, 50)
    game_over_text = game_over_page_font.render("Game Over", True, (0, 0, 0))
    game_over_rect = game_over_text.get_rect()
    game_over_rect.center = (consts.data_constant["screen_width"] / 2, consts.data_constant["screen_height"] / 2 - 50)

    # 이번 게임 score
    score_text = game_over_page_font.render(f"Score: {variables.current_score[0]}", True, (0, 0, 0))
    score_text_rect = score_text.get_rect()
    score_text_rect.center = (consts.data_constant["screen_width"] / 2 - 8,
                              consts.data_constant["screen_height"] / 2 + 10)

    # 이번 게임 경과 시간
    time_text = game_over_page_font.render("time: {:02d}:{:02d}".format(variables.elapsed_time[0] // 60,
                                                                        variables.elapsed_time[0] % 60),
                                           True, (0, 0, 0))
    time_text_rect = score_text.get_rect()
    time_text_rect.center = (consts.data_constant["screen_width"] / 2 - 13,
                             consts.data_constant["screen_height"] / 2 + 50)

    # 이번 게임 최대 레벨
    level_text = game_over_page_font.render(f"Level: {variables.level[0]}", True, (0, 0, 0))
    level_text_rect = level_text.get_rect()
    level_text_rect.center = (consts.data_constant["screen_width"] / 2 - 26,
                              consts.data_constant["screen_height"] / 2 + 90)

    screen.fill((255, 255, 255))
    screen.blit(game_over_text, game_over_rect)
    screen.blit(score_text, score_text_rect)
    screen.blit(time_text, time_text_rect)
    screen.blit(level_text, level_text_rect)

    pygame.display.update()
    pygame.time.wait(2000)

    # Quit pygame
    pygame.quit()
    variables.show_score.set(f"최고 점수: {str(variables.top_score[0])}")
    variables.show_time.set("최고 시간: {:02d}:{:02d}".format(variables.max_time[0] // 60, variables.max_time[0] % 60))

    variables.level[0] = 1
    variables.current_score[0] = 0
    variables.elapsed_time[0] = 0


def game_start():
    """게임 시작 함수"""
    pygame.init()
    global screen
    screen = pygame.display.set_mode(
        (consts.data_constant["screen_width"], consts.data_constant["screen_height"]))  # pygame screen
    pygame.display.set_caption("화살 피하기 게임")
    bg_img = pygame.transform.scale(pygame.image.load("background.jpg"),
                                    (consts.data_constant["screen_width"], consts.data_constant["screen_height"]))
    screen.blit(bg_img, (0, 0))

    all_sprites = pygame.sprite.Group()
    arrows = pygame.sprite.Group()
    items = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    invincible_group = pygame.sprite.Group()

    player = pl.Player()
    all_sprites.add(player)
    player_group.add(player)

    invincible_item = Item.InvincibleItem()
    all_sprites.add(invincible_item)
    items.add(invincible_item)
    invincible_group.add(invincible_item)

    item_invincible_collision = Item.InvincbleItemCollision(player, player_group, invincible_group)
    player_group.add(item_invincible_collision)

    clock = pygame.time.Clock()
    start_time = pygame.time.get_ticks()  # 경과 시간 표시하기 위해 가져옴.
    level_up_time = 7000

    running = True
    while running:
        # 배경 이미지
        screen.blit(bg_img, (0, 0))

        # 가운데 원 그리기
        pygame.draw.circle(screen, consts.data_constant["circle_color"], consts.data_constant["center"], consts.data_constant["radius"],
                           consts.data_constant["circle_width"])
        pygame.draw.circle(screen, (0, 0, 0), consts.data_constant["center"],
                           consts.data_constant["radius"] - consts.data_constant["circle_width"])
        # FPS
        clock.tick(60)

        # 이벤트 처리
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # 화살 랜덤 생성 (확률을 randint로 조정)

        arrow_select = random.randint(1, variables.probability[0])
        if len(arrows.sprites()) < variables.level[0] * 10:
            if arrow_select == 1:
                new_arrow = arrow.TopArrow()
                arrows.add(new_arrow)
                all_sprites.add(new_arrow)
            elif arrow_select == 2:
                new_arrow = arrow.LeftArrow()
                arrows.add(new_arrow)
                all_sprites.add(new_arrow)
            elif arrow_select == 3:
                new_arrow = arrow.RightArrow()
                arrows.add(new_arrow)
                all_sprites.add(new_arrow)
            elif arrow_select == 4:
                new_arrow = arrow.BottomArrow()
                arrows.add(new_arrow)
                all_sprites.add(new_arrow)

        # 현재 점수 표시
        font = pygame.font.SysFont(None, 30)
        score_text = font.render("Score: " + str(variables.current_score[0]), True, (255, 255, 255))
        screen.blit(score_text, (10, 10))

        # 현재 경과 시간 표시
        temp = pygame.time.get_ticks()
        variables.elapsed_time[0] = (temp - start_time) // 1000  # 밀리초를 초 단위로 변환
        minutes = variables.elapsed_time[0] // 60  # 분 계산
        seconds = variables.elapsed_time[0] % 60  # 초 계산
        text = font.render("{:02d}:{:02d}".format(minutes, seconds), True, (255, 255, 255))

        # 현재 레벨 표시
        level_text = font.render(f"Level: {variables.level[0]}", True, (255, 255, 255))
        screen.blit(level_text, (10, 70))

        if seconds > 0 and (temp - start_time) >= level_up_time:
            variables.level[0] += 1
            if variables.probability[0] > 15:
                variables.probability[0] -= 7
            level_up_time += 7000

        screen.blit(text, (10, 40))

        if player.invincible:
            invincible_text = font.render("INVINCIBLE!!", True, (255, 255, 255))
            screen.blit(invincible_text, (10, 100))

        # 충돌시 중지
        if pygame.sprite.spritecollide(player, arrows, True):
            if player.invincible:
                variables.current_score[0] += 1
            else:
                running = False

        # 게임 로직 업데이트
        player_group.update()
        arrows.update()
        items.update()
        # 게임 화면 그리기
        all_sprites.draw(screen)
        pygame.display.update()

    # 충돌 후, 최고 점수 및 최고 시간 전역 변수에 기록
    if variables.current_score[0] > variables.top_score[0]:
        variables.top_score[0] = variables.current_score[0]
    if variables.elapsed_time[0] > variables.max_time[0]:
        variables.max_time[0] = variables.elapsed_time[0]
    if variables.level[0] > variables.max_level[0]:
        variables.max_level[0] = variables.level[0]

    variables.probability[0] = 60

    all_sprites.empty()
    items.empty()
    arrows.empty()
    game_over()
