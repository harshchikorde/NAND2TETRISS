import sys
import re
import os

class Parser():
    def __init__(self, rawprogram):
        self.rawprogram = rawprogram

    def cleanup(self, rawprogram):
        """INPUT - Textfile containing all raw assembly instructions.
          OUTPUT - Textfile containing all parsed instructions(sampleparsed.txt)
          Removes all comments as well as before
          and after each instruction also removes
          white spaces before each instruction
          and writes all instruction in file named sampleparsed.txt"""

        with open("D:/nand2tetris/projects/sampleparsed.txt", "a+") as rawprogram_object:
            rawprogram_object.seek(0)
            data = rawprogram_object.read(100)
            if len(data) > 0:
                rawprogram_object.write("\n")
            for eachline in rawprogram:
                if eachline.isspace() == False and eachline.startswith('//') == False:
                    eachline = eachline.split('//')[0]
                    eachline = eachline.lstrip().rstrip()
                    rawprogram_object.write(eachline)
                    rawprogram_object.write("\n")

class SymbolTable():
    def __init__(self, parsedprogram):
        self.parsedprogram = parsedprogram
        self.symbols = self.PREDEFINED_SYMBOLS
        self.next_available_memory_address = 0

    PREDEFINED_SYMBOLS = {
        'SP': 0,
        'LCL': 1,
        'ARG': 2,
        'THIS': 3,
        'THAT': 4,
        'R0': 0,
        'R1': 1,
        'R2': 2,
        'R3': 3,
        'R4': 4,
        'R5': 5,
        'R6': 6,
        'R7': 7,
        'R8': 8,
        'R9': 9,
        'R10': 10,
        'R11': 11,
        'R12': 12,
        'R13': 13,
        'R14': 14,
        'R15': 15,
        'SCREEN': 16384,
        'KBD': 24576
    }
    DEST_MNEMONIC_TO_BITS = {
        None: '000',
        'M': '001',
        'D': '010',
        'MD': '011',
        'DM': '011',
        'A': '100',
        'AM': '101',
        'MA': '101',
        'AD': '110',
        'DA': '110',
        'AMD': '111',
        'MDA': '111',
        'DAM': '111',
        'DMA': '111',
        'MAD': '111',
        'ADM': '111'
    }
    COMP_MNEMONIC_TO_BITS = {
        None: '',
        '0': '0101010',
        '1': '0111111',
        '-1': '0111010',
        'D': '0001100',
        'A': '0110000',
        'M': '1110000',
        '!D': '0001101',
        '!A': '0110001',
        '!M': '1110001',
        '-D': '0001111',
        '-A': '0110011',
        '-M': '1110011',
        'D+1': '0011111',
        '1+D': '0011111',
        'A+1': '0110111',
        '1+A': '0110111',
        'M+1': '1110111',
        '1+M': '1110111',
        'D-1': '0001110',
        '-1+D': '0001110',
        'A-1': '0110010',
        '-1+A': '0110010',
        'M-1': '1110010',
        '-1+M': '1110010',
        'D+A': '0000010',
        'A+D': '0000010',
        'D+M': '1000010',
        'M+D': '1000010',
        'D-A': '0010011',
        '-A+D': '0010011',
        'D-M': '1010011',
        '-M+D': '1010011',
        'A-D': '0000111',
        '-D+A': '0000111',
        'M-D': '1000111',
        '-D+M': '1000111',
        'D&A': '0000000',
        'A&D': '0000000',
        'D&M': '1000000',
        'M&D': '1000000',
        'D|A': '0010101',
        'A|D': '0010101',
        'D|M': '1010101',
        'M|D': '1010101'
    }
    JUMP_MNEMONIC_TO_BITS = {
        None: '000',
        'JGT': '001',
        'JEQ': '010',
        'JGE': '011',
        'JLT': '100',
        'JNE': '101',
        'JLE': '110',
        'JMP': '111'
    }

    # FIRST PASS
    def add_labels(self,parsedprogram):
        """INPUT - Textfile containing all parsed instructions(sampleparsed.txt
          OUTPUT - Updated SymbolTable with LABELS of sampleparsed.txt
          Updates SymbolTable with new labels and their address from parsed assembly instructions file"""
        parsedprogram.seek(0)
        for parsed_program in self.parsedprogram:
            parsed_program = parsed_program.lstrip().rstrip()
            if parsed_program.endswith(")") and parsed_program.startswith("("):
                parsed_program = parsed_program.replace("(", "")
                parsed_program = parsed_program.replace(")", "")
                self.symbols[parsed_program] = self.next_available_memory_address
                self.next_available_memory_address = self.next_available_memory_address - 1
            self.next_available_memory_address += 1
        print("SymbolTable after LABEL entry \n", self.symbols)  # View all the labels for confirmation


    def add_variables(self, parsedprogram):
        """INPUT - Textfile containing all parsed instructions(sampleparsed.txt
          OUTPUT - Updated SymbolTable with VARIABLES of sampleparsed.txt
          Updates SymbolTable with new variables and assigns new address from parsed assembly instructions file"""
        parsedprogram.seek(0)
        for a_instr in self.parsedprogram:
            a_instr = a_instr.lstrip().rstrip()
            if a_instr.startswith('@'):
                if a_instr[1:].isdigit() == False:
                    self.symbols.setdefault(a_instr[1:])
        self.next_available_memory_address = 16
        for x, y in self.symbols.items():
            if y == None:
                self.symbols[x] = self.next_available_memory_address
                self.next_available_memory_address += 1
        print("SymbolTable after VARIABLE entry \n", self.symbols)

    def decimal_to_binary_string(self):
        """Converts a numeric string into 16-bit binary word"""
        return '{0:016b}'.format(self)

# SECOND PASS
    def convert_to_machinecode(self,parsedprogram):
        """Converts each parsed instruction into machine-code and writes in an output file named HACK.asm"""
        parsedprogram.seek(0)
        for instr in self.parsedprogram:
            print(instr)
            instr = instr.lstrip().rstrip()
            #Come out of loop if encoutered a LABEL
            if instr.startswith("(") and instr.endswith(")"):
                continue
            #Conversion of A-Type instruction into machinecode( @variable, @23, @RX )
            if instr.startswith('@'):
                #If symbol/Label is follwed by '@' then its a reference to a variable
                if instr[1:].isdigit() == False:
                    value = self.symbols.get(instr[1:])
                    value_b = SymbolTable.decimal_to_binary_string(value)
                # If digit is follwed by '@' then its a reference to General Purpose Register
                elif instr[1:].isdigit() == True:
                    print(instr[1:])
                    value = int(instr[1:])
                    value_b = SymbolTable.decimal_to_binary_string(value)
                print(value_b)
                print("\n")
                # Write generated binary code into file named HACK.asm
                with open(dirname + '/' + basename +'hack.hack','a+') as binary_file:
                    binary_file.write(value_b)
                    binary_file.write("\n")
            else:
                # Conversion of C-Type instruction into machinecode (Destination = Computation ; Jump)
                x = re.split(";", instr)
                # Split for ; symbol

                if len(x) > 1: # For C-instruction of type (Destination = Computation ; Jump)
                    comp = x[0]
                    jmp = x[1]
                    com = re.split("=", comp)
                    if len(com) > 1:
                        dest = com[0]
                        comp = com[1]
                    else: # For C-instruction of type (Computation ; Jump)
                        comp = x[0]
                        dest = None

                else:# For C-instruction of type (Destination = Computation)
                    comp = x[0]
                    com = re.split("=", comp)
                    dest = com[0]
                    comp = com[1]
                    jmp = None
                # Convert into binary by referring the dictionaries of Computation, Destination and Jump
                dst = self.DEST_MNEMONIC_TO_BITS.get(dest)
                cmp = self.COMP_MNEMONIC_TO_BITS.get(comp)
                jp = self.JUMP_MNEMONIC_TO_BITS.get(jmp)
                # Print on Screen for debugging
                print("computation = ", comp, " ", cmp)
                print("Destination = ", dest, " ", dst)
                print("Jump = ", jmp, " ", jp)
                a = '111' + cmp + dst + jp
                print(a)
                print("\n")
                # Write generated binary code into file named HACK.asm
                with open(dirname + '/' + basename +'hack.hack','a+') as binary_file:
                    binary_file.write(a)
                    binary_file.write("\n")


if __name__ == "__main__":
    asm_input_file = sys.argv[-1]
    if sys.argv[-1] == 'asm':
        # Opening the file containing the asssembly program
        path = 'D:/nand2tetris/projects/06/max/Max.asm'
        dirname = os.path.dirname(path)
        basename = os.path.splitext(os.path.basename(path))[0]
        with open(path, 'r') as rawprogram:
            print("Max.txt opened")  # file opened confirmation
            x = Parser(rawprogram)
            x.cleanup(rawprogram) # Call for parsing
        # Opening the temporary file containing the cleaned-up asssembly program
        with open('D:/nand2tetris/projects/sampleparsed.txt', 'r') as parsedprogram:
            print("sampleparsed.txt opened")  # file opened confirmation
            y = SymbolTable(parsedprogram)
            y.add_labels(parsedprogram)# Call for adding labels to symbol table
            print("LABELS added to SymbolTable")
            y.add_variables(parsedprogram) # Call for adding variables to symbol table
            print("VARIABLES added to SymbolTable")
            y.convert_to_machinecode(parsedprogram) # Call for conversion to machine code
            print("""Your assembly language program is been converted to machinecode which is in file named HACK.asm which you can check at 
""" + path)
        # Delete the temporary created reference file sampleparsed.txt
        os.remove('D:/nand2tetris/projects/sampleparsed.txt')