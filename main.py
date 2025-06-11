import pygame
import random
import tkinter as tk
from tkinter import messagebox
from recursos.funcoes import inicializarBancoDeDados, escreverDados
import json
import math
import datetime
import pyttsx3  # Para síntese de voz (item 20)
import speech_recognition as sr

pygame.init()
inicializarBancoDeDados()
#isso daqui é de propósito que esta aqui, 
tamanho = (1000, 700)
tamanho_boasvindas = (100, 100)
relogio = pygame.time.Clock()
tela = pygame.display.set_mode(tamanho)
pygame.display.set_caption("Stay Natural do Cadu")
icone = pygame.image.load("recursos/imagens/icone.webp")
pygame.display.set_icon(icone)

# Cores
branco = (255, 255, 255)
azul_claro = (0, 200, 255)
preto = (0, 0, 0)
amarelo = (255, 255, 0)
vermelho = (255,0,0)

#recursos
natural = pygame.image.load("recursos/imagens/natural.png")
fundostart = pygame.image.load("recursos/imagens/academiastart.webp")
fundoJogo = pygame.image.load("recursos/imagens/atgym.jpg")
fundoDead = pygame.image.load("recursos/imagens/hospital.jpg")
trembo = pygame.image.load("recursos/imagens/trembo.png")
fundorecepcao = pygame.image.load("recursos/imagens/fundorecepcao.jpg")
ramonrandom = pygame.image.load("recursos/imagens/ramonrandom.png")  # Novo asset (item 14)
global halter
halter = pygame.image.load("recursos/imagens/halteresdecora.png")
global altura_halter 
global largura_halter
largura_halter = 130
altura_halter = 130

#audios
trembosound = pygame.mixer.Sound("recursos/audios/audiocontra.mp3")
mortesound = pygame.mixer.Sound("recursos/audios/quandomorre.mp3")
pygame.mixer.music.load("recursos/audios/fundogame.mp3")
#direcoes
global direcao_animacao
direcao_animacao = "aumentando"
global contador_animacao
contador_animacao = 0
global falou_nome
falou_nome = False

#fontes
fonteMenu = pygame.font.SysFont("comicsans",18)
fonterecepcao = pygame.font.SysFont("comicsans", 40)
fonteMorte = pygame.font.SysFont("arial", 120)
fonteRanking = pygame.font.SysFont("arial", 24)
fontevoz = pygame.font.SysFont("comicsans", 20)
fontedead = pygame.font.SysFont("timesnewroman", 40)

#imagens.ok
fundostart = pygame.transform.scale(fundostart, tamanho)
trembo = pygame.transform.scale(trembo, (140, 140))
natural = pygame.transform.scale(natural, (200, 200))
fundoJogo = pygame.transform.scale(fundoJogo, tamanho)
fundoDead = pygame.transform.scale(fundoDead, tamanho)
ramonrandom = pygame.transform.scale(ramonrandom, (150, 100))  # Item 14
fundorecepcao = pygame.transform.scale(fundorecepcao, (1000,700))
halter = pygame.transform.scale(halter, (130,130))
fundoDead = pygame.transform.scale(fundoDead, (1000, 700))

#função telas boas vindas
def tela_boas_vindas(nome_jogador):
    esperando_inicio = True
    recognizer = sr.Recognizer()
    
    while esperando_inicio:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                quit()
               
            
            # Tecla V ativa o reconhecimento
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_v:
                try:
                    with sr.Microphone() as source:
                        #microfone captando
                        tela.fill(preto)
                        tela.blit(fundorecepcao, (0, 0))
                        tela.blit(fonterecepcao.render("Ouvindo... diga 'INICIAR'", True, vermelho), (300, 550))
                        pygame.display.update()
                        
                        recognizer.adjust_for_ambient_noise(source)
                        audio = recognizer.listen(source, timeout=3)
                        comando = recognizer.recognize_google(audio, language="pt-BR").lower()
                        
                        if "iniciar" in comando:
                            esperando_inicio = False
                except Exception as e:
                    print(f"Erro no reconhecimento: {e}")
            
            
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if botao_iniciar.collidepoint(evento.pos):
                    esperando_inicio = False

        
        tela.fill(preto)
        tela.blit(fundorecepcao, (0, 0))
        
        #escritas da tela boa vinda
        texto_boas_vindas = fonterecepcao.render(f"Bem-vindo, {nome_jogador}!", True, branco)
        texto_instrucao = fonterecepcao.render("Use as setas do eixo X para evitar as Trembolonas!", True, branco)
        tela.blit(texto_boas_vindas, (20, 20))
        tela.blit(texto_instrucao, (20, 500))

        #clica no iniciar
        pygame.draw.rect(tela, branco, (395, 595, 210, 60), 2, border_radius=12)
        botao_iniciar = pygame.draw.rect(tela, azul_claro, (400, 600, 200, 50), border_radius=10)
        texto_botao = fonterecepcao.render("INICIAR", True, preto)
        tela.blit(texto_botao, (410, 600))
        
        #intrução para falar
        texto_voz = fontevoz.render("Pressione V e fale 'INICIAR'", True, branco)
        tela.blit(texto_voz, (700, 20))
        
        pygame.display.update()
        relogio.tick(60)

        global falou_nome
        if not falou_nome:
            falou_nome = True
            engine = pyttsx3.init()
            texto = f"Bem vindo, {nome_jogador}!"
            engine.say(texto)

            engine.runAndWait()
#função Jogar
def jogar():
    def obter_nome():
        global nome
        nome = entry_nome.get()
        if not nome:
            messagebox.showwarning("Aviso", "Por favor, digite seu nome!")
        else:
            root.destroy()

    root = tk.Tk()
    root.title("Informe seu nickname")
    
    largura_janela = 450
    altura_janela = 100 
    
    
    largura_tela = root.winfo_screenmmwidth()  #largura da tela = 1000
    altura_tela = root.winfo_screenheight()  #altura da tela = 700

    
    pos_x = (largura_tela //2 + largura_janela ) 
    pos_y = (altura_tela //2 - altura_janela ) 
    root.geometry(f"{largura_janela}x{altura_janela}+{pos_x}+{pos_y}")
    root.resizable(False, False)  
    
   
    tk.Label(root, text="Digite seu nome:").pack(pady=5)
    entry_nome = tk.Entry(root)
    entry_nome.pack(pady=5)
    
    
    tk.Button(root, text="Enviar", command=obter_nome).pack(pady=5)
    
    root.mainloop()

    tela_boas_vindas(nome)  

    #variaveis
    posicaoXPersona = 500
    posicaoYPersona = 400
    movimentoXPersona = 0
    posicaoXtrembo = random.randint(0, 800)
    posicaoYtrembo = -140
    velocidadetrembo = 1
    pontos = 0
    pausado = False  # Item 11

    
    posicao_ramonrandom = [random.randint(0, 1000), random.randint(0, 700)]
    velocidade_ramonrandom = random.uniform(0.5, 1.5)

    pygame.mixer.music.play(-1)

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RIGHT:
                    movimentoXPersona = 15
                elif evento.key == pygame.K_LEFT:
                    movimentoXPersona = -15
                elif evento.key == pygame.K_SPACE:  # Item 11
                    pausado = not pausado
            elif evento.type == pygame.KEYUP:
                if evento.key in (pygame.K_RIGHT, pygame.K_LEFT):
                    movimentoXPersona = 0
        #pausado
        if pausado:  
            texto_pause = fonteMorte.render("PAUSE", True, branco)
            tela.blit(texto_pause, (350, 250))
            pygame.display.update()
            continue

        
        posicaoXPersona += movimentoXPersona
        posicaoXPersona = max(0, min(800, posicaoXPersona))
        
        posicaoYtrembo += velocidadetrembo
        if posicaoYtrembo > 700:
            posicaoYtrembo = -140
            pygame.mixer.Sound.play(trembosound)
            pontos += 1
            velocidadetrembo += 0.5
            posicaoXtrembo = random.randint(0, 800)

        
        posicao_ramonrandom[0] -= velocidade_ramonrandom
        if posicao_ramonrandom[0] < -150:
            posicao_ramonrandom[0] = 1000
            posicao_ramonrandom[1] = random.randint(50, 200)

        
        tela.blit(fundoJogo, (0, 0))
        global altura_halter
        global largura_halter
        def animar():
            global direcao_animacao
            global contador_animacao
            if direcao_animacao == 'aumentando':
                if contador_animacao < 100:
                    contador_animacao += 1
                else:
                    direcao_animacao = 'diminuindo'
            else:
                if contador_animacao > 0:
                    contador_animacao -= 1
                else:
                    direcao_animacao = 'aumentando'

            escala = 1 + contador_animacao * 0.00115
            return escala
        escala = animar()
        nova_largura = int(largura_halter * escala)
        nova_altura = int(altura_halter * escala)
    
        
        image = pygame.transform.smoothscale(halter, (nova_largura,nova_altura))
        tela.blit(image,(820,20))
        

        tela.blit(ramonrandom, posicao_ramonrandom)  
        tela.blit(natural, (posicaoXPersona, posicaoYPersona))
        tela.blit(trembo, (posicaoXtrembo, posicaoYtrembo))
        
        
        texto_pontos = fonteMenu.render(f"Pontos: {pontos}", True, branco)
        texto_pause_info = fonteMenu.render("Press SPACE to Pause", True, branco)
        tela.blit(texto_pontos, (15, 15))
        tela.blit(texto_pause_info, (20, 660))

        #colisão
        if (abs(posicaoXPersona - posicaoXtrembo) < 124 and 
            abs(posicaoYPersona - posicaoYtrembo) < 124):
            data_hora = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            escreverDados(nome, pontos)  
            dead()

        pygame.display.update()
        relogio.tick(120)

#função morte
def dead():
    pygame.mixer.music.stop()
    pygame.mixer.Sound.play(mortesound)

    # Carrega os últimos 5 registros
    try:
        with open("recursos/log.dat", "r") as f:
            registros = json.load(f)
        # Converte para lista e ordena por pontos (decrescente)
        registros_lista = sorted(registros.items(), key=lambda item: item[1][0], reverse=True)
        ultimos_5 = registros_lista[:5]
    except Exception as e:
        print(f"Erro ao carregar registros: {e}")
        ultimos_5 = []

    esperando = True
    while esperando:
        mouse_pos = pygame.mouse.get_pos()
        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                quit()
            
            if evento.type == pygame.MOUSEBUTTONDOWN:
                # Verifica clique nos botões
                if 400 <= mouse_pos[0] <= 600 and 500 <= mouse_pos[1] <= 550:  # Botão Reiniciar
                    esperando = False
                    pygame.mixer.music.play(-1)
                    jogar()
                    return
                
                elif 400 <= mouse_pos[0] <= 600 and 600 <= mouse_pos[1] <= 650:  # Botão Sair
                    pygame.quit()
                    quit()

        tela.blit(fundoDead, (0, 0))
        
        # Título GAME OVER
        texto_morte = fonteMorte.render("GAME OVER", True, (255, 0, 0))
        tela.blit(texto_morte, (tamanho[0]//2 - texto_morte.get_width()//2, 30))
        
        # Subtítulo "Últimos Pacientes"
        texto_subtitulo = fontedead.render("Últimos Pacientes:", True, branco)
        tela.blit(texto_subtitulo, (tamanho[0]//2 - texto_subtitulo.get_width()//2, 150))
        
        # Lista de pacientes (ou mensagem se não houver registros)
        y = 200
        if ultimos_5:
            for i, (nome_reg, dados_reg) in enumerate(ultimos_5):
                try:
                    pontos_reg = dados_reg[0]
                    data_str = dados_reg[1]  # Já está no formato "dd/mm/aaaa"
                    hora_str = dados_reg[2]  # Já está no formato "hh:mm:ss"
                    
                    # Renderiza texto do paciente
                    texto_paciente = fonteRanking.render(
                        f"Paciente: {nome_reg} - {pontos_reg} pts - {data_str}", 
                        True, branco
                    )
                    tela.blit(texto_paciente, (tamanho[0]//2 - texto_paciente.get_width()//2, y))
                    
                    # Renderiza horário e motivo
                    texto_horario_motivo = fonteRanking.render(
                        f"Horário: {hora_str} - Motivo: overdose", 
                        True, vermelho
                    )
                    tela.blit(texto_horario_motivo, (tamanho[0]//2 - texto_horario_motivo.get_width()//2, y + 25))
                    
                    y += 60
                except Exception as e:
                    print(f"Erro ao exibir registro {i}: {e}")
        else:
            texto_sem_registros = fonteRanking.render("Nenhum paciente registrado ainda", True, branco)
            tela.blit(texto_sem_registros, (tamanho[0]//2 - texto_sem_registros.get_width()//2, y))
        
        # Efeito hover para os botões
        reiniciar_color = azul_claro if 400 <= mouse_pos[0] <= 600 and 500 <= mouse_pos[1] <= 550 else branco
        sair_color = azul_claro if 400 <= mouse_pos[0] <= 600 and 600 <= mouse_pos[1] <= 650 else branco

        # Botão Reiniciar
        pygame.draw.rect(tela, reiniciar_color, (400, 500, 200, 50), border_radius=10)
        pygame.draw.rect(tela, azul_claro, (400, 500, 200, 50), 2, border_radius=10)  # Borda
        texto_reiniciar = fontedead.render("Reiniciar", True, preto)
        tela.blit(texto_reiniciar, (400 + 100 - texto_reiniciar.get_width()//2, 500 + 25 - texto_reiniciar.get_height()//2))
        
        # Botão Sair
        pygame.draw.rect(tela, sair_color, (400, 600, 200, 50), border_radius=10)
        pygame.draw.rect(tela, azul_claro, (400, 600, 200, 50), 2, border_radius=10)  # Borda
        texto_sair = fontedead.render("Sair", True, preto)
        tela.blit(texto_sair, (400 + 100 - texto_sair.get_width()//2, 600 + 25 - texto_sair.get_height()//2))
        
        pygame.display.update()
        relogio.tick(60)
#função jogar 
def start():
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if startButton.collidepoint(evento.pos):
                    jogar()
                elif quitButton.collidepoint(evento.pos):
                    pygame.quit()
                    quit()

        tela.blit(fundostart, (0, 0))
        
        startButton = pygame.draw.rect(tela, azul_claro, (10, 10, 165, 40), border_radius=15)
        startTexto = fonteMenu.render("Matricular-se", True, preto)
        tela.blit(startTexto, (25, 12))
        
        quitButton = pygame.draw.rect(tela, azul_claro, (10, 60, 165, 40), border_radius=15)
        quitTexto = fonteMenu.render("Continuar Frango", True, preto)
        tela.blit(quitTexto, (25, 62))
        
        pygame.display.update()
        relogio.tick(60)
        

start()