from tkinter import *
from tkinter import ttk
from PIL import Image, ImageDraw


root = Tk()
root.geometry('600x600')
frm = ttk.Frame(root, padding=5)
frm.grid()

label1 = ttk.Label(frm, text='Hello user!').grid(row=1, column=4)





root.mainloop()