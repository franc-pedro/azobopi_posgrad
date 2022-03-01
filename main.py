from AzobopiCanvas import *
from AzobopiButton import *
from tkinter import *
import pygame
from pygame import mixer

pygame.init()

# Variáveis iniciais
bg = "#ffe6e6"
width = 900
height = 650
azopi = None  # O nosso azobopi ainda não existe
pos_star = []  # Lista com posição e id da estrela
pos_tree = []  # Lista com posição e id da árvore
trees = []  # Lista com a informação de todas as árvores
start = False  # Ainda não começámos
grid_large = False  # Tamanho da grelha
restart = False  # Recomeço do jogo
commands = []  # Lista com os comandos inseridos pelo utilizador
img_cmd = [0]  # Objectos das imagens dos comandos
img_cmd_created = []  # Lista de todos os objetos das imagens dos comandos
cmd_counter = 50  # Contador para espaçamento das imagens dos comandos eixo x
cmd_y = 550  # Contador para espaçamento das imagens dos comandos eixo y
running = False  # Para termos a certeza que o jogo não arrancou


# Função para adicionar o comando de cada botão premido
def add_command(direction):
    global cmd_counter, cmd_y
    if not start:  # Ainda não começámos o jogo
        commands.append(direction)  # Podemos adicionar comandos
        # Criamos a imagem e acrescentamos à lista
        img_cmd_created.append(img_cmd[direction].create_img(cmd_counter, cmd_y, canvas, CENTER))
        cmd_counter = cmd_counter + 40  # Incremetamos em 40px o contador do eixo x
        if cmd_counter > 820:  # Se chegarmos ao fim da janela
            cmd_counter = 50 # voltamos no eixo x
            cmd_y += 40 # baixamos no eixo y - nova linha


# Função quando o botão amarelo esquerda é premido
# Arrancamos o jogo se não o tivermos já feito e se existirem comandos
def change_state():
    global start
    if not running:
        if commands:  # Vemos se existem comandos inseridos
            start = True
            game()


# Iniciamos o jogo após a entrada inicial
# Criamos no canvas o azobopi, a estrela e as árvores
def update_init(grid=1):
    global azopi
    global pos_star, grid_large
    canvas.delete("all")    # Reset do canvas - não a melhor solução
    if grid == 1:  # Grelha 5x5
        bg_grid_1.create_img(0, 0, canvas, NW) # Imagem da grelha 5x5
        pos_star = star.item_create(canvas, 1, "star")  # criação da estrela E retorno da posição da estrela, grelha pequena
        azopi = robot.create_img(50, 50, canvas, CENTER)  # O nosso robot
        for z in range(4):
            trees.append(tree.item_create(canvas, 1, "tree", pos_star, trees))       # Árvores 5 se tudo correr bem
        grid_large = False
    else:  # Grelha 10x10
        bg_grid_10.create_img(0, 0, canvas, NW) # Imagem da grelha 10x10
        pos_star = star.item_create(canvas, 10, "star")  # criação da estrela E retorno da posição da estrela, grelha grande
        azopi = robot.create_img(25, 25, canvas, CENTER)  # O nosso robot
        for z in range(8):
            trees.append(tree.item_create(canvas, 10, "tree", pos_star, trees))  # Árvores 10 se tudo correr bem
        grid_large = True
    # Criamos os botões de comando e escondemos os outros dois
    button_red.button_create(650, 180)
    button_blue.button_create(720, 120)
    button_green.button_create(790, 180)
    button_yellow_left.button_create(560, 180)
    button_yellow.button_create(720, 240)
    button_simples.button_hide()
    button_avancado.button_hide()


# O jogo - lê os comandos e executa o movimento do robot
#  Em função do movimento terminamos o jogo
def game():
    global running, restart, grid_large
    if grid_large:
        dt = 50  # distância a percorrer pelo azobopi
    else:
        dt = 100
    for i in range(len(commands)):  # Enquanto houver comandos
        if start:
            running = True
            # Damos inicio ao movimento do Azobopi
            res = robot.move(canvas, azopi, dt, commands[i], pos_star, trees, restart, grid_large)
            if restart:  # Evitamos que o restart seja continuamente enviado
                restart = False
            if not res:  # Não houve resposta até agora
                canvas.delete(img_cmd_created[i])  # eliminamos uma imagem de comando
                # Só precisamos de saber se temos os comandos todos
                # Se já estão todos e não temos resposta da estrela faltou o danoninho
                if i + 1 == len(commands):
                    end_game(3)  # E saímos
            if res == "Star":  # Encontrámos a estrela
                canvas.delete(img_cmd_created[i])
                canvas.delete(pos_star[2])  # Eliminamos a estrela através do seu id
                end_game(1)  # E saímos
            if res == "Tree":  # Encontrámos uma árvore
                canvas.delete(img_cmd_created[i])
                end_game(4)  # E saímos
            if res == "Out":  # Se correu mal finalizamos o jogo
                end_game(2)  # E saímos


# Chegámos ao fim ou falhámos
# Em função do status final enviamos uma mensagem ao utilizador
def end_game(status):
    global start, cmd_y, cmd_counter, restart, running
    if status == 1:  # Encontrámos a estrela
        print("Boa Encontrastes a estrela")
        time.sleep(0.025)
        win.create_img(0, 0, canvas, NW)
    if status == 2:  # Saímos da grelha
        print("Saistes da grelha")
        time.sleep(0.025)
        out_grid.create_img(0, 0, canvas, NW)
    if status == 3:  # Não introduzimos comandos suficientes
        print("Faltou um danoninho")
        time.sleep(0.025)
        miss_commands.create_img(0, 0, canvas, NW)
    if status == 4:  # Batemos numa árvore
        print("Ups")
        time.sleep(0.025)
        loose.create_img(0, 0, canvas, NW)
    # Reinicializamos algumas varáveis e recriamos os botões principais
    start = False
    restart = True
    running = False
    commands.clear()
    img_cmd_created.clear()
    trees.clear()
    cmd_counter = 50
    cmd_y = 550
    button_simples.button_create(525, 350)
    button_avancado.button_create(725, 350)


if __name__ == '__main__':
    root = Tk()
    root.title("Azobopi")
    root.resizable(False, False)
    canvas = Canvas(root, bg=bg, width=width, height=height)
    canvas.pack(padx=2, pady=2)

    # Instâncias referentes às diferentes imagens a usar no jogo
    bg_init = AzobopiCanvas("img/2.png")
    img_init = bg_init.create_img(200, 0, canvas, NW)
    bg_grid_1 = AzobopiCanvas("img/grelha.png")
    bg_grid_10 = AzobopiCanvas("img/grelha10.png")
    star = AzobopiCanvas("img/star.png")
    robot = AzobopiCanvas("img/square.png")
    tree = AzobopiCanvas("img/tree.png")
    loose = AzobopiCanvas("img/loose.png")
    win = AzobopiCanvas("img/win.png")
    out_grid = AzobopiCanvas ("img/out_grid.png")
    miss_commands = AzobopiCanvas ("img/miss_commands.png")

    # Lista de instâncias das imagens de comando
    img_cmd.append(AzobopiCanvas("img/cmd/1.png"))
    img_cmd.append(AzobopiCanvas("img/cmd/2.png"))
    img_cmd.append(AzobopiCanvas("img/cmd/3.png"))
    img_cmd.append(AzobopiCanvas("img/cmd/4.png"))

    # Instâncias de botões e sua criação
    button_simples = AzobopiButton(100, 160, "Simples", '#ff6600', lambda: update_init(1), "img/simples.png")
    button_simples.button_create(280, 500)
    button_avancado = AzobopiButton(100, 160, "Avançado", "#003399", lambda: update_init(10), "img/avancado.png")
    button_avancado.button_create(480, 500)

    # Botões de Comando
    button_red = AzobopiButton(50, 50, "red", "#f2f2f2", lambda: add_command(4), "img/button_new/red.png")
    button_blue = AzobopiButton(50, 50, "blue", "#f2f2f2", lambda: add_command(1), "img/button_new/blue.png")
    button_green = AzobopiButton(50, 50, "green", "#f2f2f2", lambda: add_command(2), "img/button_new/green.png")
    button_yellow_left = AzobopiButton(50, 50, "yellow", "#f2f2f2", lambda: change_state(),
                                       "img/button_new/yellow_start.png")
    button_yellow = AzobopiButton(50, 50, "yellow", "#f2f2f2", lambda: add_command(3), "img/button_new/yellow.png")

    # Um pouco de som
    mixer.music.load('img/sound.wav')
    mixer.music.play(-1)

    # E jogamos
    game()
    mainloop()
