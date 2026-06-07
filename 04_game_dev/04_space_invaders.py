"""
╔══════════════════════════════════════════════════════════════════╗
║  🎮 Хичээл 4.4: Сансрын Довтолгоо (Space Invaders)                ║
║  Олон объект удирдах, Сум харвах ба Объект устгах логик           ║
╚══════════════════════════════════════════════════════════════════╝

🎯 Энэ хичээлээр үзэх сэдвүүд:
   1. Тоглогч (Player Ship) ба Сум (Lasers)-ны удирдлага
   2. Дайсны бүлэг (Enemy Grid) үүсгэх ба Хөдөлгөөний хэв маяг
   3. Олон объектын мөргөлдөөн (Lasers vs Enemies)
   4. Тоглогчийн амь (Lives), Оноо (Score) болон Ялалт/Ялагдлын төлөв
"""

import sys
import random

try:
    import pygame
except ImportError:
    print("⚠️ Pygame суугаагүй байна! 'pip install pygame' ажиллуулна уу.")
    sys.exit(1)


def run_space_invaders():
    pygame.init()
    
    # Цонхны хэмжээ
    WIDTH, HEIGHT = 800, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("🚀 Сансрын Довтолгоо — Хичээл 4.4")
    
    # Өнгөнүүд
    BG_COLOR = (10, 10, 20)
    PLAYER_COLOR = (166, 227, 161) # Ногоон
    ENEMY_COLOR = (243, 139, 168)  # Улаан
    BULLET_COLOR = (249, 226, 175) # Шар
    ENEMY_BULLET_COLOR = (203, 166, 247) # Нил ягаан
    TEXT_COLOR = (205, 214, 244)
    
    # FPS хянагч
    clock = pygame.time.Clock()
    FPS = 60
    
    # Тоглогчийн мэдээлэл
    player_width, player_height = 50, 30
    player_x = WIDTH // 2 - player_width // 2
    player_y = HEIGHT - 60
    player_speed = 6
    player_lives = 3
    
    # Сумны мэдээлэл
    bullet_width, bullet_height = 4, 15
    bullet_speed = 8
    bullets = [] # Тоглогчийн сумнуудын жагсаалт
    
    # Дайсны сумнуудын жагсаалт
    enemy_bullets = []
    enemy_bullet_speed = 4
    
    # Дайснуудын мэдээлэл (Enemy grid)
    enemy_width, enemy_height = 40, 25
    enemies = []
    enemy_speed_x = 1.5
    enemy_direction = 1 # 1: Баруун, -1: Зүүн
    enemy_drop_distance = 15
    
    # Дайснуудыг үүсгэх функц
    def spawn_enemies():
        nonlocal enemies, enemy_speed_x, enemy_direction
        enemies.clear()
        enemy_speed_x = 1.5
        enemy_direction = 1
        rows = 4
        cols = 10
        x_spacing = 60
        y_spacing = 40
        start_x = 100
        start_y = 70
        
        for r in range(rows):
            for c in range(cols):
                ex = start_x + c * x_spacing
                ey = start_y + r * y_spacing
                enemies.append(pygame.Rect(ex, ey, enemy_width, enemy_height))
                
    # Тоглоомын төлөв
    score = 0
    game_state = "START" # START, PLAYING, WIN, GAME_OVER
    
    spawn_enemies()
    
    running = True
    while running:
        # 1. Events (Гараас оролт авах)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
            if event.type == pygame.KEYDOWN:
                if game_state == "START":
                    if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                        game_state = "PLAYING"
                elif game_state in ("WIN", "GAME_OVER"):
                    if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                        # Тоглоомыг шинээр эхлүүлэх
                        player_lives = 3
                        score = 0
                        bullets.clear()
                        enemy_bullets.clear()
                        spawn_enemies()
                        game_state = "PLAYING"
                elif game_state == "PLAYING":
                    # Сум харвах (Space)
                    if event.key == pygame.K_SPACE:
                        # Тоглогчийн цоргоноос сум гаргах
                        bx = player_x + player_width // 2 - bullet_width // 2
                        by = player_y
                        bullets.append(pygame.Rect(bx, by, bullet_width, bullet_height))
                        
        # Escape товчоор гарах
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            running = False
            
        # 2. Тоглоомын логик шинэчлэл
        if game_state == "PLAYING":
            # А. Тоглогчийн хөдөлгөөн
            if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and player_x > 0:
                player_x -= player_speed
            if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and player_x < WIDTH - player_width:
                player_x += player_speed
                
            # Б. Тоглогчийн сумны хөдөлгөөн
            for b in bullets[:]:
                b.y -= bullet_speed
                # Дэлгэцээс гарсан сумыг жагсаалтаас устгах
                if b.y < 0:
                    bullets.remove(b)
                    
            # В. Дайсны хөдөлгөөн
            move_down = False
            for enemy in enemies:
                enemy.x += enemy_speed_x * enemy_direction
                # Дэлгэцийн зах мөргөсөн эсэх
                if enemy.x <= 0 or enemy.x >= WIDTH - enemy_width:
                    move_down = True
                    
            if move_down:
                enemy_direction *= -1 # Чиглэлийг өөрчлөх
                for enemy in enemies:
                    enemy.y += enemy_drop_distance # Доошлуулах
                    
            # Г. Дайснууд доош хэт ойртож Тоглогчийг мөргөх эсвэл хамгаалалтын шугам давах
            for enemy in enemies:
                if enemy.y + enemy_height >= player_y:
                    game_state = "GAME_OVER"
                    
            # Д. Дайснууд сум харвах (Санамсаргүй байдлаар)
            if len(enemies) > 0 and random.random() < 0.02: # 2% магадлал
                shooter = random.choice(enemies)
                ebx = shooter.x + enemy_width // 2 - bullet_width // 2
                eby = shooter.y + enemy_height
                enemy_bullets.append(pygame.Rect(ebx, eby, bullet_width, bullet_height))
                
            # Е. Дайсны сумнуудын хөдөлгөөн
            for eb in enemy_bullets[:]:
                eb.y += enemy_bullet_speed
                if eb.y > HEIGHT:
                    enemy_bullets.remove(eb)
                # Тоглогчийг мөргөх
                player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
                if eb.colliderect(player_rect):
                    player_lives -= 1
                    enemy_bullets.remove(eb)
                    if player_lives <= 0:
                        game_state = "GAME_OVER"
                        
            # Ж. Мөргөлдөөнийг хянах: Тоглогчийн сум vs Дайсан
            for b in bullets[:]:
                for enemy in enemies[:]:
                    if b.colliderect(enemy):
                        score += 50
                        enemies.remove(enemy)
                        bullets.remove(b)
                        break
                        
            # З. Ялалтын нөхцөл (Бүх дайсныг устгах)
            if len(enemies) == 0:
                game_state = "WIN"
                
        # 3. Зураглал хийх (Drawing)
        screen.fill(BG_COLOR)
        
        # Тоглогчийг зурах (Сансрын хөлөг дүрс)
        player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
        pygame.draw.rect(screen, PLAYER_COLOR, player_rect, border_radius=5)
        # Хөлөгний буу
        pygame.draw.rect(screen, PLAYER_COLOR, (player_x + player_width // 2 - 4, player_y - 8, 8, 8))
        
        # Дайснуудыг зурах
        for enemy in enemies:
            pygame.draw.rect(screen, ENEMY_COLOR, enemy, border_radius=3)
            # Дайсны нүднүүд
            pygame.draw.rect(screen, BG_COLOR, (enemy.x + 8, enemy.y + 6, 6, 6))
            pygame.draw.rect(screen, BG_COLOR, (enemy.x + enemy_width - 14, enemy.y + 6, 6, 6))
            
        # Сумнуудыг зурах
        for b in bullets:
            pygame.draw.rect(screen, BULLET_COLOR, b)
        for eb in enemy_bullets:
            pygame.draw.rect(screen, ENEMY_BULLET_COLOR, eb)
            
        # Статистик зурах (Оноо, Амь)
        font = pygame.font.SysFont("Consolas", 20)
        score_text = font.render(f"SCORE: {score}", True, TEXT_COLOR)
        lives_text = font.render(f"LIVES: {'❤️ ' * player_lives}", True, TEXT_COLOR)
        screen.blit(score_text, (20, 20))
        screen.blit(lives_text, (WIDTH - lives_text.get_width() - 20, 20))
        
        # Нүүр хуудас болон Төлөвийн дэлгэцүүд
        if game_state == "START":
            overlay = pygame.Surface((WIDTH, HEIGHT))
            overlay.fill(BG_COLOR)
            screen.blit(overlay, (0, 0))
            
            font_title = pygame.font.SysFont("Arial", 45, bold=True)
            font_sub = pygame.font.SysFont("Arial", 20)
            
            title_text = font_title.render("SPACE INVADERS", True, PLAYER_COLOR)
            sub_text = font_sub.render("Press [ENTER / SPACE] to Start | W, A, S, D эсвэл Сумнуудаар удирдана", True, TEXT_COLOR)
            
            screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 2 - 40))
            screen.blit(sub_text, (WIDTH // 2 - sub_text.get_width() // 2, HEIGHT // 2 + 20))
            
        elif game_state == "GAME_OVER":
            overlay = pygame.Surface((WIDTH, HEIGHT))
            overlay.set_alpha(180)
            overlay.fill(BG_COLOR)
            screen.blit(overlay, (0, 0))
            
            font_title = pygame.font.SysFont("Arial", 50, bold=True)
            font_sub = pygame.font.SysFont("Arial", 22)
            
            title_text = font_title.render("GAME OVER", True, ENEMY_COLOR)
            sub_text = font_sub.render(f"Score: {score} | Press [ENTER] to Restart", True, TEXT_COLOR)
            
            screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 2 - 45))
            screen.blit(sub_text, (WIDTH // 2 - sub_text.get_width() // 2, HEIGHT // 2 + 15))
            
        elif game_state == "WIN":
            overlay = pygame.Surface((WIDTH, HEIGHT))
            overlay.set_alpha(180)
            overlay.fill(BG_COLOR)
            screen.blit(overlay, (0, 0))
            
            font_title = pygame.font.SysFont("Arial", 50, bold=True)
            font_sub = pygame.font.SysFont("Arial", 22)
            
            title_text = font_title.render("MISSION ACCOMPLISHED 🏆", True, PLAYER_COLOR)
            sub_text = font_sub.render(f"Score: {score} | Press [ENTER] to Play Again", True, TEXT_COLOR)
            
            screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 2 - 45))
            screen.blit(sub_text, (WIDTH // 2 - sub_text.get_width() // 2, HEIGHT // 2 + 15))
            
        pygame.display.flip()
        clock.tick(FPS)
        
    pygame.quit()


if __name__ == "__main__":
    print("""
🚀 Сансрын Довтолгоо тоглоом эхэлж байна!
- Зүүн/Баруун тийш 'A', 'D' эсвэл Сумтай товчоор хөдөлнө.
- Сум харвахдаа 'Space' товчийг дарна уу.
- Дайснуудын суманд өртөхөөс сэргийлж, бүх дайсныг устгаарай!
    """)
    run_space_invaders()
