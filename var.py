import pygame

# #main_window = UI_new.MainWindow()

# 전역 변수
current_score = [0]  # 점수 (매 게임 마다)
top_score = [0]  # 최고점

elapsed_time = [0]  # 경과 시간 (매 게임마다)
max_time = [0]  # 최고 경과 시간

level = [1]
max_level = [1]

probability = [60]

all_sprites = pygame.sprite.Group()
arrows = pygame.sprite.Group()
items = pygame.sprite.Group()
player_group = pygame.sprite.Group()
invincible_group = pygame.sprite.Group()
instantkill_group = pygame.sprite.Group()
freeze_group = pygame.sprite.Group()
arrow_kill_group = pygame.sprite.Group()

sprite_group = [arrows, items, player_group, invincible_group, instantkill_group, freeze_group, arrow_kill_group]
for item in sprite_group:
    all_sprites.add(item)

arrow_speed = [1]
level_up_time = [8000]

volume = 0.5



