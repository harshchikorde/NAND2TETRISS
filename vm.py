import sys
import re
import os
import asm


class code_writer():
    def __init__(self, parsedprogram):
        self.parsedprogram = parsedprogram
        self.arthematic_instr = self.arthematic_instr
        self.memory_access_instr = self.memory_access_instr
        self.program_flow_instr = self.program_flow_instr
        self.function_calling_instr = self.function_calling_instr

    arthematic_instr = ['add', 'sub', 'neg', 'eq', 'gt', 'lt', 'and', 'or', 'not']
    memory_access_instr = ['push', 'pop']
    program_flow_instr = ['label', 'goto', 'if-goto']
    function_calling_instr = ['call', 'function', 'return']
    def instruction_type(self, parsedprogram):
        """Determines the type of instruction and writes the relevant assembly code for the particular VM instruction.
        The relevant assembly code for a particular instruction is stored in the variable 'code'."""
        parsedprogram.seek(0)
        i = 0 # Line count in the code
        count_call = 0 # Count for number of times same function is been called in the code
        for instr in self.parsedprogram:
            #All the code is convertedd into lower case except if it is program flow instruction and function calling code because these are case sensitive
            if any(ele in instr for ele in self.memory_access_instr) or any(ele in instr for ele in self.arthematic_instr) == True:
                instr = instr.lower()
            a = instr.split()
            print(a)
            if any(ele in a for ele in self.memory_access_instr) == True:
                print('memory_access_type')
                type = 'memory_access_type'
            elif any(ele in a for ele in self.arthematic_instr) == True:
                print("arthematic_instr")
                type = 'arthematic_instr'
            elif any(ele in a for ele in self.program_flow_instr) == True:
                print("program_flow_instr")
                type = 'program_flow_instr'
            elif any(ele in a for ele in self.function_calling_instr) == True:
                print("function_calling_instr")
                type = 'function_calling_instr'
            with open(dirname + '/' + basename + '.asm','a+') as rawprogram:
                if type == 'memory_access_type':
                    if a[0] == 'push':
                        segment = a[1]
                        index = a[2]
                        if segment == 'constant':
                            code = '//' + instr + '\n' + '@' + index + '\n' + 'D=A' + '\n' + '@SP' + '\n' + 'A=M' + '\n' + 'M=D' + '\n' + '@SP' + '\n' + 'M=M+1' + '\n' +'\n'
                        elif segment == 'temp':
                            code = '//' + instr + '\n' + '@5' + '\n' + 'D=A' + '\n' + '@' + index + '\n' + 'A=A+D' + '\n' + 'D=M' + '\n' + '@SP' + '\n' + 'A=M' + '\n' + 'M=D' + '\n' + '@SP' + '\n' + 'M=M+1' + '\n' +'\n'
                        elif segment == 'pointer':
                            code = '//' + instr + '\n' + '@3' + '\n' + 'D=A' + '\n' + '@' + index + '\n' + 'A=A+D' + '\n' + 'D=M' + '\n' + '@SP' + '\n' + 'A=M' + '\n' + 'M=D' + '\n' + '@SP' + '\n' + 'M=M+1' + '\n' + '\n'
                        elif segment == 'static':
                            if int(index) > 239:
                                print("Line number: ", i + 1, '\n',"ERROR: Static variable index out of range in: ", instr)
                            else:
                                code = '//' + instr + '\n' + '@' + os.path.basename(path) + '.' + index + '\n' + 'D=M' + '\n' + '@SP' + '\n' + 'M=M+1' + '\n' + 'A=M-1' + '\n' + 'M=D' + '\n' + '\n'
                        elif segment == 'argument':
                            code = '//' + instr + '\n' + '@ARG' + '\n' + 'D=M' + '\n' + '@' + index + '\n' + 'A=A+D' + '\n' + 'D=M' + '\n' + '@SP' + '\n' + 'A=M' + '\n' + 'M=D' + '\n' + '@SP' + '\n' + 'M=M+1' + '\n' + '\n'
                        elif segment == 'local':
                            code = '//' + instr + '\n' + '@LCL' + '\n' + 'D=M' + '\n' + '@' + index + '\n' + 'A=A+D' + '\n' + 'D=M' + '\n' + '@SP' + '\n' + 'A=M' + '\n' + 'M=D' + '\n' + '@SP' + '\n' + 'M=M+1' + '\n' + '\n'
                        elif segment == 'this':
                            code = '//' + instr + '\n' + '@THIS' + '\n' + 'D=M' + '\n' + '@' + index + '\n' + 'A=A+D' + '\n' + 'D=M' + '\n' + '@SP' + '\n' + 'A=M' + '\n' + 'M=D' + '\n' + '@SP' + '\n' + 'M=M+1' + '\n' + '\n'
                        elif segment == 'that':
                            code = '//' + instr + '\n' + '@THAT' + '\n' + 'D=M' + '\n' + '@' + index + '\n' + 'A=A+D' + '\n' + 'D=M' + '\n' + '@SP' + '\n' + 'A=M' + '\n' + 'M=D' + '\n' + '@SP' + '\n' + 'M=M+1' + '\n' + '\n'

                    elif a[0] == 'pop':
                        segment = a[1]
                        index = a[2]
                        if segment == 'constant':
                            print("Line number: ", i + 1, '\n', "ERROR: Invalid instruction: ", instr)
                        if segment == 'temp':
                            code = '//' + instr + '\n' + '@5' + '\n' + 'D=A' + '\n' + '@' + index + '\n' + 'D=A+D' + '\n' + '@R13' + '\n' + 'M=D' + '\n' + '@SP' + '\n' + 'A=M' + '\n' + 'A=A-1' + '\n' + 'D=M' + '\n' + '@R13' + '\n' + 'A=M' + '\n' + 'M=D' + '\n' + '@SP' + '\n' + 'M=M-1' + '\n' + '\n'
                        elif segment == 'pointer':
                            code = '//' + instr + '\n' + '@3' + '\n' + 'D=A' + '\n' + '@' + index + '\n' + 'D=A+D' + '\n' + '@R13' + '\n' + 'M=D' + '\n' + '@SP' + '\n' + 'A=M' + '\n' + 'A=A-1' + '\n' + 'D=M' + '\n' + '@R13' + '\n' + 'A=M' + '\n' + 'M=D' + '\n' + '@SP' + '\n' + 'M=M-1' + '\n' + '\n'
                        elif segment == 'static':
                            if int(index) > 239:
                                print("Line number: ", i + 1, '\n',"ERROR: Static variable index out of range in: ", instr)
                                break
                            else:
                                code = '//' + instr + '\n' + '@SP' + '\n' + 'AM=M-1' + '\n' + 'D=M' + '\n' + '@' + os.path.basename(path) + '.' + index + '\n' + 'M=D' + '\n' + '\n'
                        elif segment == 'argument':
                            code = '//' + instr + '\n' + '@ARG' + '\n' + 'D=M' + '\n' + '@' + index + '\n' + 'D=A+D' + '\n' + '@R13' + '\n' + 'M=D' + '\n' + '@SP' + '\n' + 'A=M' + '\n' + 'A=A-1' + '\n' + 'D=M' + '\n' + '@R13' + '\n' + 'A=M' + '\n' + 'M=D' + '\n' + '@SP' + '\n' + 'M=M-1' + '\n' + '\n'
                        elif segment == 'local':
                            code = '//' + instr + '\n' + '@LCL' + '\n' + 'D=M' + '\n' + '@' + index + '\n' + 'D=A+D' + '\n' + '@R13' + '\n' + 'M=D' + '\n' + '@SP' + '\n' + 'A=M' + '\n' + 'A=A-1' + '\n' + 'D=M' + '\n' + '@R13' + '\n' + 'A=M' + '\n' + 'M=D' + '\n' + '@SP' + '\n' + 'M=M-1' + '\n' + '\n'
                        elif segment == 'this':
                            code = '//' + instr + '\n' + '@THIS' + '\n' + 'D=M' + '\n' + '@' + index + '\n' + 'D=A+D' + '\n' + '@R13' + '\n' + 'M=D' + '\n' + '@SP' + '\n' + 'A=M' + '\n' + 'A=A-1' + '\n' + 'D=M' + '\n' + '@R13' + '\n' + 'A=M' + '\n' + 'M=D' + '\n' + '@SP' + '\n' + 'M=M-1' + '\n' + '\n'
                        elif segment == 'that':
                            code = '//' + instr + '\n' + '@THAT' + '\n' + 'D=M' + '\n' + '@' + index + '\n' + 'D=A+D' + '\n' + '@R13' + '\n' + 'M=D' + '\n' + '@SP' + '\n' + 'A=M' + '\n' + 'A=A-1' + '\n' + 'D=M' + '\n' + '@R13' + '\n' + 'A=M' + '\n' + 'M=D' + '\n' + '@SP' + '\n' + 'M=M-1' + '\n' + '\n'


                elif type == 'arthematic_instr':
                    if a[0] == 'add':
                       code = '//' + instr + '\n' + '@SP' + '\n' + 'A=M' + '\n' + 'A=A-1' + '\n' + 'D=M' + '\n' + 'A=A-1' + '\n' + 'M=M+D' + '\n' + '@SP' + '\n' + 'M=M-1' + '\n' +'\n'
                    elif a[0] == 'sub':
                        code = '//' + instr + '\n' + '@SP' + '\n' + 'A=M' + '\n' + 'A=A-1' + '\n' + 'D=M' + '\n' + 'A=A-1' + '\n' + 'M=M-D' + '\n' + '@SP' + '\n' + 'M=M-1' + '\n' +'\n'
                    elif a[0] == 'and':
                        code = '//' + instr + '\n' + '@SP' + '\n' + 'A=M' + '\n' + 'A=A-1' + '\n' + 'D=M' + '\n' + 'A=A-1' + '\n' + 'M=M&D' + '\n' + '@SP' + '\n' + 'M=M-1' + '\n' +'\n'
                    elif a[0] == 'or':
                        code = '//' + instr + '\n' + '@SP' + '\n' + 'A=M' + '\n' + 'A=A-1' + '\n' + 'D=M' + '\n' + 'A=A-1' + '\n' + 'M=M|D' + '\n' + '@SP' + '\n' + 'M=M-1' + '\n' + '\n'
                    elif a[0] == 'not':
                        code = '//' + instr + '\n' + '@SP' + '\n' + 'A=M' + '\n' + 'A=A-1' + '\n' + 'M=!M' + '\n' + '\n'
                    elif a[0] == 'neg':
                        code = '//' + instr + '\n' + '@SP' + '\n' + 'A=M' + '\n' + 'A=A-1' + '\n' + 'M=-M' + '\n' + '\n'
                    elif a[0] == 'eq':
                        code = '//' + instr + '\n' + '@SP' + '\n' + 'A=M' + '\n' + 'A=A-1' + '\n' + 'D=M' + '\n' + 'A=A-1' + '\n' + 'D=M-D' + '\n' + '@EQ_' + str(i) + '\n' + 'D;JEQ' + '\n' + 'D=0' + '\n' + '@EQ_' + str(i + 1) + '\n' + '0;JMP' + '\n' + '(EQ_' + str(i) + ')' + '\n' + 'D=-1' + '\n' + '(EQ_' + str(i + 1) + ')' + '\n' + '@SP' + '\n' + 'M=M-1' + '\n' + 'A=M' + '\n' + 'A=A-1' + '\n' + 'M=D' + '\n' + '\n'
                    elif a[0] == 'lt':
                        code = '//' + instr + '\n' + '@SP' + '\n' + 'A=M' + '\n' + 'A=A-1' + '\n' + 'D=M' + '\n' + 'A=A-1' + '\n' + 'D=M-D' + '\n' + '@LT_' + str(i) + '\n' + 'D;JLT' + '\n' + 'D=0' + '\n' + '@LT_' + str(i + 1) + '\n' + '0;JMP' + '\n' + '(LT_' + str(i) + ')' + '\n' + 'D=-1' + '\n' + '(LT_' + str(i + 1) + ')' + '\n' + '@SP' + '\n' + 'M=M-1' + '\n' + 'A=M' + '\n' + 'A=A-1' + '\n' + 'M=D' + '\n' + '\n'
                    elif a[0] == 'gt':
                        code = '//' + instr + '\n' + '@SP' + '\n' + 'A=M' + '\n' + 'A=A-1' + '\n' + 'D=M' + '\n' + 'A=A-1' + '\n' + 'D=M-D' + '\n' + '@GT_' + str(i) + '\n' + 'D;JGT' + '\n' + 'D=0' + '\n' + '@GT_' + str(i + 1) + '\n' + '0;JMP' + '\n' + '(GT_' + str(i) + ')' + '\n' + 'D=-1' + '\n' + '(GT_' + str(i + 1) + ')' + '\n' + '@SP' + '\n' + 'M=M-1' + '\n' + 'A=M' + '\n' + 'A=A-1' + '\n' + 'M=D' + '\n' +'\n'

                elif type == 'program_flow_instr':
                    if a[0] == 'label':
                        code = '//' + instr + '\n' + '(' + a[1].upper() + '_' + os.path.basename(path) + ')' + '\n' + '\n'
                    elif a[0] == 'goto':
                        code = '//' + instr + '\n' + '@' + a[1].upper() + '_' + os.path.basename(path) + '\n' + '0;JMP' + '\n' + '\n'
                    elif a[0] == 'if-goto':
                        code = '//' + instr + '\n' + '@SP' + '\n' + 'M=M-1' + '\n' + 'A=M' + '\n' + 'D=M' + '\n' + '@' + a[1].upper() + '_' + os.path.basename(path) + '\n' + 'D;JNE' + '\n' + '\n'

                elif type == 'function_calling_instr':
                    if a[0] == 'call':
                        count_call += 1
                        code = '//##########Call ' + str(count_call) + '##########' + '\n' + \
                               '//' + instr + '\n' +\
                               '//Push return address' + '\n' +\
                               '@RA_after_' + a[1] + '_' + str(count_call) + '_' + os.path.basename(path) + '\n' +\
                               'D=A' + '\n' +\
                               '@SP' + '\n' +\
                               'A=M' + '\n' +\
                               'M=D' + '\n' +\
                               '@SP' + '\n' +\
                               'M=M+1' + '\n' +\
                               '//Push LCL' + '\n' +\
                               '@LCL' + '\n' +\
                               'D=M' + '\n' +\
                               '@SP' + '\n' +\
                               'A=M' + '\n' +\
                               'M=D' + '\n' +\
                               '@SP' + '\n' +\
                               'M=M+1' + '\n' +\
                               '//Push ARG' + '\n' +\
                               '@ARG' + '\n' +\
                               'D=M' + '\n' +\
                               '@SP' + '\n' +\
                               'A=M' + '\n' +\
                               'M=D' + '\n' +\
                               '@SP' + '\n' +\
                               'M=M+1' + '\n' + \
                               '//Push THIS' + '\n' + \
                               '@THIS' + '\n' + \
                               'D=M' + '\n' + \
                               '@SP' + '\n' + \
                               'A=M' + '\n' + \
                               'M=D' + '\n' + \
                               '@SP' + '\n' + \
                               'M=M+1' + '\n' + \
                               '//Push THAT' + '\n' + \
                               '@THAT' + '\n' + \
                               'D=M' + '\n' + \
                               '@SP' + '\n' + \
                               'A=M' + '\n' + \
                               'M=D' + '\n' + \
                               '@SP' + '\n' + \
                               'M=M+1' + '\n' + \
                               '//ARG=SP-n-5' + '\n' +\
                               '@SP' + '\n' +\
                               'D=M' + '\n' +\
                               '@' + a[2] + '\n' +\
                               'D=D-A' + '\n' +\
                               '@5' + '\n' +\
                               'D=D-A' + '\n' +\
                               '@ARG' + '\n' +\
                               'M=D' + '\n'+\
                               '//LCL=SP' + '\n' +\
                               '@SP' + '\n' +\
                               'D=M' + '\n' +\
                               '@LCL' + '\n' +\
                               'M=D' + '\n' +\
                               '//goto ' + a[1] + '\n' +\
                               '@' + a[1] + '\n' +\
                               '0;JMP' + '\n' +\
                               '(RA_after_' + a[1] + '_' + str(count_call)+ '_' + os.path.basename(path) + ')' + '\n' +\
                               '//##########Call ' + str(count_call) + ' Ends##########' + '\n' +'\n'
                    elif a[0] == 'return':
                        code = '//!!!!!!!!!!RETURN!!!!!!!!!!' + '\n' +\
                               '//' + instr + '\n' +\
                               '//FRAME(R13)=LCL' + '\n' +\
                               '@LCL' + '\n' +\
                               'D=M' + '\n' +\
                               '@R13' + '\n' +\
                               'M=D' + '\n' +\
                               '//RET=*(FRAME)-5' + '\n'\
                               '@5' + '\n' +\
                               'A=D-A' + '\n' +\
                               'D=M' + '\n' +\
                               '@R14' + '\n' +\
                               'M=D' + '\n' +\
                               '//*ARG=pop()' + '\n' +\
                               '@SP' + '\n' +\
                               'M=M-1' + '\n' +\
                               'A=M' + '\n' +\
                               'D=M' + '\n' +\
                               '@ARG' + '\n' +\
                               'A=M' + '\n' +\
                               'M=D' + '\n' +\
                               '//SP=ARG+1' + '\n' +\
                               '@ARG' + '\n' +\
                               'D=M' + '\n' +\
                               'D=D+1' + '\n' +\
                               '@SP' + '\n' +\
                               'M=D' + '\n' +\
                               '//THAT=*(FRAME-1)' + '\n' +\
                               '@R13' + '\n' +\
                               'M=M-1' + '\n' +\
                               'A=M' + '\n' +\
                               'D=M' + '\n' +\
                               '@THAT' + '\n' +\
                               'M=D' + '\n' +\
                               '//THIS=*(FRAME-2)' + '\n' + \
                               '@R13' + '\n' + \
                               'M=M-1' + '\n' + \
                               'A=M' + '\n' + \
                               'D=M' + '\n' + \
                               '@THIS' + '\n' + \
                               'M=D' + '\n' + \
                               '//ARG=*(FRAME-3)' + '\n' + \
                               '@R13' + '\n' + \
                               'M=M-1' + '\n' + \
                               'A=M' + '\n' + \
                               'D=M' + '\n' + \
                               '@ARG' + '\n' + \
                               'M=D' + '\n' + \
                               '//LCL=*(FRAME-4)' + '\n' + \
                               '@R13' + '\n' + \
                               'M=M-1' + '\n' + \
                               'A=M' + '\n' + \
                               'D=M' + '\n' + \
                               '@LCL' + '\n' + \
                               'M=D' + '\n' + \
                               '//goto RET' + '\n' + \
                               '@R14' + '\n' + \
                               'A=M' + '\n' + \
                               '0;JMP' + '\n' +\
                               '//!!!!!!!!!!RETURN ENDS!!!!!!!!!!' + '\n' + '\n'
                    elif a[0] == 'function':
                        code = '//%%%%%%%%%%FUNCTION%%%%%%%%%%' + '\n' +\
                               '//' + instr + '\n' +\
                               '(' + a[1] + ')' + '\n' +\
                               '@' + a[2] + '\n' +\
                               'D=A' + '\n' +\
                               '(' + 'LOOP_' + a[1] + ')' + '\n' +\
                               '@' + a[1] + '_LABEL' + '\n' +\
                               'D;JEQ' + '\n' +\
                               '@SP' + '\n' +\
                               'A=M' + '\n' +\
                               'M=0' + '\n' +\
                               '@SP' + '\n' +\
                               'M=M+1' + '\n' +\
                               'D=D-1' + '\n' +\
                               '@' + 'LOOP_' + a[1] + '\n' +\
                               '0;JMP' + '\n' +\
                               '(' + a[1] + '_LABEL' + ')' + '\n' +\
                               '//%%%%%%%%%%FUNCTION ENDS%%%%%%%%%%' + '\n' + '\n'

                rawprogram.write(code)
                print(code)
                print(i)
            i += 1
    def bootstrap(self):
        """Set SP to 256 and call Sys.init function"""
        if bootstrap_switch == True:
            bootcode = '//**********Bootstrap code**********' + '\n' +\
                       '@256' + '\n' +\
                       'D=A' + '\n' +\
                       '@SP' + '\n' +\
                       'M=D' + '\n' +\
                       '@LCL' + '\n' +\
                       'M=D' + '\n' +\
                       '@ARG' + '\n' +\
                       'M=D' + '\n' + '\n'+\
                       '//Calling Sys.init' + '\n' +\
                       '//Push return address' + '\n' +\
                       '@RA_after_Sys.init_0_Sys.vm' + '\n' +\
                       'D=A' + '\n' +\
                       '@SP' + '\n' +\
                       'A=M' + '\n' +\
                       'M=D' + '\n' +\
                       '@SP' + '\n' +\
                       'M=M+1' + '\n' +\
                       '//Push LCL' + '\n' +\
                       '@LCL' + '\n' +\
                       'D=M' + '\n' +\
                       '@SP' + '\n' +\
                       'A=M' + '\n' +\
                       'M=D' + '\n' +\
                       '@SP' + '\n' +\
                       'M=M+1' + '\n' +\
                       '//Push ARG' + '\n' +\
                       '@ARG' + '\n' +\
                       'D=M' + '\n' +\
                       '@SP' + '\n' +\
                       'A=M' + '\n' +\
                       'M=D' + '\n' +\
                       '@SP' + '\n' +\
                       'M=M+1' + '\n' + \
                       '//Push THIS' + '\n' + \
                       '@THIS' + '\n' + \
                       'D=M' + '\n' + \
                       '@SP' + '\n' + \
                       'A=M' + '\n' + \
                       'M=D' + '\n' + \
                       '@SP' + '\n' + \
                       'M=M+1' + '\n' + \
                       '//Push THAT' + '\n' + \
                       '@THAT' + '\n' + \
                       'D=M' + '\n' + \
                       '@SP' + '\n' + \
                       'A=M' + '\n' + \
                       'M=D' + '\n' + \
                       '@SP' + '\n' + \
                       'M=M+1' + '\n' + \
                       '//ARG=SP-n-5' + '\n' +\
                       '@SP' + '\n' +\
                       'D=M' + '\n' +\
                       '@0' + '\n' +\
                       'D=D-A' + '\n' +\
                       '@5' + '\n' +\
                       'D=D-A' + '\n' +\
                       '@ARG' + '\n' +\
                       'M=D' + '\n'+\
                       '//LCL=SP' + '\n' +\
                       '@SP' + '\n' +\
                       'D=M' + '\n' +\
                       '@LCL' + '\n' +\
                       'M=D' + '\n' +\
                       '//goto ' + '\n' +\
                       '@Sys.init' + '\n' +\
                       '0;JMP' + '\n' +\
                       '(RA_after_Sys.init_0_Sys.vm' + ')' + '\n' +\
                       '//**********End of Bootstrap code**********' + '\n' + '\n'
        else:
            bootcode = '//Bootstrap code is not present' + '\n' + '\n'
        with open(dirname + '/' + basename + '.asm', 'a+') as rawprogram:
             rawprogram.write(bootcode)
             print(bootcode)

if __name__ == "__main__":
    asm_input_file = sys.argv[-1]
    if sys.argv[-1] == 'vm':
        # Opening the file containing the VM code
        path = 'D:/nand2tetris/projects/08/FunctionCalls/StaticsTest/Class2.vm'
        dirname = os.path.dirname(path)
        basename = os.path.splitext(os.path.basename(path))[0]
        bootstrap_switch = False # Switch for bootstrap code
        #Cleaning up all comments and spaces in the code
        with open(path, 'r') as rawprogram:
            x = asm.Parser(rawprogram)
            x.cleanup(rawprogram)
        with open('D:/nand2tetris/projects/sampleparsed.txt', 'r') as parsedprogram:
            y = code_writer(parsedprogram)
            y.bootstrap()
            y.instruction_type(parsedprogram)
        print("""Your VM language program is been converted to assembly
code which is in file named " """
+ basename +
""".asm " which you can check at 
""" + path)
    # Deleting temporary generated text file
    os.remove('D:/nand2tetris/projects/sampleparsed.txt')
