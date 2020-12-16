'''module docstring'''
import turtle
from quoridor import Quoridor


class QuoridorX(Quoridor):
    '''class docstring'''
    def __init__(self, joueurs, murs=None):
        #TODO: création d'une fenêtre graphique et l'affichage d'un damier avec les deux jetons dans leur position initiale
        super().__init__(joueurs, murs)
        self.afficher()

    def afficher(self):
        #TODO: mettre à jour la représentation graphique de l'état actuel du damier.
        pass

def square(side):
    '''function docstring'''
    for i in range(4):
        grid.forward(side)
        grid.left(90)

def row(n, side):
    '''function docstring'''
    for i in range(n):
        square(side)
        grid.forward(side)
    grid.penup()
    grid.left(180)
    grid.forward(n * side)
    grid.left(180)
    grid.pendown()

def row_of_rows(m, n, side):
    '''function docstring'''
    for i in range(m):
        row(n, side)
        grid.penup()
        grid.left(90)
        grid.forward(side)
        grid.right(90)
        grid.pendown()
    grid.penup()
    grid.right(90)
    grid.forward(m * side)
    grid.left(90)
    grid.pendown()

# For testing
if __name__ == '__main__':
    window = turtle.Screen()
    grid = turtle.Turtle()
    grid.speed(1)
    window.colormode(255)
    grid.pensize(1)
    #window.mainloop()
    window.tracer(0)
    grid.hideturtle()
    row_of_rows(10,10, 20)
    window.listen()
