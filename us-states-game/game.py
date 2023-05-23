from turtle import Turtle, Screen
import pandas

states_cords = pandas.read_csv("50_states.csv")
ALL_STATES = states_cords.state.to_list()


class Game(Turtle):
    def __init__(self):
        super().__init__()

    def get_mouse_click_cor(self, x, y):
        print(x, y)

    def check_file_states(self, answer, answers_list):

        all_states = states_cords.state.to_list()

        if answer in all_states:
            answers_list.append(answer)

        t = Turtle()
        t.hideturtle()
        t.penup()
        state_data = states_cords[states_cords.state == answer]
        t.goto(int(state_data.x), int(state_data.y))
        t.write(answer)


def unguessed_states(self, guessed_states):
    missing_state = [state for state in ALL_STATES if state not in guessed_states]
    new_data = pandas.DataFrame(missing_state)
    new_data.to_csv("states_to_learn.csv")
