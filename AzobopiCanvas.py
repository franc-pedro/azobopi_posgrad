from tkinter import PhotoImage
from AzobopiGrid import *

import time


# Classe responsável pelos objectos do canvas
# Entrada - img - a imagem a usar
# Criação de instância do objecto
# Herda métodos da classe AzobopiGrid
class AzobopiCanvas(AzobopiGrid):
    def __init__(self, img):
        super().__init__()
        self.restart = None
        self.img = img
        self.imagem = PhotoImage(file=self.img)
        self.posx = 0
        self.posy = 0
        self.gridx = 0
        self.gridy = 0
        self.id_img = None

    # Função para criar uma imagem no canvas
    # :param x1: posição x da imagem no canvas
    # :param y1: posição y da imagem no canvas
    # :param canvas: A área do jogo
    # :param anchor: posição relativa na grelha
    # :return: retorna o id da imagem
    def create_img(self, x1, y1, canvas, anchor):
        id_img = canvas.create_image(x1, y1, image=self.imagem, anchor=anchor)
        return id_img  # retornamos o id da imagem

    # Função para actualizar uma imagem no canvas
    # :param canvas: A área do jogo
    # :param imagem: A nova imagem  no canvas
    # :return: retorna o id da imagem
    def update_img(self, canvas, imagem):
        id_img = canvas.itemconfig(imagem, image=self.imagem)
        return id_img

    # Função responsável pelo movimento do azobopi
    # :param canvas: A área do jogo
    # :param robot: instância do azobopi
    # :param amount: distância a percorrer pelo azobopi
    # :param direction: direcção do movimento (1,2,3,4)
    # :param star: posição e id da estrela
    # :param trees: lista com posições e id das árvores
    # :param restart: reinicialização da posição do azobopi
    # :param grid_large: que tipo de grelha (5x5, 10x10)
    # :return: retorna Out, Tree, ou Star consoante o movimento
    def move(self, canvas, robot, amount, direction, star, trees, restart=False, grid_large=False):
        if restart:
            self.posx = 0
            self.posy = 0
        if grid_large:
            # valores para compensar o encontro do azobopi com outros objectos
            x = 25
            y = 25
        else:
            x = 50
            y = 50
        for k in range(amount):
            mov = AzobopiGrid.movement(direction)
            self.posx = self.posx + mov[0]
            self.posy = self.posy + mov[1]
            # Estamos dentro, encontrámos a estrela ou árvores?
            robot_inside = AzobopiGrid.inside(self.posx, self.posy)
            robot_star = AzobopiGrid.find_star(self.posx + x, self.posy + y, star)
            robot_tree = AzobopiGrid.find_trees(self.posx + x, self.posy + y, trees)
            # Não encontrámos nada vamos em frente
            if not robot_star:
                if not robot_tree:
                    if robot_inside:
                        time.sleep(0.025)
                        canvas.move(robot, mov[0], mov[1])
                        canvas.update()
                    # Encontrámos alguma coisa paramos e anunciamos
                    else:
                        return "Out"
                else:
                    return "Tree"
            else:
                return "Star"

    # Função para criação da estrela e árvores
    # :param canvas: A área do jogo
    # :param grid: O tipo de grelha
    # :param imagem: imagem do objecto a inserir "tree" ou "star"
    # :param star: id e posição da estrela
    # :param trees: lista com id's e poisções das estrelas
    # :return: posição e id da imagem criada
    def item_create(self, canvas, grid, imagem, star=None, trees=None):
        random_pos = AzobopiGrid.random_position(grid, imagem)
        while 1:  # Tentamos que a posição gerada aleatoriamente não coincide com a estrela nem as árvores
            if AzobopiGrid.find_star(random_pos[0], random_pos[1], star):
                random_pos = AzobopiGrid.random_position(grid, imagem)
            elif AzobopiGrid.find_trees(random_pos[0], random_pos[1], trees):
                random_pos = AzobopiGrid.random_position(grid, imagem)
            else:
                break
        # Criamos a imagem
        self.id_img = canvas.create_image(random_pos[0], random_pos[1], image=self.imagem, anchor="center")
        return random_pos[0], random_pos[1], self.id_img
