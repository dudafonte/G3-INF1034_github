import pygame
import sys

pygame.init()

# Janela
tela = pygame.display.set_mode((620,360))
pygame.display.set_caption("movimentos do personagem")

# Cores
BRANCO = (255, 255, 255)

# Tamanhos
tile_width = 77
tile_height = 50
fundo = pygame.image.load(r"C:\Users\u2320450\Documents\G3_INF1034\tilesets\Image without mist.png").convert()

###################################### CARREGA TODOS OS FRAMES ######################################################
caminho = "C:\\Users\\u2320450\\Documents\\G3_INF1034\\tilesets_inteiros\\"

# Frames de ataque para a direita 
ataque_direita_frames = []
tile = pygame.image.load(caminho + "attackrt.png").convert_alpha()
t_wdt = tile.get_width() // 6
t_hgt = tile.get_height() // 1
print(t_wdt, t_hgt)
for i in range(6):
    ataque_direita_frames.append(tile.subsurface((i*t_wdt, 0, t_wdt, t_hgt)))

# Frames de ataque para a esquerda
ataque_esquerda_frames = []
reverse = []
tile = pygame.image.load(caminho + "attackrt.png")
t_wdt = tile.get_width() // 6
t_hgt = tile.get_height() // 1
for i in range(6):
    ataque_esquerda_frames.append(pygame.transform.flip(tile.subsurface((i*t_wdt, 0, t_wdt, t_hgt)), True, False))


# Frames de ataque para cima
ataque_cima_direita_frames = []
tile = pygame.image.load(caminho + "attackrt_up.png")
t_wdt = tile.get_width() // 4
t_hgt = tile.get_height() // 1
for i in range(4):
    ataque_cima_direita_frames.append(tile.subsurface((i*t_wdt, 0, t_wdt, t_hgt)))

ataque_cima_esquerda_frames = []
tile = pygame.image.load(caminho + "attackrt_up.png")
t_wdt = tile.get_width() // 4
t_hgt = tile.get_height() // 1
for i in range(4):
    ataque_cima_esquerda_frames.append(pygame.transform.flip(tile.subsurface((i*t_wdt, 0, t_wdt, t_hgt)), True, False))

# Frames de pulo 
pulo_frames_direita = []
tile = pygame.image.load(caminho + "jumprt.png")
t_wdt = tile.get_width() // 3
t_hgt = tile.get_height() // 1
for i in range(3):
    pulo_frames_direita.append(tile.subsurface((i*t_wdt, 0, t_wdt, t_hgt)))

pulo_frames_esquerda = []
tile = pygame.image.load(caminho + "jumplft.png")
t_wdt = tile.get_width() // 3
t_hgt = tile.get_height() // 1
for i in range(3):
    pulo_frames_esquerda.append(tile.subsurface((i*t_wdt, 0, t_wdt, t_hgt)))

corrida_direita_frames = []
tile = pygame.image.load(caminho + "_Run.png")
t_wdt = tile.get_width() // 10
t_hgt = tile.get_height() // 1
for i in range(10):
    corrida_direita_frames.append(tile.subsurface((i*t_wdt, 0, t_wdt, t_hgt)))


corrida_esquerda_frames = []
tile = pygame.image.load(caminho + "_Run.png")
t_wdt = tile.get_width() // 10
t_hgt = tile.get_height() // 1
for i in range(10):
    corrida_esquerda_frames.append(pygame.transform.flip(tile.subsurface((i*t_wdt, 0, t_wdt, t_hgt)), True, False))

# Frames parado direita - Outro método (bom)
parado_direita_frames = []
tile = pygame.image.load(caminho + "_Idle.png")
t_wdt = tile.get_width() // 10
t_hgt = tile.get_height() // 1
for i in range(10):
    parado_direita_frames.append(tile.subsurface((i*t_wdt, 0, t_wdt, t_hgt)))

# Frames parado esquerda 
parado_esquerda_frames = []
tile = pygame.image.load(caminho + "_Idlelft.png")
t_wdt = tile.get_width() // 10
t_hgt = tile.get_height() // 1
for i in range(10):
    parado_esquerda_frames.append(tile.subsurface((i*t_wdt, 0, t_wdt, t_hgt)))

desliza_direita = []
tile = pygame.image.load(caminho + "_SlideAll.png")
t_wdt = tile.get_width() // 4
t_hgt = tile.get_height() // 1
for i in range(4):
    desliza_direita.append(tile.subsurface((i*t_wdt, 0, t_wdt, t_hgt)))

desliza_esquerda = []
tile = pygame.image.load(caminho + "_SlideAll_lft.png")
t_wdt = tile.get_width() // 4
t_hgt = tile.get_height() // 1
for i in range(4):
    desliza_esquerda.append(tile.subsurface((i*t_wdt, 0, t_wdt, t_hgt)))


###################################### VARIÁVEIS INICIAIS ######################################################

frame_parado_atual = 0
tempo_parado_animacao = 0

frame_pulo_atual = 0
tempo_pulo_animacao = 0

frame_deslize_atual = 0 
tempo_deslize_atual = 0

# Estado inicial
personagem_tile = parado_direita_frames[frame_parado_atual]
x, y = 0, 250

velocidade = 5

# Controle de ataque
em_ataque = False
frame_ataque_atual = 0
tempo_animacao = 0
movimento = None  # <-- salva a direção atual do ataque
direcao = "direita"

# Variáveis para pulo
pulando = False
velocidade_pulo = -10  # valor menos extremo
gravidade = 0.5        # gravidade mais suave
chao = 250             # posição Y inicial (onde o personagem fica em pé)

# Variáveis do deslize
deslizando = False
tempo_deslize = 0
duracao_deslize = 10
velocidade_deslize = 5

clock = pygame.time.Clock()

###################################### LÓGICA DOS MOVIMENTOS ######################################################
while True:
    tela.fill(BRANCO)

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    teclas = pygame.key.get_pressed()
    mover_direita = teclas[pygame.K_d]
    mover_esquerda = teclas[pygame.K_a]
    mover_cima = teclas[pygame.K_UP]
    pulo = teclas[pygame.K_SPACE]
    deslize = teclas[pygame.K_DOWN] 
    atacar = teclas[pygame.K_f]

    ###################### Lógica de corrida para a direita e esquerda ###################### 
    if mover_direita:
        direcao = "direita"
        x += velocidade
        tempo_parado_animacao += 1
        if tempo_parado_animacao >= 5:
            tempo_parado_animacao = 0
            frame_parado_atual = (frame_parado_atual + 1) % len(corrida_direita_frames)
            personagem_tile = corrida_direita_frames[frame_parado_atual]
    
    elif mover_esquerda:
        direcao = "esquerda"
        x -= velocidade
        tempo_parado_animacao += 1
        if tempo_parado_animacao >= 5:
            tempo_parado_animacao = 0
            frame_parado_atual = (frame_parado_atual + 1) % len(corrida_esquerda_frames)
            personagem_tile = corrida_esquerda_frames[frame_parado_atual]

    ###################### Lógica de ataque para a direita, esquerda e de cima para baixo (esquerda/direita) ###################### 
    if atacar and not em_ataque:
        if teclas[pygame.K_RIGHT]:
            movimento = "direita"
            frame_ataque_atual = 0
            tempo_animacao = 0
            em_ataque = True
        elif teclas[pygame.K_LEFT]:
            movimento = "esquerda"
            frame_ataque_atual = 0
            tempo_animacao = 0
            em_ataque = True  
        elif mover_cima:
            movimento = "cima"
            frame_ataque_atual = 0
            tempo_animacao = 0
            em_ataque = True
            
    # Animação de ataque
    if em_ataque:
        tempo_animacao += 1
        if tempo_animacao >= 5:
            tempo_animacao = 0
            frame_ataque_atual += 1

            if movimento == "direita":
                if frame_ataque_atual >= len(ataque_direita_frames):
                    em_ataque = False
                    
                else:
                    personagem_tile = ataque_direita_frames[frame_ataque_atual]
            elif movimento == "esquerda":
                if frame_ataque_atual >= len(ataque_esquerda_frames):
                    em_ataque = False 
                else:
                    personagem_tile = ataque_esquerda_frames[frame_ataque_atual]
        
            elif movimento == "cima" and direcao == "direita":
                if frame_ataque_atual >= len(ataque_cima_direita_frames):
                    em_ataque = False
                    
                else:
                    personagem_tile = ataque_cima_direita_frames[frame_ataque_atual]
                
            elif movimento == "cima" and direcao == "esquerda":
                if frame_ataque_atual >= len(ataque_cima_esquerda_frames):
                    em_ataque = False 
                else:
                    personagem_tile = ataque_cima_esquerda_frames[frame_ataque_atual]
    
    ###################### Lógica de pulo para esquerda e direita ###################### 
    if pulo and not pulando and not em_ataque:  # Só pode pular se não estiver atacando
        pulando = True
        vel_y = velocidade_pulo
        frame_pulo_atual = 0  # Reseta a animação do pulo

    if pulando:
        # Atualiza posição Y
        y += vel_y
        vel_y += gravidade
        
        # Animação do pulo
        tempo_pulo_animacao += 1
        if tempo_pulo_animacao >= 7:  # Controla velocidade da animação
            tempo_pulo_animacao = 0
            frame_pulo_atual = (frame_pulo_atual + 1) % len(pulo_frames_direita)
        
        # Usa o frame atual do pulo
        if direcao == "direita":
            personagem_tile = pulo_frames_direita[frame_pulo_atual]
        else:
            personagem_tile = pulo_frames_esquerda[frame_pulo_atual]

        # Verifica se atingiu o chão
        if y >= chao:  
            y = chao
            pulando = False
            vel_y = 0
            # Volta para animação parado ao cair
            frame_parado_atual = 0


    ###################### Lógica de deslize para esquerda e direita ###################### 
    if deslize and not deslizando and not em_ataque:
        deslizando = True 
        frame_deslize_atual = 0
    
    if deslizando:
        tempo_deslize_atual += 1
        if tempo_deslize_atual >= 7:
            tempo_deslize_atual = 0 
            frame_deslize_atual = (frame_deslize_atual + 1) % len(desliza_direita)
        
        if direcao == "direita":
            personagem_tile = desliza_direita[frame_deslize_atual]
        else:
            personagem_tile = desliza_esquerda[frame_deslize_atual]
        
        if direcao == "direita":
            personagem_tile = desliza_direita[frame_deslize_atual]
            x += velocidade_deslize
        else:
            personagem_tile = desliza_esquerda[frame_deslize_atual]
            x -= velocidade_deslize

        tempo_deslize += 1
        if tempo_deslize >= duracao_deslize:
            deslizando = False
            tempo_deslize = 0
            frame_deslize_atual = 0

    ###################### Lógica para quando o boneco estiver parado para direita e esquerda ###################### 
    if not mover_direita and not mover_esquerda and not pulando and not em_ataque and not deslizando:
        tempo_parado_animacao += 1
        if tempo_parado_animacao >= 10:
            tempo_parado_animacao = 0
            frame_parado_atual = (frame_parado_atual + 1) % len(parado_direita_frames)
        if direcao == "direita":
            personagem_tile = parado_direita_frames[frame_parado_atual]
        else:
            personagem_tile = parado_esquerda_frames[frame_parado_atual]

    # Desenha o fundo e o personagem
    tela.blit(fundo, (0, 0))
    tela.blit(personagem_tile, (x, y))

    pygame.display.update()
    clock.tick(60)  # Limita a 60 frames por segundo
