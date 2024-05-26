import pygame
import random

# Inizializzazione di Pygame
pygame.init()

# schermo
larghezza, altezza = 288, 512
schermo = pygame.display.set_mode((larghezza, altezza))
clock = pygame.time.Clock()

# immagini   
sfondo = pygame.image.load('sfondo.png')
uccello = pygame.image.load('uccello.png')
base = pygame.image.load('base.png')
gameover = pygame.image.load('gameover.png')
tubo_giu = pygame.image.load('tubogiu.png')
tubo_su = pygame.image.load('tubo.png')

# Variabili
FPS = 60
velocita_gioco = 3
velocita_uccello_y = 0
basex = 0
tubi = []
punteggio = 0

# Aggiungi tubo
def aggiungi_tubo():
    x = larghezza
    y = random.randint(-200, 0)
    tubi.append((x, y))

# Disegnare gli oggetti
def disegna_oggetti():
    schermo.blit(sfondo, (0, 0))
    for x, y in tubi:
        schermo.blit(tubo_giu, (x, y))
        schermo.blit(tubo_su, (x, y + tubo_giu.get_height() + 150))
    schermo.blit(uccello, (50, uccello_y))
    schermo.blit(base, (basex, 400))
    schermo.blit(base, (basex + 288, 400))
    mostra_punteggio()

# Punteggio
def mostra_punteggio():
    font = pygame.font.SysFont(None, 36)
    punteggio_surface = font.render(str(punteggio), True, (255, 255, 255))
    schermo.blit(punteggio_surface, (larghezza // 2, 20))

# Inizializzazione del gioco
def inizializza():
    global uccello_y, velocita_uccello_y, basex, tubi, punteggio
    uccello_y = 150
    velocita_uccello_y = 0
    basex = 0
    tubi.clear()
    aggiungi_tubo()
    punteggio = 0

# Fine del gioco
def fine_gioco():
    schermo.blit(gameover, (50, 180))
    pygame.display.update()
    ricominciamo = False
    while not ricominciamo:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                inizializza()
                ricominciamo = True
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

# Ciclo principale del gioco
inizializza()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            velocita_uccello_y = -8

    # Movimento dell'uccello
    velocita_uccello_y += 1
    uccello_y += velocita_uccello_y

    # Verifica punteggio e movimento tubi
    nuovi_tubi = []
    for i, (x, y) in enumerate(tubi):
        x -= velocita_gioco
        if x > -tubo_giu.get_width():
            nuovi_tubi.append((x, y))
        else:
            punteggio += 1
            aggiungi_tubo()
        
        # Controllo collisione
        tubo_giu_rettangolo = pygame.Rect(x, y, tubo_giu.get_width(), tubo_giu.get_height())
        tubo_su_rettangolo = pygame.Rect(x, y + tubo_giu.get_height() + 150, tubo_su.get_width(), tubo_su.get_height())
        uccello_rettangolo = pygame.Rect(50, uccello_y, uccello.get_width(), uccello.get_height())
        
        if tubo_giu_rettangolo.colliderect(uccello_rettangolo) or tubo_su_rettangolo.colliderect(uccello_rettangolo) or uccello_y > 380:
            fine_gioco()

    tubi = nuovi_tubi

    # Movimento base
    basex -= velocita_gioco
    if basex <= -288:
        basex = 0

    # Aggiornamento della grafica
    disegna_oggetti()
    pygame.display.update()
    clock.tick(FPS)
