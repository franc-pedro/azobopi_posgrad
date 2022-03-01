from tkinter import PhotoImage, Button
import tkinter.font as font


# Class para criação do botões
# Entrada
# (x2, y2)-altura e largura do botão
# text-texto a ser inserido no botão
# color-cor de fundo do botão
# command - comando a ser executado pelo botão
# imagem - se existir a imagem a ser inserida no botão
class AzobopiButton:
    def __init__(self, x2, y2, text="", color="", command='', imagem=""):
        self.buttonFont = font.Font(family='Tahoma', size=15)
        if imagem:
            self.buttonImage = PhotoImage(file=imagem)
            self.button_cr = Button(text=text, font=self.buttonFont, height=x2, width=y2, bg=color, fg='White',
                                    command=command, image=self.buttonImage)
        else:
            self.button_cr = Button(text=text, font=self.buttonFont, height=x2, width=y2, bg=color, fg='White',
                                    command=command)

    # Criamos um botão
    # :param x1: posição x do botão
    # :param y1: posição y do botão
    def button_create(self, x1, y1):
        self.button_cr.place(x=x1, y=y1)

    # Escondemos o botão
    def button_hide(self):
        self.button_cr.place_forget()
