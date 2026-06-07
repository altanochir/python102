"""
╔══════════════════════════════════════════════════════════════════╗
║  🧩 Хичээл 4.7: Сонгодог Тетрис (Classic Tetris)                  ║
║  Матрицын мөргөлдөөн (Matrix Grid Collision), Эргэлтийн алгоритм ║
║  (Rotation Matrix), Мөр устгах ба Дараагийн дүрсийг харах        ║
╚══════════════════════════════════════════════════════════════════╝

🎯 Энэ хичээлээр үзэх сэдвүүд:
   1. Тетрис хүснэгт (10x20 Grid Matrix) ба Дүрсийн өгөгдөл (Tetrominoes)
   2. Дүрсийг эргүүлэх (Rotation) ба Хязгаар шалгах (Wall Kick/Boundaries)
   3. Автомат уналтын хурд болон Зөөлөн/Хатуу уналт (Soft/Hard Drop)
   4. Бүтэн мөрүүдийг илрүүлж устгах ба Оноо бодох (Line Clear & Score)
   5. Дараагийн дүрс харуулах (Next Piece) ба Хадгалах (Hold Piece)
"""

import sys
import random

try:
    import pygame
except ImportError:
    print("⚠️ Pygame суугаагүй байна! 'pip install pygame' ажиллуулна уу.")
    sys.exit(1)


# --- Тоглоомын хэмжээнүүд ---
CELL_SIZE = 30
GRID_WIDTH = 10
GRID_HEIGHT = 20
PLAY_WIDTH = GRID_WIDTH * CELL_SIZE
PLAY_HEIGHT = GRID_HEIGHT * CELL_SIZE

# Нийт дэлгэцийн хэмжээ
WIDTH, HEIGHT = 800, 700

# --- Catppuccin Theme Colors ---
BG_COLOR = (30, 30, 46)        # Deep charcoal
PANEL_COLOR = (24, 24, 37)      # Darker panels
TEXT_COLOR = (205, 214, 244)    # Soft white
GRID_COLOR = (49, 50, 68)       # Soft grid lines
ACCENT_COLOR = (137, 180, 250)  # Sapphire blue
WHITE = (255, 255, 255)


# Тетромино дүрсийн загвар ба өнгөнүүд (Arcade colors)
SHAPES = {
    "I": [[1, 1, 1, 1]],
    
    "J": [[1, 0, 0],
          [1, 1, 1]],
          
    "L": [[0, 0, 1],
          [1, 1, 1]],
          
    "O": [[1, 1],
          [1, 1]],
          
    "S": [[0, 1, 1],
          [1, 1, 0]],
          
    "T": [[0, 1, 0],
          [1, 1, 1]],
          
    "Z": [[1, 1, 0],
          [0, 1, 1]]
}

SHAPE_COLORS = {
    "I": (137, 180, 250), # Цэнхэр
    "J": (114, 135, 253), # Нил ягаан
    "L": (250, 179, 135), # Шаргал
    "O": (249, 226, 175), # Шар
    "S": (166, 227, 161), # Ногоон
    "T": (203, 166, 247), # Ягаан
    "Z": (243, 139, 168)  # Улаан
}


class Piece:
    def __init__(self, shape_name):
        self.name = shape_name
        self.matrix = [row[:] for row in SHAPES[shape_name]]
        self.color = SHAPE_COLORS[shape_name]
        
        # Хүснэгтийн оройн төвийн байрлал
        self.x = GRID_WIDTH // 2 - len(self.matrix[0]) // 2
        self.y = 0
        
    def rotate(self):
        # Матрицыг цагийн зүүний дагуу 90 градус эргүүлэх
        self.matrix = [list(x) for x in zip(*self.matrix[::-1])]


class TetrisGame:
    def __init__(self):
        self.grid = [[None for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.current_piece = self.get_random_piece()
        self.next_piece = self.get_random_piece()
        self.hold_piece = None
        self.has_held_this_turn = False
        
        # Үзүүлэлтүүд
        self.score = 0
        self.lines_cleared = 0
        self.level = 1
        self.game_over = False
        
    def get_random_piece(self):
        shape_name = random.choice(list(SHAPES.keys()))
        return Piece(shape_name)
        
    def hold(self):
        if self.has_held_this_turn:
            return
            
        if self.hold_piece is None:
            # Хадгалсан дүрс байхгүй бол одоогийн дүрсийг хадгалаад дараагийн дүрсийг гаргах
            self.hold_piece = Piece(self.current_piece.name)
            self.current_piece = self.next_piece
            self.next_piece = self.get_random_piece()
        else:
            # Хадгалсан дүрс байвал солих
            temp = self.hold_piece.name
            self.hold_piece = Piece(self.current_piece.name)
            self.current_piece = Piece(temp)
            
        self.has_held_this_turn = True
        
    def check_collision(self, dx=0, dy=0, custom_matrix=None):
        matrix = custom_matrix if custom_matrix is not None else self.current_piece.matrix
        for r_idx, row in enumerate(matrix):
            for c_idx, val in enumerate(row):
                if val:
                    new_x = self.current_piece.x + c_idx + dx
                    new_y = self.current_piece.y + r_idx + dy
                    
                    # Хил хязгаар шалгах
                    if new_x < 0 or new_x >= GRID_WIDTH or new_y >= GRID_HEIGHT:
                        return True
                    # Бусад түгжигдсэн дүрсүүдтэй мөргөлдөх
                    if new_y >= 0 and self.grid[new_y][new_x] is not None:
                        return True
        return False
        
    def rotate_piece(self):
        # Дүрсийг түр эргүүлж шалгах
        original_matrix = self.current_piece.matrix
        self.current_piece.rotate()
        
        # Хэрэв эргэхэд мөргөлдөөн үүсвэл буцаах (Wall Kick үндсэн шалгалт)
        if self.check_collision():
            # Баруун тийш 1 нүд түлхэж үзэх
            self.current_piece.x += 1
            if self.check_collision():
                # Зүүн тийш 1 нүд түлхэж үзэх
                self.current_piece.x -= 2
                if self.check_collision():
                    # Буцаад хуучин байранд нь оруулна
                    self.current_piece.x += 1
                    self.current_piece.matrix = original_matrix

    def move_left(self):
        if not self.check_collision(dx=-1):
            self.current_piece.x -= 1
            
    def move_right(self):
        if not self.check_collision(dx=1):
            self.current_piece.x += 1
            
    def soft_drop(self):
        if not self.check_collision(dy=1):
            self.current_piece.y += 1
            return True
        else:
            self.lock_piece()
            return False
            
    def hard_drop(self):
        # Доош мөргөлдөх хүртэл явна
        while not self.check_collision(dy=1):
            self.current_piece.y += 1
        self.lock_piece()
        
    def lock_piece(self):
        # Дүрсийг хүснэгтэд шилжүүлж түгжих
        for r_idx, row in enumerate(self.current_piece.matrix):
            for c_idx, val in enumerate(row):
                if val:
                    grid_y = self.current_piece.y + r_idx
                    grid_x = self.current_piece.x + c_idx
                    # Дэлгэцээс гарсан хэсэгт түгжигдвэл Game Over
                    if grid_y < 0:
                        self.game_over = True
                    else:
                        self.grid[grid_y][grid_x] = self.current_piece.color
                        
        if not self.game_over:
            self.clear_lines()
            # Шинэ дүрс оруулах
            self.current_piece = self.next_piece
            self.next_piece = self.get_random_piece()
            self.has_held_this_turn = False
            
            # Шинэ дүрс орж ирээд шууд мөргөлдвөл тоглоом дуусна
            if self.check_collision():
                self.game_over = True
                
    def clear_lines(self):
        lines_to_clear = []
        for r_idx in range(GRID_HEIGHT):
            if all(cell is not None for cell in self.grid[r_idx]):
                lines_to_clear.append(r_idx)
                
        # Мөрүүдийг устгах
        for r_idx in lines_to_clear:
            del self.grid[r_idx]
            # Дээд талд хоосон мөр нэмэх
            self.grid.insert(0, [None for _ in range(GRID_WIDTH)])
            
        # Оноо бодох (Nintendo Tetris дүрэм)
        num_cleared = len(lines_to_clear)
        if num_cleared == 1:
            self.score += 40 * self.level
        elif num_cleared == 2:
            self.score += 100 * self.level
        elif num_cleared == 3:
            self.score += 300 * self.level
        elif num_cleared == 4:
            self.score += 1200 * self.level
            
        self.lines_cleared += num_cleared
        self.level = self.lines_cleared // 10 + 1

    def draw(self, screen):
        # 1. Төв тоглох талбарын арын суурь
        play_x = 260
        play_y = 50
        pygame.draw.rect(screen, PANEL_COLOR, (play_x, play_y, PLAY_WIDTH, PLAY_HEIGHT), border_radius=6)
        
        # Сүлжээний шугамууд (Dotted Lines)
        for x in range(1, GRID_WIDTH):
            pygame.draw.line(screen, GRID_COLOR, (play_x + x * CELL_SIZE, play_y), (play_x + x * CELL_SIZE, play_y + PLAY_HEIGHT), 1)
        for y in range(1, GRID_HEIGHT):
            pygame.draw.line(screen, GRID_COLOR, (play_x, play_y + y * CELL_SIZE), (play_x + PLAY_WIDTH, play_y + y * CELL_SIZE), 1)
            
        # 2. Түгжигдсэн дүрсүүдийг (Grid) зурах
        for r in range(GRID_HEIGHT):
            for c in range(GRID_WIDTH):
                color = self.grid[r][c]
                if color:
                    self.draw_block(screen, play_x + c * CELL_SIZE, play_y + r * CELL_SIZE, color)
                    
        # 3. Одоо унаж буй дүрсийг зурах
        if not self.game_over:
            for r_idx, row in enumerate(self.current_piece.matrix):
                for c_idx, val in enumerate(row):
                    if val:
                        bx = play_x + (self.current_piece.x + c_idx) * CELL_SIZE
                        by = play_y + (self.current_piece.y + r_idx) * CELL_SIZE
                        if by >= play_y: # Зөвхөн талбар доторхыг зурна
                            self.draw_block(screen, bx, by, self.current_piece.color)
                            
        # Талбарын гаднах неон хүрээ
        pygame.draw.rect(screen, (74, 85, 114), (play_x, play_y, PLAY_WIDTH, PLAY_HEIGHT), width=3, border_radius=6)
        
        # 4. Зүүн талын ХАНЕЛИ: HOLD дэлгэц
        self.draw_side_panel(screen, 40, 50, 180, 150, "HOLD")
        if self.hold_piece:
            self.draw_preview_piece(screen, 40, 50, 180, 150, self.hold_piece)
            
        # Онооны самбар
        self.draw_side_panel(screen, 40, 240, 180, 360, "INFO")
        self.draw_info_text(screen, 40, 240)
        
        # 5. Баруун талын ХАНЕЛИ: NEXT дэлгэц
        self.draw_side_panel(screen, 580, 50, 180, 150, "NEXT")
        self.draw_preview_piece(screen, 580, 50, 180, 150, self.next_piece)
        
        # Удирдлагын заавар
        self.draw_side_panel(screen, 580, 240, 180, 360, "CONTROLS")
        self.draw_controls_text(screen, 580, 240)

    def draw_block(self, screen, x, y, color):
        """Хөзөр мэт bevel хийж 3D загвартай блок зурах"""
        pygame.draw.rect(screen, color, (x + 1, y + 1, CELL_SIZE - 2, CELL_SIZE - 2), border_radius=4)
        # Гялгар ирмэг (Light top/left highlight)
        pygame.draw.line(screen, (255, 255, 255), (x + 3, y + 3), (x + CELL_SIZE - 4, y + 3), 2)
        pygame.draw.line(screen, (255, 255, 255), (x + 3, y + 3), (x + 3, y + CELL_SIZE - 4), 2)
        # Бараан ирмэг (Shadow bottom/right highlight)
        shadow_col = (max(0, color[0]-50), max(0, color[1]-50), max(0, color[2]-50))
        pygame.draw.line(screen, shadow_col, (x + 3, y + CELL_SIZE - 3), (x + CELL_SIZE - 3, y + CELL_SIZE - 3), 2)
        pygame.draw.line(screen, shadow_col, (x + CELL_SIZE - 3, y + 3), (x + CELL_SIZE - 3, y + CELL_SIZE - 3), 2)

    def draw_side_panel(self, screen, x, y, w, h, title):
        # Самбар сүүдэр
        pygame.draw.rect(screen, (17, 17, 27), (x + 4, y + 4, w, h), border_radius=8)
        # Суурь
        pygame.draw.rect(screen, PANEL_COLOR, (x, y, w, h), border_radius=8)
        pygame.draw.rect(screen, GRID_COLOR, (x, y, w, h), width=2, border_radius=8)
        
        # Гарчиг
        font = pygame.font.SysFont("Impact", 18)
        title_surf = font.render(title, True, ACCENT_COLOR)
        screen.blit(title_surf, (x + w//2 - title_surf.get_width()//2, y + 10))
        
    def draw_preview_piece(self, screen, x, y, w, h, piece):
        # Бага зэрэг голлуулах
        piece_w = len(piece.matrix[0]) * CELL_SIZE
        piece_h = len(piece.matrix) * CELL_SIZE
        start_x = x + w//2 - piece_w//2
        start_y = y + h//2 - piece_h//2 + 10
        
        for r_idx, row in enumerate(piece.matrix):
            for c_idx, val in enumerate(row):
                if val:
                    self.draw_block(screen, start_x + c_idx * CELL_SIZE, start_y + r_idx * CELL_SIZE, piece.color)
                    
    def draw_info_text(self, screen, x, y):
        font_lbl = pygame.font.SysFont("Arial", 14, bold=True)
        font_val = pygame.font.SysFont("Consolas", 24, bold=True)
        
        labels = [
            ("SCORE", f"{self.score:06d}"),
            ("LEVEL", f"{self.level:02d}"),
            ("LINES", f"{self.lines_cleared:03d}")
        ]
        
        for idx, (lbl, val) in enumerate(labels):
            lbl_surf = font_lbl.render(lbl, True, TEXT_COLOR)
            val_surf = font_val.render(val, True, WHITE)
            
            y_pos = y + 50 + idx * 90
            screen.blit(lbl_surf, (x + 20, y_pos))
            screen.blit(val_surf, (x + 20, y_pos + 20))
            
    def draw_controls_text(self, screen, x, y):
        font = pygame.font.SysFont("Arial", 12, bold=True)
        controls = [
            ("LEFT / A", "Move Left"),
            ("RIGHT / D", "Move Right"),
            ("UP / W", "Rotate"),
            ("DOWN / S", "Soft Drop"),
            ("SPACE", "Hard Drop"),
            ("C / L-SHIFT", "Hold Piece"),
            ("ESC", "Quit Game")
        ]
        
        for idx, (key, desc) in enumerate(controls):
            key_surf = font.render(key, True, ACCENT_COLOR)
            desc_surf = font.render(desc, True, TEXT_COLOR)
            
            y_pos = y + 50 + idx * 42
            screen.blit(key_surf, (x + 15, y_pos))
            screen.blit(desc_surf, (x + 15, y_pos + 16))


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("🧩 Classic Tetris — Хичээл 4.7")
    
    clock = pygame.time.Clock()
    game = TetrisGame()
    
    # Автомат уналтын хугацаа (Миллесекундээр)
    fall_time = 0
    fall_speed = 600 # Унах давтамж (түвшин нэмэгдэх тусам хурдасна)
    
    running = True
    while running:
        # Уналтын хугацааг тоолох
        dt = clock.tick(60)
        if not game.game_over:
            fall_time += dt
            
        # Уналтын хурдыг түвшингөөс хамааруулж шинэчлэх
        fall_speed = max(100, 600 - (game.level - 1) * 60)
        
        # Автоматаар 1 нүд доош унах
        if fall_time >= fall_speed:
            game.soft_drop()
            fall_time = 0
            
        # 1. Events (Гараас оролт авах)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
            if event.type == pygame.KEYDOWN:
                if game.game_over:
                    if event.key in (pygame.K_SPACE, pygame.K_RETURN):
                        game = TetrisGame()
                else:
                    if event.key in (pygame.K_LEFT, pygame.K_a):
                        game.move_left()
                    elif event.key in (pygame.K_RIGHT, pygame.K_d):
                        game.move_right()
                    elif event.key in (pygame.K_UP, pygame.K_w):
                        game.rotate_piece()
                    elif event.key in (pygame.K_DOWN, pygame.K_s):
                        game.soft_drop()
                        fall_time = 0
                    elif event.key == pygame.K_SPACE:
                        game.hard_drop()
                        fall_time = 0
                    elif event.key in (pygame.K_c, pygame.K_LSHIFT):
                        game.hold()
                        fall_time = 0
                        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            running = False
            
        # 2. ЗУРАГЛАЛ ХИЙХ (Drawing)
        screen.fill(BG_COLOR)
        
        # Загварын сүлжээ хээ
        for x in range(0, WIDTH, 50):
            for y in range(0, HEIGHT, 50):
                pygame.draw.circle(screen, (35, 37, 56), (x, y), 1.2)
                
        game.draw(screen)
        
        # Game Over дэлгэц
        if game.game_over:
            overlay = pygame.Surface((WIDTH, HEIGHT))
            overlay.set_alpha(200)
            overlay.fill(BG_COLOR)
            screen.blit(overlay, (0, 0))
            
            font_title = pygame.font.SysFont("Impact", 60)
            font_sub = pygame.font.SysFont("Arial", 22)
            
            title_text = font_title.render("GAME OVER", True, (243, 139, 168))
            sub_text = font_sub.render(f"Final Score: {game.score} | Press [ENTER] to Restart", True, TEXT_COLOR)
            
            screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 2 - 50))
            screen.blit(sub_text, (WIDTH // 2 - sub_text.get_width() // 2, HEIGHT // 2 + 20))
            
        pygame.display.flip()
        
    pygame.quit()


if __name__ == "__main__":
    print("""
🧩 Classic Tetris тоглоом ажиллаж байна!
- Баруун, зүүн сумаар дүрсийг хэвтээ чиглэлд удирдах
- Дээш сумаар дүрсийг эргүүлэх
- Доош сумаар хурдлуулах (Soft Drop)
- Space даран шууд унагах (Hard Drop)
- 'C' эсвэл Left Shift даран дүрсийг хадгалах (Hold)
    """)
    main()
