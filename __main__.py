from tkinter import *
from tkinter.ttk import Combobox
import diceq


def roll(nb_dice, nb_face):
    roll_list = []
    for i in range(nb_dice):
        roll_list.append(diceq.randint(1, nb_face))
    return roll_list

root = Tk()

class App:
#define the widgets
    def __init__(self, master):
        self.title = Label(master, fg="black", text="The Quantum Dice", font=('times', 40))
        self.nb_dices_entry = Combobox(master, values=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20])
        self.nb_faces_entry = Combobox(master, values=[4, 6, 10, 12, 20])
        self.mod_entry = Combobox(master, values=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20])
        self.nb_dices_label = Label(master, fg="black", text="How many dices? ", font=('times', 20))
        self.nb_faces_label = Label(master, fg="black", text="How many side?", font=('times', 20))
        self.mod_label = Label(master, fg="black", text="Would you like to include a modifier?", font=('times', 20))
        self.generate_button = Button(master, text="ROLL DICE", command=self.get_output)
        self.list_output_int = Label(master, fg="black", bg="white", text="? ? ?")  # TODO: add text function
        self.mod_output_int = Label(master, fg="black", bg="white", text="0")
        self.final_output_int = Label(master, fg="black", bg="white", text="0")
        self.space = Label(master, fg="black", bg="white", text="")
        self.list_output_lab = Label(master, fg="black", bg="white", text="Dices Thrown: ")  # TODO: add text function
        self.mod_output_lab = Label(master, fg="black", bg="white", text="Modifier: ")
        self.final_output_lab = Label(master, fg="black", bg="white", text="Final: ")

# Call the widgets
        self.title.grid(row=0, columnspan=3)
        self.nb_dices_entry.grid(row=2, column=1)
        self.nb_dices_entry.current(3)
        self.nb_dices_label.grid(row=2, sticky=E)
        self.nb_faces_entry.grid(row=3, column=1)
        self.nb_faces_entry.current(4)
        self.nb_faces_label.grid(row=3, sticky=E)
        self.mod_entry.grid(row=4, column=1)
        self.mod_entry.current(0)
        self.mod_label.grid(row=4, sticky=E)
        self.generate_button.grid(row=6, columnspan=3)
        self.space.grid(row=7, columnspan=3)
        self.list_output_lab.grid(row=8, sticky=E)
        self.list_output_int.grid(row=8, column=1)

        self.mod_output_lab.grid(row=9, sticky=E)
        self.mod_output_int.grid(row=9, column=1)

        self.final_output_lab.grid(row=10, sticky=E)
        self.final_output_int.grid(row=10, column=1)

    def get_output(self):
        nb_dice = int(self.nb_dices_entry.get())
        nb_face = int(self.nb_faces_entry.get())
        output = roll(nb_dice, nb_face)
        mod = int(self.mod_entry.get())
        final = sum(output) + mod
        self.list_output_int["text"] = output
        self.mod_output_int["text"] = mod
        self.final_output_int["text"] = final


app = App(root)

root.mainloop()
