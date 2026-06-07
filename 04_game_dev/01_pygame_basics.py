"""
╔══════════════════════════════════════════════════════════════════╗
║  📖 Хичээл 4.1: Pygame Basics — Тоглоом хөгжүүлэлтийн үндэс        ║
║  Game Loop, Event Handling, Дүрс зурах ба Хөдөлгөөн              ║
╚══════════════════════════════════════════════════════════════════╝

🎯 Энэ хичээлээр үзэх сэдвүүд:
   1. Pygame-ийг эхлүүлэх ба Үндсэн Цонх (Window)
   2. Game Loop (Тоглоомын үндсэн давталт)
   3. Event Handling (Гараас оролт авах)
   4. Дүрс зурах, Өнгө тохируулах
   5. FPS (Frames Per Second) ба Хөдөлгөөн

📌 Суулгах заавар:
   pip install pygame
"""

import sys

try:
    import pygame
except ImportError:
    print("""
⚠️ Pygame суугаагүй байна!
Дараах тушаалаар суулгана уу:
    pip install pygame
    """)
    sys.exit(1)


def run_basics_demo():
    # 1. Pygame-ийг эхлүүлэх
    pygame.init()
    
    # 2. Цонхны хэмжээ тохируулах (Өргөн, Өндөр)
    WIDTH, HEIGHT = 800, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("🎮 Pygame-ий Үндэс — Хичээл 4.1")
    
    # 3. Өнгөнүүд (RGB хэлбэрээр)
    BG_COLOR = (30, 30, 46)      # Dark space-like color
    RED = (243, 139, 168)
    GREEN = (166, 227, 161)
    BLUE = (137, 180, 250)
    WHITE = (205, 214, 244)
    
    # Тоглогчийн анхны байрлал, хэмжээ
    player_x = WIDTH // 2
    player_y = HEIGHT // 2
    player_size = 50
    player_speed = 5
    
    # FPS хянах цаг (Clock)
    clock = pygame.time.Clock()
    FPS = 60  # Секундэд 60 удаа зурагдана
    
    # 4. GAME LOOP (Тоглоом ажиллаж байх хугацаанд зогсолтгүй эргэнэ)
    running = True
    while running:
        # --- А. EVENTS (Үйл явдлыг хянах) ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # Цонхны X дээр дарах
                running = False
                
        # --- Б. KEYBOARD INPUT (Гарын товч хянах) ---
        keys = pygame.key.get_pressed()
        
        # Тоглогчийг хөдөлгөх (Цонхноос гаргахгүй байх хязгаарлалттай)
        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and player_x > 0:
            player_x -= player_speed
        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and player_x < WIDTH - player_size:
            player_x += player_speed
        if (keys[pygame.K_UP] or keys[pygame.K_w]) and player_y > 0:
            player_y -= player_speed
        if (keys[pygame.K_DOWN] or keys[pygame.K_s]) and player_y < HEIGHT - player_size:
            player_y += player_speed
            
        # --- В. DRAWING (Зураглал хийх) ---
        # 1. Арын өнгөөр цонхыг будах (хуучин зурсан дүрсийг арилгана)
        screen.fill(BG_COLOR)
        
        # 2. Туслах дүрсүүд зурах
        # Тойрог (Дэлгэц, Өнгө, Төв цэг, Радиус, Хүрээний зузаан - 0 бол дүүргэнэ)
        pygame.draw.circle(screen, BLUE, (150, 150), 60)
        
        # Шугам (Дэлгэц, Өнгө, Эхлэл цэг, Төгсгөл цэг, Зузаан)
        pygame.draw.line(screen, GREEN, (50, 400), (300, 450), 5)
        
        # 3. Тоглогчийг зурах (Тэгш өнцөгт)
        # Rect (Дэлгэц, Өнгө, (X, Y, Өргөн, Өндөр))
        player_rect = pygame.Rect(player_x, player_y, player_size, player_size)
        pygame.draw.rect(screen, RED, player_rect)
        
        # 4. Текст зурах (Заавар)
        font = pygame.font.SysFont("Arial", 20)
        instructions = font.render("Удирдах: Сумнууд эсвэл W, A, S, D | Escape = Хаах", True, WHITE)
        screen.blit(instructions, (20, 20))
        
        # Escape товч дарахад хаах
        if keys[pygame.K_ESCAPE]:
            running = False
            
        # --- Г. UPDATE DISPLAY (Дэлгэцийг шинэчлэх) ---
        pygame.display.flip()
        
        # FPS-ийг 60 дээр барих
        clock.tick(FPS)
        
    # Pygame-ийг хааж санах ойг чөлөөлөх
    pygame.quit()


if __name__ == "__main__":
    print("""
🎮 Pygame Basics хичээл ажиллаж байна.
- Нээгдэх цонхон дээр Улаан квадратыг удирдах боломжтой.
- Хаахын тулд цонхны 'X' эсвэл 'Escape' товчийг дарна уу.
    """)
    run_basics_demo()
