import sys
import os
import random
import pygame
width = 500
height = 500
cols = 25
rows = 20
class RecordManager:
    def __init__(self, filename="record.txt"):
        self.filename = filename
        self.record = self._read_record()
    def _read_record(self):
        if os.path.exists(self.filename):
            with open(self.filename, "r") as f:
                try:
                    return int(f.read())
                except ValueError:
                    return 0  
        return 0
    def update_record(self, new_score):
        if new_score > self.record:
            self.record = new_score
            self._save_record()
    def _save_record(self):
        with open(self.filename, "w") as f:
            f.write(str(self.record))
class Cube():
    rows = 20
    w = 500
    def __init__(self, start, dirnx=1, dirny=0, color=(196, 22, 22)): #красный 
        self.pos = start
        self.dirnx = dirnx
        self.dirny = dirny  #направление движения
        self.color = color
    def move(self, dirnx, dirny):
        self.dirnx = dirnx
        self.dirny = dirny
        self.pos = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny)
    def draw(self, surface, eyes=False):
        dis = self.w // self.rows
        i = self.pos[0]
        j = self.pos[1]
        pygame.draw.rect(surface, self.color, (i * dis + 1, j * dis + 1, dis - 2, dis - 2))
        if eyes:
            centre = dis // 2
            radius = 3
            circleMiddle = (i * dis + centre - radius, j * dis + 8)
            circleMiddle2 = (i * dis + dis - radius * 2, j * dis + 8)
            pygame.draw.circle(surface, (0, 0, 0), circleMiddle, radius)
            pygame.draw.circle(surface, (0, 0, 0), circleMiddle2, radius)
class Snake():
    body = []
    turns = {}
    def __init__(self, color, pos):
        self.color = color 
        self.head = Cube(pos, color=self.color)
        self.body.append(self.head)
        self.dirnx = 0
        self.dirny = 1
    def move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        keys = pygame.key.get_pressed()
        #управление 
        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and self.dirnx == 0:
            self.dirnx = -1
            self.dirny = 0
            self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
        elif (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and self.dirnx == 0:
            self.dirnx = 1
            self.dirny = 0
            self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
        elif (keys[pygame.K_UP] or keys[pygame.K_w]) and self.dirny == 0:
            self.dirny = -1
            self.dirnx = 0
            self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
        elif (keys[pygame.K_DOWN] or keys[pygame.K_s]) and self.dirny == 0:
            self.dirny = 1
            self.dirnx = 0
            self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
        for i, c in enumerate(self.body):
            p = c.pos[:]
            if p in self.turns:
                turn = self.turns[p]
                c.move(turn[0], turn[1])
                if i == len(self.body) - 1:
                    self.turns.pop(p)
            else:
                c.move(c.dirnx, c.dirny)
    def reset(self, pos):
        self.head = Cube(pos, color=self.color)
        self.body = [self.head]
        self.turns = {}
        self.dirnx = 0
        self.dirny = 1
    def addCube(self):
        tail = self.body[-1]
        dx, dy = tail.dirnx, tail.dirny
        if dx == 1 and dy == 0:
            self.body.append(Cube((tail.pos[0] - 1, tail.pos[1]), color=self.color))
        elif dx == -1 and dy == 0:
            self.body.append(Cube((tail.pos[0] + 1, tail.pos[1]), color=self.color))
        elif dx == 0 and dy == 1:
            self.body.append(Cube((tail.pos[0], tail.pos[1] - 1), color=self.color))
        elif dx == 0 and dy == -1:
            self.body.append(Cube((tail.pos[0], tail.pos[1] + 1), color=self.color))
        self.body[-1].dirnx = dx
        self.body[-1].dirny = dy
    def draw(self, surface):
        for i, c in enumerate(self.body):
            if i == 0:
                c.draw(surface, True)
            else:
                c.draw(surface)
#окно игры
def redrawWindow():
    global win
    win.fill((255, 239, 204))
    #рекорд и счет на экране
    font = pygame.font.SysFont('Times New Roman', 25, bold=True)
    score_text = font.render(f"Счёт: {len(s.body)}", True, (0, 0, 0))
    record_text = font.render(f"Рекорд: {record_manager.record}", True, (0, 0, 0))
    win.blit(score_text, (10, 1)) 
    win.blit(record_text, (10, 25)) 
    drawGrid(width, rows, win)
    s.draw(win)
    snack.draw(win)
    pygame.display.update()
def drawGrid(w, rows, surface):  #сетка
    sizeBtwn = w // rows
    x = 0
    y = 0
    for l in range(rows):
        x = x + sizeBtwn
        y = y + sizeBtwn
        pygame.draw.line(surface, (139, 69, 19), (x, 0), (x, w))
        pygame.draw.line(surface, (139, 69, 19), (0, y), (w, y))
#случайные позиции еды
def randomSnack(rows, item):
    positions = {cube.pos for cube in item.body}
    while True:
        x, y = random.randint(0, rows - 1), random.randint(0, rows - 1)
        if (x, y) not in positions:
            return (x, y)
def start_screen():
    global win
    start = True
    bg_color = (230, 230, 250)  #лаванда
    button_color = (53, 135, 53)  #тёмно-зелёный
    button_hover_color = (50, 205, 50)  #сочный зелёный
    exit_button_color = (168, 39, 39)  #тёмно-красный
    exit_hover_color = (247, 40, 81)  #ярко-красный
    rules_button_color = (43, 149, 255)  #синий
    rules_hover_color = (0, 191, 255)  #светло-синий
    while start:
        win.fill(bg_color)
        #заголовок
        font = pygame.font.SysFont('Times New Roman', 70, bold=True)
        title_text = font.render("Snake Game", True, (0, 102, 0))
        win.blit(title_text, (width // 2 - title_text.get_width() // 2, height // 4))
        #рекорд
        record_font = pygame.font.SysFont('Times New Roman', 50, bold=True)
        record_text = record_font.render(f"Рекорд: {record_manager.record}", True, (0, 100, 0))
        win.blit(record_text, (width // 2 - record_text.get_width() // 2, height // 2 - 50))
        #кнопка "Начать игру"
        mouse_pos = pygame.mouse.get_pos()
        button_rect = pygame.Rect(width // 2 - 70, height // 2 + 40, 140, 40)
        if button_rect.collidepoint(mouse_pos):
            pygame.draw.rect(win, button_hover_color, button_rect)
        else:
            pygame.draw.rect(win, button_color, button_rect)
        button_font = pygame.font.SysFont('Times New Roman', 23, bold=True)
        button_text = button_font.render("Начать игру", True, (255, 255, 255))
        button_text_rect = button_text.get_rect(center=button_rect.center) 
        win.blit(button_text, button_text_rect)
        #кнопка "Правила" 
        rules_button_rect = pygame.Rect(width // 2 - 70, height // 2 + 90, 140, 40)
        if rules_button_rect.collidepoint(mouse_pos):
            pygame.draw.rect(win, rules_hover_color, rules_button_rect)
        else:
            pygame.draw.rect(win, rules_button_color, rules_button_rect)
        rules_button_font = pygame.font.SysFont('Times New Roman', 26, bold=True)
        rules_button_text = rules_button_font.render("Правила", True, (255, 255, 255))
        rules_button_text_rect = rules_button_text.get_rect(center=rules_button_rect.center)  
        win.blit(rules_button_text, rules_button_text_rect)
        #кнопка "Выйти из игры" 
        exit_button_rect = pygame.Rect(width // 2 - 70, height // 2 + 140, 140, 40)
        if exit_button_rect.collidepoint(mouse_pos):
            pygame.draw.rect(win, exit_hover_color, exit_button_rect)
        else:
            pygame.draw.rect(win, exit_button_color, exit_button_rect)
        exit_button_font = pygame.font.SysFont('Times New Roman', 26, bold=True)
        exit_button_text = exit_button_font.render("Выйти", True, (255, 255, 255))
        exit_button_text_rect = exit_button_text.get_rect(center=exit_button_rect.center)  
        win.blit(exit_button_text, exit_button_text_rect)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):  
                    start = False
                elif exit_button_rect.collidepoint(event.pos):  
                    pygame.quit()
                    sys.exit()
                elif rules_button_rect.collidepoint(event.pos):
                    show_rules()  
def show_rules():
    running = True
    while running:
        win.fill((240, 240, 240)) 
        font = pygame.font.SysFont('Times New Roman', 19)
        rules_text = [
            "Правила игры Snake:",
            "1. Управляйте змейкой с помощью стрелок или WASD.",
            "2. Собирайте яблоки, чтобы змейка увеличивалась.",
            "3. Не врежьтесь в стены или себя!",
            "4. Ваш счёт увеличивается с каждым яблоком.",
        ]
        for i, line in enumerate(rules_text):
            text = font.render(line, True, (0, 0, 0))
            win.blit(text, (20, 50 + i * 40))
        #кнопка "Назад"
        back_button_rect = pygame.Rect(width // 2 - 100, height - 100, 200, 50)
        mouse_pos = pygame.mouse.get_pos()
        if back_button_rect.collidepoint(mouse_pos):
            pygame.draw.rect(win, (200, 200, 200), back_button_rect)
        else:
            pygame.draw.rect(win, (180, 180, 180), back_button_rect)
        back_font = pygame.font.SysFont('Times New Roman', 40, bold=True)
        back_text = back_font.render("Назад", True, (0, 0, 0))
        back_text_rect = back_text.get_rect(center=back_button_rect.center)
        win.blit(back_text, back_text_rect)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button_rect.collidepoint(event.pos):
                    running = False
def draw_pause_screen():
    global win
    pause = True
    bg_color = (230, 230, 250) #лаванда
    button_color = (128, 128, 128)  #тёмно-серый
    button_hover_color = (169, 169, 169)  #светлый серый
    while pause:
        win.fill(bg_color)
        #заголовок
        font = pygame.font.SysFont('Times New Roman', 70, bold=True)
        pause_text = font.render("Пауза", True, (0, 102, 0))
        win.blit(pause_text, (width // 2 - pause_text.get_width() // 2, height // 4))
        #кнопка "Продолжить"
        mouse_pos = pygame.mouse.get_pos()
        resume_button_rect = pygame.Rect(width // 4, height // 2, width // 2, 50)
        if resume_button_rect.collidepoint(mouse_pos):  #мигающий эффект при наведении
            pygame.draw.rect(win, button_hover_color, resume_button_rect)  
        else:
            pygame.draw.rect(win, button_color, resume_button_rect) 
        resume_button_font = pygame.font.SysFont('Times New Roman', 35, bold=True)
        resume_button_text = resume_button_font.render("Продолжить", True, (0, 0, 0))
        resume_button_text_rect = resume_button_text.get_rect(center=resume_button_rect.center)
        win.blit(resume_button_text, resume_button_text_rect)
        #кнопка "Выйти"
        quit_button_rect = pygame.Rect(width // 4, height // 1.5, width // 2, 50)
        if quit_button_rect.collidepoint(mouse_pos):  
            pygame.draw.rect(win, button_hover_color, quit_button_rect)  
        else:
            pygame.draw.rect(win, button_color, quit_button_rect)  
        quit_button_font = pygame.font.SysFont('Times New Roman', 35, bold=True)
        quit_button_text = quit_button_font.render("Выйти", True, (0, 0, 0))
        quit_button_text_rect = quit_button_text.get_rect(center=quit_button_rect.center)
        win.blit(quit_button_text, quit_button_text_rect)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if resume_button_rect.collidepoint(event.pos): 
                    pause = False
                    countdown_timer()
                elif quit_button_rect.collidepoint(event.pos): 
                    pygame.quit()
                    sys.exit()
    
    return resume_button_rect, quit_button_rect
def countdown_timer():
    global win
    circle_color = (50, 205, 50)  #cочный зелёный
    text_color = (0, 0, 0)  
    font = pygame.font.SysFont('Times New Roman', 100, bold=True)  
    circle_center = (width // 2, height // 2) 
    circle_radius = 100  
    thickness = 15  # 
    for count in range(3, 0, -1):  
        redrawWindow()
        #угол для цветной обводки
        start_angle = 0
        end_angle = (count / 3) * 360  #пропорция длины обводки
        pygame.draw.arc(win, circle_color, 
                        (circle_center[0] - circle_radius, circle_center[1] - circle_radius, 
                         2 * circle_radius, 2 * circle_radius), 
                        -end_angle * (3.14 / 180),  
                        -start_angle * (3.14 / 180), 
                        thickness)
        #цифра внутри круга
        number_text = font.render(str(count), True, text_color)
        text_rect = number_text.get_rect(center=circle_center)
        win.blit(number_text, text_rect)
        pygame.display.update()
        pygame.time.delay(1000)  #задержка 1 секунда
    redrawWindow()
    font = pygame.font.SysFont('Times New Roman', 70, bold=True) 
    start_text = font.render("Старт!", True, text_color)
    start_rect = start_text.get_rect(center=(width // 2, height // 2))
    win.blit(start_text, start_rect)
    pygame.display.update()
    pygame.time.delay(500)  #задержка на старте
def main():
    pygame.init()
    global s, snack, win, record_manager
    win = pygame.display.set_mode((width, height))
    record_manager = RecordManager() 
    pygame.display.set_caption("Snake Game")
    start_screen() 
    s = Snake((20, 143, 24), (10, 10))
    snack = Cube(randomSnack(rows, s), color=(128, 0, 0))
    clock = pygame.time.Clock()
    game_running = True
    game_paused = False 
    while game_running:
        pygame.time.delay(50)
        clock.tick(9)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_paused = not game_paused  
                if game_paused:
                    if event.key == pygame.K_r:  
                        game_paused = False
                    if event.key == pygame.K_q:  
                        game_running = False
        if game_paused:
            resume_button, quit_button = draw_pause_screen()  #окно паузы 
            mouse_pos = pygame.mouse.get_pos()
            mouse_click = pygame.mouse.get_pressed()
            #проверка нажатия кнопок
            if resume_button.collidepoint(mouse_pos) and mouse_click[0]:
                game_paused = False
            if quit_button.collidepoint(mouse_pos) and mouse_click[0]:
                game_running = False
        else:
            #логика игры
            s.move()
            headPos = s.head.pos
            if headPos[0] >= cols or headPos[0] < 0 or headPos[1] >= rows or headPos[1] < 0:
                record_manager.update_record(len(s.body))  
                print("Score:", len(s.body))
                s.reset((10, 10))
            if s.body[0].pos == snack.pos:
                s.addCube()
                snack = Cube(randomSnack(rows, s), color=(128, 0, 0))
            for x in range(len(s.body)):
                if s.body[x].pos in list(map(lambda z: z.pos, s.body[x + 1:])):
                    record_manager.update_record(len(s.body))
                    print("Score:", len(s.body))
                    s.reset((10, 10))
                    break
            redrawWindow()
    
    sys.exit()
main()
