# Snake

Klasyczna gra Snake napisana w Pythonie z użyciem pygame-ce. Zawiera tryb dla jednego i dwóch graczy oraz zapis rekordu w bazie SQLite.

## Funkcje

- Klasyczna rozgrywka Snake — sterowanie strzałkami
- Tryb dla dwóch graczy (lokalny multiplayer) — drugi gracz steruje WASD
- Kolizje między wężami w trybie multiplayer
- Zapis najlepszego wyniku w bazie danych SQLite (rekord zachowany między uruchomieniami)
- Ekran menu z wyborem trybu gry
- Ekran końca gry z restartem

## Wymagania

- Python 3.10+
- pygame-ce

## Instalacja i uruchomienie

```bash
pip install -r requirements.txt
python snake.py
```

## Sterowanie

**Gracz 1:** strzałki
**Gracz 2 (tryb multiplayer):** W, A, S, D

Na ekranie startowym: `1` — jeden gracz, `2` — dwóch graczy
Po przegranej: spacja — restart

## Technologie

- Python
- pygame-ce
- SQLite (sqlite3)