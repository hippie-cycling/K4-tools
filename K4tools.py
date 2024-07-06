import tkinter as tk
from tkinter import ttk

class CryptoToolGUI:
    def __init__(self, master):
        self.master = master
        master.title("K4 toolkit")

        self.create_widgets()

    def create_widgets(self):
    # Input frames
        self.single_input_frame = self.create_labeled_frame("Single Input Operations", 0, 0)
        self.double_input_frame = self.create_labeled_frame("Double Input Operations", 0, 1)
        
        # Single input widgets
        self.input_text = self.create_text_widget(self.single_input_frame, "Input", 1, 0)
        self.alphabet_text = self.create_text_widget(self.single_input_frame, "Alphabet", 3, 0)
        
        self.shift = tk.IntVar()
        self.create_dropdown(self.single_input_frame, "Shift", self.shift, range(1, 27), 5, 0)
        
        # Double input widgets
        self.input1_text = self.create_text_widget(self.double_input_frame, "Input 1", 1, 0)
        self.input2_text = self.create_text_widget(self.double_input_frame, "Input 2", 3, 0)
        
        self.operation = tk.StringVar()
        self.create_dropdown(self.double_input_frame, "Operation", self.operation, 
                            ["AND", "OR", "NOT", "NAND", "NOR", "XOR"], 5, 0)

        # Output frame
        self.output_frame = self.create_labeled_frame("Output", 1, 0, columnspan=2)
        self.output_text = self.create_text_widget(self.output_frame, "", 0, 0, 
                                                height=20, width=100, bg="#88C0D0", 
                                                font=("Cambria", 12))

        # Buttons
        self.create_button(self.single_input_frame, "IoC", self.ioc, 2, 0)
        self.create_button(self.single_input_frame, "Reverse", self.reverse, 2, 1)
        self.create_button(self.single_input_frame, "Transpose", self.transposition, 5, 1)
        self.create_button(self.single_input_frame, "Morse", self.get_morse_code, 2, 2)
        self.create_button(self.single_input_frame, "Invert Morse", self.convert_to_opposite_morse, 2, 3)
        
        self.create_button(self.double_input_frame, "Calculate", self.boolean_operations, 5, 1)
        self.create_button(self.double_input_frame, "Base 5 Addition", self.base5_addition, 5, 2)
        
        self.create_button(self.output_frame, "Clear", self.clear_output, 1, 0)

    def create_labeled_frame(self, text, row, column, **kwargs):
        frame = ttk.LabelFrame(self.master, text=text)
        frame.grid(row=row, column=column, padx=5, **kwargs)
        return frame

    def create_text_widget(self, parent, label_text, row, column, **kwargs):
        if label_text:
            ttk.Label(parent, text=label_text).grid(row=row-1, column=column, padx=5)
        
        # Default values
        default_kwargs = {
            'height': 3,
            'width': 50,
            'font': ("Cambria", 8)
        }
        # Update default values with any provided kwargs
        default_kwargs.update(kwargs)
        
        text_widget = tk.Text(parent, **default_kwargs)
        text_widget.grid(row=row, column=column, padx=5, columnspan=8, sticky='nsew')
        return text_widget

    def create_dropdown(self, parent, label_text, variable, values, row, column):
        ttk.Label(parent, text=label_text).grid(row=row-1, column=column, padx=5)
        ttk.OptionMenu(parent, variable, values[0], *values).grid(row=row, column=column)

    def create_button(self, parent, text, command, row, column):
        ttk.Button(parent, text=text, command=command).grid(row=row, column=column, pady=5)

    # Implement your crypto functions here (ioc, reverse, transposition, etc.)
    # Make sure to update them to use self.input_text, self.output_text, etc.

    def convert_to_opposite_morse(self):
        input_text = self.input_text.get("1.0", 'end-1c')
        morse_dict = {
            'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.',
            'G': '--.', 'H': '....', 'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..',
            'M': '--', 'N': '-.', 'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.',
            'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-',
            'Y': '-.--', 'Z': '--..'}

        morse_input = ''.join(morse_dict.get(char, '') + ' ' for char in input_text.upper())
        inverted_morse = ''.join('.' if char == '-' else '-' if char == '.' else char for char in morse_input)

        reverse_morse_dict = {v: k for k, v in morse_dict.items()}
        output = ''.join(reverse_morse_dict.get(code, ' ') for code in inverted_morse.split())

        self.output_text.insert("1.0", f"\nReversed Morse: {output.strip()}")

    def get_morse_code(self):
        input_text = self.input_text.get("1.0", 'end-1c')
        morse_dict = {
            'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.',
            'G': '--.', 'H': '....', 'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..',
            'M': '--', 'N': '-.', 'O': '---', 'P': '.--.',  'Q': '--.-', 'R': '.-.',
            'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-',
            'Y': '-.--', 'Z': '--..', ' ': ' '
        }
        
        morse_code = ''
        total_dots = total_dashes = 0
        for char in input_text.upper():
            if char in morse_dict:
                code = morse_dict[char]
                morse_code += code + ' '
                total_dots += code.count('.')
                total_dashes += code.count('-')
            else:
                morse_code += 'Invalid character '

        self.output_text.insert("1.0", f"\n{morse_code.strip()}\nDots: {total_dots}, Dashes: {total_dashes}")

    def transposition(self):
        input_text = self.input_text.get("1.0", 'end-1c')
        step = self.shift.get()
        alphabet = self.alphabet_text.get("1.0", 'end-1c').upper()
        
        shifted_str = ""
        for char in input_text:
            if char.isalpha():
                index = alphabet.index(char.upper())
                shifted_index = (index + step) % len(alphabet)
                shifted_str += alphabet[shifted_index].lower() if char.islower() else alphabet[shifted_index]
            else:
                shifted_str += char

        self.output_text.insert("1.0", f"\n{shifted_str}")

    def ioc(self):
        input_text = self.input_text.get("1.0", 'end-1c')
        char_counts = {}
        for char in input_text:
            char_counts[char] = char_counts.get(char, 0) + 1

        n = sum(char_counts.values())
        numerator = sum(count * (count - 1) for count in char_counts.values())
        denominator = n * (n - 1)
        ic = numerator / denominator if denominator != 0 else 0

        self.output_text.insert("1.0", f"\n{input_text}\nIoC (English): {ic:.4f}")

    def reverse(self):
        input_text = self.input_text.get("1.0", 'end-1c')
        reversed_text = input_text[::-1]
        self.output_text.insert("1.0", f"\nReversed output: {reversed_text}")

    def boolean_operations(self):
        op = self.operation.get()
        cypher = self.input1_text.get("1.0", 'end-1c')
        dictionary = self.input2_text.get("1.0", 'end-1c')

        ascii_dict = {
        'A': '00001', 'B': '00010', 'C': '00011', 'D': '00100', 'E': '00101',
        'F': '00110', 'G': '00111', 'H': '01000', 'I': '01001', 'J': '01010',
        'K': '01011', 'L': '01100', 'M': '01101', 'N': '01110', 'O': '01111',
        'P': '10000', 'Q': '10001', 'R': '10010', 'S': '10011', 'T': '10100',
        'U': '10101', 'V': '10110', 'W': '10111', 'X': '11000', 'Y': '11001',
        'Z': '11010'
    }
        reverse_ascii_dict = {v: k for k, v in ascii_dict.items()}

        # Convert the input strings to binary
        binary1 = ''.join(ascii_dict[char] for char in cypher)
        binary2 = ''.join(ascii_dict[char] for char in dictionary)

        # Perform boolean operations on the binary strings
        if op == "XOR":
            result_binary = ''.join('1' if bit1 != bit2 else '0' for bit1, bit2 in zip(binary1, binary2))
        elif op == "AND":
            result_binary = ''.join('1' if bit1 == '1' and bit2 == '1' else '0' for bit1, bit2 in zip(binary1, binary2))
        elif op == "OR":
            result_binary = ''.join('1' if bit1 == '1' or bit2 == '1' else '0' for bit1, bit2 in zip(binary1, binary2))
        elif op == "NOT":
            result_binary = ''.join('1' if bit == '0' else '0' for bit in binary1)
        elif op == "NOR":
            result_binary = ''.join('0' if bit1 == '1' or bit2 == '1' else '1' for bit1, bit2 in zip(binary1, binary2))
        elif op == "NAND":
            result_binary = ''.join('0' if bit1 == '1' and bit2 == '1' else '1' for bit1, bit2 in zip(binary1, binary2))
        else:
            result_binary = ''

        result_text = ''
        for i in range(0, len(result_binary), 5):
            chunk = result_binary[i:i+5]
            if chunk == '00000' or chunk == "11111":
                result_text += next(key for key, value in ascii_dict.items() if value == binary1[i:i+5])
            elif chunk in ascii_dict.values():
                result_text += next(key for key, value in ascii_dict.items() if value == chunk)
            else:
                result_text += next(key for key, value in ascii_dict.items() if value == binary1[i:i+5])

        self.output_text.insert("1.0", f"\nCalculated {op} output: {result_text}")

    def base5_addition(self):
        cypher = self.input1_text.get("1.0", 'end-1c')
        dictionary = self.input2_text.get("1.0", 'end-1c')

        base5_dict = {chr(65+i): f'{i//5}{i%5}' for i in range(26)}
        base5_dict['W'] = '00'  # Special case for 'W'

        num1 = ''.join(base5_dict[char] for char in cypher.upper() if char in base5_dict)
        num2 = ''.join(base5_dict[char] for char in dictionary.upper() if char in base5_dict)

        result = ''.join(str((int(d1) + int(d2)) % 5) for d1, d2 in zip(num1, num2))

        reverse_base5_dict = {v: k for k, v in base5_dict.items()}
        letters = ''.join(reverse_base5_dict.get(result[i:i+2], '?') for i in range(0, len(result), 2))

        self.output_text.insert("1.0", f"\nBase 5 mod 26 addition: {letters}")

    def clear_output(self):
        self.output_text.delete("1.0", tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    app = CryptoToolGUI(root)
    root.mainloop()