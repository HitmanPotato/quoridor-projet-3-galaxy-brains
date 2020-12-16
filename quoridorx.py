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
        '''method docstring'''
        window = turtle.Screen()
        window.title('Quoridor')
        window.setup(width=800, height=600)
        grid = turtle.Turtle()
        grid.speed('fastest')
        grid.pensize(1)
        grid.pencolor('black')


        def square(side_length):
            '''function docstring'''
            for i in range(4):
                dot = (side_length / 12)
                for j in range(4):
                    grid.forward(dot)
                    grid.penup()
                    grid.forward(dot)
                    grid.pendown()
                    grid.forward(dot)
                grid.left(90)

        def row(col_size, side_length):
            '''function docstring'''
            for i in range(col_size):
                square(side_length)
                grid.penup()
                grid.forward(side_length)
                grid.pendown()
            grid.penup()
            grid.left(180)
            grid.forward(col_size * side_length)
            grid.left(180)
            grid.pendown()

        def row_of_rows(row_size, col_size, side_length):
            '''function docstring'''
            for i in range(2):
                grid.forward(side_length * col_size)
                grid.left(90)
                grid.forward(side_length * row_size)
                grid.left(90)
            for i in range(row_size):
                row(col_size, side_length)
                grid.penup()
                grid.left(90)
                grid.forward(side_length)
                grid.right(90)
                grid.pendown()
            grid.hideturtle()
            grid.penup()
            grid.right(90)
            grid.forward(row_size * side_length)
            grid.left(90)
            grid.pendown()
        
        # Positioning player 1
        player1 = turtle.Turtle()
        window.tracer(False)
        player1.penup()
        player1.setx((self.etat['joueurs'][0]['pos'][0] - 5) * 30)
        player1.sety((self.etat['joueurs'][0]['pos'][1] - 5) * 30)
        player1.pendown()
        window.tracer(True)
        player1.dot(10, 'blue')
        player1.hideturtle()
        
        # Positioning player 2
        player2 = turtle.Turtle()
        window.tracer(False)
        player2.penup()
        player2.setx((self.etat['joueurs'][1]['pos'][0] - 5) * 30)
        player2.sety((self.etat['joueurs'][1]['pos'][1] - 5) * 30)
        player2.pendown()
        window.tracer(True)
        player2.dot(10, 'red')
        player2.hideturtle()

        
        # Centering the grid
        grid.penup()
        grid.backward(135)
        grid.left(90)
        grid.backward(135)
        grid.right(90)
        grid.pendown()

        # Drawing the grid
        grid.hideturtle()
        window.tracer(False)
        row_of_rows(9, 9, 30)
        window.tracer(True)
        grid.hideturtle()
        window.mainloop()

        # Placing the players

if __name__ == '__main__':
    game = QuoridorX(['player', 'robot'])
    game.déplacer_jeton(1, (5, 2))
    game.afficher()
