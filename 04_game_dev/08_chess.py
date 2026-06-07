"""
╔══════════════════════════════════════════════════════════════════╗
║  ♟️ Хичээл 4.8: Шатар (Classic Chess)                              ║
║  Хоёр хэмжээст тоглоомын хөлөг (Board coordinate mapping),         ║
║  Дүрмийн дагуу нүүдэл шалгах (Move validation), Ээлж солих        ║
╚══════════════════════════════════════════════════════════════════╝

🎯 Энэ хичээлээр үзэх сэдвүүд:
   1. Шатрын хөлөг дүрслэх (8x8 Board Grid) ба Chess.com загварын тэмдэглэгээ
   2. Шатрын боддогуудыг Юникод тэмдэгтээр төвд нь зэрэгцүүлж зурах
   3. Боддог тус бүрийн үндсэн нүүх дүрэм (Pawn, Rook, Knight, Bishop, Queen, King)
   4. Хиймэл оюуны энгийн алгоритм (Heuristic AI for Black)
   5. Хажуугийн самбараар удирдах (AI vs 2-Player горим шилжүүлэгч)
"""

import sys
import random

try:
    import pygame
except ImportError:
    print("⚠️ Pygame суугаагүй байна! 'pip install pygame' ажиллуулна уу.")
    sys.exit(1)


# --- Хэмжээ болон Тоглоомын Тохиргоо ---
BOARD_SIZE = 8
SQUARE_SIZE = 70
BOARD_WIDTH = BOARD_SIZE * SQUARE_SIZE
BOARD_HEIGHT = BOARD_SIZE * SQUARE_SIZE

WIDTH, HEIGHT = 880, 620

# Chess.com өнгөний палитр
LIGHT_SQUARE = (238, 238, 210) # Цайвар шар
DARK_SQUARE = (118, 150, 86)    # Ногоон
BG_COLOR = (30, 30, 46)         # Харанхуй дэвсгэр
PANEL_COLOR = (24, 24, 37)       # Хажуугийн самбарын өнгө
HIGHLIGHT_COLOR = (247, 247, 105, 130) # Шар хагас тунгалаг
WHITE_COLOR = (255, 255, 255)
BLACK_COLOR = (17, 17, 27)
ACCENT_COLOR = (137, 180, 250)  # Цэнхэр
TEXT_COLOR = (205, 214, 244)    # Цайвар саарал бичвэр
TEXT_MUTED = (108, 112, 134)    # Бараан саарал бичвэр
GRID_COLOR = (49, 50, 68)       # Хүрээний зөөлөн саарал өнгө


# Шатрын боддогуудын Юникод тэмдэгтүүд (Солид загвар)
PIECE_SYMBOLS = {
    "P": "♟", "R": "♜", "N": "♞", "B": "♝", "Q": "♛", "K": "♚"
}

# Боддогуудын оноо (AI тооцоололд ашиглана)
PIECE_VALUES = {
    "P": 10, "N": 30, "B": 30, "R": 50, "Q": 90, "K": 900
}


class ChessPiece:
    def __init__(self, name, color, row, col):
        self.name = name     # "P" (Хүү), "R" (Тэрэг), "N" (Морь), "B" (Тэмээ), "Q" (Бэр), "K" (Хаан)
        self.color = color   # "W" (Цагаан), "B" (Хар)
        self.row = row
        self.col = col
        self.has_moved = False


class ChessGame:
    def __init__(self):
        self.board = [[None for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self.selected_piece = None
        self.valid_moves = []
        self.turn = "W" # "W" - Цагаан, "B" - Хар
        self.game_over = False
        self.winner = None
        self.ai_mode = True # Компьютерийн эсрэг тоглох горим
        
        self.setup_board()
        
    def setup_board(self):
        # Хар талын боддогууд (Black Pieces)
        self.board[0][0] = ChessPiece("R", "B", 0, 0)
        self.board[0][1] = ChessPiece("N", "B", 0, 1)
        self.board[0][2] = ChessPiece("B", "B", 0, 2)
        self.board[0][3] = ChessPiece("Q", "B", 0, 3)
        self.board[0][4] = ChessPiece("K", "B", 0, 4)
        self.board[0][5] = ChessPiece("B", "B", 0, 5)
        self.board[0][6] = ChessPiece("N", "B", 0, 6)
        self.board[0][7] = ChessPiece("R", "B", 0, 7)
        for col in range(BOARD_SIZE):
            self.board[1][col] = ChessPiece("P", "B", 1, col)
            
        # Цагаан талын боддогууд (White Pieces)
        self.board[7][0] = ChessPiece("R", "W", 7, 0)
        self.board[7][1] = ChessPiece("N", "W", 7, 1)
        self.board[7][2] = ChessPiece("B", "W", 7, 2)
        self.board[7][3] = ChessPiece("Q", "W", 7, 3)
        self.board[7][4] = ChessPiece("K", "W", 7, 4)
        self.board[7][5] = ChessPiece("B", "W", 7, 5)
        self.board[7][6] = ChessPiece("N", "W", 7, 6)
        self.board[7][7] = ChessPiece("R", "W", 7, 7)
        for col in range(BOARD_SIZE):
            self.board[6][col] = ChessPiece("P", "W", 6, col)

    def select_piece(self, row, col):
        if self.game_over:
            return
            
        piece = self.board[row][col]
        
        # Өөрийн өнгийн боддог дээр дарвал сонгоно
        if piece and piece.color == self.turn:
            self.selected_piece = piece
            self.valid_moves = self.get_valid_moves(piece)
        # Нүүх боломжтой нүд дээр дарвал нүүнэ
        elif self.selected_piece and (row, col) in self.valid_moves:
            self.move_piece(self.selected_piece, row, col)
        else:
            self.selected_piece = None
            self.valid_moves = []
            
    def move_piece(self, piece, target_row, target_col):
        target_piece = self.board[target_row][target_col]
        # Хэрэв Хааныг идвэл тоглоом дуусна
        if target_piece and target_piece.name == "K":
            self.game_over = True
            self.winner = "WHITE" if self.turn == "W" else "BLACK"
            
        self.board[piece.row][piece.col] = None
        piece.row = target_row
        piece.col = target_col
        piece.has_moved = True
        self.board[target_row][target_col] = piece
        
        self.selected_piece = None
        self.valid_moves = []
        self.turn = "B" if self.turn == "W" else "W"

    def make_ai_move(self):
        """Хар талын компьютерийн ухаалаг AI нүүдэл (Heuristic-based)"""
        if self.game_over or self.turn != "B":
            return
            
        all_moves = [] # [(боддог, (очих_мөр, очих_багана), нүүдлийн_оноо)]
        
        # Цагааны Хааны байрлалыг олох
        white_king_pos = None
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                p = self.board[r][c]
                if p and p.name == "K" and p.color == "W":
                    white_king_pos = (r, c)
                    break
            if white_king_pos:
                break
        
        # Хар талын бүх боломжит нүүдлийг олох
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                piece = self.board[r][c]
                if piece and piece.color == "B":
                    piece_moves = self.get_valid_moves(piece)
                    for tr, tc in piece_moves:
                        score = 0
                        target_piece = self.board[tr][tc]
                        
                        # 1. Идэх оноо (Capture score)
                        if target_piece:
                            score += PIECE_VALUES.get(target_piece.name, 0) * 10
                            
                        # 2. Нүүдлийг түр хийж аюулгүй байдлыг шалгах (Defense & Attack checks)
                        orig_row, orig_col = piece.row, piece.col
                        self.board[orig_row][orig_col] = None
                        self.board[tr][tc] = piece
                        piece.row, piece.col = tr, tc
                        
                        # Аюултай нүд рүү нүүж байгаа эсэхийг шалгах (White can capture us?)
                        is_attacked = False
                        for wr in range(BOARD_SIZE):
                            for wc in range(BOARD_SIZE):
                                w_piece = self.board[wr][wc]
                                if w_piece and w_piece.color == "W":
                                    w_moves = self.get_valid_moves(w_piece)
                                    if (tr, tc) in w_moves:
                                        is_attacked = True
                                        break
                            if is_attacked:
                                break
                                
                        if is_attacked:
                            # Өөрийн боддогийг үнэгүй алдахаас сэргийлнэ (Avoid hanging pieces)
                            score -= PIECE_VALUES.get(piece.name, 0) * 10
                            # Харин идэж авч буй боддог нь илүү үнэтэй бол ашигтай арилжаа
                            if target_piece:
                                score += PIECE_VALUES.get(target_piece.name, 0) * 2
                        
                        # Хааныг шаглах боломжийг олох (Check bonus)
                        if white_king_pos:
                            new_attack_moves = self.get_valid_moves(piece)
                            if white_king_pos in new_attack_moves:
                                score += 15 # Шаг хийх онооны урамшуулал
                                
                        # 3. Байрлалын оноо (Positional Heuristics)
                        # Төв хэсгийг хянах (rows 3,4 and cols 3,4)
                        if tr in (3, 4) and tc in (3, 4):
                            score += 2
                            
                        # Морь, Тэмээг арын эгнээнээс гаргаж хөгжүүлэх
                        if piece.name in ("N", "B") and orig_row == 0 and tr > 0:
                            score += 3
                            
                        # Хүүг урагшлуулахыг дэмжих (Хар тал доошоо нүүнэ)
                        if piece.name == "P":
                            score += tr * 0.5
                            
                        # Түр хийсэн нүүдлийг буцааж хэвийн болгох
                        self.board[orig_row][orig_col] = piece
                        self.board[tr][tc] = target_piece
                        piece.row, piece.col = orig_row, orig_col
                        
                        all_moves.append((piece, (tr, tc), score))
                        
        if not all_moves:
            # Боломжит нүүдэл байхгүй бол ялагдлыг тооцно
            self.game_over = True
            self.winner = "WHITE"
            return
            
        # Хамгийн их оноотой нүүдлийг олох
        max_score = max(move[2] for move in all_moves)
        
        # Хамгийн сайн нүүдлүүдийг шүүх
        best_moves = [move for move in all_moves if move[2] == max_score]
        
        # Сонгогдсон шилдэг нүүдлүүдээс санамсаргүй нэгийг нь хийнэ
        selected_move = random.choice(best_moves)
        piece, (tr, tc), score = selected_move
        
        # Нүүх үйлдлийг гүйцэтгэх
        self.move_piece(piece, tr, tc)

    def get_valid_moves(self, piece):
        moves = []
        r, c = piece.row, piece.col
        
        # --- Хүү (Pawn) ---
        if piece.name == "P":
            direction = -1 if piece.color == "W" else 1
            
            # Урагшаа 1 алхам
            next_row = r + direction
            if 0 <= next_row < BOARD_SIZE and self.board[next_row][c] is None:
                moves.append((next_row, c))
                # Анхны байрлалаас урагшаа 2 алхах боломж
                start_row = 6 if piece.color == "W" else 1
                two_steps_row = r + 2 * direction
                if r == start_row and self.board[two_steps_row][c] is None:
                    moves.append((two_steps_row, c))
                    
            # Диагонал дагуу идэх үйлдэл
            for dc in [-1, 1]:
                target_c = c + dc
                if 0 <= target_c < BOARD_SIZE:
                    target_piece = self.board[next_row][target_c]
                    if target_piece and target_piece.color != piece.color:
                        moves.append((next_row, target_c))

        # --- Тэрэг (Rook) ---
        elif piece.name == "R":
            directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
            for dr, dc in directions:
                for step in range(1, BOARD_SIZE):
                    nr, nc = r + dr * step, c + dc * step
                    if 0 <= nr < BOARD_SIZE and 0 <= nc < BOARD_SIZE:
                        target = self.board[nr][nc]
                        if target is None:
                            moves.append((nr, nc))
                        else:
                            if target.color != piece.color:
                                moves.append((nr, nc))
                            break
                    else:
                        break

        # --- Тэмээ (Bishop) ---
        elif piece.name == "B":
            directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
            for dr, dc in directions:
                for step in range(1, BOARD_SIZE):
                    nr, nc = r + dr * step, c + dc * step
                    if 0 <= nr < BOARD_SIZE and 0 <= nc < BOARD_SIZE:
                        target = self.board[nr][nc]
                        if target is None:
                            moves.append((nr, nc))
                        else:
                            if target.color != piece.color:
                                moves.append((nr, nc))
                            break
                    else:
                        break

        # --- Бэр (Queen) ---
        elif piece.name == "Q":
            directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
            for dr, dc in directions:
                for step in range(1, BOARD_SIZE):
                    nr, nc = r + dr * step, c + dc * step
                    if 0 <= nr < BOARD_SIZE and 0 <= nc < BOARD_SIZE:
                        target = self.board[nr][nc]
                        if target is None:
                            moves.append((nr, nc))
                        else:
                            if target.color != piece.color:
                                moves.append((nr, nc))
                            break
                    else:
                        break

        # --- Морь (Knight) ---
        elif piece.name == "N":
            knight_moves = [
                (-2, -1), (-2, 1), (-1, -2), (-1, 2),
                (1, -2), (1, 2), (2, -1), (2, 1)
            ]
            for dr, dc in knight_moves:
                nr, nc = r + dr, c + dc
                if 0 <= nr < BOARD_SIZE and 0 <= nc < BOARD_SIZE:
                    target = self.board[nr][nc]
                    if target is None or target.color != piece.color:
                        moves.append((nr, nc))

        # --- Хаан (King) ---
        elif piece.name == "K":
            king_moves = [
                (-1, -1), (-1, 0), (-1, 1),
                (0, -1),           (0, 1),
                (1, -1),  (1, 0),  (1, 1)
            ]
            for dr, dc in king_moves:
                nr, nc = r + dr, c + dc
                if 0 <= nr < BOARD_SIZE and 0 <= nc < BOARD_SIZE:
                    target = self.board[nr][nc]
                    if target is None or target.color != piece.color:
                        moves.append((nr, nc))
                        
        return moves

    def draw(self, screen, mouse_pos):
        # 1. Шатрын хөлөг хүрээ зурах (Board Offset)
        board_offset_x = 30
        board_offset_y = 30
        
        # Хөлөгний арын сүүдэр
        pygame.draw.rect(screen, (17, 17, 27), (board_offset_x - 6, board_offset_y - 6, BOARD_WIDTH + 12, BOARD_HEIGHT + 12), border_radius=8)
        # Хүрээ модон хавтан
        pygame.draw.rect(screen, PANEL_COLOR, (board_offset_x - 5, board_offset_y - 5, BOARD_WIDTH + 10, BOARD_HEIGHT + 10), border_radius=8)
        pygame.draw.rect(screen, GRID_COLOR, (board_offset_x - 5, board_offset_y - 5, BOARD_WIDTH + 10, BOARD_HEIGHT + 10), width=2, border_radius=8)
        
        # 2. Нүднүүдийг зурах (Draw Squares)
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                x = board_offset_x + c * SQUARE_SIZE
                y = board_offset_y + r * SQUARE_SIZE
                
                color = LIGHT_SQUARE if (r + c) % 2 == 0 else DARK_SQUARE
                pygame.draw.rect(screen, color, (x, y, SQUARE_SIZE, SQUARE_SIZE))
                
        # 3. Chess.com шиг координатуудыг нүдэн дотор нь зурах (Цайвар/Бараан солигдоно)
        font_coords = pygame.font.SysFont("Arial", 11, bold=True)
        files = ["a", "b", "c", "d", "e", "f", "g", "h"]
        ranks = ["8", "7", "6", "5", "4", "3", "2", "1"]
        
        # Босоо тэнхлэгийн тоо (左)
        for r in range(BOARD_SIZE):
            color = DARK_SQUARE if r % 2 == 0 else LIGHT_SQUARE
            rank_lbl = font_coords.render(ranks[r], True, color)
            screen.blit(rank_lbl, (board_offset_x + 5, board_offset_y + r * SQUARE_SIZE + 5))
            
        # Хэвтээ тэнхлэгийн үсэг (下)
        for c in range(BOARD_SIZE):
            color = DARK_SQUARE if c % 2 != 0 else LIGHT_SQUARE
            file_lbl = font_coords.render(files[c], True, color)
            screen.blit(file_lbl, (board_offset_x + c * SQUARE_SIZE + SQUARE_SIZE - 12, board_offset_y + 7 * SQUARE_SIZE + SQUARE_SIZE - 16))

        # 4. Сонгосон боддогийг тодруулах (Highlight selected)
        if self.selected_piece:
            sx = board_offset_x + self.selected_piece.col * SQUARE_SIZE
            sy = board_offset_y + self.selected_piece.row * SQUARE_SIZE
            
            s = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
            s.fill((247, 247, 105, 130)) # Шар тунгалаг гэрэл
            screen.blit(s, (sx, sy))
            
            # 5. Нүүж болох нүднүүдийг хагас тунгалаг тойргоор тэмдэглэх
            for row, col in self.valid_moves:
                mx = board_offset_x + col * SQUARE_SIZE + SQUARE_SIZE // 2
                my = board_offset_y + row * SQUARE_SIZE + SQUARE_SIZE // 2
                
                target = self.board[row][col]
                s = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
                if target:
                    # Идэх боломжтой дайсны боддогийг улаан цагиргаар тэмдэглэх
                    pygame.draw.circle(s, (239, 68, 68, 160), (SQUARE_SIZE//2, SQUARE_SIZE//2), SQUARE_SIZE//2 - 6, width=4)
                else:
                    # Хоосон нүдэнд саарал цэг зурах
                    pygame.draw.circle(s, (108, 112, 134, 150), (SQUARE_SIZE//2, SQUARE_SIZE//2), 9)
                screen.blit(s, (mx - SQUARE_SIZE//2, my - SQUARE_SIZE//2))
                
        # 6. Боддогуудыг Юникодоор хөлөг дээр зурах (Double shadow render)
        font_pieces = pygame.font.SysFont("Segoe UI Symbol", 44)
        
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                piece = self.board[r][c]
                if piece:
                    symbol = PIECE_SYMBOLS[piece.name]
                    # Цагаан: Цагаан бие + Хар хүрээ, Хар: Хар бие + Цагаан хүрээ
                    piece_color = (255, 255, 255) if piece.color == "W" else (30, 30, 46)
                    outline_color = (30, 30, 46) if piece.color == "W" else (255, 255, 255)
                    
                    px = board_offset_x + c * SQUARE_SIZE + SQUARE_SIZE // 2
                    py = board_offset_y + r * SQUARE_SIZE + SQUARE_SIZE // 2
                    
                    # Хүрээ гаргаж 4 тал руу нь үл ялиг зөрүүлж зурах
                    shadow = font_pieces.render(symbol, True, outline_color)
                    screen.blit(shadow, (px - shadow.get_width()//2 + 1, py - shadow.get_height()//2 + 1))
                    screen.blit(shadow, (px - shadow.get_width()//2 - 1, py - shadow.get_height()//2 - 1))
                    screen.blit(shadow, (px - shadow.get_width()//2 + 1, py - shadow.get_height()//2 - 1))
                    screen.blit(shadow, (px - shadow.get_width()//2 - 1, py - shadow.get_height()//2 + 1))
                    
                    # Үндсэн дүрсийг төвд нь зурах
                    core = font_pieces.render(symbol, True, piece_color)
                    screen.blit(core, (px - core.get_width()//2, py - core.get_height()//2 - 4))

        # 7. Баруун талын самбар (Side Control Panel)
        panel_x = 615
        panel_y = 30
        panel_w = 230
        panel_h = BOARD_HEIGHT
        
        # Сүүдэр болон суурь самбар
        pygame.draw.rect(screen, (17, 17, 27), (panel_x + 4, panel_y + 4, panel_w, panel_h), border_radius=12)
        pygame.draw.rect(screen, PANEL_COLOR, (panel_x, panel_y, panel_w, panel_h), border_radius=12)
        pygame.draw.rect(screen, GRID_COLOR, (panel_x, panel_y, panel_w, panel_h), width=2, border_radius=12)
        
        # Гарчиг
        font_title = pygame.font.SysFont("Impact", 24)
        font_info = pygame.font.SysFont("Arial", 16, bold=True)
        
        title_surf = font_title.render("CHESS ARENA", True, ACCENT_COLOR)
        screen.blit(title_surf, (panel_x + panel_w//2 - title_surf.get_width()//2, panel_y + 25))
        
        # Идэвхтэй тоглогчийн карт (Turn Status)
        box_y = panel_y + 80
        pygame.draw.rect(screen, BG_COLOR, (panel_x + 20, box_y, panel_w - 40, 50), border_radius=6)
        active_str = "WHITE TURN" if self.turn == "W" else "BLACK TURN (AI)" if self.ai_mode else "BLACK TURN"
        active_color = WHITE_COLOR if self.turn == "W" else ACCENT_COLOR
        active_surf = font_info.render(active_str, True, active_color)
        screen.blit(active_surf, (panel_x + panel_w//2 - active_surf.get_width()//2, box_y + 15))
        
        # Горим солих товчлуур (AI Mode Toggle)
        toggle_rect = pygame.Rect(panel_x + 20, panel_y + 160, panel_w - 40, 45)
        toggle_hover = toggle_rect.collidepoint(mouse_pos)
        toggle_color = (49, 50, 68) if toggle_hover else (30, 30, 46)
        pygame.draw.rect(screen, toggle_color, toggle_rect, border_radius=6)
        pygame.draw.rect(screen, ACCENT_COLOR, toggle_rect, width=1, border_radius=6)
        
        mode_lbl = "VS COMPUTER: ON" if self.ai_mode else "VS COMPUTER: OFF"
        mode_surf = font_info.render(mode_lbl, True, ACCENT_COLOR)
        screen.blit(mode_surf, (panel_x + panel_w//2 - mode_surf.get_width()//2, panel_y + 172))
        
        # Зааварчилгаа / Боддогуудын тэмдэглэгээ
        desc_y = panel_y + 230
        desc_lines = [
            "  ♟  Pawn (P)",
            "  ♜  Rook (R)",
            "  ♞  Knight (N)",
            "  ♝  Bishop (B)",
            "  ♛  Queen (Q)",
            "  ♚  King (K)",
            "",
            "Objective:",
            "Capture opponent's",
            "King to win."
        ]
        font_desc = pygame.font.SysFont("Arial", 13, bold=True)
        for idx, line in enumerate(desc_lines):
            line_surf = font_desc.render(line, True, TEXT_COLOR)
            screen.blit(line_surf, (panel_x + 25, desc_y + idx * 22))
            
        # Сонголт цуцлах заавар
        reset_surf = font_info.render("Deselect Piece: ESC", True, TEXT_MUTED)
        screen.blit(reset_surf, (panel_x + panel_w//2 - reset_surf.get_width()//2, panel_y + panel_h - 40))


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("♟️ Classic Chess — Lesson 4.8")
    
    clock = pygame.time.Clock()
    game = ChessGame()
    
    # AI нүүдэл хийхээс өмнөх саатал (ms)
    ai_delay_timer = 0
    
    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()
        
        # AI ээлж ирсэн үед тодорхой хугацааны дараа автоматаар нүүх
        if not game.game_over and game.turn == "B" and game.ai_mode:
            ai_delay_timer += clock.get_time()
            if ai_delay_timer >= 600: # 600ms саатал
                game.make_ai_move()
                ai_delay_timer = 0
        else:
            ai_delay_timer = 0
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    pos = event.pos
                    
                    # Горим солих товчлуур дарагдсан уу
                    toggle_rect = pygame.Rect(635, 190, 190, 45)
                    if toggle_rect.collidepoint(pos) and not game.game_over:
                        game.ai_mode = not game.ai_mode
                        game.selected_piece = None
                        game.valid_moves = []
                        continue
                        
                    # Хөлөг дээрх нүд дарагдсан уу
                    if not game.game_over:
                        # Хөлөг (30, 30) координатаас эхэлж байгаа
                        col = (pos[0] - 30) // SQUARE_SIZE
                        row = (pos[1] - 30) // SQUARE_SIZE
                        
                        # Хөлгийн хил дотор байгаа эсэх
                        if 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE:
                            # AI нүүх үед тоглогч удирдахаас сэргийлнэ
                            if not (game.turn == "B" and game.ai_mode):
                                game.select_piece(row, col)
                                
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # Сонголтыг цуцлах
                    game.selected_piece = None
                    game.valid_moves = []
                elif game.game_over and event.key in (pygame.K_SPACE, pygame.K_RETURN):
                    # Шинээр эхлүүлэх
                    game = ChessGame()
                    
        # --- ЗУРАГЛАЛ ХИЙХ ---
        screen.fill(BG_COLOR)
        
        # Суурь сүлжээ хээ
        for x in range(0, WIDTH, 50):
            for y in range(0, HEIGHT, 50):
                pygame.draw.circle(screen, (35, 37, 56), (x, y), 1.2)
                
        game.draw(screen, mouse_pos)
        
        # Ялалтын дэлгэц overlay
        if game.game_over:
            overlay = pygame.Surface((WIDTH, HEIGHT))
            overlay.set_alpha(200)
            overlay.fill(BG_COLOR)
            screen.blit(overlay, (0, 0))
            
            font_title = pygame.font.SysFont("Impact", 50)
            font_sub = pygame.font.SysFont("Arial", 22)
            
            winner_str = f"{game.winner} WINS! 🏆"
            title_text = font_title.render(winner_str, True, (249, 226, 175))
            sub_text = font_sub.render("Press [ENTER] to Rematch", True, TEXT_COLOR)
            
            screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 2 - 50))
            screen.blit(sub_text, (WIDTH // 2 - sub_text.get_width() // 2, HEIGHT // 2 + 20))
            
        pygame.display.flip()
        clock.tick(60)
        
    pygame.quit()


if __name__ == "__main__":
    print("""
♟️ Classic Chess тоглоом ажиллаж байна!
- Хулганаар боддог дээрээ дарж сонгоно.
- Очих боломжтой цэгүүд саарал/улаан өнгөөр тодорно. Дарж нүүнэ.
- Хажуугийн самбараас 'VS COMPUTER' горимыг асааж компьютертэй тоглох боломжтой.
- Сонголтыг цуцлах бол 'ESC' дарна.
    """)
    main()
