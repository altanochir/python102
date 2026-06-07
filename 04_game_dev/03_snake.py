"""
╔══════════════════════════════════════════════════════════════════╗
║  🎮 Хичээл 4.3: Сонгодог Могой (Snake) Тоглоом                     ║
║  Хүснэгтэн систем (Grid layout), Могойг удирдах, Хооллох логик     ║
╚══════════════════════════════════════════════════════════════════╝

🎯 Энэ хичээлээр үзэх сэдвүүд:
   1. Хүснэгтэн сүлжээ (Grid system) болон Могойн бүтэц (Segments)
   2. Чиглэлээр удирдах ба Сүүл нь толгойгоо дагах хөдөлгөөн
   3. Санамсаргүй байдлаар хоол гаргах (Food spawning)
   4. Өөрийгөө болон Хана мөргөхөд Game Over болох
   5. Тоглоомыг шинээр эхлүүлэх (Restart mechanics)
"""

import sys
import random

try:
    import pygame
except ImportError:
    print("⚠️ Pygame суугаагүй байна! 'pip install pygame' ажиллуулна уу.")
    sys.exit(1)


def run_snake():
    pygame.init()
    
    # Сүлжээний (Grid) тохиргоо
    CELL_SIZE = 20
    GRID_WIDTH = 30
    GRID_HEIGHT = 20
    
    # Цонхны хэмжээ
    WIDTH = GRID_WIDTH * CELL_SIZE
    HEIGHT = GRID_HEIGHT * CELL_SIZE
    
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("🐍 Сонгодог Могой — Хичээл 4.3")
    
    # Өнгөнүүд
    BG_COLOR = (15, 23, 42)
    GRID_LINE_COLOR = (30, 41, 59)
    SNAKE_HEAD_COLOR = (34, 197, 94) # Ногоон
    SNAKE_BODY_COLOR = (74, 222, 128) # Цайвар ногоон
    FOOD_COLOR = (239, 68, 68) # Улаан
    TEXT_COLOR = (248, 250, 252)
    
    # FPS хянагч (Могойн хурд FPS-ээр шууд удирдагдана)
    clock = pygame.time.Clock()
    FPS = 10 # Хэт хурдан байвал тоглоход хэцүү тул 10 фрэймээр хязгаарлана
    
    # Чиглэлүүдийн вектор
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)
    
    # Тоглоомын төлөвүүд
    snake = []
    direction = RIGHT
    food = (0, 0)
    score = 0
    game_over = False
    
    def reset_game():
        nonlocal snake, direction, score, game_over
        # Могойг дэлгэцийн голд 3 сегменттэйгээр эхлүүлэх
        start_x = GRID_WIDTH // 2
        start_y = GRID_HEIGHT // 2
        snake = [(start_x, start_y), (start_x - 1, start_y), (start_x - 2, start_y)]
        direction = RIGHT
        score = 0
        game_over = False
        spawn_food()
        
    def spawn_food():
        nonlocal food
        while True:
            # Сүлжээн дотор санамсаргүй байрлал сонгох
            x = random.randint(0, GRID_WIDTH - 1)
            y = random.randint(0, GRID_HEIGHT - 1)
            food_pos = (x, y)
            # Хэрэв сонгосон байрлал могойн бие дээр таарвал дахин өөр байрлал сонгоно
            if food_pos not in snake:
                food = food_pos
                break
                
    # Тоглоомыг анхлан эхлүүлэх
    reset_game()
    
    running = True
    while running:
        # 1. Events (Гараас оролт авах)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
            if event.type == pygame.KEYDOWN:
                if game_over:
                    if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                        reset_game()
                else:
                    # Чиглэл өөрчлөх (Могой 180 градус шууд буцаж эргэж болохгүй!)
                    if event.key == pygame.K_UP and direction != DOWN:
                        direction = UP
                    elif event.key == pygame.K_DOWN and direction != UP:
                        direction = DOWN
                    elif event.key == pygame.K_LEFT and direction != RIGHT:
                        direction = LEFT
                    elif event.key == pygame.K_RIGHT and direction != LEFT:
                        direction = RIGHT
                        
        # Escape товчоор шууд гарах
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            running = False
            
        # 2. Тоглоомын логик шинэчлэл
        if not game_over:
            # Толгой хэсгийг тодорхойлох
            head_x, head_y = snake[0]
            dir_x, dir_y = direction
            new_head = (head_x + dir_x, head_y + dir_y)
            
            # А. Мөргөлдөөн шалгах: Хана мөргөсөн эсэх
            new_x, new_y = new_head
            if new_x < 0 or new_x >= GRID_WIDTH or new_y < 0 or new_y >= GRID_HEIGHT:
                game_over = True
                
            # Б. Мөргөлдөөн шалгах: Өөрийн биеийг мөргөсөн эсэх
            if new_head in snake:
                game_over = True
                
            if not game_over:
                # Толгойг нэмэх
                snake.insert(0, new_head)
                
                # В. Хооллох логик: Хоол мөргөх
                if new_head == food:
                    score += 10
                    spawn_food() # Шинэ хоол үүсгэх (Сүүл хасагдахгүй тул могой уртсана)
                else:
                    # Хоол идэгүй бол сүүлийг хасаж хөдөлгөөнийг хэвийн хадгална
                    snake.pop()
                    
        # 3. Зураглал хийх (Drawing)
        screen.fill(BG_COLOR)
        
        # Тоглоомын талбарын сүлжээ (Grid) зурах
        for x in range(0, WIDTH, CELL_SIZE):
            pygame.draw.line(screen, GRID_LINE_COLOR, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, CELL_SIZE):
            pygame.draw.line(screen, GRID_LINE_COLOR, (0, y), (WIDTH, y))
            
        # Могой зурах
        for idx, segment in enumerate(snake):
            seg_x, seg_y = segment
            rect = pygame.Rect(seg_x * CELL_SIZE + 1, seg_y * CELL_SIZE + 1, CELL_SIZE - 2, CELL_SIZE - 2)
            # Толгойг арай өөр ногооноор ялгаж зурах
            color = SNAKE_HEAD_COLOR if idx == 0 else SNAKE_BODY_COLOR
            pygame.draw.rect(screen, color, rect, border_radius=4)
            
        # Хоол зурах
        food_x, food_y = food
        food_rect = pygame.Rect(food_x * CELL_SIZE + 2, food_y * CELL_SIZE + 2, CELL_SIZE - 4, CELL_SIZE - 4)
        pygame.draw.ellipse(screen, FOOD_COLOR, food_rect)
        
        # Оноог дэлгэцэнд зурах
        font = pygame.font.SysFont("Consolas", 20)
        score_text = font.render(f"Score: {score}", True, TEXT_COLOR)
        screen.blit(score_text, (10, 10))
        
        # Game Over дэлгэц
        if game_over:
            # Бүдгэрүүлэгч overlay зурах
            overlay = pygame.Surface((WIDTH, HEIGHT))
            overlay.set_alpha(180)
            overlay.fill((15, 23, 42))
            screen.blit(overlay, (0, 0))
            
            # Текстүүд зурах
            font_title = pygame.font.SysFont("Arial", 40, bold=True)
            font_sub = pygame.font.SysFont("Arial", 20)
            
            title_text = font_title.render("GAME OVER", True, FOOD_COLOR)
            sub_text = font_sub.render(f"Final Score: {score} | Press [Space] to Play Again", True, TEXT_COLOR)
            
            screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 2 - 40))
            screen.blit(sub_text, (WIDTH // 2 - sub_text.get_width() // 2, HEIGHT // 2 + 10))
            
        pygame.display.flip()
        clock.tick(FPS)
        
    pygame.quit()


if __name__ == "__main__":
    print("""
🐍 Сонгодог Могой тоглоом эхэлж байна!
- Могойг Дээш, Доош, Зүүн, Баруун сумтай товчоор удирдана.
- Хоол идэж оноо цуглуулан могойгоо уртасгаарай.
- Хана болон өөрийн сүүлийг мөргөвөл тоглоом дуусна.
    """)
    run_snake()
