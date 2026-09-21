import pygame
import sys
import random
import time
import math

# --- PYGAME BAŞLATMA ---
pygame.init()
pygame.font.init()

# --- EKRAN VE RENK AYARLARI ---
WIDTH, HEIGHT = 1200, 850
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Arcade Hub Ultimate - 16 Oyunlu Dev Paket")

# Modern Neon Paleti
BG_COLOR = (10, 10, 15)
CARD_BG = (22, 24, 32)
HOVER_BG = (35, 38, 50)
NEON_BLUE = (0, 255, 255)
NEON_PINK = (255, 0, 127)
NEON_GREEN = (57, 255, 20)
NEON_ORANGE = (255, 165, 0)
NEON_YELLOW = (255, 255, 0)
NEON_PURPLE = (153, 50, 204)
WHITE = (245, 245, 250)
GRAY = (100, 105, 120)
RED = (255, 50, 50)

# Fontlar
FONT_TITLE = pygame.font.SysFont("Segoe UI", 42, bold=True)
FONT_BTN = pygame.font.SysFont("Segoe UI", 16, bold=True)
FONT_SUB = pygame.font.SysFont("Segoe UI", 12)
FONT_GAME = pygame.font.SysFont("Consolas", 30, bold=True)
FONT_BIG = pygame.font.SysFont("Consolas", 56, bold=True)

# --- BUTON SINIFI ---
class Button:
    def __init__(self, x, y, width, height, title, subtitle, target, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.title = title
        self.subtitle = subtitle
        self.target = target
        self.color = color
        self.hovered = False

    def draw(self, surface):
        bg = HOVER_BG if self.hovered else CARD_BG
        border = self.color if self.hovered else GRAY
        
        pygame.draw.rect(surface, bg, self.rect, border_radius=8)
        pygame.draw.rect(surface, border, self.rect, width=2, border_radius=8)
        
        title_surf = FONT_BTN.render(self.title, True, WHITE)
        sub_surf = FONT_SUB.render(self.subtitle, True, GRAY)
        
        surface.blit(title_surf, (self.rect.x + 10, self.rect.y + 6))
        surface.blit(sub_surf, (self.rect.x + 10, self.rect.y + 30))

    def check_hover(self, pos):
        self.hovered = self.rect.collidepoint(pos)

# --- ANA SİSTEM ---
class ArcadeHub:
    def __init__(self):
        self.state = "MENU"
        self.clock = pygame.time.Clock()
        self.running = True

        # Menü Yerleşimi (3 Sütun x 6 Satır)
        bw, bh = 340, 52
        xs = 370
        ys = 58
        ox, oy = 60, 95

        self.buttons = [
            # Sütun 1
            Button(ox + 0*xs, oy + 0*ys, bw, bh, "1. T-Rex Runner (Dino)", "1 Kişilik - SPACE ile Zıpla", "DINO", NEON_GREEN),
            Button(ox + 0*xs, oy + 1*ys, bw, bh, "2. Tic-Tac-Toe (XOX)", "2 Kişilik - Taktik Savaşı", "XOX", NEON_BLUE),
            Button(ox + 0*xs, oy + 2*ys, bw, bh, "3. Pong (Masa Tenisi)", "2 Kişilik - W/S vs Yön", "PONG", NEON_PINK),
            Button(ox + 0*xs, oy + 3*ys, bw, bh, "4. Uzay Savaşı", "1 Kişilik - Yön + SPACE", "SPACE", NEON_ORANGE),
            Button(ox + 0*xs, oy + 4*ys, bw, bh, "5. Yılan Oyunu (Snake)", "1 Kişilik - WASD / Yön", "SNAKE", NEON_GREEN),
            Button(ox + 0*xs, oy + 5*ys, bw, bh, "6. Tuğla Kırma (Arkanoid)", "1 Kişilik - Yön Tuşları", "BRICK", NEON_YELLOW),

            # Sütun 2
            Button(ox + 1*xs, oy + 0*ys, bw, bh, "7. Flappy Neon", "1 Kişilik - SPACE ile Uç", "FLAPPY", NEON_BLUE),
            Button(ox + 1*xs, oy + 1*ys, bw, bh, "8. Hedef 4 (Connect 4)", "2 Kişilik - 4'lü Birleştir", "C4", NEON_PURPLE),
            Button(ox + 1*xs, oy + 2*ys, bw, bh, "9. Refleks Testi", "1 Kişilik - Hız Testi", "REFLEX", RED),
            Button(ox + 1*xs, oy + 3*ys, bw, bh, "10. Neon Bisikletler", "2 Kişilik Kapışma!", "TRON", NEON_PINK),
            Button(ox + 1*xs, oy + 4*ys, bw, bh, "11. Mayın Tarlası", "1 Kişilik - Mantık", "MINES", NEON_ORANGE),
            Button(ox + 1*xs, oy + 5*ys, bw, bh, "12. Kutu Yakalama", "1 Kişilik - Düşenleri Topla", "CATCH", NEON_GREEN),

            # Sütun 3
            Button(ox + 2*xs, oy + 0*ys, bw, bh, "13. İp Çekme Yarışı", "2 Kişilik - Seri Basan Kazanır", "TUG", NEON_YELLOW),
            Button(ox + 2*xs, oy + 1*ys, bw, bh, "14. Bilek Güreşi", "2 Kişilik - Tork & Güç", "ARM", RED),
            Button(ox + 2*xs, oy + 2*ys, bw, bh, "15. Parmak Güreşi", "2 Kişilik - Pin / Tuş Etme", "THUMB", NEON_BLUE),
            Button(ox + 2*xs, oy + 3*ys, bw, bh, "16. ARABA YARIŞI [YENİ]", "2 Kişilik Gece Otobanı Yarışı!", "RACE", NEON_GREEN),
        ]
        self.init_all_games()

    def init_all_games(self):
        self.init_dino()
        self.init_xox()
        self.init_pong()
        self.init_space()
        self.init_snake()
        self.init_brick()
        self.init_flappy()
        self.init_c4()
        self.init_reflex()
        self.init_tron()
        self.init_mines()
        self.init_catch()
        self.init_tug()
        self.init_arm()
        self.init_thumb()
        self.init_race()

    def draw_bg_grid(self):
        for x in range(0, WIDTH, 50):
            pygame.draw.line(SCREEN, (20, 20, 30), (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, 50):
            pygame.draw.line(SCREEN, (20, 20, 30), (0, y), (WIDTH, y))

    # ================= OYUN 16: 2 KİŞİLİK ARABA YARIŞI =================
    def init_race(self):
        # P1 (Sol kulvar)
        self.r_p1_x = 280
        self.r_p1_y = HEIGHT - 130
        self.r_p1_speed = 0
        self.r_p1_dist = 0
        self.r_p1_hp = 3
        self.r_p1_nitro = 100
        self.r_p1_obs = []

        # P2 (Sağ kulvar)
        self.r_p2_x = 880
        self.r_p2_y = HEIGHT - 130
        self.r_p2_speed = 0
        self.r_p2_dist = 0
        self.r_p2_hp = 3
        self.r_p2_nitro = 100
        self.r_p2_obs = []

        self.r_target_dist = 1500 # 1500 Metre
        self.r_finish = False
        self.r_winner = None
        self.r_line_offset = 0

    def update_race(self, k):
        if self.r_finish: return

        # Yol çizgisi animasyonu
        self.r_line_offset = (self.r_line_offset + 12) % 60

        # P1 Kontrolleri (WASD + LSHIFT Nitro)
        if self.r_p1_hp > 0:
            if k[pygame.K_w]:
                boost = 1.7 if (k[pygame.K_LSHIFT] and self.r_p1_nitro > 0) else 1.0
                if k[pygame.K_LSHIFT] and self.r_p1_nitro > 0: self.r_p1_nitro -= 0.6
                self.r_p1_speed = min(220 * boost, self.r_p1_speed + 2.5)
            elif k[pygame.K_s]:
                self.r_p1_speed = max(0, self.r_p1_speed - 5)
            else:
                self.r_p1_speed = max(0, self.r_p1_speed - 1)

            if k[pygame.K_a] and self.r_p1_x > 110: self.r_p1_x -= (5 + self.r_p1_speed*0.02)
            if k[pygame.K_d] and self.r_p1_x < 470: self.r_p1_x += (5 + self.r_p1_speed*0.02)

        # P2 Kontrolleri (Yön Tuşları + RSHIFT Nitro)
        if self.r_p2_hp > 0:
            if k[pygame.K_UP]:
                boost = 1.7 if (k[pygame.K_RSHIFT] and self.r_p2_nitro > 0) else 1.0
                if k[pygame.K_RSHIFT] and self.r_p2_nitro > 0: self.r_p2_nitro -= 0.6
                self.r_p2_speed = min(220 * boost, self.r_p2_speed + 2.5)
            elif k[pygame.K_DOWN]:
                self.r_p2_speed = max(0, self.r_p2_speed - 5)
            else:
                self.r_p2_speed = max(0, self.r_p2_speed - 1)

            if k[pygame.K_LEFT] and self.r_p2_x > 710: self.r_p2_x -= (5 + self.r_p2_speed*0.02)
            if k[pygame.K_RIGHT] and self.r_p2_x < 1070: self.r_p2_x += (5 + self.r_p2_speed*0.02)

        # Mesafeleri Güncelle
        self.r_p1_dist += self.r_p1_speed * 0.04
        self.r_p2_dist += self.r_p2_speed * 0.04

        # P1 Engel Üretimi
        if self.r_p1_speed > 10 and random.random() < 0.03:
            ox = random.randint(110, 450)
            t = random.choice(['car', 'car', 'oil', 'nitro'])
            self.r_p1_obs.append({'rect': pygame.Rect(ox, -70, 42, 68 if t=='car' else 35), 'type': t})

        # P2 Engel Üretimi
        if self.r_p2_speed > 10 and random.random() < 0.03:
            ox = random.randint(710, 1050)
            t = random.choice(['car', 'car', 'oil', 'nitro'])
            self.r_p2_obs.append({'rect': pygame.Rect(ox, -70, 42, 68 if t=='car' else 35), 'type': t})

        # P1 Çarpışma Kontrolü
        p1_rect = pygame.Rect(self.r_p1_x - 20, self.r_p1_y - 32, 40, 65)
        for ob in self.r_p1_obs[:]:
            ob['rect'].y += (self.r_p1_speed * 0.07) + 2
            if ob['rect'].colliderect(p1_rect):
                if ob['type'] == 'car':
                    self.r_p1_hp -= 1; self.r_p1_speed = 20; self.r_p1_obs.remove(ob)
                elif ob['type'] == 'oil':
                    self.r_p1_speed = max(10, self.r_p1_speed - 70); self.r_p1_obs.remove(ob)
                elif ob['type'] == 'nitro':
                    self.r_p1_nitro = min(100, self.r_p1_nitro + 35); self.r_p1_obs.remove(ob)
            elif ob['rect'].y > HEIGHT:
                self.r_p1_obs.remove(ob)

        # P2 Çarpışma Kontrolü
        p2_rect = pygame.Rect(self.r_p2_x - 20, self.r_p2_y - 32, 40, 65)
        for ob in self.r_p2_obs[:]:
            ob['rect'].y += (self.r_p2_speed * 0.07) + 2
            if ob['rect'].colliderect(p2_rect):
                if ob['type'] == 'car':
                    self.r_p2_hp -= 1; self.r_p2_speed = 20; self.r_p2_obs.remove(ob)
                elif ob['type'] == 'oil':
                    self.r_p2_speed = max(10, self.r_p2_speed - 70); self.r_p2_obs.remove(ob)
                elif ob['type'] == 'nitro':
                    self.r_p2_nitro = min(100, self.r_p2_nitro + 35); self.r_p2_obs.remove(ob)
            elif ob['rect'].y > HEIGHT:
                self.r_p2_obs.remove(ob)

        # Kazanma ve Bitiş Kontrolü
        if self.r_p1_dist >= self.r_target_dist:
            self.r_finish = True; self.r_winner = "OYUNCU 1 (MAVİ) KAZANDI!"
        elif self.r_p2_dist >= self.r_target_dist:
            self.r_finish = True; self.r_winner = "OYUNCU 2 (PEMBE) KAZANDI!"
        elif self.r_p1_hp <= 0 and self.r_p2_hp <= 0:
            self.r_finish = True; self.r_winner = "İKİ OYUNCU DA KAZA YAPTI!"
        elif self.r_p1_hp <= 0:
            self.r_finish = True; self.r_winner = "OYUNCU 2 (PEMBE) KAZANDI!"
        elif self.r_p2_hp <= 0:
            self.r_finish = True; self.r_winner = "OYUNCU 1 (MAVİ) KAZANDI!"

    def draw_race(self):
        SCREEN.fill(BG_COLOR)

        # PİSTLER (P1 Sol, P2 Sağ)
        pygame.draw.rect(SCREEN, (25, 28, 36), (80, 0, 420, HEIGHT)) # P1 Yol
        pygame.draw.rect(SCREEN, (25, 28, 36), (680, 0, 420, HEIGHT)) # P2 Yol

        # Yol Çizgileri ve Kenarlıklar
        pygame.draw.rect(SCREEN, RED, (75, 0, 8, HEIGHT))
        pygame.draw.rect(SCREEN, RED, (497, 0, 8, HEIGHT))
        pygame.draw.rect(SCREEN, RED, (675, 0, 8, HEIGHT))
        pygame.draw.rect(SCREEN, RED, (1097, 0, 8, HEIGHT))

        # Kesikli Çizgiler (Şeritler)
        for y in range(-60 + int(self.r_line_offset), HEIGHT + 60, 60):
            pygame.draw.rect(SCREEN, WHITE, (285, y, 8, 35))
            pygame.draw.rect(SCREEN, WHITE, (885, y, 8, 35))

        # P1 ARAÇ VE ENGELLER
        for ob in self.r_p1_obs:
            if ob['type'] == 'car':
                pygame.draw.rect(SCREEN, RED, ob['rect'], border_radius=6)
                pygame.draw.rect(SCREEN, WHITE, (ob['rect'].x+6, ob['rect'].y+10, 30, 15), border_radius=3)
            elif ob['type'] == 'oil':
                pygame.draw.ellipse(SCREEN, (100, 80, 20), ob['rect'])
            elif ob['type'] == 'nitro':
                pygame.draw.rect(SCREEN, NEON_GREEN, ob['rect'], border_radius=4)
                SCREEN.blit(FONT_SUB.render("N2O", True, BG_COLOR), (ob['rect'].x+6, ob['rect'].y+8))

        if self.r_p1_hp > 0:
            pygame.draw.rect(SCREEN, NEON_BLUE, (self.r_p1_x - 20, self.r_p1_y - 32, 40, 65), border_radius=8)
            pygame.draw.rect(SCREEN, WHITE, (self.r_p1_x - 14, self.r_p1_y - 10, 28, 16), border_radius=4) # Ön Cam

        # P2 ARAÇ VE ENGELLER
        for ob in self.r_p2_obs:
            if ob['type'] == 'car':
                pygame.draw.rect(SCREEN, RED, ob['rect'], border_radius=6)
                pygame.draw.rect(SCREEN, WHITE, (ob['rect'].x+6, ob['rect'].y+10, 30, 15), border_radius=3)
            elif ob['type'] == 'oil':
                pygame.draw.ellipse(SCREEN, (100, 80, 20), ob['rect'])
            elif ob['type'] == 'nitro':
                pygame.draw.rect(SCREEN, NEON_GREEN, ob['rect'], border_radius=4)
                SCREEN.blit(FONT_SUB.render("N2O", True, BG_COLOR), (ob['rect'].x+6, ob['rect'].y+8))

        if self.r_p2_hp > 0:
            pygame.draw.rect(SCREEN, NEON_PINK, (self.r_p2_x - 20, self.r_p2_y - 32, 40, 65), border_radius=8)
            pygame.draw.rect(SCREEN, WHITE, (self.r_p2_x - 14, self.r_p2_y - 10, 28, 16), border_radius=4)

        # ORTA BİLGİ PANELİ
        pygame.draw.rect(SCREEN, CARD_BG, (505, 0, 168, HEIGHT))
        pygame.draw.rect(SCREEN, GRAY, (505, 0, 168, HEIGHT), width=2)

        SCREEN.blit(FONT_SUB.render("[ESC] Menü", True, GRAY), (540, 15))
        SCREEN.blit(FONT_SUB.render("P1: WASD+LSHIFT", True, NEON_BLUE), (515, 45))
        SCREEN.blit(FONT_SUB.render("P2: YÖN+RSHIFT", True, NEON_PINK), (515, 65))

        # P1 Göstergeler
        p1_speed_txt = FONT_BTN.render(f"{int(self.r_p1_speed)} KM/H", True, NEON_BLUE)
        p1_dist_txt = FONT_SUB.render(f"Mesafe: {int(self.r_p1_dist)}m", True, WHITE)
        p1_hp_txt = FONT_SUB.render(f"Can: {'❤️'*self.r_p1_hp}", True, RED)
        SCREEN.blit(p1_speed_txt, (520, 120))
        SCREEN.blit(p1_dist_txt, (520, 150))
        SCREEN.blit(p1_hp_txt, (520, 175))

        # Nitro Bar P1
        pygame.draw.rect(SCREEN, HOVER_BG, (520, 200, 138, 12), border_radius=6)
        pygame.draw.rect(SCREEN, NEON_GREEN, (520, 200, int(138 * (self.r_p1_nitro/100)), 12), border_radius=6)

        pygame.draw.line(SCREEN, GRAY, (510, 380), (665, 380), 2)

        # P2 Göstergeler
        p2_speed_txt = FONT_BTN.render(f"{int(self.r_p2_speed)} KM/H", True, NEON_PINK)
        p2_dist_txt = FONT_SUB.render(f"Mesafe: {int(self.r_p2_dist)}m", True, WHITE)
        p2_hp_txt = FONT_SUB.render(f"Can: {'❤️'*self.r_p2_hp}", True, RED)
        SCREEN.blit(p2_speed_txt, (520, 410))
        SCREEN.blit(p2_dist_txt, (520, 440))
        SCREEN.blit(p2_hp_txt, (520, 465))

        # Nitro Bar P2
        pygame.draw.rect(SCREEN, HOVER_BG, (520, 490, 138, 12), border_radius=6)
        pygame.draw.rect(SCREEN, NEON_GREEN, (520, 490, int(138 * (self.r_p2_nitro/100)), 12), border_radius=6)

        # BİTİŞ KAZANAN EKRANI
        if self.r_finish:
            rect = pygame.Rect(WIDTH//2 - 280, HEIGHT//2 - 80, 560, 160)
            pygame.draw.rect(SCREEN, CARD_BG, rect, border_radius=15)
            pygame.draw.rect(SCREEN, NEON_YELLOW, rect, width=3, border_radius=15)
            
            w_txt = FONT_GAME.render(self.r_winner, True, NEON_YELLOW)
            sub_txt = FONT_BTN.render("Tekrar Oynamak İçin R Tuşuna Basın", True, WHITE)
            SCREEN.blit(w_txt, (WIDTH//2 - w_txt.get_width()//2, HEIGHT//2 - 40))
            SCREEN.blit(sub_txt, (WIDTH//2 - sub_txt.get_width()//2, HEIGHT//2 + 20))

    # ================= OYUN 14: BİLEK GÜREŞİ =================
    def init_arm(self):
        self.arm_angle, self.arm_p1_score, self.arm_p2_score = 0, 0, 0
        self.arm_p1_presses, self.arm_p2_presses = [], []
        self.arm_p1_cps, self.arm_p2_cps = 0, 0
        self.arm_state, self.arm_cd_start, self.arm_winner, self.arm_round = "COUNTDOWN", time.time(), None, 1

    def press_arm(self, player):
        if self.arm_state != "PLAYING": return
        now = time.time()
        if player == 1:
            self.arm_p1_presses.append(now)
            self.arm_angle -= 8.5 if self.arm_p1_cps >= 7 else 5.0
        elif player == 2:
            self.arm_p2_presses.append(now)
            self.arm_angle += 8.5 if self.arm_p2_cps >= 7 else 5.0

    def update_arm(self):
        now = time.time()
        self.arm_p1_presses = [t for t in self.arm_p1_presses if now - t <= 1.0]
        self.arm_p2_presses = [t for t in self.arm_p2_presses if now - t <= 1.0]
        self.arm_p1_cps, self.arm_p2_cps = len(self.arm_p1_presses), len(self.arm_p2_presses)

        if self.arm_state == "COUNTDOWN" and now - self.arm_cd_start >= 3.0: self.arm_state = "PLAYING"
        elif self.arm_state == "PLAYING":
            if self.arm_angle > 0: self.arm_angle = max(0.0, self.arm_angle - 0.3)
            elif self.arm_angle < 0: self.arm_angle = min(0.0, self.arm_angle + 0.3)

            if self.arm_angle <= -100:
                self.arm_p1_score += 1
                if self.arm_p1_score >= 3: self.arm_state, self.arm_winner = "MATCH_WIN", "OYUNCU 1 (MAVİ)"
                else: self.arm_state, self.arm_winner, self.arm_cd_start = "ROUND_WIN", "OYUNCU 1", now
            elif self.arm_angle >= 100:
                self.arm_p2_score += 1
                if self.arm_p2_score >= 3: self.arm_state, self.arm_winner = "MATCH_WIN", "OYUNCU 2 (PEMBE)"
                else: self.arm_state, self.arm_winner, self.arm_cd_start = "ROUND_WIN", "OYUNCU 2", now
        elif self.arm_state == "ROUND_WIN" and now - self.arm_cd_start >= 2.0:
            self.arm_angle, self.arm_round, self.arm_state, self.arm_cd_start = 0, self.arm_round + 1, "COUNTDOWN", now

    def draw_arm(self):
        SCREEN.fill(BG_COLOR); self.draw_bg_grid()
        SCREEN.blit(FONT_SUB.render("[ESC] Menü | P1: 'A'/'W' | P2: 'L'/SAĞ YÖN | R: Sıfırla", True, GRAY), (20, 15))
        SCREEN.blit(FONT_GAME.render(f"P1 (MAVİ): {self.arm_p1_score}", True, NEON_BLUE), (100, 50))
        SCREEN.blit(FONT_GAME.render(f"P2 (PEMBE): {self.arm_p2_score}", True, NEON_PINK), (WIDTH - 320, 50))
        cx, cy = WIDTH // 2, HEIGHT // 2 + 80
        pygame.draw.rect(SCREEN, (50, 35, 25), (cx - 280, cy, 560, 40), border_radius=8)
        bar_w = 500; bar_x = cx - bar_w // 2; bar_y = cy - 220
        pygame.draw.rect(SCREEN, CARD_BG, (bar_x, bar_y, bar_w, 24), border_radius=12)
        ind_x = cx + (self.arm_angle / 100.0) * (bar_w // 2)
        pygame.draw.circle(SCREEN, NEON_YELLOW, (int(ind_x), bar_y + 12), 14)
        angle_rad = math.radians(self.arm_angle * 0.45)
        hand_x, hand_y = cx + 160 * math.sin(angle_rad), cy - 160 * math.cos(angle_rad)
        pygame.draw.line(SCREEN, NEON_BLUE, (cx - 120, cy), (hand_x, hand_y), 16)
        pygame.draw.line(SCREEN, NEON_PINK, (cx + 120, cy), (hand_x, hand_y), 16)
        pygame.draw.circle(SCREEN, WHITE, (int(hand_x), int(hand_y)), 20)
        if self.arm_state == "COUNTDOWN":
            rem = 3 - int(time.time() - self.arm_cd_start)
            txt = FONT_BIG.render("BAŞLA!" if rem <= 0 else str(rem), True, NEON_YELLOW)
            SCREEN.blit(txt, (cx - txt.get_width()//2, cy - 140))
        elif self.arm_state == "MATCH_WIN":
            mw_txt = FONT_BIG.render(f"ŞAMPİYON: {self.arm_winner}!", True, NEON_GREEN)
            SCREEN.blit(mw_txt, (cx - mw_txt.get_width()//2, cy - 160))

    # ================= OYUN 15: PARMAK GÜREŞİ =================
    def init_thumb(self):
        self.thumb_pos, self.thumb_p1_score, self.thumb_p2_score = 0, 0, 0
        self.thumb_p1_presses, self.thumb_p2_presses = [], []
        self.thumb_p1_cps, self.thumb_p2_cps = 0, 0
        self.thumb_state, self.thumb_pin_start, self.thumb_cd_start, self.thumb_winner, self.thumb_round = "COUNTDOWN", 0, time.time(), None, 1

    def press_thumb(self, player):
        if self.thumb_state not in ["PLAYING", "PIN_P1", "PIN_P2"]: return
        now = time.time()
        if player == 1:
            self.thumb_p1_presses.append(now)
            self.thumb_pos -= 7.0 if self.thumb_p1_cps >= 6 else 4.0
        elif player == 2:
            self.thumb_p2_presses.append(now)
            self.thumb_pos += 7.0 if self.thumb_p2_cps >= 6 else 4.0

    def update_thumb(self):
        now = time.time()
        self.thumb_p1_presses = [t for t in self.thumb_p1_presses if now - t <= 1.0]
        self.thumb_p2_presses = [t for t in self.thumb_p2_presses if now - t <= 1.0]
        self.thumb_p1_cps, self.thumb_p2_cps = len(self.thumb_p1_presses), len(self.thumb_p2_presses)

        if self.thumb_state == "COUNTDOWN" and now - self.thumb_cd_start >= 3.0: self.thumb_state = "PLAYING"
        elif self.thumb_state == "PLAYING":
            if self.thumb_pos <= -75: self.thumb_state, self.thumb_pin_start = "PIN_P1", now
            elif self.thumb_pos >= 75: self.thumb_state, self.thumb_pin_start = "PIN_P2", now
        elif self.thumb_state == "PIN_P1":
            if self.thumb_pos > -70: self.thumb_state = "PLAYING"
            elif now - self.thumb_pin_start >= 3.0:
                self.thumb_p1_score += 1
                if self.thumb_p1_score >= 3: self.thumb_state, self.thumb_winner = "MATCH_WIN", "OYUNCU 1 (MAVİ)"
                else: self.thumb_state, self.thumb_winner, self.thumb_cd_start = "ROUND_WIN", "OYUNCU 1", now
        elif self.thumb_state == "PIN_P2":
            if self.thumb_pos < 70: self.thumb_state = "PLAYING"
            elif now - self.thumb_pin_start >= 3.0:
                self.thumb_p2_score += 1
                if self.thumb_p2_score >= 3: self.thumb_state, self.thumb_winner = "MATCH_WIN", "OYUNCU 2 (PEMBE)"
                else: self.thumb_state, self.thumb_winner, self.thumb_cd_start = "ROUND_WIN", "OYUNCU 2", now
        elif self.thumb_state == "ROUND_WIN" and now - self.thumb_cd_start >= 2.0:
            self.thumb_pos, self.thumb_round, self.thumb_state, self.thumb_cd_start = 0, self.thumb_round + 1, "COUNTDOWN", now

    def draw_thumb(self):
        SCREEN.fill(BG_COLOR); self.draw_bg_grid()
        SCREEN.blit(FONT_GAME.render(f"P1 (MAVİ): {self.thumb_p1_score}", True, NEON_BLUE), (100, 50))
        SCREEN.blit(FONT_GAME.render(f"P2 (PEMBE): {self.thumb_p2_score}", True, NEON_PINK), (WIDTH - 320, 50))
        cx, cy = WIDTH // 2, HEIGHT // 2 + 50
        bar_w = 600; bar_x = cx - bar_w // 2; bar_y = cy - 200
        pygame.draw.rect(SCREEN, CARD_BG, (bar_x, bar_y, bar_w, 30), border_radius=15)
        ind_x = cx + (self.thumb_pos / 100.0) * (bar_w // 2)
        pygame.draw.circle(SCREEN, NEON_YELLOW, (int(ind_x), bar_y + 15), 16)
        p1_thumb_x = cx - 120 - (self.thumb_pos * 0.8)
        p2_thumb_x = cx + 50 - (self.thumb_pos * 0.8)
        pygame.draw.rect(SCREEN, NEON_BLUE, (p1_thumb_x, cy - 60, 70, 120), border_radius=30)
        pygame.draw.rect(SCREEN, NEON_PINK, (p2_thumb_x, cy - 60, 70, 120), border_radius=30)
        if self.thumb_state == "COUNTDOWN":
            rem = 3 - int(time.time() - self.thumb_cd_start)
            txt = FONT_BIG.render("BAŞLA!" if rem <= 0 else str(rem), True, NEON_YELLOW)
            SCREEN.blit(txt, (cx - txt.get_width()//2, cy - 130))
        elif self.thumb_state in ["PIN_P1", "PIN_P2"]:
            rem_pin = 3 - int(time.time() - self.thumb_pin_start)
            txt = FONT_BIG.render(f"TUŞ EDİLİYOR! {max(1, rem_pin)}", True, RED)
            SCREEN.blit(txt, (cx - txt.get_width()//2, cy - 140))

    # ================= OYUN 13: İP ÇEKME =================
    def init_tug(self):
        self.tug_pos, self.tug_p1_score, self.tug_p2_score = 0, 0, 0
        self.tug_p1_presses, self.tug_p2_presses = [], []
        self.tug_p1_cps, self.tug_p2_cps, self.tug_target, self.tug_round = 0, 0, 260, 1
        self.tug_state, self.tug_cd_start, self.tug_winner = "COUNTDOWN", time.time(), None

    def press_tug(self, player):
        if self.tug_state != "PLAYING": return
        now = time.time()
        if player == 1:
            self.tug_p1_presses.append(now)
            self.tug_pos -= 12 if self.tug_p1_cps >= 7 else 7
        elif player == 2:
            self.tug_p2_presses.append(now)
            self.tug_pos += 12 if self.tug_p2_cps >= 7 else 7

    def update_tug(self):
        now = time.time()
        self.tug_p1_presses = [t for t in self.tug_p1_presses if now - t <= 1.0]
        self.tug_p2_presses = [t for t in self.tug_p2_presses if now - t <= 1.0]
        self.tug_p1_cps, self.tug_p2_cps = len(self.tug_p1_presses), len(self.tug_p2_presses)

        if self.tug_state == "COUNTDOWN" and now - self.tug_cd_start >= 3.0: self.tug_state = "PLAYING"
        elif self.tug_state == "PLAYING":
            if self.tug_pos > 0: self.tug_pos = max(0, self.tug_pos - 0.5)
            elif self.tug_pos < 0: self.tug_pos = min(0, self.tug_pos + 0.5)

            if self.tug_pos <= -self.tug_target:
                self.tug_p1_score += 1
                if self.tug_p1_score >= 3: self.tug_state, self.tug_winner = "MATCH_WIN", "OYUNCU 1 (MAVİ)"
                else: self.tug_state, self.tug_winner, self.tug_cd_start = "ROUND_WIN", "OYUNCU 1", now
            elif self.tug_pos >= self.tug_target:
                self.tug_p2_score += 1
                if self.tug_p2_score >= 3: self.tug_state, self.tug_winner = "MATCH_WIN", "OYUNCU 2 (PEMBE)"
                else: self.tug_state, self.tug_winner, self.tug_cd_start = "ROUND_WIN", "OYUNCU 2", now
        elif self.tug_state == "ROUND_WIN" and now - self.tug_cd_start >= 2.0:
            self.tug_pos, self.tug_round, self.tug_state, self.tug_cd_start = 0, self.tug_round + 1, "COUNTDOWN", now

    def draw_tug(self):
        SCREEN.fill(BG_COLOR); self.draw_bg_grid()
        SCREEN.blit(FONT_GAME.render(f"P1 (MAVİ): {self.tug_p1_score}", True, NEON_BLUE), (100, 50))
        SCREEN.blit(FONT_GAME.render(f"P2 (PEMBE): {self.tug_p2_score}", True, NEON_PINK), (WIDTH - 320, 50))
        cx, rope_y = WIDTH // 2, HEIGHT // 2 + 50
        pygame.draw.line(SCREEN, (180, 140, 90), (150, rope_y), (WIDTH - 150, rope_y), 12)
        ribbon_x = cx + self.tug_pos
        pygame.draw.circle(SCREEN, RED, (int(ribbon_x), rope_y), 16)
        if self.tug_state == "COUNTDOWN":
            rem = 3 - int(time.time() - self.tug_cd_start)
            txt = FONT_BIG.render("BAŞLA!" if rem <= 0 else str(rem), True, NEON_YELLOW)
            SCREEN.blit(txt, (cx - txt.get_width()//2, 180))

    # ================= OYUN 1: DINO =================
    def init_dino(self):
        self.d_y, self.d_vy, self.d_gravity, self.d_is_jumping = HEIGHT - 150, 0, 0.8, False
        self.d_rect = pygame.Rect(100, self.d_y, 40, 50)
        self.d_obstacles, self.d_score, self.d_speed, self.d_over = [], 0, 8, False

    def update_dino(self):
        if self.d_over: return
        self.d_vy += self.d_gravity; self.d_rect.y += self.d_vy
        if self.d_rect.y >= HEIGHT - 150: self.d_rect.y, self.d_is_jumping, self.d_vy = HEIGHT - 150, False, 0
        if random.randint(1, max(40, 100 - int(self.d_score))) == 1:
            if not self.d_obstacles or self.d_obstacles[-1].x < WIDTH - 300:
                self.d_obstacles.append(pygame.Rect(WIDTH, HEIGHT - 100 - random.randint(30, 70), random.randint(20, 40), 40))
        for ob in self.d_obstacles[:]:
            ob.x -= self.d_speed
            if ob.colliderect(self.d_rect): self.d_over = True
            if ob.right < 0: self.d_obstacles.remove(ob)
        self.d_score += 0.1; self.d_speed = 8 + (self.d_score / 100)

    def draw_dino(self):
        SCREEN.fill(BG_COLOR)
        pygame.draw.line(SCREEN, NEON_GREEN, (0, HEIGHT - 100), (WIDTH, HEIGHT - 100), 4)
        pygame.draw.rect(SCREEN, NEON_BLUE, self.d_rect, border_radius=8)
        for ob in self.d_obstacles: pygame.draw.rect(SCREEN, RED, ob, border_radius=4)
        if self.d_over: SCREEN.blit(FONT_TITLE.render("YANDIN! (R ile Tekrar)", True, RED), (WIDTH//2 - 200, HEIGHT//2 - 50))

    # ================= OYUN 2: XOX =================
    def init_xox(self): self.xox_board, self.xox_turn, self.xox_winner = [[""]*3 for _ in range(3)], "X", None
    def draw_xox(self):
        SCREEN.fill(BG_COLOR); self.draw_bg_grid()
        bs, sx, sy = 450, (WIDTH-450)//2, (HEIGHT-450)//2; cs = 150
        for i in range(1, 3):
            pygame.draw.line(SCREEN, GRAY, (sx + i*cs, sy), (sx + i*cs, sy + bs), 4)
            pygame.draw.line(SCREEN, GRAY, (sx, sy + i*cs), (sx + bs, sy + i*cs), 4)
        for r in range(3):
            for c in range(3):
                v = self.xox_board[r][c]
                if v: SCREEN.blit(FONT_BIG.render(v, True, NEON_BLUE if v=="X" else NEON_PINK), (sx + c*cs + 50, sy + r*cs + 30))

    def click_xox(self, pos):
        if self.xox_winner: self.init_xox(); return
        sx, sy, cs = (WIDTH - 450) // 2, (HEIGHT - 450) // 2, 150
        x, y = pos
        if sx <= x <= sx + 450 and sy <= y <= sy + 450:
            c, r = (x - sx) // cs, (y - sy) // cs
            if not self.xox_board[r][c]:
                self.xox_board[r][c] = self.xox_turn
                b, t = self.xox_board, self.xox_turn
                win = any(b[i][0]==b[i][1]==b[i][2]==t or b[0][i]==b[1][i]==b[2][i]==t for i in range(3)) or b[0][0]==b[1][1]==b[2][2]==t or b[0][2]==b[1][1]==b[2][0]==t
                if win: self.xox_winner = t
                elif all(b[i][j] for i in range(3) for j in range(3)): self.xox_winner = "Berabere"
                else: self.xox_turn = "O" if t == "X" else "X"

    # ================= OYUN 3: PONG =================
    def init_pong(self):
        self.p1, self.p2 = pygame.Rect(40, HEIGHT//2 - 60, 15, 120), pygame.Rect(WIDTH - 55, HEIGHT//2 - 60, 15, 120)
        self.ball = pygame.Rect(WIDTH//2 - 10, HEIGHT//2 - 10, 20, 20)
        self.bx, self.by, self.s1, self.s2 = 7*random.choice((1,-1)), 7*random.choice((1,-1)), 0, 0

    def update_pong(self, k):
        if k[pygame.K_w] and self.p1.top > 0: self.p1.y -= 8
        if k[pygame.K_s] and self.p1.bottom < HEIGHT: self.p1.y += 8
        if k[pygame.K_UP] and self.p2.top > 0: self.p2.y -= 8
        if k[pygame.K_DOWN] and self.p2.bottom < HEIGHT: self.p2.y += 8
        self.ball.x += self.bx; self.ball.y += self.by
        if self.ball.top <= 0 or self.ball.bottom >= HEIGHT: self.by *= -1
        if self.ball.colliderect(self.p1) or self.ball.colliderect(self.p2): self.bx *= -1.05
        if self.ball.left < 0: self.s2 += 1; self.ball.center=(WIDTH//2,HEIGHT//2); self.bx=7
        if self.ball.right > WIDTH: self.s1 += 1; self.ball.center=(WIDTH//2,HEIGHT//2); self.bx=-7

    def draw_pong(self):
        SCREEN.fill(BG_COLOR); pygame.draw.aaline(SCREEN, GRAY, (WIDTH//2, 0), (WIDTH//2, HEIGHT))
        pygame.draw.rect(SCREEN, NEON_BLUE, self.p1, border_radius=5)
        pygame.draw.rect(SCREEN, NEON_PINK, self.p2, border_radius=5)
        pygame.draw.ellipse(SCREEN, WHITE, self.ball)

    # ================= OYUN 4: UZAY SAVAŞI =================
    def init_space(self): self.sp_ship, self.sp_bul, self.sp_en, self.sp_score, self.sp_hp = pygame.Rect(WIDTH//2 - 25, HEIGHT - 80, 50, 40), [], [], 0, 3
    def update_space(self, k):
        if self.sp_hp <= 0: return
        if k[pygame.K_LEFT] and self.sp_ship.left > 0: self.sp_ship.x -= 10
        if k[pygame.K_RIGHT] and self.sp_ship.right < WIDTH: self.sp_ship.x += 10
        for b in self.sp_bul[:]:
            b.y -= 15
            if b.bottom < 0: self.sp_bul.remove(b)
        if random.random() < 0.05: self.sp_en.append(pygame.Rect(random.randint(0, WIDTH-40), -40, 40, 40))
        for e in self.sp_en[:]:
            e.y += 6
            if e.colliderect(self.sp_ship): self.sp_hp -= 1; self.sp_en.remove(e)
            elif e.top > HEIGHT: self.sp_en.remove(e)
            else:
                for b in self.sp_bul[:]:
                    if b.colliderect(e):
                        if b in self.sp_bul: self.sp_bul.remove(b)
                        if e in self.sp_en: self.sp_en.remove(e)
                        self.sp_score += 10

    def draw_space(self):
        SCREEN.fill(BG_COLOR); self.draw_bg_grid()
        if self.sp_hp > 0:
            pygame.draw.polygon(SCREEN, NEON_ORANGE, [(self.sp_ship.centerx, self.sp_ship.top), (self.sp_ship.left, self.sp_ship.bottom), (self.sp_ship.right, self.sp_ship.bottom)])
            for b in self.sp_bul: pygame.draw.rect(SCREEN, NEON_BLUE, b)
            for e in self.sp_en: pygame.draw.rect(SCREEN, RED, e, border_radius=5)
        else: SCREEN.blit(FONT_TITLE.render("OYUN BİTTİ (R ile Tekrar)", True, RED), (WIDTH//2 - 200, HEIGHT//2))

    # ================= OYUN 5: SNAKE =================
    def init_snake(self): self.snk_b, self.snk_d, self.snk_f, self.snk_sc, self.snk_over, self.snk_t = [(WIDTH//2, HEIGHT//2)], (20, 0), (random.randrange(40, WIDTH-40, 20), random.randrange(40, HEIGHT-40, 20)), 0, False, time.time()
    def update_snake(self):
        if self.snk_over or time.time() - self.snk_t < 0.08: return
        head = (self.snk_b[0][0] + self.snk_d[0], self.snk_b[0][1] + self.snk_d[1])
        if head in self.snk_b or head[0]<0 or head[0]>=WIDTH or head[1]<0 or head[1]>=HEIGHT: self.snk_over = True; return
        self.snk_b.insert(0, head)
        if pygame.Rect(head[0], head[1], 20, 20).colliderect(pygame.Rect(self.snk_f[0], self.snk_f[1], 20, 20)):
            self.snk_sc += 10; self.snk_f = (random.randrange(40, WIDTH-40, 20), random.randrange(40, HEIGHT-40, 20))
        else: self.snk_b.pop()
        self.snk_t = time.time()

    def draw_snake(self):
        SCREEN.fill(BG_COLOR)
        pygame.draw.rect(SCREEN, RED, (*self.snk_f, 20, 20), border_radius=4)
        for i, (x, y) in enumerate(self.snk_b): pygame.draw.rect(SCREEN, NEON_GREEN if i==0 else (0,150,0), (x, y, 20, 20), border_radius=2)
        if self.snk_over: SCREEN.blit(FONT_TITLE.render("YANDIN (R ile Tekrar)", True, RED), (WIDTH//2-200, HEIGHT//2))

    # ================= OYUN 6: TUĞLA KIRMA =================
    def init_brick(self):
        self.br_pad, self.br_ball, self.br_bx, self.br_by, self.br_bricks, self.br_over = pygame.Rect(WIDTH//2 - 60, HEIGHT - 50, 120, 15), pygame.Rect(WIDTH//2 - 8, HEIGHT - 80, 16, 16), 6, -6, [], False
        for r in range(6):
            for c in range(12): self.br_bricks.append(pygame.Rect(c*90 + 60, r*35 + 80, 80, 25))

    def update_brick(self, k):
        if self.br_over: return
        if k[pygame.K_LEFT] and self.br_pad.left > 0: self.br_pad.x -= 10
        if k[pygame.K_RIGHT] and self.br_pad.right < WIDTH: self.br_pad.x += 10
        self.br_ball.x += self.br_bx; self.br_ball.y += self.br_by
        if self.br_ball.left <= 0 or self.br_ball.right >= WIDTH: self.br_bx *= -1
        if self.br_ball.top <= 0: self.br_by *= -1
        if self.br_ball.bottom >= HEIGHT: self.br_over = True
        if self.br_ball.colliderect(self.br_pad): self.br_by = -abs(self.br_by); self.br_bx = (self.br_ball.centerx - self.br_pad.centerx) * 0.15
        for b in self.br_bricks[:]:
            if self.br_ball.colliderect(b): self.br_by *= -1; self.br_bricks.remove(b); break

    def draw_brick(self):
        SCREEN.fill(BG_COLOR)
        pygame.draw.rect(SCREEN, NEON_BLUE, self.br_pad, border_radius=5)
        pygame.draw.ellipse(SCREEN, WHITE, self.br_ball)
        colors = [RED, NEON_ORANGE, NEON_YELLOW, NEON_GREEN, NEON_BLUE, NEON_PINK]
        for b in self.br_bricks: pygame.draw.rect(SCREEN, colors[(b.y-80)//35 % 6], b, border_radius=4)
        if self.br_over: SCREEN.blit(FONT_TITLE.render("DÜŞÜRDÜN (R ile Tekrar)", True, RED), (WIDTH//2-250, HEIGHT//2))

    # ================= OYUN 7: FLAPPY NEON =================
    def init_flappy(self): self.fl_y, self.fl_vy, self.fl_pipes, self.fl_sc, self.fl_over = HEIGHT//2, 0, [], 0, False
    def update_flappy(self):
        if self.fl_over: return
        self.fl_vy += 0.5; self.fl_y += self.fl_vy
        rect = pygame.Rect(200, self.fl_y, 30, 30)
        if random.random() < 0.015:
            gap_y = random.randint(150, HEIGHT - 250)
            self.fl_pipes.append(pygame.Rect(WIDTH, 0, 60, gap_y))
            self.fl_pipes.append(pygame.Rect(WIDTH, gap_y + 180, 60, HEIGHT))
        for p in self.fl_pipes[:]:
            p.x -= 4
            if p.colliderect(rect): self.fl_over = True
            if p.right < 0: self.fl_pipes.remove(p); self.fl_sc += 0.5
        if self.fl_y > HEIGHT or self.fl_y < 0: self.fl_over = True

    def draw_flappy(self):
        SCREEN.fill(BG_COLOR); self.draw_bg_grid()
        pygame.draw.rect(SCREEN, NEON_PINK, (200, self.fl_y, 30, 30), border_radius=8)
        for p in self.fl_pipes: pygame.draw.rect(SCREEN, NEON_GREEN, p, border_radius=4)
        if self.fl_over: SCREEN.blit(FONT_TITLE.render("ÇAKILDIN (R ile Tekrar)", True, RED), (WIDTH//2-200, HEIGHT//2))

    # ================= OYUN 8: HEDEF 4 =================
    def init_c4(self): self.c4_b, self.c4_t, self.c4_win = [[0]*7 for _ in range(6)], 1, 0
    def draw_c4(self):
        SCREEN.fill(BG_COLOR)
        ox, oy = WIDTH//2 - 350, HEIGHT//2 - 300
        pygame.draw.rect(SCREEN, (30,40,80), (ox-10, oy-10, 720, 620), border_radius=15)
        for r in range(6):
            for c in range(7):
                v = self.c4_b[r][c]
                col = BG_COLOR if v==0 else (RED if v==1 else NEON_YELLOW)
                pygame.draw.circle(SCREEN, col, (ox + c*100 + 50, oy + r*100 + 50), 40)

    def click_c4(self, pos):
        if self.c4_win: self.init_c4(); return
        ox = WIDTH//2 - 350
        if ox <= pos[0] <= ox+700:
            c = int((pos[0] - ox) // 100)
            for r in range(5, -1, -1):
                if self.c4_b[r][c] == 0: self.c4_b[r][c] = self.c4_t; self.c4_t = 2 if self.c4_t == 1 else 1; break

    # ================= OYUN 9: REFLEKS TESTİ =================
    def init_reflex(self): self.ref_state, self.ref_start, self.ref_score, self.ref_target = "WAIT", 0, 0, time.time() + random.uniform(1.5, 4.0)
    def draw_reflex(self):
        SCREEN.fill(BG_COLOR)
        rect = pygame.Rect(WIDTH//2-250, HEIGHT//2-100, 500, 200)
        if self.ref_state == "WAIT":
            if time.time() >= self.ref_target: self.ref_state, self.ref_start = "CLICK", time.time()
            pygame.draw.rect(SCREEN, RED, rect, border_radius=20)
            t = FONT_BTN.render("BEKLE... YEŞİL OLUNCA TIKLA!", True, WHITE)
        elif self.ref_state == "CLICK":
            pygame.draw.rect(SCREEN, NEON_GREEN, rect, border_radius=20)
            t = FONT_BTN.render("ŞİMDİ TIKLA!", True, BG_COLOR)
        else:
            pygame.draw.rect(SCREEN, CARD_BG, rect, border_radius=20)
            t = FONT_BTN.render(f"Sonuç: {self.ref_score} ms", True, NEON_BLUE)
        SCREEN.blit(t, (rect.centerx - t.get_width()//2, rect.centery - t.get_height()//2))

    def click_reflex(self):
        if self.ref_state == "CLICK": self.ref_score, self.ref_state = int((time.time()-self.ref_start)*1000), "DONE"
        elif self.ref_state == "WAIT": self.ref_score, self.ref_state = "Çok Erken!", "DONE"
        else: self.init_reflex()

    # ================= OYUN 10: TRON =================
    def init_tron(self): self.tr1_p, self.tr2_p, self.tr1_d, self.tr2_d, self.tr1_t, self.tr2_t, self.tr_over = [200, HEIGHT//2], [WIDTH-200, HEIGHT//2], (5, 0), (-5, 0), [], [], False
    def update_tron(self, k):
        if self.tr_over: return
        if k[pygame.K_w] and self.tr1_d!=(0,5): self.tr1_d=(0,-5)
        if k[pygame.K_s] and self.tr1_d!=(0,-5): self.tr1_d=(0,5)
        if k[pygame.K_a] and self.tr1_d!=(5,0): self.tr1_d=(-5,0)
        if k[pygame.K_d] and self.tr1_d!=(-5,0): self.tr1_d=(5,0)
        if k[pygame.K_UP] and self.tr2_d!=(0,5): self.tr2_d=(0,-5)
        if k[pygame.K_DOWN] and self.tr2_d!=(0,-5): self.tr2_d=(0,5)
        if k[pygame.K_LEFT] and self.tr2_d!=(5,0): self.tr2_d=(-5,0)
        if k[pygame.K_RIGHT] and self.tr2_d!=(-5,0): self.tr2_d=(5,0)

        self.tr1_t.append(tuple(self.tr1_p)); self.tr2_t.append(tuple(self.tr2_p))
        self.tr1_p[0]+=self.tr1_d[0]; self.tr1_p[1]+=self.tr1_d[1]
        self.tr2_p[0]+=self.tr2_d[0]; self.tr2_p[1]+=self.tr2_d[1]
        c1 = self.tr1_p[0]<0 or self.tr1_p[0]>WIDTH or self.tr1_p[1]<0 or self.tr1_p[1]>HEIGHT
        c2 = self.tr2_p[0]<0 or self.tr2_p[0]>WIDTH or self.tr2_p[1]<0 or self.tr2_p[1]>HEIGHT
        for t in self.tr1_t+self.tr2_t:
            if tuple(self.tr1_p)==t: c1=True
            if tuple(self.tr2_p)==t: c2=True
        if c1 or c2: self.tr_over = True

    def draw_tron(self):
        SCREEN.fill(BG_COLOR)
        for x,y in self.tr1_t: pygame.draw.rect(SCREEN, NEON_BLUE, (x,y,5,5))
        for x,y in self.tr2_t: pygame.draw.rect(SCREEN, NEON_PINK, (x,y,5,5))
        if self.tr_over: SCREEN.blit(FONT_TITLE.render("ÇARPIŞMA! (R ile Tekrar)", True, WHITE), (WIDTH//2-250, HEIGHT//2))

    # ================= OYUN 11: MAYIN TARLASI =================
    def init_mines(self):
        self.m_w, self.m_h, self.m_cs = 12, 10, 45
        self.m_ox, self.m_oy = (WIDTH - self.m_w*self.m_cs)//2, (HEIGHT - self.m_h*self.m_cs)//2
        self.m_b, self.m_r, self.m_f, self.m_over = [[0]*self.m_w for _ in range(self.m_h)], [[False]*self.m_w for _ in range(self.m_h)], [[False]*self.m_w for _ in range(self.m_h)], False
        p = 0
        while p < 15:
            r, c = random.randint(0,self.m_h-1), random.randint(0,self.m_w-1)
            if self.m_b[r][c] != -1: self.m_b[r][c] = -1; p += 1
        for r in range(self.m_h):
            for c in range(self.m_w):
                if self.m_b[r][c] == -1: continue
                self.m_b[r][c] = sum(1 for dr in [-1,0,1] for dc in [-1,0,1] if 0<=r+dr<self.m_h and 0<=c+dc<self.m_w and self.m_b[r+dr][c+dc]==-1)

    def draw_mines(self):
        SCREEN.fill(BG_COLOR)
        for r in range(self.m_h):
            for c in range(self.m_w):
                rect = pygame.Rect(self.m_ox+c*self.m_cs, self.m_oy+r*self.m_cs, self.m_cs-2, self.m_cs-2)
                if self.m_r[r][c]:
                    pygame.draw.rect(SCREEN, CARD_BG, rect)
                    if self.m_b[r][c]==-1: pygame.draw.circle(SCREEN, RED, rect.center, 10)
                    elif self.m_b[r][c]>0: SCREEN.blit(FONT_BTN.render(str(self.m_b[r][c]), True, NEON_BLUE), (rect.centerx-5, rect.centery-10))
                else:
                    pygame.draw.rect(SCREEN, HOVER_BG, rect)
                    if self.m_f[r][c]: pygame.draw.circle(SCREEN, NEON_ORANGE, rect.center, 8)
        if self.m_over: SCREEN.blit(FONT_TITLE.render("PATLADIN!", True, RED), (WIDTH//2-100, HEIGHT-100))

    def click_mines(self, pos, btn):
        if self.m_over: self.init_mines(); return
        c, r = (pos[0]-self.m_ox)//self.m_cs, (pos[1]-self.m_oy)//self.m_cs
        if 0<=r<self.m_h and 0<=c<self.m_w:
            if btn==3 and not self.m_r[r][c]: self.m_f[r][c] = not self.m_f[r][c]
            elif btn==1 and not self.m_f[r][c]: 
                self.m_r[r][c] = True
                if self.m_b[r][c]==-1: self.m_over = True

    # ================= OYUN 12: KUTU YAKALAMA =================
    def init_catch(self): self.ct_pad, self.ct_items, self.ct_sc, self.ct_hp = pygame.Rect(WIDTH//2-50, HEIGHT-40, 100, 20), [], 0, 3
    def update_catch(self, k):
        if self.ct_hp <= 0: return
        if k[pygame.K_LEFT] and self.ct_pad.left > 0: self.ct_pad.x -= 12
        if k[pygame.K_RIGHT] and self.ct_pad.right < WIDTH: self.ct_pad.x += 12
        if random.random() < 0.04: self.ct_items.append(pygame.Rect(random.randint(0,WIDTH-30), -30, 30, 30))
        for i in self.ct_items[:]:
            i.y += 7
            if i.colliderect(self.ct_pad): self.ct_sc += 1; self.ct_items.remove(i)
            elif i.top > HEIGHT: self.ct_hp -= 1; self.ct_items.remove(i)

    def draw_catch(self):
        SCREEN.fill(BG_COLOR)
        pygame.draw.rect(SCREEN, NEON_GREEN, self.ct_pad, border_radius=10)
        for i in self.ct_items: pygame.draw.rect(SCREEN, NEON_PINK, i, border_radius=5)
        if self.ct_hp<=0: SCREEN.blit(FONT_TITLE.render("BİTTİ! (R)", True, RED), (WIDTH//2-100, HEIGHT//2))

    # --- ANA DÖNGÜ ---
    def run(self):
        while self.running:
            keys = pygame.key.get_pressed()
            mouse_pos = pygame.mouse.get_pos()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT: self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE: self.state = "MENU"
                    # Reset tuşları (R)
                    if event.key == pygame.K_r:
                        if self.state=="SPACE": self.init_space()
                        if self.state=="SNAKE": self.init_snake()
                        if self.state=="BRICK": self.init_brick()
                        if self.state=="FLAPPY": self.init_flappy()
                        if self.state=="TRON": self.init_tron()
                        if self.state=="CATCH": self.init_catch()
                        if self.state=="DINO": self.init_dino()
                        if self.state=="TUG": self.init_tug()
                        if self.state=="ARM": self.init_arm()
                        if self.state=="THUMB": self.init_thumb()
                        if self.state=="RACE": self.init_race()

                    # Tuş Basmalı Oyunlar
                    if self.state == "TUG":
                        if event.key in [pygame.K_a, pygame.K_w]: self.press_tug(1)
                        if event.key in [pygame.K_l, pygame.K_RIGHT, pygame.K_UP]: self.press_tug(2)

                    if self.state == "ARM":
                        if event.key in [pygame.K_a, pygame.K_w]: self.press_arm(1)
                        if event.key in [pygame.K_l, pygame.K_RIGHT, pygame.K_UP]: self.press_arm(2)

                    if self.state == "THUMB":
                        if event.key in [pygame.K_a, pygame.K_w]: self.press_thumb(1)
                        if event.key in [pygame.K_l, pygame.K_RIGHT, pygame.K_UP]: self.press_thumb(2)

                    # Diğer Oyun Tuşları
                    if self.state=="DINO" and event.key==pygame.K_SPACE and not self.d_is_jumping and not self.d_over:
                        self.d_vy = -16; self.d_is_jumping = True
                    if self.state=="SPACE" and event.key==pygame.K_SPACE and self.sp_hp>0:
                        self.sp_bul.append(pygame.Rect(self.sp_ship.centerx-3, self.sp_ship.top, 6, 15))
                    if self.state=="FLAPPY" and event.key==pygame.K_SPACE and not self.fl_over:
                        self.fl_vy = -8
                    if self.state=="SNAKE" and not self.snk_over:
                        if event.key in [pygame.K_UP,pygame.K_w] and self.snk_d!=(0,20): self.snk_d=(0,-20)
                        if event.key in [pygame.K_DOWN,pygame.K_s] and self.snk_d!=(0,-20): self.snk_d=(0,20)
                        if event.key in [pygame.K_LEFT,pygame.K_a] and self.snk_d!=(20,0): self.snk_d=(-20,0)
                        if event.key in [pygame.K_RIGHT,pygame.K_d] and self.snk_d!=(-20,0): self.snk_d=(20,0)

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.state == "MENU" and event.button == 1:
                        for btn in self.buttons:
                            if btn.hovered: self.state = btn.target; self.init_all_games()
                    elif self.state == "XOX" and event.button == 1: self.click_xox(mouse_pos)
                    elif self.state == "C4" and event.button == 1: self.click_c4(mouse_pos)
                    elif self.state == "REFLEX" and event.button == 1: self.click_reflex()
                    elif self.state == "MINES": self.click_mines(mouse_pos, event.button)

            # Ekran Çizimleri
            if self.state == "MENU":
                SCREEN.fill(BG_COLOR)
                self.draw_bg_grid()
                t = FONT_TITLE.render("ARCADE HUB ULTIMATE (16 OYUN)", True, WHITE)
                SCREEN.blit(t, (WIDTH//2 - t.get_width()//2, 25))
                for btn in self.buttons:
                    btn.check_hover(mouse_pos); btn.draw(SCREEN)
            elif self.state == "DINO": self.update_dino(); self.draw_dino()
            elif self.state == "XOX": self.draw_xox()
            elif self.state == "PONG": self.update_pong(keys); self.draw_pong()
            elif self.state == "SPACE": self.update_space(keys); self.draw_space()
            elif self.state == "SNAKE": self.update_snake(); self.draw_snake()
            elif self.state == "BRICK": self.update_brick(keys); self.draw_brick()
            elif self.state == "FLAPPY": self.update_flappy(); self.draw_flappy()
            elif self.state == "C4": self.draw_c4()
            elif self.state == "REFLEX": self.draw_reflex()
            elif self.state == "TRON": self.update_tron(keys); self.draw_tron()
            elif self.state == "MINES": self.draw_mines()
            elif self.state == "CATCH": self.update_catch(keys); self.draw_catch()
            elif self.state == "TUG": self.update_tug(); self.draw_tug()
            elif self.state == "ARM": self.update_arm(); self.draw_arm()
            elif self.state == "THUMB": self.update_thumb(); self.draw_thumb()
            elif self.state == "RACE": self.update_race(keys); self.draw_race()

            pygame.display.flip()
            self.clock.tick(60)
        pygame.quit(); sys.exit()

if __name__ == "__main__": ArcadeHub().run()