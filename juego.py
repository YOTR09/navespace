import random  # Para posiciones aleatorias de enemigos
import pygame  # Librería del juego

# ---------- CONSTANTES (valores fáciles de ajustar) ----------
ANCHO, ALTO = 480, 640            # Tamaño de la ventana
ANCHO2, ALTO2 = 520, 680
FPS = 60                          # Fotogramas por segundo
VEL_NAVE = 6                      # Píxeles por fotograma de la nave
VEL_BALA = 10                     # Velocidad de las balas (hacia arriba)
VEL_ENEMIGO = 3                   # Velocidad constante de descenso
CADENCIA_MS = 250                 # Milisegundos mínimos entre disparos
APARICION_MS = 700                # Milisegundos entre enemigos nuevos

NEGRO = (10, 10, 25)              # Color de fondo
BLANCO = (240, 240, 240)
VERDE = (60, 220, 120)            # Nave
AMARILLO = (255, 230, 80)         # Balas
ROJO = (230, 70, 70)              # Enemigos


# ---------- CLASES ----------
class Nave:

    """La nave del jugador: un triángulo verde."""

    def __init__(self):
        # Rect guarda posición y tamaño; se usa también para colisiones
        self.rect = pygame.Rect(ANCHO // 2 - 20, ALTO - 80, 40, 30)

    def mover(self, teclas):
        # Izquierda: flecha o A
        if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
            self.rect.x -= VEL_NAVE
        # Derecha: flecha o D
        if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
            self.rect.x += VEL_NAVE
        # Evita que salga de la pantalla
        self.rect.clamp_ip(pygame.Rect(0, 0, ANCHO, ALTO))

    def dibujar(self, pantalla):
        r = self.rect
        # Triángulo: punta arriba, base abajo
        puntos = [(r.centerx, r.top), (r.left, r.bottom), (r.right, r.bottom)]
        pygame.draw.polygon(pantalla, VERDE, puntos)

class Nave2:

    """La nave del jugador: un triángulo verde."""

    def __init__(self):
        # Rect guarda posición y tamaño; se usa también para colisiones
        self.rect = pygame.Rect(ANCHO // 2 - 20, ALTO - 80, 40, 30)

    def mover(self, teclas):
        # Izquierda: flecha o A
        if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
            self.rect.x -= VEL_NAVE
        # Derecha: flecha o D
        if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
            self.rect.x += VEL_NAVE
        # Evita que salga de la pantalla
        self.rect.clamp_ip(pygame.Rect(0, 0, ANCHO, ALTO))

    def dibujar(self, pantalla):
        r = self.rect
        # Triángulo: punta arriba, base abajo
        puntos = [(r.centerx, r.top), (r.left, r.bottom), (r.right, r.bottom)]
        pygame.draw.polygon(pantalla, ROJO, puntos)      


class Bala:
    """Proyectil: rectángulo amarillo que sube."""

    def __init__(self, x, y):
        self.rect = pygame.Rect(x - 2, y, 4, 14)

    def actualizar(self):
        self.rect.y -= VEL_BALA  # Sube por la pantalla

    def dibujar(self, pantalla):
        pygame.draw.rect(pantalla, AMARILLO, self.rect)


class Enemigo:
    """Enemigo: cuadrado rojo que baja a velocidad constante."""

    def __init__(self):
        x = random.randint(0, ANCHO - 36)           # Posición X aleatoria
        self.rect = pygame.Rect(x, -36, 36, 36)     # Empieza justo sobre la pantalla

    def actualizar(self):
        self.rect.y += VEL_ENEMIGO  # Desciende

    def dibujar(self, pantalla):
        pygame.draw.rect(pantalla, ROJO, self.rect)
        # Dos "ojos" para darle personalidad
        pygame.draw.circle(pantalla, BLANCO, (self.rect.x + 11, self.rect.y + 14), 4)
        pygame.draw.circle(pantalla, BLANCO, (self.rect.x + 25, self.rect.y + 14), 4)


# ---------- FUNCIONES AUXILIARES ----------
def reiniciar():
    """Devuelve el estado inicial de una partida nueva."""
    return Nave(), Nave2(), [], [], 0  # nave, balas, enemigos, puntos


def texto_centrado(pantalla, fuente, texto, y):
    """Dibuja texto horizontalmente centrado en la altura y."""
    img = fuente.render(texto, True, BLANCO)
    pantalla.blit(img, img.get_rect(center=(ANCHO // 2, y)))


# ---------- PROGRAMA PRINCIPAL ----------
def main():
    pygame.init()                                        # Inicia Pygame
    pantalla = pygame.display.set_mode((ANCHO, ALTO))    # Crea la ventana
    pygame.display.set_caption("Space Shooter")          # Título de ventana
    reloj = pygame.time.Clock()                          # Controla los FPS
    fuente = pygame.font.Font(None, 36)                  # Fuente por defecto

    nave, nave2, balas, enemigos, puntos = reiniciar()          # Estado inicial
    game_over = False
    ultimo_disparo = 0                                   # Momento del último disparo
    ultimo_enemigo = 0                                   # Momento de la última aparición
    corriendo = True

    # ===== GAME LOOP =====
    while corriendo:
        ahora = pygame.time.get_ticks()  # Milisegundos desde que inició

        # --- 1. EVENTOS ---||
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:               # Cerrar ventana
                corriendo = False
            if evento.type == pygame.KEYDOWN and game_over and evento.key == pygame.K_r:
                nave, balas, enemigos, puntos = reiniciar()  # Reinicio con R
                game_over = False

        # --- 2. ACTUALIZAR LÓGICA (solo si seguimos vivos) ---
        if not game_over:
            teclas = pygame.key.get_pressed()            # Teclas mantenidas
            nave.mover(teclas)

            # Disparo con cadencia: solo si pasó suficiente tiempo
            if teclas[pygame.K_SPACE] and ahora - ultimo_disparo >= CADENCIA_MS:
                balas.append(Bala(nave.rect.centerx, nave.rect.top))
                balas.append(Bala(nave2.rect.centerx, nave.rect.top))
                ultimo_disparo = ahora

            # Aparición periódica de enemigos
            if ahora - ultimo_enemigo >= APARICION_MS:
                enemigos.append(Enemigo())
                ultimo_enemigo = ahora

            for b in balas:
                b.actualizar()
            for e in enemigos:
                e.actualizar()

            # Descarta balas fuera de pantalla
            balas = [b for b in balas if b.rect.bottom > 0]

            # --- 3. COLISIONES ---
            for e in enemigos[:]:                        # Copia: modificamos la lista original
                for b in balas[:]:
                    if e.rect.colliderect(b.rect):       # Bala toca enemigo
                        enemigos.remove(e)
                        balas.remove(b)
                        puntos += 10
                        break                            # Este enemigo ya murió
                else:
                    # Solo si no fue destruido: ¿toca la nave?
                    if e.rect.colliderect(nave.rect):
                        game_over = True

            # Enemigos que llegan al fondo también hacen perder
            if any(e.rect.top > ALTO for e in enemigos):
                game_over = True

        # --- 4. DIBUJAR ---
        pantalla.fill(NEGRO)                             # Limpia el fotograma
        nave.dibujar(pantalla)
        for b in balas:
            b.dibujar(pantalla)
        for e in enemigos:
            e.dibujar(pantalla)
        pantalla.blit(fuente.render(f"Puntos: {puntos}", True, BLANCO), (10, 10))

        if game_over:
            texto_centrado(pantalla, fuente, "GAME OVER", ALTO // 2 - 20)
            texto_centrado(pantalla, fuente, "Pulsa R para reiniciar", ALTO // 2 + 20)

        pygame.display.flip()                            # Muestra lo dibujado
        reloj.tick(FPS)                                  # Limita a 60 FPS

    pygame.quit()  # Cierra Pygame limpiamente


if __name__ == "__main__":
    main()
