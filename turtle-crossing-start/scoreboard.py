from turtle import Turtle

FONT = ("Courier", 22, "normal")


class Scoreboard(Turtle):
    def __init__(self):
        super().__init__()
        self.level = 1
        self.hideturtle()
        self.penup()
        self.goto(-280, 250)
        self.update_scoreboard()

    def update_scoreboard(self):
        self.clear()
        self.write(f"Level: {self.level} ", font=FONT, align="left")

    def increase_level(self):
        self.level += 1
        self.update_scoreboard()

    def game_over_lost(self):
        self.goto(-100, 0)
        self.write(f"Game is over!\n You have lost!", font=FONT, align="left")




