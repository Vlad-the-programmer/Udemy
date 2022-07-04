from turtle import Turtle

STARTING_POSITION = (0, -280)
MOVE_DISTANCE = 10
FINISH_LINE_Y = 280


class Player(Turtle):
    def __init__(self):
        super().__init__()
        self.create_player()

    def create_player(self):
        self.shape("turtle")
        self.penup()
        self.go_to_start()
        self.setheading(90)

    def go_to_start(self):
        self.goto(STARTING_POSITION)

    def go_up(self):
        self.forward(MOVE_DISTANCE)

    def is_at_finished_line(self):
        if self.ycor() > FINISH_LINE_Y:
            return True
        elif self.ycor() < FINISH_LINE_Y:
            return False


