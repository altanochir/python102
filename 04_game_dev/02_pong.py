"""
╔══════════════════════════════════════════════════════════════════╗
║  🎮 Хичээл 4.2: Pong Тоглоом — Сонгодог 2D Тоглоом                ║
║  Мөргөлдөөн (Collisions), Бөмбөгний хөдөлгөөн ба Оноо тооцох       ║
╚══════════════════════════════════════════════════════════════════╝

🎯 Энэ хичээлээр үзэх сэдвүүд:
   1. Paddle (Цохиур) болон Ball (Бөмбөг) үүсгэх
   2. Бөмбөгний ойлтын физик (Хана болон Цохиур мөргөх)
   3. Оноо цуглуулах ба Текст хэлбэрээр дэлгэцэнд зурах
   4. Сонгодог хиймэл оюун ухаан (Simple Bot AI)
"""

import sys
import random

try:
    import pygame
except ImportError:
    print("⚠️ Pygame суугаагүй байна! 'pip install pygame' ажиллуулна уу.")
    sys.exit(1)


def run_pong():
    pygame.init()
    
    # Цонхны хэмжээ
    WIDTH, HEIGHT = 800, 500
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("🏓 Pong — Хичээл 4.2")
    
    # Өнгөнүүд
    BG_COLOR = (20, 20, 30)
    WHITE = (235, 235, 245)
    ACCENT = (137, 180, 250) # Цэнхэр өнгө
    RED = (243, 139, 168)
    GREEN = (166, 227, 161)
    
    # Тоглоомын тохиргоонууд
    FPS = 60
    clock = pygame.time.Clock()
    
    # Цохиуруудын хэмжээ ба байрлал
    PADDLE_WIDTH = 15
    PADDLE_HEIGHT = 90
    paddle_speed = 6
    
    # Зүүн цохиур (Тоглогч 1 - W/S)
    left_x = 30
    left_y = HEIGHT // 2 - PADDLE_HEIGHT // 2
    
    # Баруун цохиур (Тоглогч 2 эсвэл AI)
    right_x = WIDTH - 30 - PADDLE_WIDTH
    right_y = HEIGHT // 2 - PADDLE_HEIGHT // 2
    
    # Бөмбөгний хэмжээ, байрлал, хурд
    BALL_SIZE = 15
    ball_x = WIDTH // 2 - BALL_SIZE // 2
    ball_y = HEIGHT // 2 - BALL_SIZE // 2
    
    # Бөмбөгний хурдны вектор (X, Y чиглэлд)
    ball_speed_x = 5 * random.choice((1, -1))
    ball_speed_y = 5 * random.choice((1, -1))
    
    # Оноо
    score_left = 0
    score_right = 0
    
    # Фонт
    font = pygame.font.SysFont("Consolas", 40)
    small_font = pygame.font.SysFont("Arial", 16)
    
    # Тоглоомын горим: True бол Баруун цохиурыг AI удирдана. False бол Дээш/Доош сумаар Тоглогч 2 удирдана.
    ai_mode = True
    
    def reset_ball():
        nonlocal ball_x, ball_y, ball_speed_x, ball_speed_y
        ball_x = WIDTH // 2 - BALL_SIZE // 2
        ball_y = HEIGHT // 2 - BALL_SIZE // 2
        ball_speed_x = 5 * random.choice((1, -1))
        ball_speed_y = 5 * random.choice((1, -1))
        
    running = True
    while running:
        # 1. Events хянах
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    ai_mode = not ai_mode # Space дарвал AI горимыг асааж/унтраана
                    
        # 2. Оролт хянах (Keyboard Input)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            running = False
            
        # Зүүн цохиурын хөдөлгөөн (W, S)
        if keys[pygame.K_w] and left_y > 0:
            left_y -= paddle_speed
        if keys[pygame.K_s] and left_y < HEIGHT - PADDLE_HEIGHT:
            left_y += paddle_speed
            
        # Баруун цохиурын хөдөлгөөн
        if ai_mode:
            # AI логик: Бөмбөгний Y координатыг дагаж хөдлөх
            # Саатал (Delay) оруулахын тулд төв цэгийг харьцуулна
            paddle_center = right_y + PADDLE_HEIGHT // 2
            ball_center = ball_y + BALL_SIZE // 2
            
            if paddle_center < ball_center - 10 and right_y < HEIGHT - PADDLE_HEIGHT:
                right_y += paddle_speed - 1 # AI нь тоглогчоос арай удаан хөдөлнө
            elif paddle_center > ball_center + 10 and right_y > 0:
                right_y -= paddle_speed - 1
        else:
            # 2-р тоглогчийн гарны удирдлага (Дээш, Доош сум)
            if keys[pygame.K_UP] and right_y > 0:
                right_y -= paddle_speed
            if keys[pygame.K_DOWN] and right_y < HEIGHT - PADDLE_HEIGHT:
                right_y += paddle_speed
                
        # 3. Бөмбөгний хөдөлгөөн
        ball_x += ball_speed_x
        ball_y += ball_speed_y
        
        # Дээд, доод хана мөргөхөд ойх
        if ball_y <= 0 or ball_y >= HEIGHT - BALL_SIZE:
            ball_speed_y *= -1
            
        # 4. Мөргөлдөөнийг хянах (Collisions)
        # Rect хэлбэрт шилжүүлэх
        ball_rect = pygame.Rect(ball_x, ball_y, BALL_SIZE, BALL_SIZE)
        left_rect = pygame.Rect(left_x, left_y, PADDLE_WIDTH, PADDLE_HEIGHT)
        right_rect = pygame.Rect(right_x, right_y, PADDLE_WIDTH, PADDLE_HEIGHT)
        
        # Зүүн эсвэл Баруун цохиур мөргөсөн эсэх
        if ball_rect.colliderect(left_rect):
            # Бөмбөгийг зүүн талаас ойлгох ба хурдыг нь үл ялиг нэмэх
            ball_speed_x = abs(ball_speed_x) + 0.3
            # Ойх өнцгийг Y чиглэлд өөрчлөх
            ball_speed_y += random.uniform(-1, 1)
        elif ball_rect.colliderect(right_rect):
            # Бөмбөгийг баруун талаас ойлгох ба хурдыг нь үл ялиг нэмэх
            ball_speed_x = -(abs(ball_speed_x) + 0.3)
            ball_speed_y += random.uniform(-1, 1)
            
        # 5. Оноо авах & Бөмбөг алдах
        if ball_x < 0:
            score_right += 1
            reset_ball()
        elif ball_x > WIDTH:
            score_left += 1
            reset_ball()
            
        # 6. Зураглал хийх (Drawing)
        screen.fill(BG_COLOR)
        
        # Голын хуваах зураас зурах
        for y in range(0, HEIGHT, 30):
            if y % 2 == 0:
                pygame.draw.rect(screen, (50, 50, 70), (WIDTH // 2 - 2, y, 4, 15))
                
        # Цохиуруудыг зурах
        pygame.draw.rect(screen, ACCENT, left_rect)
        pygame.draw.rect(screen, RED if ai_mode else GREEN, right_rect)
        
        # Бөмбөг зурах
        pygame.draw.ellipse(screen, WHITE, ball_rect)
        
        # Оноог зурах
        score_text = font.render(f"{score_left}   {score_right}", True, WHITE)
        screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 20))
        
        # Горимын тайлбар зурах
        mode_str = f"Горим: {'Хиймэл Оюун (AI)' if ai_mode else 'Хоёр Тоглогч'} | [Space] - Горим солих"
        mode_text = small_font.render(mode_str, True, (150, 150, 170))
        screen.blit(mode_text, (20, HEIGHT - 30))
        
        instructions = small_font.render("Зүүн: W, S | Баруун: Дээш/Доош сум | Esc: Гарах", True, (150, 150, 170))
        screen.blit(instructions, (WIDTH - instructions.get_width() - 20, HEIGHT - 30))
        
        pygame.display.flip()
        clock.tick(FPS)
        
    pygame.quit()


if __name__ == "__main__":
    print("""
🏓 Pong тоглоом эхэлж байна!
- Зүүн талыг 'W', 'S' товчоор удирдана.
- Space товч дарж AI горимыг асааж/унтрааж болно.
- AI унтарсан үед Баруун талыг 'Дээш', 'Доош' сумаар удирдана.
    """)
    run_pong()
