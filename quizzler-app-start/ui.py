from tkinter import *
from quiz_brain import QuizBrain

THEME_COLOR = "#375362"
FONT = ("Arial", 20, "italic")


class QuizInterface:
    def __init__(self, quiz_brain: QuizBrain):
        self.quiz = quiz_brain
        self.window = Tk()
        self.window.title("Quizzler")
        self.window.config(padx=20, pady=20, bg=THEME_COLOR)

        self.score_label = Label(text="Score: 0", fg="white", bg=THEME_COLOR)
        self.score_label.grid(row=0, column=1)

        self.canvas = Canvas(width=300, height=250, bg="white")
        self.question_text = self.canvas.create_text(150,
                                                     125,
                                                     width= 280,
                                                     text='Text',
                                                     fill=THEME_COLOR,
                                                     font=FONT
                                                     )

        self.canvas.grid(row= 1, column= 0, columnspan=2, pady=50)

        true_image = PhotoImage(file="images/true.png")

        self.green_button = Button(image=true_image, highlightthickness=0, command=self.true_button)
        self.green_button.grid(row=2, column=0)

        false_image = PhotoImage(file="images/false.png")
        self.red_buttton = Button(image=false_image, highlightthickness=0, command=self.wrong_button)
        self.red_buttton.grid(row=2, column=1)
        self.get_next_question()

        self.window.mainloop()

    def get_next_question(self):
        self.canvas.config(bg="white")

        if self.quiz.still_has_questions():
            self.score_label.config(text=f"Score: {self.quiz.score}")
            q_text = self.quiz.next_question()
            self.canvas.itemconfig(self.question_text, text=q_text)
        else:
            self.canvas.itemconfig(self.question_text, text="You've reached the end of the quiz")
            self.green_button.config(state="disabled")
            self.red_buttton.config(state="disabled")

    def true_button(self):
       self.give_feedback(self.quiz.check_answer("True"))


    def wrong_button(self):
        is_right = self.quiz.check_answer("False")
        self.give_feedback(is_right)

    def give_feedback(self, is_right):

        if is_right:
            self.canvas.config(bg="green")
        else:
            self.canvas.config(bg="red")

        self.window.after(1000, self.get_next_question)


