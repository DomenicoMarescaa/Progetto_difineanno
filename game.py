import pygame
import random

# Inizializzazione di Pygame
pygame.init()

# Impostazioni dello schermo
larghezza, altezza = 288, 512
schermo = pygame.display.set_mode((larghezza, altezza))
clock = pygame.time.Clock()

# Caricamento delle immagini   
sfondo = pygame.image.load('game/sfondo.png')
uccello = pygame.image.load('game/uccello.png')
base = pygame.image.load('game/base.png')
gameover = pygame.image.load('game/gameover.png')
tubo_giu = pygame.image.load('game/tubo.png')
tubo_su = pygame.transform.flip(tubo_giu, False, True)

# Variabili globali
FPS = 50
velocita_gioco = 3
velocita_uccello_y = 0
basex = 0
tubi = []
punteggio = 0

# Funzione per creare nuovi tubi
def aggiungi_tubo():
    x = larghezza
    y = random.randint(-200, 0)
    tubi.append((x, y))

# Funzione per disegnare gli oggetti
def disegna_oggetti():
    schermo.blit(sfondo, (0, 0))
    for x, y in tubi:
        schermo.blit(tubo_giu, (x, y))
        schermo.blit(tubo_su, (x, y + tubo_giu.get_height() + 150))
    schermo.blit(uccello, (50, uccello_y))
    schermo.blit(base, (basex, 400))
    schermo.blit(base, (basex + 288, 400))
    mostra_punteggio()

# Funzione per mostrare il punteggio
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
    tubi = []
    punteggio = 0
    aggiungi_tubo()

# Funzione per gestire la fine del gioco
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

    # Movimento dei tubi e verifica collisione
    for i, (x, y) in enumerate(tubi):
        x -= velocita_gioco
        tubi[i] = (x, y)
        if x <= -tubo_giu.get_width():
            punteggio += 1
            tubi.pop(0)
            aggiungi_tubo()

        # Controllo collisione
        tubo_rettangolo = pygame.Rect(x, y, tubo_giu.get_width(), tubo_giu.get_height())
        uccello_rettangolo = pygame.Rect(50, uccello_y, uccello.get_width(), uccello.get_height())
        if tubo_rettangolo.colliderect(uccello_rettangolo) or uccello_y > 380:
            fine_gioco()

    # Movimento della base
    basex -= velocita_gioco
    if basex <= -288:
        basex = 0

    # Aggiornamento della grafica
    disegna_oggetti()
    pygame.display.update()
    clock.tick(FPS)
