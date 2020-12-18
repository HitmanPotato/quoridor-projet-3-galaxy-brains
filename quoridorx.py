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
        # Screen setup
        win = turtle.Screen()
        win.title('Quoridor Game')
        win.bgcolor('lightgreen')
        win.setup(width=800, height=600)
        win.tracer(0)

        # Background grid
        grid = turtle.Turtle()
        side_length = 30
        # Centering the grid
        grid.penup()
        grid.backward(side_length * 9 / 2)
        grid.left(90)
        grid.backward(side_length * 9 / 2)
        grid.right(90)
        grid.pendown()
        # Draw full exterior lines
        for i in range(4):
            grid.forward(side_length * 9)
            grid.left(90)
        # Legend information
        pen = turtle.Turtle()
        pen.speed(0)
        pen.shape('square')
        pen.color('black')
        pen.penup()
        pen.hideturtle()
        pen.goto(-(side_length*9/2), (side_length*9/2) + 15)
        pen.write('Hello i am pen')
        # Drawing dotted grid
        def draw_square():
            for i in range(4):
                for j in range(4):
                    grid.forward(side_length / 12)
                    grid.penup()
                    grid.forward(side_length / 12)
                    grid.pendown()
                    grid.forward(side_length / 12)
                grid.left(90)

        for j in range(9):
            for i in range(9):
                draw_square()
                grid.penup()
                grid.forward(side_length)
                grid.pendown()
            grid.penup()
            grid.backward(9 * side_length)
            grid.left(90)
            grid.forward(side_length)
            grid.right(90)
        grid.hideturtle()
        
        # Positioning player 1
        p1 = turtle.Turtle()
        p1.speed(0)
        p1.shape('circle')
        p1.color('blue')
        p1.penup()
        p1.setx((self.etat['joueurs'][0]['pos'][0] - 5) * 30)
        p1.sety((self.etat['joueurs'][0]['pos'][1] - 5) * 30)
        p1.pendown()
        win.tracer(True)
        p1.showturtle()
        win.tracer(False)
        
        # Positioning player 2
        p2 = turtle.Turtle()
        p2.speed(0)
        p2.shape('circle')
        p2.color('red')
        p2.penup()
        p2.setx((self.etat['joueurs'][1]['pos'][0] - 5) * 30)
        p2.sety((self.etat['joueurs'][1]['pos'][1] - 5) * 30)
        p2.pendown()
        win.tracer(True)
        p2.showturtle()
        win.tracer(False)

        win.mainloop()
        win.update()
        turtle.exitonclick()

if __name__ == '__main__':
    game = QuoridorX(['player', 'robot'])
