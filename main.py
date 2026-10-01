import pygame
import random


class Raquete:
    def __init__(self, x, y, largura, altura, velocidade):
        self.x = x
        self.y = y
        self.largura = largura
        self.altura = altura
        self.velocidade = velocidade

    def mover(self, direcao, dt, limite_tela):
        self.y += direcao * self.velocidade * dt
        self.y = max(0, min(self.y, limite_tela - self.altura))

    def retangulo(self):
        return pygame.Rect(self.x, self.y, self.largura, self.altura)


class Bola:
    def __init__(self, x, y, tamanho, vx, vy):
        self.x = x
        self.y = y
        self.tamanho = tamanho
        self.vx = vx
        self.vy = vy
        self.x_inicial = x
        self.y_inicial = y
        self.vx_inicial = vx
        self.vy_inicial = vy

    def retangulo(self):
        return pygame.Rect(self.x, self.y, self.tamanho, self.tamanho)

    def mover(self, dt, limite_y):
        self.x += self.vx * dt
        self.y += self.vy * dt

        if self.y < 0:
            self.y = 0
            self.vy = -self.vy
        elif self.y + self.tamanho > limite_y:
            self.y = limite_y - self.tamanho
            self.vy = -self.vy

    def reset(self):
        if self.vx > 0:
            self.x = self.x_inicial
            self.vx = abs(self.vx_inicial)
        else:
            self.x = self.x_inicial
            self.vx = abs(self.vx_inicial) * -1
        self.y = self.y_inicial
        self.vy = abs(self.vy_inicial) * random.choice([1, -1])


pygame.init()

tamanho_tela_x, tamanho_tela_y = 800, 600

tela = pygame.display.set_mode((tamanho_tela_x, tamanho_tela_y))
clock = pygame.time.Clock()


largura_raquete = 15
altura_raquete = 100
distancia_raquete_x = 30
inicio_raquete = 300
velocidade_raquete = 300

raquete_esquerda = Raquete(
    distancia_raquete_x,
    inicio_raquete,
    largura_raquete,
    altura_raquete,
    velocidade_raquete,
)
raquete_direita = Raquete(
    tamanho_tela_x - distancia_raquete_x - largura_raquete,
    inicio_raquete,
    largura_raquete,
    altura_raquete,
    velocidade_raquete,
)

tamanho = 40

bola = Bola(
    ((tamanho_tela_x / 2) - (tamanho / 2)),
    ((tamanho_tela_y / 2) - (tamanho / 2)),
    tamanho,
    (400 * random.choice([1, -1])),
    (300 * random.choice([1, -1])),
)

pontos_esquerda = 0
pontos_direita = 0

fonte = pygame.font.Font(None, 74)

rodando = True
while rodando:
    # delta time, serve para rodar da mesma forma independente do fps
    dt = clock.tick(60) / 1000  # segundos desde o último frame

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

    teclas = pygame.key.get_pressed()

    raquete_esquerda.mover(
        (teclas[pygame.K_s] - teclas[pygame.K_w]), dt, tamanho_tela_y
    )
    raquete_direita.mover(
        (teclas[pygame.K_DOWN] - teclas[pygame.K_UP]), dt, tamanho_tela_y
    )

    # movimento automático com velocidade setada para cada movimento x e y da bolinha
    bola.mover(dt, tamanho_tela_y)
    bola_rect = bola.retangulo()

    ## rebatendo nas raquetes
    if bola_rect.colliderect(raquete_esquerda.retangulo()) and bola.vx < 0:
        bola.x = raquete_esquerda.largura + raquete_esquerda.x
        bola.vx = -bola.vx

    if bola_rect.colliderect(raquete_direita.retangulo()) and bola.vx > 0:
        bola.x = raquete_direita.x - bola.tamanho
        bola.vx = -bola.vx

    if bola.x + bola.tamanho < 0:
        pontos_direita += 1
        bola.reset()
    elif bola.x > tamanho_tela_x:
        pontos_esquerda += 1
        bola.reset()

    texto_esquerda = fonte.render(str(pontos_esquerda), True, (100, 100, 255))
    texto_direita = fonte.render(str(pontos_direita), True, (255, 100, 100))

    tela.fill((20, 20, 30))

    tela.blit(texto_esquerda, (((tamanho_tela_x / 2) - 50), 20))
    tela.blit(texto_direita, (((tamanho_tela_x / 2) + 50), 20))

    ## bolinha
    pygame.draw.ellipse(tela, (80, 200, 120), bola.retangulo())

    ## raquete esquerda
    pygame.draw.rect(
        tela,
        (100, 100, 255),
        raquete_esquerda.retangulo(),
    )

    ## raquete direita
    pygame.draw.rect(
        tela,
        (255, 100, 100),
        raquete_direita.retangulo(),
    )

    pygame.display.flip()

pygame.quit()
