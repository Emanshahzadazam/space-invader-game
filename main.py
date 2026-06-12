import pygame
import random
import os
import math

pygame.init()

# ---------------- SCREEN ----------------
WIDTH, HEIGHT = 600, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invader - By Eman Shahzad")

# ---------------- COLORS ----------------
WHITE = (255, 255, 255)
BLACK = (5, 5, 15)
BLUE = (70, 180, 255)
CYAN = (100, 230, 255)
RED = (255, 70, 70)
ORANGE = (255, 150, 50)
YELLOW = (255, 255, 100)
GREEN = (80, 255, 120)
PURPLE = (200, 100, 255)
DARK_BLUE = (10, 15, 40)
MID_BLUE = (25, 35, 80)
SOFT_GRAY = (190, 190, 210)

font = pygame.font.SysFont("Consolas", 22, bold=True)
big_font = pygame.font.SysFont("Consolas", 56, bold=True)
small_font = pygame.font.SysFont("Consolas", 16)
clock = pygame.time.Clock()

HIGH_SCORE_FILE = "highscore.txt"


def load_high_score():
    if os.path.exists(HIGH_SCORE_FILE):
        try:
            with open(HIGH_SCORE_FILE, "r") as f:
                return int(f.read())
        except:
            return 0
    return 0


def save_high_score(score):
    with open(HIGH_SCORE_FILE, "w") as f:
        f.write(str(score))


# ---------------- BACKGROUND GRADIENT ----------------
def draw_gradient_background():
    for y in range(HEIGHT):
        blend = y / HEIGHT
        r = int(DARK_BLUE[0] * (1 - blend) + MID_BLUE[0] * blend)
        g = int(DARK_BLUE[1] * (1 - blend) + MID_BLUE[1] * blend)
        b = int(DARK_BLUE[2] * (1 - blend) + MID_BLUE[2] * blend)
        pygame.draw.line(screen, (r, g, b), (0, y), (WIDTH, y))


# ---------------- STARFIELD ----------------
class Starfield:
    def __init__(self, n=80):
        self.stars = []
        for _ in range(n):
            self.stars.append([
                random.randint(0, WIDTH),
                random.randint(0, HEIGHT),
                random.uniform(0.3, 2.5)
            ])

    def update_and_draw(self, surf):
        for s in self.stars:
            s[1] += s[2]
            if s[1] > HEIGHT:
                s[1] = 0
                s[0] = random.randint(0, WIDTH)
            c = int(80 + s[2] * 70)
            pygame.draw.circle(surf, (c, c, min(255, c + 40)),
                               (int(s[0]), int(s[1])), max(1, int(s[2])))


# ---------------- PARTICLES ----------------
class Particle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        angle = random.uniform(0, math.tau)
        speed = random.uniform(1, 5)
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed
        self.life = random.randint(20, 40)
        self.max_life = self.life
        self.color = color
        self.size = random.randint(2, 4)

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.08
        self.life -= 1

    def draw(self, surf):
        if self.life > 0:
            alpha = self.life / self.max_life
            c = tuple(max(0, min(255, int(v * alpha))) for v in self.color)
            pygame.draw.circle(surf, c, (int(self.x), int(self.y)),
                               max(1, int(self.size * alpha)))


# ---------------- DRAW HELPERS ----------------
def draw_glow_text(text, font_obj, color, x, y):
    glow = font_obj.render(text, True, color)
    glow_surface = pygame.Surface((glow.get_width() + 10, glow.get_height() + 10), pygame.SRCALPHA)
    for dx in range(5):
        for dy in range(5):
            glow_surface.blit(glow, (dx, dy))
    glow_surface.set_alpha(40)
    screen.blit(glow_surface, (x - 5, y - 5))
    main = font_obj.render(text, True, color)
    screen.blit(main, (x, y))


def draw_panel(x, y, w, h, border_color=CYAN):
    panel = pygame.Surface((w, h), pygame.SRCALPHA)
    panel.fill((0, 0, 0, 140))
    screen.blit(panel, (x, y))
    pygame.draw.rect(screen, border_color, (x, y, w, h), 2, border_radius=10)


def draw_player(surf, rect):
    cx = rect.centerx
    pygame.draw.polygon(surf, BLUE, [
        (cx, rect.top - 8),
        (rect.left, rect.bottom),
        (rect.right, rect.bottom)
    ])
    pygame.draw.polygon(surf, CYAN, [
        (cx, rect.top),
        (rect.left + 10, rect.bottom - 4),
        (rect.right - 10, rect.bottom - 4)
    ])
    pygame.draw.circle(surf, WHITE, (cx, rect.centery + 2), 4)
    glow = random.randint(4, 8)
    pygame.draw.circle(surf, ORANGE, (rect.left + 8, rect.bottom), glow)
    pygame.draw.circle(surf, YELLOW, (rect.right - 8, rect.bottom), glow)


def draw_enemy(surf, rect, t, kind=0):
    bob = math.sin(t * 0.1 + rect.x * 0.05) * 2
    x, y = rect.x, rect.y + bob
    w, h = rect.width, rect.height

    color = RED if kind == 0 else PURPLE if kind == 1 else ORANGE

    pygame.draw.ellipse(surf, color, (x, y, w, h))
    pygame.draw.ellipse(surf, WHITE, (x + 3, y + 3, w - 6, h - 10), 1)
    pygame.draw.circle(surf, WHITE, (int(x + w * 0.3), int(y + h * 0.5)), 3)
    pygame.draw.circle(surf, WHITE, (int(x + w * 0.7), int(y + h * 0.5)), 3)
    pygame.draw.circle(surf, BLACK, (int(x + w * 0.3), int(y + h * 0.5)), 1)
    pygame.draw.circle(surf, BLACK, (int(x + w * 0.7), int(y + h * 0.5)), 1)

    leg_offset = int(math.sin(t * 0.2) * 2)
    for i in range(3):
        lx = int(x + (i + 1) * w / 4)
        pygame.draw.line(surf, color, (lx, y + h - 2),
                         (lx, y + h + 4 + leg_offset), 2)


def draw_glow_rect(surf, rect, color):
    glow = pygame.Surface((rect.width + 10, rect.height + 10), pygame.SRCALPHA)
    pygame.draw.rect(glow, (*color, 60), glow.get_rect(), border_radius=4)
    surf.blit(glow, (rect.x - 5, rect.y - 5))
    pygame.draw.rect(surf, color, rect, border_radius=2)


# ---------------- MENU ----------------
def menu(starfield, high_score):
    t = 0
    while True:
        draw_gradient_background()
        starfield.update_and_draw(screen)
        t += 1

        draw_glow_text("SPACE INVADER", big_font, CYAN,
                       WIDTH // 2 - 190, int(120 + math.sin(t * 0.05) * 5))
        draw_glow_text("BY EMAN SHAHZAD", font, PURPLE,
                       WIDTH // 2 - 110, 200)

        draw_panel(170, 255, 260, 55, YELLOW)
        hs = font.render(f"High Score: {high_score}", True, YELLOW)
        screen.blit(hs, (WIDTH // 2 - hs.get_width() // 2, 272))

        if (t // 30) % 2 == 0:
            draw_panel(150, 360, 300, 55, CYAN)
            play = font.render("Press ENTER to Start", True, WHITE)
            screen.blit(play, (WIDTH // 2 - play.get_width() // 2, 378))

        controls = small_font.render(
            "Arrows/A-D = Move    SPACE = Shoot    Q = Quit", True, SOFT_GRAY)
        screen.blit(controls, (WIDTH // 2 - controls.get_width() // 2, 520))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    return True
                if event.key == pygame.K_q:
                    return False

        pygame.display.update()
        clock.tick(60)


# ---------------- GAME ----------------
def game():
    starfield = Starfield(100)
    high_score = load_high_score()

    if not menu(starfield, high_score):
        return

    while True:
        result = play_round(starfield, high_score)
        if result is None:
            return
        high_score = max(high_score, result)
        save_high_score(high_score)


def play_round(starfield, high_score):
    player = pygame.Rect(270, 630, 50, 30)
    bullets = []
    enemy_bullets = []
    enemies = []
    particles = []

    score = 0
    lives = 3
    level = 1
    enemy_dir = 1
    enemy_speed = 1.0
    shoot_cooldown = 0
    enemy_shoot_timer = 60
    t = 0

    def spawn_wave(level):
        enemies.clear()
        rows = min(3 + level, 5)
        for r in range(rows):
            for c in range(8):
                kind = 0 if r >= rows - 2 else (1 if r >= rows - 3 else 2)
                e = pygame.Rect(50 + c * 60, 70 + r * 45, 36, 24)
                enemies.append((e, kind))

    spawn_wave(level)

    game_over = False
    player_flash = 0

    running = True
    while running:
        clock.tick(60)
        t += 1

        draw_gradient_background()
        starfield.update_and_draw(screen)

        pygame.draw.rect(screen, (20, 60, 40), (0, 670, WIDTH, 30))
        pygame.draw.line(screen, GREEN, (0, 670), (WIDTH, 670), 2)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    return None
                if event.key == pygame.K_SPACE and not game_over and shoot_cooldown <= 0:
                    bullets.append(pygame.Rect(player.centerx - 2, player.y, 4, 12))
                    shoot_cooldown = 15
                if game_over and event.key == pygame.K_r:
                    return score

        keys = pygame.key.get_pressed()
        if not game_over:
            if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and player.x > 0:
                player.x -= 6
            if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and player.x < WIDTH - player.width:
                player.x += 6

        if shoot_cooldown > 0:
            shoot_cooldown -= 1
        if player_flash > 0:
            player_flash -= 1

        if not game_over:
            for bullet in bullets[:]:
                bullet.y -= 10
                if bullet.y < 0:
                    bullets.remove(bullet)
                    continue
                for e_tuple in enemies[:]:
                    e_rect, e_kind = e_tuple
                    if bullet.colliderect(e_rect):
                        if bullet in bullets:
                            bullets.remove(bullet)
                        enemies.remove(e_tuple)
                        color = [RED, PURPLE, ORANGE][e_kind]
                        for _ in range(18):
                            particles.append(Particle(e_rect.centerx, e_rect.centery, color))
                        score += 10 * (e_kind + 1)
                        break

        if not game_over and enemies:
            edge = False
            for e_rect, _ in enemies:
                e_rect.x += int(enemy_dir * enemy_speed)
                if e_rect.left <= 0 or e_rect.right >= WIDTH:
                    edge = True
            if edge:
                enemy_dir *= -1
                for e_rect, _ in enemies:
                    e_rect.y += 18

        if not game_over and enemies:
            enemy_shoot_timer -= 1
            if enemy_shoot_timer <= 0:
                shooter = random.choice(enemies)[0]
                enemy_bullets.append(pygame.Rect(shooter.centerx - 2, shooter.bottom, 4, 12))
                enemy_shoot_timer = max(20, 80 - level * 8)

        for eb in enemy_bullets[:]:
            eb.y += 6
            if eb.y > HEIGHT:
                enemy_bullets.remove(eb)
                continue
            if not game_over and eb.colliderect(player):
                enemy_bullets.remove(eb)
                lives -= 1
                player_flash = 20
                for _ in range(25):
                    particles.append(Particle(player.centerx, player.centery, BLUE))
                if lives <= 0:
                    game_over = True

        for e_rect, _ in enemies:
            if e_rect.colliderect(player) or e_rect.bottom >= 670:
                lives = 0
                game_over = True
                for _ in range(60):
                    particles.append(Particle(player.centerx, player.centery, ORANGE))
                break

        if not enemies and not game_over:
            level += 1
            enemy_speed = min(3.0, 1.0 + level * 0.3)
            spawn_wave(level)
            score += 50

        for p in particles[:]:
            p.update()
            if p.life <= 0:
                particles.remove(p)
            else:
                p.draw(screen)

        for bullet in bullets:
            draw_glow_rect(screen, bullet, YELLOW)
        for eb in enemy_bullets:
            draw_glow_rect(screen, eb, RED)

        for e_rect, kind in enemies:
            draw_enemy(screen, e_rect, t, kind)

        if not game_over and (player_flash == 0 or player_flash % 4 < 2):
            draw_player(screen, player)

        # Better HUD
        draw_panel(10, 8, 580, 42, CYAN)
        screen.blit(font.render(f"SCORE {score}", True, WHITE), (25, 17))
        screen.blit(font.render(f"HI {max(high_score, score)}", True, YELLOW), (220, 17))
        screen.blit(font.render(f"LV {level}", True, GREEN), (390, 17))

        for i in range(lives):
            x = 500 + i * 28
            pygame.draw.polygon(screen, BLUE, [
                (x + 10, 14), (x, 30), (x + 20, 30)
            ])

        if game_over:
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 170))
            screen.blit(overlay, (0, 0))

            draw_panel(100, 180, 400, 300, PURPLE)
            msg = big_font.render("GAME OVER", True, RED)
            screen.blit(msg, (WIDTH // 2 - msg.get_width() // 2, 215))

            for i, line in enumerate([
                f"Final Score: {score}",
                f"High Score: {max(high_score, score)}",
                f"Level Reached: {level}",
            ]):
                txt = font.render(line, True, WHITE)
                screen.blit(txt, (WIDTH // 2 - txt.get_width() // 2, 320 + i * 35))

            if (t // 30) % 2 == 0:
                restart = font.render("Press R to Restart  |  Q to Quit", True, YELLOW)
                screen.blit(restart, (WIDTH // 2 - restart.get_width() // 2, 420))

        pygame.display.update()


if __name__ == "__main__":
    try:
        game()
    finally:
        pygame.quit()