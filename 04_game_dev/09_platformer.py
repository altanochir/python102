"""
╔══════════════════════════════════════════════════════════════════╗
║  🏃 Хичээл 4.9: Платформер Тоглоом (Side-scrolling Platformer)     ║
║  Гравитацийн физик (Gravity), Мөргөлдөөн засах (AABB Collision),  ║
║  Камер дагах эффект (Camera scroll), Дайсны хиймэл ухаан          ║
╚══════════════════════════════════════════════════════════════════╝

🎯 Энэ хичээлээр үзэх сэдвүүд:
   1. Платформерын физик (Гравитаци, Хурдатгал, Хөдөлгөөний үрэлт)
   2. Хана, шал мөргөлтийн физикийг зөв тооцох (AABB collision resolution)
   3. Камер тоглогчийг дагаж гүйх хөдөлгөөн (Camera scrolling / offset)
   4. Дайсны автомат эргүүл (Patrolling enemy logic)
   5. Алтан зоос цуглуулах ба Төгсгөлийн туг (Goal flag)
"""

import sys

try:
    import pygame
except ImportError:
    print("⚠️ Pygame суугаагүй байна! 'pip install pygame' ажиллуулна уу.")
    sys.exit(1)


# --- Тоглоомын хэмжээнүүд ---
WIDTH, HEIGHT = 900, 600
TILE_SIZE = 40
FPS = 60

# --- Catppuccin Theme Colors ---
BG_COLOR = (30, 30, 46)        # Deep charcoal
SKY_BLUE = (137, 180, 250)      # Soft blue sky
DIRT_COLOR = (108, 112, 134)    # Slate grey/brown
GRASS_COLOR = (166, 227, 161)   # Pastel green
PLAYER_COLOR = (203, 166, 247)  # Lavender
ENEMY_COLOR = (243, 139, 168)   # Rose Red
COIN_COLOR = (249, 226, 175)    # Yellow
SPIKE_COLOR = (250, 179, 135)   # Peach
WHITE = (255, 255, 255)
SHADOW = (17, 17, 27)
PANEL_COLOR = (24, 24, 37)      # Darker panel color
GRID_COLOR = (49, 50, 68)       # Soft grey border/grid color

# --- Түвшний зураглал (Tile Map Representation) ---
# X: Хана / Шал
# C: Алтан зоос
# S: Сэжигтэй өргөс (Hazard Spikes)
# E: Дайсан (Enemy)
# G: Барианы туг (Goal)
LEVEL_MAP = [
    "                                                                                ",
    "                                                                                ",
    "                                                                                ",
    "                                                                                ",
    "                                                                                ",
    "                                                                                ",
    "                                       XXXXXX                                   ",
    "                                                                                ",
    "             XXXX                                  XXXXX                        ",
    "                                                                            G   ",
    "         XXXX    XXXX          XXXXXX           XXXX    XXXX            XXXXXXXX",
    "                       XXXXX            XXXX                    XXXX            ",
    "                                                                                ",
    "    P     C      S   E    C     S        C     E   S     C      S    E   C        ",
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
]

LEVEL_WIDTH = len(LEVEL_MAP[0]) * TILE_SIZE
LEVEL_HEIGHT = len(LEVEL_MAP) * TILE_SIZE


class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 32, 48)
        self.vel_x = 0
        self.vel_y = 0
        self.speed = 4
        self.jump_power = -14
        self.is_grounded = False
        
        # Визуаль эффектүүд
        self.facing_right = True
        
    def update(self, keys, blocks):
        # 1. Гравитацийн үйлчлэл
        self.vel_y += 0.6 # Таталцлын хурдатгал
        if self.vel_y > 12:
            self.vel_y = 12 # Хамгийн их унах хурд
            
        # 2. Хэвтээ тэнхлэгийн хурд
        move_dir = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            move_dir = -1
            self.facing_right = False
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            move_dir = 1
            self.facing_right = True
            
        # Хурдатгал болон Үрэлт (Acceleration & Friction)
        if move_dir != 0:
            self.vel_x = move_dir * self.speed
        else:
            self.vel_x *= 0.8 # Зөөлөн гулсаж зогсох
            if abs(self.vel_x) < 0.2:
                self.vel_x = 0
                
        # 3. Үсрэх үйлдэл
        if (keys[pygame.K_UP] or keys[pygame.K_w] or keys[pygame.K_SPACE]) and self.is_grounded:
            self.vel_y = self.jump_power
            self.is_grounded = False
            
        # 4. Мөргөлдөөн шалгаж байрлал засах (AABB Collision Resolution)
        # А. Хэвтээ чиглэлд хөдөлж шалгах
        self.rect.x += self.vel_x
        for block in blocks:
            if self.rect.colliderect(block):
                if self.vel_x > 0: # Баруун тийш мөргөлдвөл
                    self.rect.right = block.left
                elif self.vel_x < 0: # Зүүн тийш мөргөлдвөл
                    self.rect.left = block.right
                self.vel_x = 0
                
        # Б. Босоо чиглэлд хөдөлж шалгах
        self.is_grounded = False
        self.rect.y += self.vel_y
        for block in blocks:
            if self.rect.colliderect(block):
                if self.vel_y > 0: # Доошоо мөргөлдвөл (Газардах)
                    self.rect.bottom = block.top
                    self.is_grounded = True
                elif self.vel_y < 0: # Дээшээ мөргөлдвөл (Тааз мөргөх)
                    self.rect.top = block.bottom
                self.vel_y = 0


class Enemy:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y + 8, 32, 32)
        self.vel_x = 2 # Эргүүлийн хурд
        
    def update(self, blocks):
        # Хэвтээ чиглэлд хөдөлнө
        self.rect.x += self.vel_x
        
        # Хана мөргөвөл эсвэл захад хүрвэл чиглэл өөрчлөх
        # (Илүү ухаалаг AI: доор нь блок байгаа эсэхийг шалгаж ирмэгээс унахгүй эргэдэг)
        turn = False
        for block in blocks:
            if self.rect.colliderect(block):
                turn = True
                break
                
        # Хэрэв ирмэгт тулбал эргэх логик
        # Дайсны урд талын доор гишгэх блок байхгүй бол буцна
        check_x = self.rect.right + 2 if self.vel_x > 0 else self.rect.left - 2
        check_rect = pygame.Rect(check_x, self.rect.bottom + 2, 5, 5)
        has_ground_ahead = any(check_rect.colliderect(b) for b in blocks)
        
        if turn or not has_ground_ahead:
            self.vel_x *= -1
            self.rect.x += self.vel_x


class Coin:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x + 10, y + 10, 20, 20)
        self.angle = 0
        
    def update(self):
        # Эргэлдэх хөдөлгөөн (Визуаль эффект)
        self.angle = (self.angle + 5) % 360


class Spike:
    def __init__(self, x, y):
        # Мөргөлдөх хитбоксыг арай жижиг болгож тоглогчид хялбар болгох
        self.rect = pygame.Rect(x + 5, y + 20, 30, 20)
        # Зурагдах оройнуудын координат
        self.points = [
            (x + 20, y + 10), # Орой
            (x + 5, y + 40),  # Зүүн доод
            (x + 35, y + 40)  # Баруун доод
        ]


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("🏃 Side-scroller Platformer — Хичээл 4.9")
    
    clock = pygame.time.Clock()
    
    # --- Түвшний элементүүдийг бэлдэх ---
    blocks = []
    coins = []
    spikes = []
    enemies = []
    goal_rect = None
    player = None
    
    # Газрын зургийг уншиж объектуудыг үүсгэх
    for r_idx, row in enumerate(LEVEL_MAP):
        for c_idx, val in enumerate(row):
            x = c_idx * TILE_SIZE
            y = r_idx * TILE_SIZE
            
            if val == "X":
                # Хана/Шалны блок
                blocks.append(pygame.Rect(x, y, TILE_SIZE, TILE_SIZE))
            elif val == "P":
                # Тоглогч эхлэх цэг
                player = Player(x, y)
            elif val == "C":
                # Алтан зоос
                coins.append(Coin(x, y))
            elif val == "S":
                # Өргөс
                spikes.append(Spike(x, y))
            elif val == "E":
                # Дайсан
                enemies.append(Enemy(x, y))
            elif val == "G":
                # Барианы туг
                goal_rect = pygame.Rect(x + 10, y, 20, TILE_SIZE)
                
    if not player:
        # Эхлэх цэг байхгүй бол default үүсгэнэ
        player = Player(100, 100)
        
    score = 0
    lives = 3
    game_state = "PLAYING" # PLAYING, WIN, GAME_OVER
    
    running = True
    while running:
        dt = clock.tick(FPS)
        
        # 1. Events (Гараас оролт авах)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if game_state in ("WIN", "GAME_OVER") and (event.key == pygame.K_SPACE or event.key == pygame.K_RETURN):
                    # Тоглоомыг дахин эхлүүлэх
                    main()
                    return
                    
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            running = False
            
        # 2. Физик шинэчлэлт (Update Logic)
        if game_state == "PLAYING":
            player.update(keys, blocks)
            
            # Зоос цуглуулах
            for coin in coins[:]:
                coin.update()
                if player.rect.colliderect(coin.rect):
                    coins.remove(coin)
                    score += 100
                    
            # Өргөс мөргөх (Амь хасагдах)
            for spike in spikes:
                if player.rect.colliderect(spike.rect):
                    # Бага зэрэг буцаж шидэгдэх эффект
                    player.vel_y = -8
                    player.vel_x = -5 if player.facing_right else 5
                    lives -= 1
                    if lives <= 0:
                        game_state = "GAME_OVER"
                        
            # Дайсантай мөргөлдөх
            for enemy in enemies[:]:
                enemy.update(blocks)
                if player.rect.colliderect(enemy.rect):
                    # Дээрээс нь үсэрч мөргөвөл дайсныг устгана (Squash enemy)
                    # Тоглогч доошилж байх үед дайсны оройгоос дээш байсан уу гэдгийг шалгана
                    if player.vel_y > 0 and player.rect.bottom < enemy.rect.centery + 10:
                        enemies.remove(enemy)
                        player.vel_y = -10 # Буцаж дээш үсрэх эффект
                        score += 200
                    else:
                        # Хажуу талаас мөргөлдвөл тоглогч амь хасагдана
                        player.vel_y = -8
                        player.vel_x = -6 if player.facing_right else 6
                        lives -= 1
                        if lives <= 0:
                            game_state = "GAME_OVER"
                            
            # Унах нүх рүү унах (Fall in pit)
            if player.rect.y > HEIGHT + 100:
                game_state = "GAME_OVER"
                
            # Барианд хүрэх (Goal trigger)
            if goal_rect and player.rect.colliderect(goal_rect):
                game_state = "WIN"
                
        # 3. Камер дагах тооцоолол (Camera Scroll)
        # Камер тоглогчийн X координатыг дэлгэцийн голд барина
        camera_x = player.rect.centerx - WIDTH // 2
        # Түвшний хязгаараас хэтрэхгүй байх хязгаарлалт
        camera_x = max(0, min(camera_x, LEVEL_WIDTH - WIDTH))
        
        # 4. ЗУРАГЛАЛ ХИЙХ (Drawing)
        screen.fill(BG_COLOR)
        
        # Тэнгэрийн налуу өнгө дуурайлгах арын хэсэг
        pygame.draw.rect(screen, (36, 39, 58), (0, 0, WIDTH, HEIGHT // 2 + 100))
        
        # Арын гэрэлт Нар / Сар
        pygame.draw.circle(screen, (249, 226, 175), (WIDTH - 150, 100), 50)
        pygame.draw.circle(screen, (36, 39, 58), (WIDTH - 170, 100), 45) # Moon crescent mask
        
        # Блокуудыг зурах (Камерын зөрүүгээр оOffset хийх)
        for block in blocks:
            # Дэлгэцийн гадна байгаануудыг зурж ачааллахгүй байх шалгалт
            if block.right >= camera_x and block.left <= camera_x + WIDTH:
                bx = block.x - camera_x
                by = block.y
                # Өвсөн оройтой шороон блок зурах
                pygame.draw.rect(screen, DIRT_COLOR, (bx, by, TILE_SIZE, TILE_SIZE))
                pygame.draw.rect(screen, GRASS_COLOR, (bx, by, TILE_SIZE, 8))
                
        # Өргөсүүдийг зурах
        for spike in spikes:
            # Камерын Offset оруулах
            p1 = (spike.points[0][0] - camera_x, spike.points[0][1])
            p2 = (spike.points[1][0] - camera_x, spike.points[1][1])
            p3 = (spike.points[2][0] - camera_x, spike.points[2][1])
            pygame.draw.polygon(screen, SPIKE_COLOR, [p1, p2, p3])
            
        # Зооснуудыг зурах
        for coin in coins:
            cx = coin.rect.x - camera_x
            cy = coin.rect.y
            # Эргэлдэх хөдөлгөөн дуурайлгаж өргөнийг өөрчлөх
            width_scale = max(2, int(coin.rect.width * abs(math.cos(math.radians(coin.angle)))))
            coin_draw_rect = pygame.Rect(cx + (coin.rect.width - width_scale)//2, cy, width_scale, coin.rect.height)
            pygame.draw.ellipse(screen, COIN_COLOR, coin_draw_rect)
            pygame.draw.ellipse(screen, (250, 179, 135), coin_draw_rect, width=1)
            
        # Дайснуудыг зурах
        for enemy in enemies:
            ex = enemy.rect.x - camera_x
            ey = enemy.rect.y
            pygame.draw.rect(screen, ENEMY_COLOR, (ex, ey, enemy.rect.width, enemy.rect.height), border_radius=6)
            # Дайсны ууртай нүднүүд
            eye_offset = 6 if enemy.vel_x > 0 else 2
            pygame.draw.rect(screen, WHITE, (ex + eye_offset, ey + 8, 6, 6))
            pygame.draw.rect(screen, WHITE, (ex + eye_offset + 14, ey + 8, 6, 6))
            pygame.draw.line(screen, SHADOW, (ex + eye_offset - 2, ey + 4), (ex + eye_offset + 8, ey + 8), 2)
            pygame.draw.line(screen, SHADOW, (ex + eye_offset + 16, ey + 4), (ex + eye_offset + 10, ey + 8), 2)
            
        # Барианы туг зурах
        if goal_rect:
            gx = goal_rect.x - camera_x
            gy = goal_rect.y
            # Иш
            pygame.draw.line(screen, WHITE, (gx, gy), (gx, gy + TILE_SIZE * 3), 4)
            # Улаан туг
            pygame.draw.polygon(screen, ENEMY_COLOR, [
                (gx + 2, gy),
                (gx + 30, gy + 15),
                (gx + 2, gy + 30)
            ])
            
        # Тоглогчийг зурах (Player render)
        if game_state != "GAME_OVER":
            px = player.rect.x - camera_x
            py = player.rect.y
            
            # Тоглогчийн бие зурах
            pygame.draw.rect(screen, PLAYER_COLOR, (px, py, player.rect.width, player.rect.height), border_radius=6)
            
            # Тоглогчийн нүүрний чиглэлийг харуулах нүд
            eye_x = px + 18 if player.facing_right else px + 6
            pygame.draw.rect(screen, WHITE, (eye_x, py + 10, 8, 12), border_radius=2)
            pygame.draw.rect(screen, SHADOW, (eye_x + (4 if player.facing_right else 0), py + 14, 4, 4), border_radius=1)
            
        # --- UI Зурж харуулах (Оноо ба Амь) ---
        font = pygame.font.SysFont("Impact", 20)
        score_surf = font.render(f"SCORE: {score:05d}", True, WHITE)
        lives_surf = font.render(f"LIVES: {'❤️ ' * lives}", True, WHITE)
        
        # UI хавтан
        pygame.draw.rect(screen, PANEL_COLOR, (15, 15, 200, 75), border_radius=8)
        pygame.draw.rect(screen, GRID_COLOR, (15, 15, 200, 75), width=2, border_radius=8)
        
        screen.blit(score_surf, (30, 25))
        screen.blit(lives_surf, (30, 50))
        
        # 5. ТӨЛӨВИЙН ДЭЛГЭЦҮҮД (Screens)
        if game_state == "GAME_OVER":
            overlay = pygame.Surface((WIDTH, HEIGHT))
            overlay.set_alpha(200)
            overlay.fill(BG_COLOR)
            screen.blit(overlay, (0, 0))
            
            font_title = pygame.font.SysFont("Impact", 60)
            font_sub = pygame.font.SysFont("Arial", 22)
            
            title_text = font_title.render("GAME OVER", True, ENEMY_COLOR)
            sub_text = font_sub.render(f"Score: {score} | Press [ENTER] to Restart", True, WHITE)
            
            screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 2 - 50))
            screen.blit(sub_text, (WIDTH // 2 - sub_text.get_width() // 2, HEIGHT // 2 + 20))
            
        elif game_state == "WIN":
            overlay = pygame.Surface((WIDTH, HEIGHT))
            overlay.set_alpha(200)
            overlay.fill(BG_COLOR)
            screen.blit(overlay, (0, 0))
            
            font_title = pygame.font.SysFont("Impact", 60)
            font_sub = pygame.font.SysFont("Arial", 22)
            
            title_text = font_title.render("LEVEL COMPLETED! 🏆", True, GRASS_COLOR)
            sub_text = font_sub.render(f"Final Score: {score} | Press [ENTER] to Play Again", True, WHITE)
            
            screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 2 - 50))
            screen.blit(sub_text, (WIDTH // 2 - sub_text.get_width() // 2, HEIGHT // 2 + 20))
            
        pygame.display.flip()
        
    pygame.quit()


if __name__ == "__main__":
    import math # Дотор нь дуудагдсан
    print("""
🏃 Side-scroller Platformer тоглоом ажиллаж байна!
- Зүүн/Баруун тийш 'A'/'D' эсвэл Сумтай товчоор хөдөлнө.
- Үсрэхдээ 'W', 'Space' эсвэл Дээш сум дарна.
- Дайсныг дээрээс нь үсэрч мөргөж устгана.
- Алтан зоос цуглуулж, барианы туганд хүрч ялаарай!
    """)
    main()
