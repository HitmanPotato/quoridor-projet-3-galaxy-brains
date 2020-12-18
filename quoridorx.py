'''module docstring'''
import turtle
from quoridor import Quoridor


class QuoridorX(Quoridor):
    '''class docstring'''
    def __init__(self, joueurs, murs=None):
        super().__init__(joueurs, murs)

        # Screen setup
        self.win = turtle.Screen()
        self.win.title('Quoridor Game')
        self.win.bgcolor('lightgreen')
        self.win.setup(width=800, height=600)
        self.win.tracer(0)

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
        self.p1 = turtle.Turtle()
        self.p1.speed(0)
        self.p1.shape('circle')
        self.p1.color('blue')
        self.p1.hideturtle()
        self.p2 = turtle.Turtle()
        self.p2.speed(0)
        self.p2.shape('circle')
        self.p2.color('red')
        self.p2.hideturtle()
        self.hwall = turtle.Turtle()
        self.hwall.speed(0)
        self.hwall.shape('square')
        self.hwall.color('black')
        self.hwall.pensize(6)
        self.hwall.hideturtle()

        self.vwall = turtle.Turtle()
        self.vwall.speed(0)
        self.vwall.shape('square')
        self.vwall.color('black')
        self.vwall.pensize(6)
        self.vwall.hideturtle()

        # Numbers (columns)
        self.number = turtle.Turtle()
        self.number.penup()
        self.number.goto(-120, -150)
        for i in range(9):
            self.number.pendown()
            self.number.write(str(i))
            self.number.penup()
            self.number.forward(30)
        self.number.hideturtle()

        # Numbers (rows)
        self.number = turtle.Turtle()
        self.number.penup()
        self.number.goto(-145, -125)
        self.number.left(90)
        for i in range(9):
            self.number.pendown()
            self.number.write(str(i))
            self.number.penup()
            self.number.forward(30)
        self.number.hideturtle()
        self.afficher()


    def afficher(self):
        '''method docstring'''
        # Positioning player 1
        self.p1.penup()
        self.p1.setx((self.etat['joueurs'][0]['pos'][0] - 5) * 30)
        self.p1.sety((self.etat['joueurs'][0]['pos'][1] - 5) * 30)
        self.p1.pendown()
        self.win.tracer(True)
        self.p1.showturtle()
        self.win.tracer(False)
        # Positioning player 2
        self.p2.penup()
        self.p2.setx((self.etat['joueurs'][1]['pos'][0] - 5) * 30)
        self.p2.sety((self.etat['joueurs'][1]['pos'][1] - 5) * 30)
        self.p2.pendown()
        self.win.tracer(True)
        self.p2.showturtle()
        self.win.tracer(False)
        # Horizontal walls
        for hwall in self.etat['murs']['horizontaux']:
            # Positioning the turtle at starting coordonates
            self.hwall.penup()
            self.hwall.goto(-135, -135)
            self.hwall.forward((hwall[0] - 1) * 30)
            self.hwall.left(90)
            self.hwall.forward((hwall[1] - 1) * 30)
            self.hwall.right(90)
            # Draw the wall
            self.hwall.pendown()
            self.hwall.forward(60)
            self.hwall.penup()
            self.hwall.goto(-135, -135)
        # Vertical walls
        for vwall in self.etat['murs']['verticaux']:
            # Positioning the turtle at starting coordonates
            self.vwall.penup()
            self.vwall.goto(-135, -135)
            self.vwall.forward((vwall[0] - 1) * 30)
            self.vwall.left(90)
            self.vwall.forward((vwall[1] - 1) * 30)
            # Draw the wall
            self.vwall.pendown()
            self.vwall.forward(60)
            self.vwall.penup()
            self.vwall.goto(-135, -135)
            self.vwall.right(90)
        # Legend information
        pen = turtle.Turtle()
        pen.clear()
        pen.speed(0)
        pen.shape('square')
        pen.color('black')
        pen.penup()
        pen.hideturtle()
        pen.goto(-(30*9/2), (30*9/2) + 15)
        j1 = [self.etat['joueurs'][0]['nom'], self.etat['joueurs'][0]['murs']]
        j2 = [self.etat['joueurs'][1]['nom'], self.etat['joueurs'][1]['murs']]
        if len(j1[0]) >= len(j2[0]):
            lenx = len(j1[0]) + 1
        else:
            lenx = len(j2[0]) + 1
        legende = f'Légende:\n   1={j1[0] + ",":<{lenx}} murs={j1[1]}\n'
        legende += f'   2={j2[0] + ",":<{lenx}} murs={j2[1]}\n'
        legende += f'   {"-" * 35}'
        pen.write(legende)
