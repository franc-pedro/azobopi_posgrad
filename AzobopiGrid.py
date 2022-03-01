import random
import numpy as np

# Conjunto de métodos relativos à grelha do jogo
class AzobopiGrid:

    @classmethod
    def inside(cls, posx, posy):
        """
        Função para determinar se o azobopi se encontra na grelha
        :param posx: posição x do azobopi
        :param posy: posição y do azobopi
        :return: False se estiver fora , True se estiver dentro
        """
        if posx < 0 or posy < 0:
            return False
        elif posy < 0:
            return False
        elif posx > 400:
            return False
        elif posy > 400:
            return False
        else:
            return True

    @classmethod
    def find_star(cls, posx, posy, star):
        """
        Função que determina se o azobopi encontrou a estrela
        :param posx: posição x do azobopi
        :param posy: posição y do azobopi
        :param star: poisiçaõ da estrela
        :return: False se não encontrámos a estrela, True caso contrário
        """
        if star is None:
            return False
        if posx == star[0] and posy == star[1]:
            return True
        return False

    @classmethod
    def find_trees(cls, posx, posy, trees):
        """
        Função que determina se o azobopi encontrou uma árvore
        :param posx: posição x do azobopi
        :param posy: posição y do azobopi
        :param trees: lista com as posições das árvores
        :return: False se não encontrámos árvores, True caso contrário
        """
        if trees is None:
            return False
        for i in range(len(trees)):
            if trees[i][0] == posx and trees[i][1] == posy:
                return True
        return False

    @classmethod
    def random_position(cls, grid_type, imagem):
        """
        Função para produzir uma posição aleatória na grelha
        :param grid_type: Tipo da grelha 1 - 5x5 ou 10 - 10x10
        :param imagem: Tipo da imagem ou estrela - star ou árvore - tree
        :return: posição aleatória para o objecto
        """
        if grid_type == 1:
            if imagem == "star":
                gridx = np.arange(250, 550, 100).tolist()
                gridy = np.arange(250, 550, 100).tolist()
            else:
                gridx = np.arange(50, 550, 100).tolist()
                gridy = np.arange(150, 550, 100).tolist()
        else:
            if imagem == "star":
                gridx = np.arange(225, 450, 50).tolist()
                gridy = np.arange(225, 450, 50).tolist()
            else:
                gridx = np.arange(25, 450, 50).tolist()
                gridy = np.arange(75, 450, 50).tolist()
        posx = random.choice(gridx)
        posy = random.choice(gridy)
        return posx, posy

    @classmethod
    def movement(cls, direction):
        """
        Função que produz o movimento do azobopi
        :param direction: Direcção do movimento 1-N, 2-E, 3-S, 4-W
        :return: valor a acrescentar ou retirar ao movimento do azobopi
        """
        if direction == 1:
            x = 0
            y = -1
        elif direction == 2:
            x = 1
            y = 0
        elif direction == 3:
            x = 0
            y = 1
        else:
            x = -1
            y = 0
        return x, y
