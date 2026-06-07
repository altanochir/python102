"""
╔══════════════════════════════════════════════════════════════════╗
║  📊 Хичээл 4.6: Шийдвэр Гаргагч Хүрд (Decision Maker Wheel)       ║
║  Тригонометр (sin, cos), Хурдны үрэлт (Deceleration Physics),      ║
║  Текст оруулах талбар ба Динамик дүрслэл                         ║
╚══════════════════════════════════════════════════════════════════╝

🎯 Энэ хичээлээр үзэх сэдвүүд:
   1. Хэрэглэгчээс текст динамикаар авах (Input text box)
   2. Сонголтуудыг хувааж хүрд зурах (Trigonometry segments)
   3. Физикийн хуулиар эргэлдэх ба зогсох (Deceleration & Friction physics)
   4. Дэлгэцийн зохион байгуулалт (Layout division)
"""

import sys
import math
import random

try:
    import pygame
except ImportError:
    print("⚠️ Pygame суугаагүй байна! 'pip install pygame' ажиллуулна уу.")
    sys.exit(1)


# --- Premium Catppuccin Theme Colors ---
BG_COLOR = (30, 30, 46)        # Deep dark gray-purple
PANEL_COLOR = (24, 24, 37)      # Rich darker panel
INPUT_BG = (49, 50, 68)         # Medium gray-purple for input box
TEXT_PRIMARY = (205, 214, 244) # Soft white
TEXT_SECONDARY = (166, 173, 200) # Muted lavender-gray
TEXT_MUTED = (108, 112, 134)    # Dark slate gray
ACCENT_COLOR = (137, 180, 250)  # Ice blue / Sapphire
ACCENT_HOVER = (180, 190, 254)  # Lavender
WHITE = (255, 255, 255)
SHADOW_COLOR = (17, 17, 27)     # Very dark shadows
HIGHLIGHT_COLOR = (249, 226, 175) # Warm Yellow


# Хүрдний өнгөнүүд (Premium pastel neon palette)
WHEEL_COLORS = [
    (245, 194, 231), # Pink
    (243, 139, 168), # Soft Red
    (250, 179, 135), # Peach
    (249, 226, 175), # Warm Yellow
    (166, 227, 161), # Green
    (148, 226, 213), # Teal
    (137, 180, 250), # Blue
    (203, 166, 247)  # Lavender
]


def run_decision_maker():
    pygame.init()
    
    # Цонхны хэмжээ
    WIDTH, HEIGHT = 900, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("🎡 Шийдвэр Гаргагч Хүрд — Хичээл 4.6")
    
    clock = pygame.time.Clock()
    FPS = 60
    
    # ФОНТУУД (Fonts)
    font_main = pygame.font.SysFont("Arial", 16, bold=True)
    font_btn = pygame.font.SysFont("Arial", 16, bold=True)
    font_large = pygame.font.SysFont("Impact", 28)
    font_result = pygame.font.SysFont("Impact", 36)
    
    # --- Оролт болон Сонголтууд ---
    options = ["Аялалд явах", "Гэртээ амрах", "Код бичих", "Кино үзэх", "Ном унших"]
    input_text = ""
    input_active = True
    
    # Text box ба Add button-ийн байрлал
    input_box = pygame.Rect(40, 110, 200, 36)
    add_btn_rect = pygame.Rect(250, 110, 50, 36)
    
    # --- Хүрдний тохиргоо ---
    wheel_center = (580, 300)
    wheel_radius = 200
    current_angle = 0
    angular_velocity = 0
    friction = 0.985  # Үл ялиг нэмэгдүүлж илүү зөөлөн эргүүлнэ
    
    # Тоглоомын төлөв
    state = "IDLE"  # IDLE, SPINNING, SHOW_RESULT
    winner_text = ""
    winner_color = WHITE
    result_timer = 0
    result_scale = 0.0 # Zoom-in эффектэд зориулсан хувьсагч
    
    def add_option():
        nonlocal input_text
        val = input_text.strip()
        if val and len(options) < 12:
            options.append(val)
            input_text = ""

    def get_selected_option():
        if not options:
            return "", WHITE
        n = len(options)
        segment_angle = 360 / n
        relative_angle = (270 - current_angle) % 360
        selected_idx = int(relative_angle // segment_angle) % n
        return options[selected_idx], WHEEL_COLORS[selected_idx % len(WHEEL_COLORS)]

    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()
        
        # 1. Events (Гараас оролт авах)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    # А. Текст оруулах талбарт дарсан уу?
                    if input_box.collidepoint(event.pos):
                        input_active = True
                    else:
                        input_active = False
                        
                    # Б. Нэмэх товч дээр дарсан уу?
                    if add_btn_rect.collidepoint(event.pos) and state == "IDLE":
                        add_option()
                        
                    # В. Сонголтуудын устгах товчлуурууд
                    for idx in range(len(options)):
                        del_rect = pygame.Rect(274, 188 + idx * 32, 20, 20)
                        if del_rect.collidepoint(event.pos) and state == "IDLE":
                            options.pop(idx)
                            break

                            
                    # Г. Эргүүлэх (Spin) товчлуур
                    spin_btn_rect = pygame.Rect(40, 500, 260, 50)
                    if spin_btn_rect.collidepoint(event.pos) and state == "IDLE" and len(options) >= 2:
                        angular_velocity = random.uniform(22, 32)
                        state = "SPINNING"
                        
            if event.type == pygame.KEYDOWN:
                if input_active and state == "IDLE":
                    if event.key == pygame.K_RETURN:
                        add_option()
                    elif event.key == pygame.K_BACKSPACE:
                        input_text = input_text[:-1]
                    else:
                        if len(input_text) < 18 and event.unicode.isprintable():
                            input_text += event.unicode
                            
        # Escape товчоор гарах
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            running = False
            
        # 2. Физик тооцоолол (Physics updates)
        if state == "SPINNING":
            current_angle += angular_velocity
            angular_velocity *= friction
            
            if angular_velocity < 0.05:
                angular_velocity = 0
                winner_text, winner_color = get_selected_option()
                state = "SHOW_RESULT"
                result_timer = 180 # 3 секунд үр дүнг харуулна
                result_scale = 0.0
                
        elif state == "SHOW_RESULT":
            # Зөөлөн томорч гарч ирэх (Zoom-in scaling)
            result_scale = min(1.0, result_scale + 0.1)
            result_timer -= 1
            if result_timer <= 0:
                state = "IDLE"
                
        # 3. ЗУРАГЛАЛ ХИЙХ (Drawing)
        screen.fill(BG_COLOR)
        
        # --- ПРЕМИУМ АРЫН ФОН: Сүлжээ хээ (Dotted Grid Background) ---
        for x in range(0, WIDTH, 40):
            for y in range(0, HEIGHT, 40):
                pygame.draw.circle(screen, (45, 47, 72), (x, y), 1.2)
                
        # --- ЗҮҮН ТАЛЫН ХАНЕЛИ (Side Panel Control Room) ---
        # Сүүдэр
        pygame.draw.rect(screen, SHADOW_COLOR, (24, 24, 320, 560), border_radius=12)
        # Үндсэн самбар
        pygame.draw.rect(screen, PANEL_COLOR, (20, 20, 320, 560), border_radius=12)
        pygame.draw.rect(screen, (49, 50, 68), (20, 20, 320, 560), width=2, border_radius=12)
        
        # Самбарын Гарчиг
        title_text = font_large.render("DECISION MAKER", True, ACCENT_COLOR)
        screen.blit(title_text, (40, 40))
        
        # Оролтын заавар
        inst_text = font_main.render("Сонголт нэмэх:", True, TEXT_SECONDARY)
        screen.blit(inst_text, (40, 85))
        
        # А. Оролтын хайрцаг (Input box UI)
        box_border_color = ACCENT_COLOR if input_active else (74, 85, 114)
        pygame.draw.rect(screen, BG_COLOR, input_box, border_radius=6)
        pygame.draw.rect(screen, box_border_color, input_box, width=2, border_radius=6)
        
        txt_surface = font_main.render(input_text, True, WHITE)
        screen.blit(txt_surface, (input_box.x + 10, input_box.y + 8))
        
        # Б. Нэмэх товчлуур (+)
        add_hover = add_btn_rect.collidepoint(mouse_pos)
        add_btn_color = ACCENT_COLOR if add_hover else (74, 85, 114)
        pygame.draw.rect(screen, add_btn_color, add_btn_rect, border_radius=6)
        add_text = font_btn.render("+", True, BG_COLOR)
        screen.blit(add_text, (add_btn_rect.x + add_btn_rect.width//2 - add_text.get_width()//2, add_btn_rect.y + 6))
        
        # Сонголтуудын жагсаалт
        list_title = font_main.render(f"Жагсаалт ({len(options)}/12):", True, TEXT_SECONDARY)
        screen.blit(list_title, (40, 160))
        
        for idx, opt in enumerate(options):
            # Жагсаалтын ард жижиг арын блок зурах (Card style)
            card_rect = pygame.Rect(40, 185 + idx * 32, 260, 26)
            pygame.draw.rect(screen, (30, 30, 46), card_rect, border_radius=4)
            
            # Сонголтын текст
            opt_text = font_main.render(f"{idx+1}. {opt}", True, TEXT_PRIMARY)
            screen.blit(opt_text, (50, 188 + idx * 32))
            
            # Устгах товч (Улаан X)
            if state == "IDLE":
                del_rect = pygame.Rect(274, 188 + idx * 32, 20, 20)
                del_hover = del_rect.collidepoint(mouse_pos)
                del_color = (243, 139, 168) if del_hover else (74, 85, 114)
                
                pygame.draw.rect(screen, del_color, del_rect, border_radius=4)
                x_text = font_main.render("x", True, BG_COLOR)
                screen.blit(x_text, (del_rect.x + 6, del_rect.y - 1))
                
        # Эргүүлэх товчлуур (Spin Button)
        spin_btn_rect = pygame.Rect(40, 510, 260, 50)
        
        if len(options) >= 2 and state == "IDLE":
            spin_hover = spin_btn_rect.collidepoint(mouse_pos)
            spin_btn_color = ACCENT_HOVER if spin_hover else ACCENT_COLOR
            text_color = BG_COLOR
            active_btn = True
        else:
            spin_btn_color = (49, 50, 68)
            text_color = TEXT_MUTED
            active_btn = False
            
        pygame.draw.rect(screen, spin_btn_color, spin_btn_rect, border_radius=8)
        # Товчны доор үл ялиг сүүдэр
        if active_btn:
            pygame.draw.rect(screen, (17, 17, 27), spin_btn_rect, width=2, border_radius=8)
            
        spin_text = font_large.render("🎡 SPIN WHEEL", True, text_color)
        screen.blit(spin_text, (spin_btn_rect.x + spin_btn_rect.width//2 - spin_text.get_width()//2, spin_btn_rect.y + 10))
        
        # --- БАРУУН ТАЛ: Эргэдэг Хүрд (The Spinning Wheel) ---
        n_segments = len(options)
        if n_segments >= 2:
            segment_angle = 360 / n_segments
            
            # 1. Хүрдний Арын сүүдэр зурах (Drop Shadow Effect)
            pygame.draw.circle(screen, SHADOW_COLOR, (wheel_center[0] + 6, wheel_center[1] + 6), wheel_radius + 4)
            
            # 2. Барааны хэсэг бүрийг зурах
            for i in range(n_segments):
                start_deg = current_angle + i * segment_angle
                end_deg = current_angle + (i + 1) * segment_angle
                
                # Нумын дагуу цэгүүд бодож хэрчим зурах
                points = [wheel_center]
                for deg in range(int(start_deg), int(end_deg) + 2):
                    rad = math.radians(deg)
                    px = wheel_center[0] + wheel_radius * math.cos(rad)
                    py = wheel_center[1] + wheel_radius * math.sin(rad)
                    points.append((px, py))
                points.append(wheel_center)
                
                color = WHEEL_COLORS[i % len(WHEEL_COLORS)]
                pygame.draw.polygon(screen, color, points)
                
                # Заагч шугамуудыг нарийн зурах
                rad_start = math.radians(start_deg)
                line_x = wheel_center[0] + wheel_radius * math.cos(rad_start)
                line_y = wheel_center[1] + wheel_radius * math.sin(rad_start)
                pygame.draw.line(screen, BG_COLOR, wheel_center, (line_x, line_y), 2)
                
                # Текст байршуулах координатууд
                mid_deg = start_deg + segment_angle / 2
                mid_rad = math.radians(mid_deg)
                text_dist = wheel_radius * 0.65
                tx = wheel_center[0] + text_dist * math.cos(mid_rad)
                ty = wheel_center[1] + text_dist * math.sin(mid_rad)
                
                display_opt = options[i]
                if len(display_opt) > 10:
                    display_opt = display_opt[:8] + ".."
                    
                text_fg = BG_COLOR if color != (15, 23, 42) else WHITE
                opt_surface = font_main.render(display_opt, True, text_fg)
                
                # Текстийг өнцгийн дагуу налуулах (Rotate)
                rotated_surface = pygame.transform.rotate(opt_surface, -mid_deg)
                screen.blit(rotated_surface, (tx - rotated_surface.get_width()//2, ty - rotated_surface.get_height()//2))
                
            # 3. Хүрдний хамгаалалтын Неон гэрэлт хүрээ (Neon Glow Border)
            pygame.draw.circle(screen, PANEL_COLOR, wheel_center, wheel_radius + 10, width=8)
            pygame.draw.circle(screen, ACCENT_COLOR, wheel_center, wheel_radius + 6, width=2)
        else:
            # Сонголт дутуу үед зурж харуулах placeholder хүрд
            pygame.draw.circle(screen, SHADOW_COLOR, (wheel_center[0] + 5, wheel_center[1] + 5), wheel_radius)
            pygame.draw.circle(screen, PANEL_COLOR, wheel_center, wheel_radius)
            pygame.draw.circle(screen, (74, 85, 114), wheel_center, wheel_radius, width=4)
            ph_text = font_large.render("СОНГОЛТОО ОРУУЛНА УУ", True, (74, 85, 114))
            screen.blit(ph_text, (wheel_center[0] - ph_text.get_width()//2, wheel_center[1] - ph_text.get_height()//2))
            
        # 4. Төвийн гялгар товчлуур (Metallic Center Pin)
        pygame.draw.circle(screen, SHADOW_COLOR, (wheel_center[0] + 2, wheel_center[1] + 2), 24)
        pygame.draw.circle(screen, PANEL_COLOR, wheel_center, 20)
        pygame.draw.circle(screen, ACCENT_COLOR, wheel_center, 20, width=3)
        pygame.draw.circle(screen, WHITE, (wheel_center[0] - 6, wheel_center[1] - 6), 4) # Glossy highlight dot
        
        # 5. Заагч сум (Pointer Arrow)
        arrow_points = [
            (wheel_center[0], wheel_center[1] - wheel_radius - 15),
            (wheel_center[0] - 15, wheel_center[1] - wheel_radius - 40),
            (wheel_center[0] + 15, wheel_center[1] - wheel_radius - 40)
        ]
        # сумны сүүдэр
        pygame.draw.polygon(screen, SHADOW_COLOR, [(p[0] + 2, p[1] + 2) for p in arrow_points])
        pygame.draw.polygon(screen, HIGHLIGHT_COLOR, arrow_points)
        pygame.draw.polygon(screen, WHITE, arrow_points, width=2)
        
        # --- ҮР ДҮНГИЙН ЦОНХ: Премиум анимацитай модал (Zooming Result Modal) ---
        if state == "SHOW_RESULT" and winner_text and result_scale > 0:
            # Анимациар хайрцагны хэмжээг томруулах
            box_w = int(450 * result_scale)
            box_h = int(140 * result_scale)
            box_x = wheel_center[0] - box_w // 2
            box_y = wheel_center[1] - box_h // 2
            res_rect = pygame.Rect(box_x, box_y, box_w, box_h)
            
            # Модалын сүүдэр болон суурь
            pygame.draw.rect(screen, SHADOW_COLOR, (box_x + 6, box_y + 6, box_w, box_h), border_radius=12)
            pygame.draw.rect(screen, PANEL_COLOR, res_rect, border_radius=12)
            pygame.draw.rect(screen, winner_color, res_rect, width=3, border_radius=12)
            
            # Текстийг зөвхөн хайрцаг бараг дүүрч томорох үед харуулна
            if result_scale > 0.8:
                res_label = font_main.render("🎉 СОНГОГДСОН ШИЙДВЭР 🎉", True, TEXT_SECONDARY)
                res_val = font_result.render(winner_text, True, winner_color)
                
                screen.blit(res_label, (box_x + box_w//2 - res_label.get_width()//2, box_y + 25))
                screen.blit(res_val, (box_x + box_w//2 - res_val.get_width()//2, box_y + 60))
                
        pygame.display.flip()
        clock.tick(FPS)
        
    pygame.quit()


if __name__ == "__main__":
    print("""
🎡 Шийдвэр Гаргагч Хүрд тоглоом ажиллаж байна!
- Зүүн талын талбарт шинээр сонголт бичиж [Enter] эсвэл [+] дээр даран нэмнэ үү.
- Сонголтын хажуугийн 'x' товчлуур дээр дарж устгана.
- '🎡 SPIN WHEEL' товч дээр дарж хүрдээ эргүүлэн шийдвэрээ гаргана уу.
    """)
    run_decision_maker()
