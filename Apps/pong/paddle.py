from turtle import Turtle

class Paddle(Turtle):

    def __init__(self, position):
        super().__init__()
        self.color('white')
        self.penup()
        self.shape('square')
        self.turtlesize(5, 1)
        self.goto(position)

    def go_up(self):
        self.goto(self.xcor(), (self.ycor() + 20))

    def go_down(self):
        self.goto(self.xcor(), (self.ycor() - 20))
