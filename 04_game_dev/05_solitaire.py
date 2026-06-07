"""
╔══════════════════════════════════════════════════════════════════╗
║  🎮 Хичээл 4.5: Сонгодог Солитер (Solitaire - Klondike)           ║
║  Хөзрийн чирэх-тавих (Drag & Drop), Тоглоомын төлөв ба Дүрслэл   ║
╚══════════════════════════════════════════════════════════════════╝

🎯 Энэ хичээлээр үзэх сэдвүүд:
   1. Хөзрийн бүтэц (Card class) болон Ангилал (Suits, Values)
   2. Солитерийн дүрмийн дагуу хөзөр өрөх (Stock, Waste, Tableau, Foundation)
   3. Хулганаар хөзөр чирж зөөх (Drag & Drop)
   4. Дүрмийн дагуу шилжүүлэлт шалгах (Validation)
   5. Өрөлтийг автоматаар нээх (Auto-flip face down cards)
"""

import sys
import random

try:
    import pygame
except ImportError:
    print("⚠️ Pygame суугаагүй байна! 'pip install pygame' ажиллуулна уу.")
    sys.exit(1)


# --- Хөзрийн хэмжээ ба Тоглоомын тохиргоо ---
CARD_WIDTH = 75
CARD_HEIGHT = 110
CARD_RADIUS = 6

# Сүйт (Suits) ба Утгууд (Values)
SUITS = ["Hearts", "Diamonds", "Clubs", "Spades"]
SUIT_SYMBOLS = {"Hearts": "♥", "Diamonds": "♦", "Clubs": "♣", "Spades": "♠"}
SUIT_COLORS = {"Hearts": (239, 68, 68), "Diamonds": (239, 68, 68), "Clubs": (15, 23, 42), "Spades": (15, 23, 42)} # Улаан, Хар

VALUES = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]


class Card:
    def __init__(self, value, suit):
        self.value = value
        self.suit = suit
        self.face_up = False
        
        # Чирэх-тавих үеийн байрлал
        self.rect = pygame.Rect(0, 0, CARD_WIDTH, CARD_HEIGHT)
        
    def draw(self, screen, x, y):
        self.rect.topleft = (x, y)
        
        if self.face_up:
            # --- Нүүр нь ил гарсан хөзөр зурах ---
            # Арын цагаан дэвсгэр
            pygame.draw.rect(screen, (255, 255, 255), self.rect, border_radius=CARD_RADIUS)
            pygame.draw.rect(screen, (200, 200, 200), self.rect, width=1, border_radius=CARD_RADIUS)
            
            # Тэмдэгт болон Хэмжээний бичвэр
            symbol = SUIT_SYMBOLS[self.suit]
            color = SUIT_COLORS[self.suit]
            
            font = pygame.font.SysFont("Consolas", 18, bold=True)
            symbol_font = pygame.font.SysFont("Arial", 28)
            
            # Зүүн дээд талд бичих
            val_text = font.render(self.value, True, color)
            screen.blit(val_text, (x + 6, y + 4))
            
            sym_text_small = font.render(symbol, True, color)
            screen.blit(sym_text_small, (x + 6, y + 20))
            
            # Голд нь томоор зурах
            sym_text_large = symbol_font.render(symbol, True, color)
            screen.blit(sym_text_large, (x + CARD_WIDTH//2 - sym_text_large.get_width()//2, y + CARD_HEIGHT//2 - sym_text_large.get_height()//2 + 5))
            
            # Баруун доод талд бичих (урвуу эргүүлсэн мэт)
            val_text_rev = font.render(self.value, True, color)
            screen.blit(val_text_rev, (x + CARD_WIDTH - val_text_rev.get_width() - 6, y + CARD_HEIGHT - val_text_rev.get_height() - 4))
        else:
            # --- Нуруу нь харагдсан хөзөр зурах ---
            pygame.draw.rect(screen, (255, 255, 255), self.rect, border_radius=CARD_RADIUS)
            # Дотор нь цэнхэр хээ зурах
            inner_rect = pygame.Rect(x + 4, y + 4, CARD_WIDTH - 8, CARD_HEIGHT - 8)
            pygame.draw.rect(screen, (59, 130, 246), inner_rect, border_radius=CARD_RADIUS-2)
            pygame.draw.rect(screen, (29, 78, 216), inner_rect, width=2, border_radius=CARD_RADIUS-2)


class SolitaireGame:
    def __init__(self):
        # Бүх хөзрийг үүсгэж холих
        self.deck = [Card(v, s) for s in SUITS for v in VALUES]
        random.shuffle(self.deck)
        
        # --- Овоолгуудын тодорхойлолт ---
        self.stock = []          # Draw pile (Face down)
        self.waste = []          # Drawn cards (Face up)
        self.foundation = [[] for _ in range(4)] # 4 халаас (Hearts, Diamonds, Clubs, Spades)
        self.tableau = [[] for _ in range(7)]    # 7 багана өрөлт
        
        # Хөзрүүдийг 7 баганаар өрөх
        deck_idx = 0
        for i in range(7):
            for j in range(i + 1):
                card = self.deck[deck_idx]
                deck_idx += 1
                if j == i:
                    card.face_up = True # Хамгийн дээд талын хөзрийг ил гаргах
                self.tableau[i].append(card)
                
        # Үлдсэн хөзрүүдийг stock-д хийх
        while deck_idx < len(self.deck):
            self.stock.append(self.deck[deck_idx])
            deck_idx += 1
            
        # Чирч байгаа хөзрийн мэдээлэл
        self.dragged_cards = []
        self.drag_source = None  # Аль овоолгоос авсан бэ ("tableau", "waste", "foundation")
        self.drag_source_idx = None # Баганын дугаар
        self.drag_offset = (0, 0)
        
    def draw(self, screen):
        screen.fill((21, 128, 61)) # Ногоон даавуу арын өнгө
        
        # 1. Stock pile зурах (Зүүн дээд талд)
        stock_x, stock_y = 50, 40
        if self.stock:
            # Дээд талын хөзрийн нурууг зурах
            temp_card = Card("A", "Spades") # Зөвхөн арыг нь зурах учир
            temp_card.draw(screen, stock_x, stock_y)
        else:
            # Хоосон бол нөхөх дугуй тэмдэг зурах
            pygame.draw.rect(screen, (16, 185, 129), (stock_x, stock_y, CARD_WIDTH, CARD_HEIGHT), width=2, border_radius=CARD_RADIUS)
            font = pygame.font.SysFont("Arial", 28)
            reload_text = font.render("↻", True, (16, 185, 129))
            screen.blit(reload_text, (stock_x + CARD_WIDTH//2 - reload_text.get_width()//2, stock_y + CARD_HEIGHT//2 - reload_text.get_height()//2))
            
        # 2. Waste pile зурах (Stock-ийн хажууд)
        waste_x, waste_y = 150, 40
        if self.waste:
            # Зөвхөн хамгийн дээд талын 1 хөзрийг ил зурна
            self.waste[-1].draw(screen, waste_x, waste_y)
        else:
            pygame.draw.rect(screen, (16, 185, 129), (waste_x, waste_y, CARD_WIDTH, CARD_HEIGHT), width=1, border_radius=CARD_RADIUS)
            
        # 3. Foundation 4 халаас зурах (Баруун дээд талд)
        for i in range(4):
            found_x = 390 + i * (CARD_WIDTH + 20)
            found_y = 40
            if self.foundation[i]:
                self.foundation[i][-1].draw(screen, found_x, found_y)
            else:
                # Хоосон халаас зурах
                pygame.draw.rect(screen, (16, 185, 129), (found_x, found_y, CARD_WIDTH, CARD_HEIGHT), width=2, border_radius=CARD_RADIUS)
                # A үсэг голд нь бичих
                font = pygame.font.SysFont("Impact", 24)
                a_text = font.render("A", True, (16, 185, 129))
                screen.blit(a_text, (found_x + CARD_WIDTH//2 - a_text.get_width()//2, found_y + CARD_HEIGHT//2 - a_text.get_height()//2))
                
        # 4. Tableau 7 багана зурах (Доод талд)
        for i in range(7):
            col_x = 50 + i * (CARD_WIDTH + 20)
            col_y = 180
            if self.tableau[i]:
                # Баганы хөзрүүдийг дээр дээрээс нь давхарлаж зурах (Y тэнхлэгт зөрүүтэй)
                for j, card in enumerate(self.tableau[i]):
                    # Хэрэв чирж байгаа хөзөр мөн бол энд зурахгүй, дараа нь хулганы байрлалд зурна
                    if card in self.dragged_cards:
                        continue
                    # Доошлох зай (Ил хөзөр бол арай урт зайтай, далд бол богино)
                    offset_y = j * (20 if not card.face_up else 28)
                    card.draw(screen, col_x, col_y + offset_y)
            else:
                # Хоосон багана зурах
                pygame.draw.rect(screen, (16, 185, 129), (col_x, col_y, CARD_WIDTH, CARD_HEIGHT), width=1, border_radius=CARD_RADIUS)
                
        # 5. Чирч яваа хөзрүүдийг хулганы байрлалд зурах
        if self.dragged_cards:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            for idx, card in enumerate(self.dragged_cards):
                card.draw(screen, mouse_x - self.drag_offset[0], mouse_y - self.drag_offset[1] + idx * 28)

    def handle_click(self, pos):
        # Хэрэв чирж яваа хөзөр байвал үл тоомсорлох
        if self.dragged_cards:
            return
            
        # А. Stock дээр дарсан уу?
        stock_rect = pygame.Rect(50, 40, CARD_WIDTH, CARD_HEIGHT)
        if stock_rect.collidepoint(pos):
            if self.stock:
                # Stock-оос нэг хөзөр авч waste-д ил гаргаж нэмэх
                card = self.stock.pop()
                card.face_up = True
                self.waste.append(card)
            else:
                # Waste-ийг буцааж stock руу шилжүүлэх (Recycle)
                while self.waste:
                    card = self.waste.pop()
                    card.face_up = False
                    self.stock.append(card)
                self.stock.reverse()
            return
            
        # Б. Waste дээрээс хөзөр чирэх
        if self.waste:
            waste_rect = pygame.Rect(150, 40, CARD_WIDTH, CARD_HEIGHT)
            if waste_rect.collidepoint(pos):
                card = self.waste[-1]
                self.dragged_cards = [card]
                self.drag_source = "waste"
                self.drag_offset = (pos[0] - card.rect.x, pos[1] - card.rect.y)
                return
                
        # В. Foundation-оос хөзөр чирэх
        for i in range(4):
            if self.foundation[i]:
                found_rect = pygame.Rect(390 + i * (CARD_WIDTH + 20), 40, CARD_WIDTH, CARD_HEIGHT)
                if found_rect.collidepoint(pos):
                    card = self.foundation[i][-1]
                    self.dragged_cards = [card]
                    self.drag_source = "foundation"
                    self.drag_source_idx = i
                    self.drag_offset = (pos[0] - card.rect.x, pos[1] - card.rect.y)
                    return
                    
        # Г. Tableau багануудаас хөзөр чирэх (Эхнээс нь давхарласан хөзрүүдийг чирч болно)
        for i in range(7):
            if self.tableau[i]:
                for j in range(len(self.tableau[i]) - 1, -1, -1):
                    card = self.tableau[i][j]
                    # Зөвхөн ил гарсан хөзрийг л чирэх боломжтой
                    if card.face_up and card.rect.collidepoint(pos):
                        self.dragged_cards = self.tableau[i][j:] # Тэр хөзөр болон түүнээс доорх бүх хөзөр
                        self.drag_source = "tableau"
                        self.drag_source_idx = i
                        self.drag_offset = (pos[0] - card.rect.x, pos[1] - card.rect.y)
                        return

    def handle_release(self, pos):
        if not self.dragged_cards:
            return
            
        target_found = False
        target_type = None
        target_idx = None
        
        # А. Foundation дээр тавьсан уу? (Зөвхөн 1 хөзөр тавих боломжтой)
        if len(self.dragged_cards) == 1:
            card = self.dragged_cards[0]
            for i in range(4):
                found_rect = pygame.Rect(390 + i * (CARD_WIDTH + 20), 40, CARD_WIDTH, CARD_HEIGHT)
                if found_rect.collidepoint(pos):
                    if self.can_place_on_foundation(card, i):
                        target_found = True
                        target_type = "foundation"
                        target_idx = i
                        break
                        
        # Б. Tableau баганууд дээр тавьсан уу?
        if not target_found:
            for i in range(7):
                col_x = 50 + i * (CARD_WIDTH + 20)
                # Баганы доод хэсэгт тавих тул сунгасан орон зайг шалгана
                col_height = CARD_HEIGHT + len(self.tableau[i]) * 28
                col_rect = pygame.Rect(col_x, 180, CARD_WIDTH, col_height)
                if col_rect.collidepoint(pos):
                    if self.can_place_on_tableau(self.dragged_cards[0], i):
                        target_found = True
                        target_type = "tableau"
                        target_idx = i
                        break
                        
        # В. Зөв овоолгод тавьсан бол шилжүүлэх
        if target_found:
            # Эх сурвалжаас нь хасах
            if self.drag_source == "waste":
                self.waste.pop()
            elif self.drag_source == "foundation":
                self.foundation[self.drag_source_idx].pop()
            elif self.drag_source == "tableau":
                # Tableau-аас чирч авсан хэсгийг нь устгана
                del self.tableau[self.drag_source_idx][-len(self.dragged_cards):]
                # Хамгийн дээд талын хөзөр нь хаалттай бол автоматаар нээх (Auto-flip)
                if self.tableau[self.drag_source_idx] and not self.tableau[self.drag_source_idx][-1].face_up:
                    self.tableau[self.drag_source_idx][-1].face_up = True
                    
            # Очих газар нь нэмэх
            if target_type == "foundation":
                self.foundation[target_idx].append(self.dragged_cards[0])
            elif target_type == "tableau":
                self.tableau[target_idx].extend(self.dragged_cards)
        else:
            # Буруу газар тавьсан бол буцаах (Хийх зүйлгүй, зүгээр л хоослоход хуучин байрандаа зурагдана)
            pass
            
        # Чирэлтийг цуцлах
        self.dragged_cards = []
        self.drag_source = None
        self.drag_source_idx = None

    def can_place_on_foundation(self, card, idx):
        dest_pile = self.foundation[idx]
        if not dest_pile:
            # Хоосон бол зөвхөн ACE (А) орно
            return card.value == "A"
        else:
            # Овоолгоны дээд хөзөр
            top_card = dest_pile[-1]
            # Ижил сүйтэй, дараалсан дараагийн тоо байх ёстой
            val_idx_top = VALUES.index(top_card.value)
            val_idx_card = VALUES.index(card.value)
            return card.suit == top_card.suit and val_idx_card == val_idx_top + 1

    def can_place_on_tableau(self, card, idx):
        dest_pile = self.tableau[idx]
        if not dest_pile:
            # Хоосон баганад зөвхөн Хаан (K) хөзөр тавих боломжтой
            return card.value == "K"
        else:
            top_card = dest_pile[-1]
            # Зөвхөн нээлттэй хөзөр дээр тавина
            if not top_card.face_up:
                return False
                
            # Өөр өнгийн сүйтэй (Улаан хөзөр дээр Хар, Хар хөзөр дээр Улаан)
            color_top = SUIT_COLORS[top_card.suit]
            color_card = SUIT_COLORS[card.suit]
            
            # Нэг тоогоор бага байх ёстой (Жишээ нь: Q дээр J тавих)
            val_idx_top = VALUES.index(top_card.value)
            val_idx_card = VALUES.index(card.value)
            
            return color_top != color_card and val_idx_card == val_idx_top - 1

    def check_victory(self):
        # Хэрэв 4 халаас бүгд дүүрч, нийт 52 хөзөр орсон бол ялна
        return sum(len(f) for f in self.foundation) == 52


def main():
    pygame.init()
    
    # Цонхны хэмжээ
    WIDTH, HEIGHT = 850, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("🃏 Classic Solitaire — Хичээл 4.5")
    
    clock = pygame.time.Clock()
    game = SolitaireGame()
    
    running = True
    while running:
        pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: # Зүүн товч
                    game.handle_click(event.pos)
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1: # Зүүн товч
                    game.handle_release(event.pos)
                    
        # Шинэчлэн зурах
        game.draw(screen)
        
        # Ялалт шалгах
        if game.check_victory():
            # Ялалтын текст харуулах
            overlay = pygame.Surface((WIDTH, HEIGHT))
            overlay.set_alpha(150)
            overlay.fill((15, 23, 42))
            screen.blit(overlay, (0, 0))
            
            font = pygame.font.SysFont("Impact", 50)
            vic_text = font.render("VICTORY! 🏆", True, (251, 191, 36))
            screen.blit(vic_text, (WIDTH//2 - vic_text.get_width()//2, HEIGHT//2 - vic_text.get_height()//2))
            
        pygame.display.flip()
        clock.tick(60)
        
    pygame.quit()


if __name__ == "__main__":
    print("""
🃏 Classic Solitaire (Klondike) тоглоом ажиллаж байна!
- Зүүн дээд талын 'Stock' овоолго дээр дарж шинэ хөзөр дэлгэнэ.
- Хөзрүүдийг чирч зөөж зөв дарааллаар байрлуулна.
- 4 халаас бүгд ACE-оос KING хүртэл ижил өнгөөр дүүрвэл та ялна.
    """)
    main()
