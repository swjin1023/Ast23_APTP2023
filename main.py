import sys
import pygame
import random
import tkinter as tk
# 스크린 정보
screen_width = 1000
screen_height = 800
center = screen_width // 2, screen_height // 2

# 원 정보
radius = 300
circle_color = (255, 255, 255)
circle_width = 1

# 전역 변수
current_score = 0  # 점수 (매 게임 마다)
top_score = 0  # 최고점
global show_score  # tkinter에 보여줄 최고점수 (tk.Stringvar() 형)

elapsed_time = 0  # 경과 시간 (매 게임마다)
max_time = 0  # 최고 경과 시간
global show_time  # tkinter에 보여줄 최고 경과 시간 (tk.Stringvar() 형)

# 객체 속도: 시간이 지남에 따라 난이도 변경 + 아이템 효과를 위해서 전역 변수로 설정
player_speed = 5
arrow_speed = 1

level = 1
max_level = 1
global show_level
global screen  # pygame screen
max_num_arrows = 15 * level

probability = 60

all_sprites = pygame.sprite.Group()
arrows = pygame.sprite.Group()
items = pygame.sprite.Group()


class DefaultArrow(pygame.sprite.Sprite):
    """화살 객체(위->아래)"""
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.flip(pygame.transform.scale(pygame.image.load("arrow.png"), (10, 30)), False, True) # 이미지 가져오기
        self.rect = self.image.get_rect()  # 화살 이미지 좌측 상단 모서리의 x, y 좌표 가져옴
        self.width = self.image.get_width()  # 화살 너비
        self.height = self.image.get_height()  # 화살 높이
        self.rect.x = random.randint(center[0] - radius, center[0] + radius - self.width)  # 화살 x좌표 변경
        self.rect.y = 0  # 화살 y좌표 변경

        # 화살 이동 속도
        self.speed = arrow_speed
        
        # 화살 delta값
        self.dx = self.speed
        self.dy = self.speed

    def update(self):  # 게임 frame당 변화
        # 화살 이동
        for i in range(0, level):
            self.rect.y += self.dy  # 기본값은 위에서 아래로 내려오는 것.
            if self.rect.y > screen_height:  # 화면 밖으로 나갔는지 확인
                self.kill()  # 객체 삭제
                global current_score
                current_score += 1
        # 왼쪽 위가 (0,0)이다!

class LeftArrow(DefaultArrow):
    """화살 객체(왼쪽->오른쪽)"""
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.rotate(self.image, 90)
        self.rect.x = 0  # 화살 x좌표 변경
        self.rect.y = random.randint(center[1] - radius, center[1] + radius - self.height) # 화살 y좌표 변경

    def update(self):
        for i in range(0, level):
            self.rect.x += self.dx
            if self.rect.x > screen_width:
                self.kill()
                global current_score
                current_score += 1

class RightArrow(DefaultArrow):
    """화살 객체(오른쪽->왼쪽)"""
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.rotate(self.image, -90)
        self.rect.x = screen_width - self.width  # 화살 x좌표 변경
        self.rect.y = random.randint(center[1] - radius, center[1] + radius - self.height) # 화살 y좌표 변경

    def update(self):
        for i in range(0, level):
            self.rect.x -= self.dx
            if self.rect.x < 0:
                self.kill()
                global current_score
                current_score += 1

class BottomArrow(DefaultArrow):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.flip(self.image, False, True)
        self.rect.x = random.randint(center[0] - radius, center[0] + radius - self.width)  # 화살 x좌표 변경
        self.rect.y = screen_height - self.height  # 화살 y좌표 변경

    def update(self):
        # 화살 이동
        for i in range(0, level):
            self.rect.y -= self.dy
        # 화면 밖으로 나갔는지 확인
            if self.rect.y < 0:
                self.kill()
                global current_score
                current_score += 1

class Player(pygame.sprite.Sprite):
    """player 객체"""
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load("target.png"), (20, 20))
        self.rect = self.image.get_rect()
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        # 초기 위치: 중앙
        self.rect.x = center[0]
        self.rect.y = center[1]
        # 객체 이동속도
        self.speed = player_speed

        # 무적 상태 (기본: False)
        self.invincible = False

    def update(self):
        # 목표물 이동
        status = (self.rect.x-center[0]) ** 2 + (self.rect.y - center[1])**2
        x_before, y_before = self.rect.x, self.rect.y
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and status < radius ** 2:
            self.rect.x -= self.speed

        if keys[pygame.K_RIGHT] and status < radius ** 2:
            self.rect.x += self.speed

        if keys[pygame.K_UP] and status < radius ** 2:
            self.rect.y -= self.speed

        if keys[pygame.K_DOWN] and status < radius ** 2:
            self.rect.y += self.speed

        status = (self.rect.x-center[0]) ** 2 + (self.rect.y - center[1])**2
        if status >= radius ** 2:
            self.rect.x = x_before
            self.rect.y = y_before


        # 화살과 충돌 여부 확인
        
class Item(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = None
        self.rect = self.image.get_rect()
        self.width = self.image.get_width()
        self.height = self.image.get_height()

    def update(self):
        pass


class Invincible(Item):
    """3초 동안 무적"""
    def __init__(self):
        super().__init__()

def game_over():
    """게임 종료 함수"""
    # Game over screen
    game_over_page_font = pygame.font.SysFont(None, 50)
    game_over_text = game_over_page_font.render("Game Over", True, (0, 0, 0))
    game_over_rect = game_over_text.get_rect()
    game_over_rect.center = (screen_width / 2, screen_height / 2 - 50)

    score_text = game_over_page_font.render(f"Score: {current_score}", True, (0, 0, 0))
    score_text_rect = score_text.get_rect()
    score_text_rect.center = (screen_width / 2 - 8, screen_height / 2 + 10)

    time_text = game_over_page_font.render("time: {:02d}:{:02d}".format(elapsed_time // 60, elapsed_time % 60), True, (0, 0, 0))
    time_text_rect = score_text.get_rect()
    time_text_rect.center = (screen_width / 2 - 13, screen_height / 2 + 50)

    level_text = game_over_page_font.render(f"Level: {level}", True, (0, 0, 0))
    level_text_rect = level_text.get_rect()
    level_text_rect.center = (screen_width / 2 - 26, screen_height / 2 + 90)

    screen.fill((255, 255, 255))
    screen.blit(game_over_text, game_over_rect)
    screen.blit(score_text, score_text_rect)
    screen.blit(time_text, time_text_rect)
    screen.blit(level_text, level_text_rect)
    pygame.display.update()
    # Wait for a few seconds before quitting
    pygame.time.wait(2000)

    # Quit pygame
    pygame.quit()
    show_score.set(f"최고 점수: {str(top_score)}")
    show_time.set("최고 시간: {:02d}:{:02d}".format(max_time // 60, max_time % 60))

def game_start():
    """게임 시작 함수"""
    pygame.init()
    global screen
    global current_score
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("화살 피하기 게임")
    bg_img = pygame.transform.scale(pygame.image.load("background.jpg"), (screen_width, screen_height))
    screen.blit(bg_img, (0, 0))
    #screen.fill((255, 255, 255))  #   # 배경



    player = Player()
    all_sprites.add(player)

    clock = pygame.time.Clock()

    running = True
    start_time = pygame.time.get_ticks()  # 경과 시간 표시하기 위해 가져옴.
    level_up_time = 7000

    while running:
        # 배경 이미지
        screen.blit(bg_img, (0, 0))

        # 가운데 원 그리기
        pygame.draw.circle(screen, circle_color, center, radius, circle_width)
        pygame.draw.circle(screen, (0, 0, 0), center, radius - circle_width)

        # FPS
        clock.tick(60)

        # 이벤트 처리
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        global probability
        # 화살 랜덤 생성 (확률을 randint로 조정)
        arrow_select = random.randint(1, probability)
        if len(arrows.sprites()) < max_num_arrows:
            if arrow_select == 1:
                new_arrow = DefaultArrow()
                arrows.add(new_arrow)
                all_sprites.add(new_arrow)
            elif arrow_select == 2:
                new_arrow = LeftArrow()
                arrows.add(new_arrow)
                all_sprites.add(new_arrow)
            elif arrow_select == 3:
                new_arrow = RightArrow()
                arrows.add(new_arrow)
                all_sprites.add(new_arrow)
            elif arrow_select == 4:
                new_arrow = BottomArrow()
                arrows.add(new_arrow)
                all_sprites.add(new_arrow)

        
        # 현재 점수 표시
        font = pygame.font.SysFont(None, 30)
        score_text = font.render("Score: " + str(current_score), True, (255, 255, 255))
        screen.blit(score_text, (10, 10))

        # 현재 경과 시간 표시
        global elapsed_time
        temp = pygame.time.get_ticks()

        elapsed_time = (temp - start_time) // 1000  # 밀리초를 초 단위로 변환
        minutes = elapsed_time // 60  # 분 계산
        seconds = elapsed_time % 60  # 초 계산
        text = font.render("{:02d}:{:02d}".format(minutes, seconds), True, (255, 255, 255))

        global level
        level_text = font.render(f"Level: {level}", True, (255, 255, 255))
        screen.blit(level_text, (10, 70))

        if seconds > 0 and (temp - start_time) >= level_up_time:
            level += 1
            if probability > 15:
                probability -= 11
            level_up_time += 7000

        screen.blit(text, (10, 40))

        if pygame.sprite.spritecollide(player, items, True):
            pass
        # 충돌시 중지
        if pygame.sprite.spritecollide(player, arrows, True) and not player.invincible:
            running = False

        # 게임 로직 업데이트
        player.update()
        arrows.update()

        # 게임 화면 그리기
        all_sprites.draw(screen)
        pygame.display.update()

    # 충돌 후, 최고 점수 및 최고 시간 전역 변수에 기록
    global top_score, max_time, max_level
    if current_score > top_score:
        top_score = current_score
    if elapsed_time > max_time:
        max_time = elapsed_time
    if level > max_level:
        max_level = level

    game_over()
    level = 1
    current_score = 0
    elapsed_time = 0
    all_sprites.empty()
    items.empty()
    arrows.empty()

def terminate():
    """tkinter 종료 (전체 프로그램 종료) 함수"""
    root.destroy()
    sys.exit()

# tkinter 말고 다른 좋은 UI쓰는 것도 좋아요! tkinter는 한번 써봤어서 급조한 UI에요.
class UI(tk.Frame):
    """메인 화면(tkinter) UI class"""
    def __init__(self, master):
        super().__init__(master)
        master.geometry("350x350")
        master.title("화살 피하기")
        title_label = tk.Label(master, text="짭림고수", width=9, font=("Helvetica", 14))
        title_label.pack(side="top")
        game_start_button = tk.Button(master, height=4, width=8, text="게임 시작!", font=("Helvetica", 14), command=game_start)
        game_start_button.pack(side="left")

        exit_button = tk.Button(master, height=4, width=8, text="게임 종료", font=("Helvetica", 14), command=terminate)
        exit_button.pack(side="right")

        global show_score
        show_score = tk.StringVar()
        show_score.set(f"최고 점수: {str(top_score)}")
        score_label = tk.Label(root, textvariable=show_score, font=("Helvetica", 14))
        score_label.pack(side="bottom")

        global show_time
        show_time = tk.StringVar()
        show_time.set("최고 시간: {:02d}:{:02d}".format(max_time // 60, max_time % 60))
        time_label = tk.Label(root, textvariable=show_time, font=("Helvetica", 14))
        time_label.pack(side="bottom")

        global show_level
        show_level = tk.StringVar()
        show_level.set(f"최고 레벨: {max_level}")
        level_label = tk.Label(root, textvariable=show_level, font=("Helvetica", 14))
        level_label.pack(side="bottom")


if __name__ == "__main__":
    root = tk.Tk()  # tkinter root
    main_page = UI(root)
    root.mainloop()
