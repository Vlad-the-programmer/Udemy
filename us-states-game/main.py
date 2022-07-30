import turtle
from game import Game

screen = turtle.Screen()
screen.title("U.S States Game")
image = "blank_states_img.gif"
screen.addshape(image)
turtle.shape(image)

game = Game()

turtle.onscreenclick(game.get_mouse_click_cor)
guessed_states = []


while len(guessed_states) < 50:
    answer_input = screen.textinput(title=f"{len(guessed_states)}/50 States Correct",
                                    prompt="What's another state's name?").title()
    if answer_input == 'Exit':
        game.unguessed_states(guessed_states)
        break

    game.check_file_states(answer_input, guessed_states)

turtle.mainloop()
