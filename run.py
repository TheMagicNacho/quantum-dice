from tkinter import *
from tkinter.ttk import Combobox
from qiskit import IBMQ
import qiskit
import math

# THIS PART IS THE QUANTUM SHIT SO PUCKER YOUR BUTTHOLES
_backend = qiskit.BasicAer.get_backend('qasm_simulator')
_circuit = None
_bitCache = ''


def setqbits(n):
    global _circuit
    qr = qiskit.QuantumRegister(n)
    cr = qiskit.ClassicalRegister(n)
    _circuit = qiskit.QuantumCircuit(qr, cr)
    _circuit.h(qr)  # Apply Hadamard gate to qubits
    _circuit.measure(qr, cr)  # Collapses qubit to either 1 or 0 w/ equal prob.


setqbits(8)  # Default Circuit is 8 Qubits


def set_backend(b='qasm_simulator'):
    global _backend
    if b == 'ibmqx4' or b == 'ibmqx5':
        _backend = IBMQ.get_backend(b)
        setqbits(5)
    elif b == 'ibmq_16_melbourne':
        _backend = IBMQ.get_backend(b)
        setqbits(16)
    elif b == 'ibmq_qasm_simulator':
        _backend = IBMQ.get_backend(b)
        setqbits(32)
    else:
        _backend = qiskit.BasicAer.get_backend('qasm_simulator')
        setqbits(8)


# Strips QISKit output to just a bitstring.
def bitcount(counts):
    return [k for k, v in counts.items() if v == 1][0]


# Populates the bitCache with at least n more bits.
def _request_bits(n):
    global _bitCache
    iterations = math.ceil(n / _circuit.width())
    for _ in range(iterations):
        # Create new job and run the quantum circuit
        job = qiskit.execute(_circuit, _backend, shots=1)
        _bitCache += bitcount(job.result().get_counts())


# Returns a random n-bit string by popping n bits from bitCache.
def bitstring(n):
    global _bitCache
    if len(_bitCache) < n:
        _request_bits(n - len(_bitCache))
    bitString = _bitCache[0:n]
    _bitCache = _bitCache[n:]
    return bitString


# Returns a random integer between and including [min, max].
# Running time is probabalistic but complexity is still O(n)
def randint(min, max):
    delta = max - min
    n = math.floor(math.log(delta, 2)) + 1
    result = int(bitstring(n), 2)
    while (result > delta):
        result = int(bitstring(n), 2)
    return result + min


def roll(nb_dice, nb_face):
    roll_list = []
    for i in range(nb_dice):
        roll_list.append(randint(1, nb_face))
    return roll_list


root = Tk()


class App:
    # define the widgets
    def __init__(self, master):
        self.title = Label(master, fg="black", text="The Quantum Dice", font=('arial', 40))
        self.nb_dices_entry = Combobox(master,
                                       values=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20])
        self.nb_faces_entry = Combobox(master, values=[4, 6, 10, 12, 20])
        self.mod_entry = Combobox(master,
                                  values=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20])
        self.nb_dices_label = Label(master, fg="black", text="How many dices? ", font=('arial', 20))
        self.nb_faces_label = Label(master, fg="black", text="How many side?", font=('arial', 20))
        self.mod_label = Label(master, fg="black", text="Would you like to include a modifier?", font=('arial', 20))
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
