import pygame
import random
import json

# 初始化 Pygame
pygame.init()

# 定义常量
WIDTH, HEIGHT = 800, 600
TILE_SIZE = 100
ROWS, COLS = 4, 8
FPS = 30
FONT_SIZE = 48
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BG_COLOR = (200, 200, 200)
STORAGE_SIZE = 5  # 储存列表的最大数量
MAX_UPDATES = 100  # 最大更新次数
GAME_OVER_FONT_SIZE = 72  # Game Over 文字的大小
TIMER_FONT_SIZE = 48  # 计时器文字的大小
TIME_LIMIT = 60  # 游戏时间限制，单位为秒
SCORE_FONT_SIZE = 48  # 计分板文字的大小
POINTS_PER_MATCH = 10  # 每次匹配消除的分数
BUTTON_COLOR = (100, 100, 100)
BUTTON_HOVER_COLOR = (150, 150, 150)

# 创建窗口
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("动物消了个消")

# 加载字体
font = pygame.font.Font(None, FONT_SIZE)

# 加载图案图片
patterns = [pygame.image.load(f"pattern_{i}.png") for i in range(1, 7)]
patterns = [pygame.transform.scale(p, (TILE_SIZE, TILE_SIZE)) for p in patterns]

# 加载背景图片
background_image = pygame.image.load("background.png")
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

# 创建多层游戏板
board = [[random.choice(patterns) for _ in range(COLS)] for _ in range(ROWS)]

# 已点击的图片储存列表
storage = []

# 更新次数计数器
update_count = 0

# 游戏结束标志
game_over = False

# 计时器
timer = TIME_LIMIT

# 玩家分数
score = 0

# 排行榜文件名
HIGH_SCORE_FILE = "high_score.json"

# 显示开始界面 AIGC生成
def show_start_screen():
    start_font = pygame.font.Font(None, 48)
    start_text = start_font.render("Game Start", True, WHITE)
    start_rect = start_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    draw_text("Game Start", WIDTH // 2, HEIGHT // 2 - 100, WHITE, font)
    draw_text("Rank", WIDTH // 2, HEIGHT // 2 + 100, WHITE, font)

    start_button_rect = draw_button("Start", WIDTH // 2, HEIGHT // 2 - 50, BUTTON_COLOR)
    rank_button_rect = draw_button("Rank", WIDTH // 2, HEIGHT // 2 + 50, BUTTON_COLOR)
    start = True
    while start:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if start_rect.collidepoint(x, y):
                    start = False
                    return
                elif rank_button_rect.collidepoint(x, y):
                    show_rank_screen()


        screen.fill(BG_COLOR)  # 先填充背景色

        screen.blit(background_image, (0, 0))  # 绘制背景图片
        screen.blit(start_text, start_rect)  # 绘制开始文字
        pygame.display.flip()
        pygame.time.delay(100)

#AIGC生成
def draw_text(text, x, y, color, font):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)

def draw_button(text, x, y, color):
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect(center=(x, y))
    mouse = pygame.mouse.get_pos()
    if text_rect.collidepoint(mouse):
        color = BUTTON_HOVER_COLOR
    button_surface = pygame.Surface((text_rect.width + 20, text_rect.height + 10))
    button_surface.fill(color)
    button_surface.blit(text_surface, (10, 5))
    screen.blit(button_surface, text_rect.topleft)
    return button_surface.get_rect()

def show_rank_screen():
    high_score = load_high_score()
    draw_text(f"High Score: {high_score}", WIDTH // 2, HEIGHT // 2, RED, font)
    pygame.display.flip()
    pygame.time.wait(3000)  # Display for 3 seconds

def load_high_score():
    try:
        with open("high_score.json", 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return 0

# 绘制游戏板
def draw_board():
    for row in range(ROWS):
        for col in range(COLS):
            tile = board[row][col]
            if tile is not None:
                screen.blit(tile, (col * TILE_SIZE, row * TILE_SIZE))

# 绘制储存列表
def draw_storage():
    global game_over
    if len(storage) > STORAGE_SIZE:
        game_over = True
    x_offset = WIDTH - TILE_SIZE * min(len(storage), STORAGE_SIZE)
    if x_offset < 0:
        x_offset = 0
    y_offset = HEIGHT - TILE_SIZE
    for i, tile in enumerate(storage):
        if tile:
            screen.blit(tile, (x_offset + i * TILE_SIZE, y_offset))

# 绘制计时器
def draw_timer():
    timer_text = pygame.font.Font(None, TIMER_FONT_SIZE).render(f"Time: {int(timer)}", True, RED)
    timer_rect = timer_text.get_rect(topleft=(10, 10))
    screen.blit(timer_text, timer_rect)

# 绘制分数
def draw_score():
    score_text = pygame.font.Font(None, SCORE_FONT_SIZE).render(f"Score: {score}", True, RED)
    score_rect = score_text.get_rect(topleft=(10, 10 + 50))
    screen.blit(score_text, score_rect)


# 检查匹配并消除
def check_and_remove_matches(clicked_tile, row, col):
    global game_over, score
    if len(storage) >= STORAGE_SIZE:
        game_over = True
        return

    if clicked_tile in storage:
        score += POINTS_PER_MATCH  # 增加分数

    if clicked_tile in storage:
        storage.remove(clicked_tile)
        board[row][col] = None
    elif clicked_tile not in storage:
        storage.append(clicked_tile)
        board[row][col] = None

# 更新游戏板  AIGC生成
def update_board():
    global update_count
    empty_tiles = [(i, j) for i in range(ROWS) for j in range(COLS) if board[i][j] is None]
    if empty_tiles and update_count < MAX_UPDATES:
        for i, j in empty_tiles:
            board[i][j] = random.choice(patterns)
            update_count += 1
        if update_count >= MAX_UPDATES:
            return  # 达到最大更新次数后不再更新

# 点击图案
def click_tile(row, col):
    global storage
    clicked_tile = board[row][col]
    if clicked_tile:
        check_and_remove_matches(clicked_tile, row, col)
        update_board()
# 197-207行为AIGC生成
# 加载最高分
def load_high_score():
    try:
        with open(HIGH_SCORE_FILE, 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return 0

# 保存最高分
def save_high_score():
    with open(HIGH_SCORE_FILE, 'w') as file:
        json.dump(max(score, load_high_score()), file)

# 主游戏循环
def main():
    global timer, score
    high_score = load_high_score()
    show_start_screen()  # 显示开始界面

    running = True
    clock = pygame.time.Clock()

    while running:
        dt = clock.tick(FPS)  # 获取上一帧的时间间隔
        timer -= dt / 1000  # 更新计时器

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                col, row = x // TILE_SIZE, y // TILE_SIZE
                if 0 <= col < COLS and 0 <= row < ROWS:
                    click_tile(row, col)

        screen.fill(BG_COLOR)
        screen.blit(background_image, (0, 0))  # 绘制背景图片
        draw_board()
        draw_storage()
        draw_timer()  # 绘制计时器
        draw_score()  # 绘制分数
        if game_over or timer <= 0:
            game_over_font = pygame.font.Font(None, GAME_OVER_FONT_SIZE)
            game_over_text = game_over_font.render("Game Over", True, RED)
            game_over_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            screen.blit(game_over_text, game_over_rect)
            draw_score()  # 再次绘制分数，确保它显示在游戏结束屏幕上
            save_high_score()  # 保存最高分
            pygame.display.flip()
            pygame.time.delay(3000)  # 显示3秒后退出
            running = False

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()