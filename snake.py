import pygame
import sys
import random
import sqlite3

pygame.init()

WIDTH, HEIGHT = 400, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake")

clock = pygame.time.Clock()
FPS = 10

running = True
CELL = 20
COLS = WIDTH // CELL
ROWS = HEIGHT // CELL

def losuj_jedzenie(snake):
    while True:
        pos = (random.randint(0, COLS - 1), random.randint(0, ROWS - 1))
        if pos not in snake:
            return pos
font = pygame.font.SysFont("Arial", 24)

def nowa_gra():
    snake = [(5, 5), (4, 5), (3, 5)]
    direction = (1, 0)
    snake2 = [(14, 14), (15, 14), (16, 14)]
    direction2 = (-1, 0)
    food = losuj_jedzenie(snake + snake2)
    score = 0
    score2 = 0
    return snake, direction, snake2, direction2, food, score, score2

snake, direction, snake2, direction2, food, score, score2 = nowa_gra()
game_over = False

stan_gry = "menu"   # "menu", "gra"
tryb_gry = 1          # 1 = jeden gracz, 2 = dwóch graczy

def inicjalizuj_baze():
    conn = sqlite3.connect("wyniki.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS rekord (
            id INTEGER PRIMARY KEY,
            najlepszy_wynik INTEGER NOT NULL
        )
    """)
    cursor.execute("SELECT COUNT(*) FROM rekord")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO rekord (najlepszy_wynik) VALUES (0)")
    conn.commit()
    conn.close()


def wczytaj_rekord():
    conn = sqlite3.connect("wyniki.db")
    cursor = conn.cursor()
    cursor.execute("SELECT najlepszy_wynik FROM rekord LIMIT 1")
    wynik = cursor.fetchone()[0]
    conn.close()
    return wynik

def zapisz_rekord(nowy_wynik):
    conn = sqlite3.connect("wyniki.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE rekord SET najlepszy_wynik = ? ", (nowy_wynik,))
    conn.commit()
    conn.close()

inicjalizuj_baze()
rekord = wczytaj_rekord()
zwyciezca = None

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if stan_gry == "menu":
                if event.key == pygame.K_1:
                    tryb_gry = 1
                    stan_gry = "gra"
                elif event.key == pygame.K_2:
                    tryb_gry = 2
                    stan_gry = "gra"
            elif game_over and event.key == pygame.K_SPACE:
                snake, direction, snake2, direction2, food, score, score2 = nowa_gra()
                game_over = False
                zwyciezca = None
            elif event.key == pygame.K_UP and direction != (0, 1):
                direction = (0, -1)
            elif event.key == pygame.K_DOWN and direction != (0, -1):
                direction = (0, 1)
            elif event.key == pygame.K_LEFT and direction != (1, 0):
                direction = (-1, 0)
            elif event.key == pygame.K_RIGHT and direction != (-1, 0):
                direction = (1, 0)
            elif tryb_gry == 2 and event.key == pygame.K_w and direction2 != (0, 1):
                direction2 = (0, -1)
            elif tryb_gry == 2 and event.key == pygame.K_s and direction2 != (0, -1):
                direction2 = (0, 1)
            elif tryb_gry == 2 and event.key == pygame.K_a and direction2 != (1, 0):
                direction2 = (-1, 0)
            elif tryb_gry == 2 and event.key == pygame.K_d and direction2 != (-1, 0):
                direction2 = (1, 0)
    # Update game state
    if stan_gry == "gra" and not game_over:
        head_x, head_y = snake[0]
        dx, dy = direction
        new_head = (head_x + dx, head_y + dy)
        new_x, new_y = new_head

        kolizja1 = new_x < 0 or new_x >= COLS or new_y < 0 or new_y >= ROWS or new_head in snake
        if tryb_gry == 2 and new_head in snake2:
            kolizja1 = True

        if kolizja1:
            game_over = True
            zwyciezca = "Gracz 2" if tryb_gry == 2 else None
            if score > rekord:
                rekord = score
                zapisz_rekord(rekord)
        else:
            snake.insert(0, new_head)
            if new_head == food:
                score += 1
                if tryb_gry == 2:
                    food = losuj_jedzenie(snake + snake2)
                else:
                    food = losuj_jedzenie(snake)
            else:
                snake.pop()

        if tryb_gry == 2:
            head_x2, head_y2 = snake2[0]
            dx2, dy2 = direction2
            new_head2 = (head_x2 + dx2, head_y2 + dy2)
            new_x2, new_y2 = new_head2

            kolizja2 = new_x2 < 0 or new_x2 >= COLS or new_y2 < 0 or new_y2 >= ROWS or new_head2 in snake2
            if new_head2 in snake:
                kolizja2 = True

            if kolizja2:
                game_over = True
                zwyciezca = "Gracz 1"
            else:
                snake2.insert(0, new_head2)
                if new_head2 == food:
                    score2 += 1
                    food = losuj_jedzenie(snake + snake2)
                else:
                    snake2.pop()

    # Draw
    screen.fill((17, 17, 27)) # ciemne tło
    if stan_gry == "menu":
        tekst_menu = font.render("1 - jeden gracz   |   2 - dwóch graczy", True, (205, 214, 244))
        rect_menu = tekst_menu.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(tekst_menu, rect_menu)
    else:
        for segment in snake:
            x, y = segment
            rect = pygame.Rect(x * CELL, y * CELL, CELL, CELL)
            pygame.draw.rect(screen, (166, 227, 161), rect)

        if tryb_gry == 2:
            for segment in snake2:
                x, y = segment
                rect = pygame.Rect(x * CELL, y * CELL, CELL, CELL)
                pygame.draw.rect(screen, (161, 196, 227), rect)

        food_x, food_y = food
        food_rect = pygame.Rect(food_x * CELL, food_y * CELL, CELL, CELL)
        pygame.draw.rect(screen, (243, 139, 168), food_rect)
        tekst = font.render(f"Wynik: {score} | Rekord: {rekord}", True, (205, 214, 244))
        screen.blit(tekst, (10, 10))

        if game_over:
            if zwyciezca:
                tekst_koncowy = f"Wygrywa {zwyciezca}! — spacja, by zagrać ponownie"
            else:
                tekst_koncowy = "KONIEC GRY — spacja, by zagrać ponownie"
            komunikat = font.render(tekst_koncowy, True, (243, 139, 168))
            rect_komunikatu = komunikat.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            screen.blit(komunikat, rect_komunikatu)
            rect_komunikatu = komunikat.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            screen.blit(komunikat, rect_komunikatu)

    pygame.display.flip()
    clock.tick(FPS)


pygame.quit()
sys.exit()