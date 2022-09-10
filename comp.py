import sys
import re
import os

class Cleanup():
    def __init__(self, rawprogram):
        self.rawprogram = rawprogram

    def cleanup(self, rawprogram):
        with open("D:/nand2tetris/projects/sampleparsed.txt", "a+") as rawprogram_object:
            rawprogram_object.seek(0)
            flag_slash_star_star = False
            flag_star_slash = False
            for eachline in rawprogram:
                print(eachline)
                if eachline.startswith('/**') and eachline.find('*/') != -1:
                    flag_slash_star_star = True
                    flag_star_slash = True
                    print('/**  and  */  Detected')

                elif eachline.startswith('/**'):
                    flag_slash_star_star = True
                    print('/**  Detected')

                elif eachline.find('*/') != -1:
                    flag_star_slash = True
                    print('*/  Detected')

                if flag_slash_star_star == True or flag_star_slash == True:
                    if flag_slash_star_star == True and flag_star_slash == True:
                       flag_slash_star_star = False
                       flag_star_slash = False
                       continue
                    elif flag_slash_star_star == True and flag_star_slash == False:
                        continue
                    elif flag_star_slash == True:
                        flag_slash_star_star = False
                        flag_star_slash = False
                        continue
                    
                elif flag_slash_star_star == False and flag_star_slash == False and eachline.isspace() == False and eachline.startswith('//') == False :
                    eachline = eachline.split('//')[0]
                    eachline = eachline.lstrip().rstrip()
                    rawprogram_object.write(eachline)
                    rawprogram_object.write("\n")
                    flag_slash_star_star = False
                    flag_star_slash = False
                print('flag_slash_star_star = ',flag_slash_star_star)
                print('flag_star_slash = ',flag_star_slash)

class Tokenizer:
    def __init__(self, cleanedupprogram):
        self.cleanedupprogram = cleanedupprogram
        self.keywords = self.keywords

    keywords = ['class', 'constructor', 'function', 'method', 'field', 'static', 'var', 'int', 'char', 'boolean',
                'void', 'true', 'false', 'null', 'this', 'let', 'do', 'if', 'else', 'while', 'return']
    symbol = ['{', '}', '(', ')', '[', ']', '.', ',', ';', '+', '-', '*', '/', '&', '|', '>', '<', '=', '~']

    def has_more_tokens(self, cleanedupprogram):
        cleanedupprogram.seek(0)
        lines = cleanedupprogram.readlines()
        count = len(lines)
        with open("D:/nand2tetris/projects/token.xml", "a+") as Tokened:
            code = '<tokens>' + '\n'
            Tokened.write(code)
            for line in lines:

                ar = re.split('([ { } ( [ ) . , ; + - * / & | < > =  ~ " ])', line)
                ls = []
                lsn = []
                for elenn in ar:
                    are = re.split('(])', elenn)
                    for eln in are:
                        if eln.strip():
                            lsn.append(eln)
                for elen in lsn:
                    are = re.split('(-)', elen)
                    for el in are:
                        if el.strip():
                            ls.append(el)
                print(ls)
                a = []
                for ele in ls:
                    if ele.strip():
                        a.append(ele)

                c = '"'
                lst = []
                count = 0
                for q in a:
                    for pos, char in enumerate(q):
                        if char == c:
                            lst.append(count)
                    count += 1
                print(lst)

                if not len(lst) == 0:
                    a[lst[0] : lst[1] + 1] = [' '.join(a[lst[0] : lst[1] + 1])]
                    print(a)
                for token in a:
                    if token in self.keywords:
                        code = '<keyword> ' + token + ' </keyword>' + '\n'
                        Tokened.write(code)
                    elif token in self.symbol:
                        code = '<symbol> ' + token + ' </symbol>' + '\n'
                        Tokened.write(code)
                    elif token.isdigit() == True:
                        code = '<integerConstant> ' + token + ' </integerConstant>' + '\n'
                        Tokened.write(code)
                    elif c in token:
                        code = '<stringConstant> ' + token.lstrip('"').rstrip('"') + ' </stringConstant>' + '\n'
                        Tokened.write(code)
                    else:
                        code = '<identifier> ' + token + ' </identifier>' + '\n'
                        Tokened.write(code)
                    print(code)
            code = '</tokens>' + '\n'
            Tokened.write(code)

class CompilationEngine():
    def __init__(self, TokenProgram):
        self.TokenProgram = TokenProgram

    def read(self, TokenProgram):
        print('*********************************************************************************************************' + '\n' + '*********************************************************************************************************')
        TokenProgram.seek(0)
        TToken = TokenProgram.readlines()
        print('In read')
        with open("D:/nand2tetris/projects/ttoken.xml", "a+") as FinalFile:
            Tokencount = 0
            this_Token, this_Token_split, Tokencount = self.advanceline(TToken, Tokencount)
            if 'class' in this_Token_split:
                self.compileclass(Tokencount, this_Token, this_Token_split, FinalFile, TToken)
                print('DONE')

    def advanceline(self, TToken, Tokencount):
        Tokencount += 1
        next_Token = TToken[Tokencount]
        next_Token_split = re.split(' ', next_Token)
        return next_Token, next_Token_split, Tokencount

    def checkblanks(self, this_Token):
        blanks = len(this_Token) - len(this_Token.lstrip())
        return blanks

    def space(self, this_Token, blanks, samespace, addspace, decspace):
        if samespace == True:
            this_Token = this_Token.rjust(blanks + len(this_Token), ' ')
        elif addspace == True:
            blanks = blanks + 2
            this_Token = this_Token.rjust(blanks + len(this_Token), ' ')
        elif decspace == True:
            blanks = blanks - 2
            this_Token = this_Token.rjust(blanks + len(this_Token), ' ')
        return this_Token, blanks

    def compileclass(self, Tokencount, this_Token, this_Token_split, FinalFile, TToken):
        keys = ['static', 'field']
        subroutine = ['constructor', 'function', 'method']
        code = '<class>' + '\n'
        FinalFile.write(code)
        print('In compileclass - Received token - ' + this_Token)
        if '<keyword>' in this_Token_split:
            print('Compileclass- Got a keyword ' + this_Token)
            blanks = self.checkblanks(this_Token)
            this_Token, blanks = self.space(this_Token, blanks, False, True, False)
            FinalFile.write(this_Token)
            print('Compileclass- Next token is ' + this_Token)
        else:
            print('Compileclass- MISSING KEYWORD CLASS')
        this_Token, this_Token_split, Tokencount = self.advanceline(TToken, Tokencount)
        if '<identifier>' in this_Token_split:
            print('Compileclass- Got a identifier ' + this_Token)
            this_Token, blanks = self.space(this_Token, blanks, True, False, False)
            FinalFile.write(this_Token)
            classname = this_Token_split[1]
            print('Class name is - ' + classname)
            print('Compileclass- Next token is ' + this_Token)
        else:
            print('Compileclass- MISSING CLASSNAME IDENTIFIER')
        this_Token, this_Token_split, Tokencount = self.advanceline(TToken, Tokencount)
        if '{' in this_Token_split:
            print('Compileclass- Got a symbol ' + this_Token)
            this_Token, blanks = self.space(this_Token, blanks, True, False, False)
            FinalFile.write(this_Token)
            print('Compileclass- Next token is ' + this_Token)
        else:
            print('Compileclass- MISSING CLASS STARTING PARENTHESIS')
        this_Token, this_Token_split, Tokencount = self.advanceline(TToken, Tokencount)

        while any(item in keys for item in this_Token_split):
            print('Compileclass - In while for CompileClassVarDec ' + this_Token)
            if any(item in keys for item in this_Token_split):
                this_Token, this_Token_split, Tokencount, blanks = self.CompileClassVarDec(Tokencount, this_Token, this_Token_split, FinalFile, TToken, classname, blanks)
            else:
                break

        print('Compileclass - Out of while for CompileClassVarDec')

        while any(item in subroutine for item in this_Token_split):
            print('Compileclass - In while for CompileSubroutineDec ' + this_Token)
            if any(item in subroutine for item in this_Token_split):
                this_Token, this_Token_split, Tokencount, blanks = self.CompileSubroutineDec(Tokencount, this_Token, this_Token_split, FinalFile, TToken, classname, blanks)
            else:
                break

        print('Compileclass - Out of while for CompileSubroutineDec')
        if '}' in this_Token_split:
            print('CompileClass- Got a symbol } ' + this_Token)
            this_Token, blanks = self.space(this_Token, blanks, True, False, False)
            FinalFile.write(this_Token)

        code = '</class>' + '\n'
        code, blanks = self.space(code, blanks, False, False, True)
        FinalFile.write(code)

        this_Token, this_Token_split, Tokencount = self.advanceline(TToken, Tokencount)
        print('Compileclass- Next token is ' + this_Token)
        return this_Token, this_Token_split, Tokencount, blanks

    def CompileClassVarDec(self, Tokencount, this_Token, this_Token_split, FinalFile, TToken, classname, blanks):
        type = ['int', 'char', 'boolean', classname]
        keys = ['static', 'field']

        code = '<classVarDec>' + '\n'
        code, blanks = self.space(code, blanks, True, False, False)
        FinalFile.write(code)

        print('In ClassVarDec - Received token - ' + this_Token)
        if any(item in keys for item in this_Token_split):
            print('CompileClassVarDec - Got a key ' + this_Token)
            this_Token, blanks = self.space(this_Token, blanks, False, True, False)
            FinalFile.write(this_Token)
            this_Token, this_Token_split, Tokencount = self.advanceline(TToken, Tokencount)
            print('CompileClassVarDec - - Next token is ' + this_Token)
            if (item in type for item in this_Token_split):
                print('CompileClassVarDec in if - Got a type ' + this_Token)
                this_Token, blanks = self.space(this_Token, blanks, True, False, False)
                FinalFile.write(this_Token)
                this_Token, this_Token_split, Tokencount = self.advanceline(TToken, Tokencount)
                print('CompileClassVarDec -Next token is ' + this_Token)
                if '<identifier>' in this_Token_split:
                    print('CompileClassVarDec in if - Got a identifier ' + this_Token)
                    this_Token, blanks = self.space(this_Token, blanks, True, False, False)
                    FinalFile.write(this_Token)
                    this_Token, this_Token_split, Tokencount = self.advanceline(TToken, Tokencount)
                    print('CompileClassVarDec -Next token is ' + this_Token)
                    while '<symbol>' in this_Token_split:
                        if ',' in this_Token_split:
                            print('CompileClassVarDec in if - Got a comma ' + this_Token)
                            this_Token, blanks = self.space(this_Token, blanks, True, False, False)
                            FinalFile.write(this_Token)
                            this_Token, this_Token_split, Tokencount = self.advanceline(TToken, Tokencount)
                            print('CompileClassVarDec -Next token is ' + this_Token)
                            if '<identifier>' in this_Token_split:
                                print('CompileClassVarDec in if - Got a identifier ' + this_Token)
                                this_Token, blanks = self.space(this_Token, blanks, True, False, False)
                                FinalFile.write(this_Token)
                                this_Token, this_Token_split, Tokencount = self.advanceline(TToken, Tokencount)
                                print('CompileClassVarDec -Next token is ' + this_Token)
                        if ';' in this_Token_split:
                            print('CompileClassVarDec in if - Got a semicolon ' + this_Token)
                            this_Token, blanks = self.space(this_Token, blanks, True, False, False)
                            FinalFile.write(this_Token)
                            break
            code = '</classVarDec>' + '\n'
            code, blanks = self.space(code, blanks, False, False, True)
            FinalFile.write(code)

            this_Token, this_Token_split, Tokencount = self.advanceline(TToken, Tokencount)
            print('CompileClassVarDec -Next token is ' + this_Token)
            return this_Token, this_Token_split, Tokencount, blanks

    def CompileSubroutineDec(self, Tokencount, this_Token, this_Token_split, FinalFile, TToken, classname, blanks):
        type = ['int', 'char', 'boolean', 'void', classname]
        subroutine = ['constructor', 'function', 'method']

        code = '<subroutineDec>' + '\n'
        code, blanks = self.space(code, blanks, True, False, False)
        FinalFile.write(code)

        print('In SubroutineDec - Received token - ' + this_Token)
        if any(item in subroutine for item in this_Token_split):
            print('CompileSubroutineDec- Got a subroutine ' + this_Token)
            this_Token, blanks = self.space(this_Token, blanks, False, True, False)
            FinalFile.write(this_Token)
            this_Token, this_Token_split, Tokencount = self.advanceline(TToken, Tokencount)
            print('CompileSubroutineDec- Next token is ' + this_Token)
            if any(item in type for item in this_Token_split):
                print('CompileSubroutineDec- Got a type ' + this_Token)
                this_Token, blanks = self.space(this_Token, blanks, True, False, False)
                FinalFile.write(this_Token)
                this_Token, this_Token_split, Tokencount = self.advanceline(TToken, Tokencount)
                print('CompileSubroutineDec- Next token is ' + this_Token)
                if '<identifier>' in this_Token_split:
                    print('CompileSubroutineDec- Got a identifier ' + this_Token)
                    this_Token, blanks = self.space(this_Token, blanks, True, False, False)
                    FinalFile.write(this_Token)
                    this_Token, this_Token_split, Tokencount = self.advanceline(TToken, Tokencount)
                    print('CompileSubroutineDec- Next token is ' + this_Token)
                    if '(' in this_Token_split:
                        print('CompileSubroutineDec- Got a symbol ' + this_Token)
                        this_Token, blanks = self.space(this_Token, blanks, True, False, False)
                        FinalFile.write(this_Token)
                        this_Token, this_Token_split, Tokencount = self.advanceline(TToken, Tokencount)
                        print('CompileSubroutineDec- Next token is ' + this_Token)
                        if ')' in this_Token_split:
                            code = '<parameterList>' + '\n'
                            code, blanks = self.space(code, blanks, True, False, False)
                            FinalFile.write(code)
                            code = '</parameterList>' + '\n'
                            code, blanks = self.space(code, blanks, True, False, False)
                            FinalFile.write(code)
                            print('CompileSubroutineDec- Got a symbol ' + this_Token)
                            this_Token, blanks = self.space(this_Token, blanks, True, False, False)
                            FinalFile.write(this_Token)
                            this_Token, this_Token_split, Tokencount = self.advanceline(TToken, Tokencount)
                            print('CompileSubroutineDec- Next token is ' + this_Token)
                        else:
                            this_Token, this_Token_split, Tokencount, blanks = self.CompileParameterList(Tokencount, this_Token, this_Token_split, FinalFile, TToken, classname, blanks)
                            print('CompileSubroutineDec - Out of CompileParameterList')

                        this_Token, this_Token_split, Tokencount, blanks = self.CompileSubroutineBody(Tokencount, this_Token, this_Token_split, FinalFile, TToken, classname, blanks)
                        print('CompileSubroutineDec - Out of CompileSubroutineBody')

        code = '</subroutineDec>' + '\n'
        code, blanks = self.space(code, blanks, False, False, True)
        FinalFile.write(code)
        return  this_Token, this_Token_split, Tokencount, blanks

    def CompileParameterList(self, Tokencount, this_Token, this_Token_split, FinalFile, TToken, classname, blanks):
        type = ['int', 'char', 'boolean', classname]

        code = '<parameterList>' + '\n'
        code, blanks = self.space(code, blanks, True, False, False)
        FinalFile.write(code)

        print('In ParameterList - Received token - ' + this_Token)
        if any(item in type for item in this_Token_split):
            print('CompileParameterList - Got a type ' + this_Token)
            this_Token, blanks = self.space(this_Token, blanks, False, True, False)
            FinalFile.write(this_Token)
            this_Token, this_Token_split, Tokencount = self.advanceline(TToken, Tokencount)
            print('CompileParameterList - Next token is ' + this_Token)
            if '<identifier>' in this_Token_split:
                print('CompileParameterList- Got a identifier ' + this_Token)
                this_Token, blanks = self.space(this_Token, blanks, True, False, False)
                FinalFile.write(this_Token)
                this_Token, this_Token_split, Tokencount = self.advanceline(TToken, Tokencount)
                print('CompileParameterList - Next token is ' + this_Token)
        while '<symbol>' in this_Token_split:
            if ',' in this_Token_split:
                print('CompileParameterList in if - Got a comma ' + this_Token)
                this_Token, blanks = self.space(this_Token, blanks, True, False, False)
                FinalFile.write(this_Token)
                this_Token, this_Token_split, Tokencount = self.advanceline(TToken, Tokencount)
                print('CompileParameterList - Next token is ' + this_Token)
                if any(item in type for item in this_Token_split):
                    print('CompileParameterList- Got a type ' + this_Token)
                    this_Token, blanks = self.space(this_Token, blanks, True, False, False)
                    FinalFile.write(this_Token)
                    this_Token, this_Token_split, Tokencount = self.advanceline(TToken, Tokencount)
                    print('CompileParameterList - Next token is ' + this_Token)
                    if '<identifier>' in this_Token_split:
                        print('CompileParameterList- Got a identifier ' + this_Token)
                        this_Token, blanks = self.space(this_Token, blanks, True, False, False)
                        FinalFile.write(this_Token)
                        this_Token, this_Token_split, Tokencount = self.advanceline(TToken, Tokencount)
                        print('CompileParameterList - Next token is ' + this_Token)
            if ')' in this_Token_split:
                print('CompileParameterList in if - Got a symbol ' + this_Token)
                this_Token, blanks = self.space(this_Token, blanks, True, False, False)
                FinalFile.write(this_Token)
                break

        code = '</parameterList>' + '\n'
        code, blanks = self.space(code, blanks, False, False, True)
        FinalFile.write(code)

        this_Token, this_Token_split, Tokencount = self.advanceline(TToken, Tokencount)
        print('CompileParameterList - Next token is ' + this_Token)
        return this_Token, this_Token_split, Tokencount, blanks

    def CompileSubroutineBody(self, Tokencount, this_Token, this_Token_split, FinalFile, TToken, classname, blanks):
        code = '<subroutineBody>' + '\n'
        code, blanks = self.space(code, blanks, True, False, False)
        FinalFile.write(code)
        print('In SubroutineBody - Received token - ' + this_Token)
        if '{' in this_Token_split:
            print('CompilesubroutineBody in if - Got a symbol ' + this_Token)
            this_Token, blanks = self.space(this_Token, blanks, False, True, False)
            FinalFile.write(this_Token)
            this_Token, this_Token_split, Tokencount = self.advanceline(TToken, Tokencount)
            print('CompilesubroutineBody- Next token is ' + this_Token)
            if 'var' in this_Token_split:
                while 'var' in this_Token_split:
                    print('In while of CompileSubroutineBody ' + this_Token)
                    if 'var' in this_Token_split:
                        this_Token, this_Token_split, Tokencount, blanks = self.CompileVarDec(Tokencount, this_Token, this_Token_split, FinalFile, TToken, classname, blanks)
                        print('CompileSubroutineBody - Out of CompileVarDec')
                    else:
                        code = '<VarDec>' + '\n'
                        code, blanks = self.space(code, blanks, True, False, False)
                        FinalFile.write(code)
                        code = '</VarDec>' + '\n'
                        code, blanks = self.space(code, blanks, True, False, False)
                        FinalFile.write(code)
                        this_Token, this_Token_split, Tokencount = self.advanceline(TToken, Tokencount)
                        print('CompilesubroutineBody- Next token is ' + this_Token)
                print('CompileSubroutineBody - Out of while in CompileSubroutineBody')
            this_Token, this_Token_split, Tokencount, blanks = self.CompileStatements(Tokencount, this_Token, this_Token_split, FinalFile, TToken, classname, blanks)
            print('CompileSubroutineBody - Out of Statements')
            if '}' in this_Token_split:
                print('CompilesubroutineBody- Got a symbol } ' + this_Token)
                this_Token, blanks = self.space(this_Token, blanks, True, False, False)
                FinalFile.write(this_Token)
                this_Token, this_Token_split, Tokencount = self.advanceline(TToken, Tokencount)
                print('CompilesubroutineBody- Next token is ' + this_Token)

        code = '</subroutineBody>' + '\n'
        code, blanks = self.space(code, blanks, False, False, True)
        FinalFile.write(code)
        return this_Token, this_Token_split, Tokencount, blanks

    def CompileVarDec(self, Tokencount, this_Token, this_Token_split, FinalFile, TToken, classname, blanks):
        type = ['int', 'char', 'boolean', classname]

        code = '<varDec>' + '\n'
        code, blanks = self.space(code, blanks, True, False, False)
        FinalFile.write(code)

        print('In VarDec - Received token - ' + this_Token)
        print(this_Token)
        if 'var' in this_Token_split:
            print('CompileVarDec- Got a keyword var ' + this_Token)
            this_Token, blanks = self.space(this_Token, blanks, False, True, False)
            FinalFile.write(this_Token)
            this_Token, this_Token_split, Tokencount = self.advanceline(TToken, Tokencount)
            print('CompileVarDec- Next token is ' + this_Token)
            if any(item in type for item in this_Token_split) or '<identifier>' in this_Token_split:
                print('CompileVarDec- Got a type ' + this_Token)
                this_Token, blanks = self.space(this_Token, blanks, True, False, False)
                FinalFile.write(this_Token)
                this_Token, this_Token_split, Tokencount = self.advanceline(TToken, Tokencount)
                print('CompileVarDec- Next token is ' + this_Token)
                if '<identifier>' in this_Token_split:
                    print('CompileVarDec- Got a identifier '  + this_Token)
                    this_Token, blanks = self.space(this_Token, blanks, True, False, False)
                    FinalFile.write(this_Token)
                    this_Token, this_Token_split, Tokencount = self.advanceline(TToken, Tokencount)
                    print('CompileVarDec- Next token is ' + this_Token)
                    while '<symbol>' in this_Token_split:
                        if ',' in this_Token_split:
                            print('CompileVarDec in if - Got a comma ' + this_Token)
                            this_Token, blanks = self.space(this_Token, blanks, True, False, False)
                            FinalFile.write(this_Token)
                            this_Token, this_Token_split, Tokencount = self.advanceline(TToken, Tokencount)
                            print('CompileVarDec- Next token is ' + this_Token)
                            if '<identifier>' in this_Token_split:
                                print('CompileVarDec in if - Got a identifier ' + this_Token)
                                this_Token, blanks = self.space(this_Token, blanks, True, False, False)
                                FinalFile.write(this_Token)
                                this_Token, this_Token_split, Tokencount = self.advanceline(TToken, Tokencount)
                                print('CompileVarDec- Next token is ' + this_Token)
                        if ';' in this_Token_split:
                            print('CompileVarDec in if - Got a semicolon ' + this_Token)
                            this_Token, blanks = self.space(this_Token, blanks, True, False, False)
                            print(this_Token)
                            FinalFile.write(this_Token)
                            break
        code = '</varDec>' + '\n'
        code, blanks = self.space(code, blanks, False, False, True)
        FinalFile.write(code)

        this_Token, this_Token_split, Tokencount = self.advanceline(TToken, Tokencount)
        print('CompileVarDec- Next token is ' + this_Token)
        return this_Token, this_Token_split, Tokencount, blanks

    def CompileStatements(self, Tokencount, this_Token, this_Token_split, FinalFile, TToken, classname, blanks):
        statements = ['let', 'if', 'else', 'while', 'do', 'return']
        code = '<statements>' + '\n'
        code, blanks = self.space(code, blanks, True, False, False)
        FinalFile.write(code)

        print('In CompileStatements - Received token - ' + this_Token)
        blanks = blanks + 2
        while any(item in statements for item in this_Token_split):
            print('CompileStatements - In while loop of statements')
            if 'let' in this_Token_split:
                print('CompileStatements - Calling let')
                this_Token, this_Token_split, Tokencount, blanks = self.CompileLet(Tokencount, this_Token, this_Token_split, FinalFile, TToken, classname, blanks)
                print('CompileStatements - Out of let')
            elif 'if' in this_Token_split:
                print('CompileStatements - Calling if')
                this_Token, this_Token_split, Tokencount, blanks = self.CompileIf(Tokencount, this_Token, this_Token_split, FinalFile, TToken, classname, blanks)
                print('CompileStatements - Out of if')
            elif 'while' in this_Token_split:
                print('CompileStatements - Calling while')
                this_Token, this_Token_split, Tokencount, blanks = self.CompileWhile(Tokencount, this_Token, this_Token_split, FinalFile, TToken, classname, blanks)
                print('CompileStatements - Out of while')
            elif 'do' in this_Token_split:
                print('CompileStatements - Calling do')
                this_Token, this_Token_split, Tokencount, blanks = self.CompileDo(Tokencount, this_Token, this_Token_split, FinalFile, TToken, classname, blanks)
                print('CompileStatements - Out of do')
            elif 'return' in this_Token_split:
                print('CompileStatements - Calling return')
                this_Token, this_Token_split, Tokencount, blanks = self.CompileReturn(Tokencount, this_Token, this_Token_split, FinalFile, TToken, classname, blanks)
                print('CompileStatements - Out of return')
            else:
                break
        print('CompileStatements - Out of while loop of statements')
        code = '</statements>' + '\n'
        code, blanks = self.space(code, blanks, False, False, True)
        FinalFile.write(code)
        return this_Token, this_Token_split, Tokencount, blanks

    def CompileIf(self, Tokencount, this_Token, this_Token_split, FinalFile, TToken, classname, blanks):
        code = '<ifStatement>' + '\n'
        code, blanks = self.space(code, blanks, True, False, False)
        FinalFile.write(code)

        print('In CompileIf - Received token - ' + this_Token)
        if 'if' in this_Token_split:
            print('CompileIf - Got a keyword if ' + this_Token)
            this_Token, blanks = self.space(this_Token, blanks, False, True, False)
            FinalFile.write(this_Token)
            this_Token, this_Token_split, Tokencount = self.advanceline(TToken, Tokencount)
            print('CompileIf - Next token is ' + this_Token)
            if '(' in this_Token_split:
                print('CompileIf - Got a symbol ( ' + this_Token)
                this_Token, blanks = self.space(this_Token, blanks, True, False, False)
                FinalFile.write(this_Token)
                this_Token, this_Token_split, Tokencount = self.advanceline(TToken, Tokencount)
                print('CompileIf - Next token is ' + this_Token)

                this_Token, this_Token_split, Tokencount, blanks = self.CompileExpression(Tokencount, this_Token, this_Token_split, FinalFile, TToken, classname, blanks)
                print("CompileIf - Out of CompileExpressions")

                if ')' in this_Token_split:
                    print('CompileIf- Got a symbol ) ' + this_Token)
                    this_Token, blanks = self.space(this_Token, blanks, True, False, False)
                    FinalFile.write(this_Token)
                    this_Token, this_Token_split, Tokencount = self.advanceline(TToken, Tokencount)
                    print('CompileIf - Next token is ' + this_Token)
                    if '{' in this_Token_split:
                        print('CompileIf- Got a symbol { ' + this_Token)
                        this_Token, blanks = self.space(this_Token, blanks, True, False, False)
                        FinalFile.write(this_Token)
                        this_Token, this_Token_split, Tokencount = self.advanceline(TToken, Tokencount)
                        print('CompileIf - Next token is ' + this_Token)

                        this_Token, this_Token_split, Tokencount, blanks = self.CompileStatements(Tokencount, this_Token, this_Token_split, FinalFile, TToken, classname, blanks)
                        print("CompileIf - Out of CompileStatements")

                        if '}' in this_Token_split:
                            print('CompileIf- Got a symbol } ' + this_Token)
                            this_Token, blanks = self.space(this_Token, blanks, True, False, False)
                            FinalFile.write(this_Token)
                            this_Token, this_Token_split, Tokencount = self.advanceline(TToken, Tokencount)
                            print('CompileIf - Next token is ' + this_Token)
                            if 'else' in this_Token_split:
                                print('CompileElse - Got a keyword else ' + this_Token)
                                this_Token, blanks = self.space(this_Token, blanks, True, False, False)
                                FinalFile.write(this_Token)
                                this_Token, this_Token_split, Tokencount = self.advanceline(TToken, Tokencount)
                                print('CompileElse -Next token is ' + this_Token)
                                if '{' in this_Token_split:
                                    print('CompileElse - Got a symbol { ' + this_Token)
                                    this_Token, blanks = self.space(this_Token, blanks, True, False, False)
                                    FinalFile.write(this_Token)
                                    this_Token, this_Token_split, Tokencount = self.advanceline(TToken, Tokencount)
                                    print('CompileElse -Next token is ' + this_Token)

                                    this_Token, this_Token_split, Tokencount, blanks = self.CompileStatements(Tokencount, this_Token, this_Token_split, FinalFile, TToken, classname, blanks)
                                    print("CompileElse - Out of CompileStatements")

                                    if '}' in this_Token_split:
                                        print('CompileElse- Got a symbol } ' + this_Token)
                                        this_Token, blanks = self.space(this_Token, blanks, True, False, False)
                                        FinalFile.write(this_Token)
                                        this_Token, this_Token_split, Tokencount = self.advanceline(TToken, Tokencount)
                                        print('CompileElse - Next token is ' + this_Token)

        code = '</ifStatement>' + '\n'
        code, blanks = self.space(code, blanks, False, False, True)
        FinalFile.write(code)
        return this_Token, this_Token_split, Tokencount, blanks

    def CompileWhile(self, Tokencount, this_Token, this_Token_split, FinalFile, TToken, classname, blanks):
        code = '<whileStatement>' + '\n'
        code, blanks = self.space(code, blanks, True, False, False)
        FinalFile.write(code)

        print('In CompileWhile - Received token - ' + this_Token)
        if 'while' in this_Token_split:
            print('CompileWhile - Got a keyword while ' + this_Token)
            this_Token, blanks = self.space(this_Token, blanks, False, True, False)
            FinalFile.write(this_Token)
            this_Token, this_Token_split, Tokencount = self.advanceline(TToken, Tokencount)
            print('CompileWhile - Next token is ' + this_Token)
            if '(' in this_Token_split:
                print('CompileWhile- Got a symbol ( ' + this_Token )
                this_Token, blanks = self.space(this_Token, blanks, True, False, False)
                FinalFile.write(this_Token)
                this_Token, this_Token_split, Tokencount = self.advanceline(TToken, Tokencount)
                print('CompileWhile - Next token is ' + this_Token)

                this_Token, this_Token_split, Tokencount, blanks = self.CompileExpression(Tokencount, this_Token, this_Token_split, FinalFile, TToken, classname, blanks)
                print("CompileWhile - Out of CompileExpressions")

                if ')' in this_Token_split:
                    print('CompileWhile- Got a symbol ) ' + this_Token)
                    this_Token, blanks = self.space(this_Token, blanks, True, False, False)
                    FinalFile.write(this_Token)
                    this_Token, this_Token_split, Tokencount = self.advanceline(TToken, Tokencount)
                    print('CompileWhile - Next token is ' + this_Token)
                    if '{' in this_Token_split:
                        print('CompileWhile- Got a symbol { ' + this_Token)
                        this_Token, blanks = self.space(this_Token, blanks, True, False, False)
                        FinalFile.write(this_Token)
                        this_Token, this_Token_split, Tokencount = self.advanceline(TToken, Tokencount)
                        print('CompileWhile - Next token is ' + this_Token)

                        this_Token, this_Token_split, Tokencount, blanks = self.CompileStatements(Tokencount, this_Token, this_Token_split, FinalFile, TToken, classname, blanks)
                        print("CompileWhile - Out of CompileStatements")

                        if '}' in this_Token_split:
                            print('CompileWhile- Got a symbol } ' + this_Token)
                            this_Token, blanks = self.space(this_Token, blanks, True, False, False)
                            FinalFile.write(this_Token)
                            this_Token, this_Token_split, Tokencount = self.advanceline(TToken, Tokencount)
                            print('CompileWhile - Next token is ' + this_Token)

        code = '</whileStatement>' + '\n'
        code, blanks = self.space(code, blanks, False, False, True)
        FinalFile.write(code)
        return this_Token, this_Token_split, Tokencount, blanks

    def CompileDo(self, Tokencount, this_Token, this_Token_split, FinalFile, TToken, classname, blanks):
        code = '<doStatement>' + '\n'
        code, blanks = self.space(code, blanks, True, False, False)
        FinalFile.write(code)

        print('In CompileDo - Received token - ' + this_Token)
        if 'do' in this_Token_split:
            print('CompileDo - Got a keyword do ' + this_Token)
            this_Token, blanks = self.space(this_Token, blanks, False, True, False)
            FinalFile.write(this_Token)
            this_Token, this_Token_split, Tokencount = self.advanceline(TToken, Tokencount)
            print('CompileDo - Next token is ' + this_Token)
            if '<identifier>' in this_Token_split:
                print('CompileDo - Got a identifier ' + this_Token)
                this_Token, blanks = self.space(this_Token, blanks, True, False, False)
                FinalFile.write(this_Token)
                this_Token, this_Token_split, Tokencount = self.advanceline(TToken, Tokencount)
                print('CompileDo - Next token is ' + this_Token)
                if '[' in this_Token_split:
                    print('CompileDo - Got a [ ' + this_Token)
                    this_Token, blanks = self.space(this_Token, blanks, True, False, False)
                    FinalFile.write(this_Token)
                    this_Token, this_Token_split, Tokencount = self.advanceline(TToken, Tokencount)
                    print('CompileDo - Next token is ' + this_Token)

                    this_Token, this_Token_split, Tokencount, blanks = self.CompileExpression(Tokencount, this_Token, this_Token_split, FinalFile, TToken, classname, blanks)
                    print('CompileDo - Out of CompileExpression')
                    if ']' in this_Token_split:
                        print('CompileDo - Got a ] ' + this_Token)
                        this_Token, blanks = self.space(this_Token, blanks, True, False, False)
                        FinalFile.write(this_Token)
                        this_Token, this_Token_split, Tokencount = self.advanceline(TToken, Tokencount)
                        print('CompileDo - Next token is ' + this_Token)

                elif '(' in this_Token_split:
                    print('CompileDo - Got a ( ' + this_Token)
                    this_Token, blanks = self.space(this_Token, blanks, True, False, False)
                    FinalFile.write(this_Token)
                    this_Token, this_Token_split, Tokencount = self.advanceline(TToken, Tokencount)
                    print('CompileDo - Next token is ' + this_Token)
                    this_Token, this_Token_split, Tokencount, blanks = self.CompileExpressionList(Tokencount, this_Token, this_Token_split, FinalFile, TToken, classname, blanks)
                    print('CompileDo - Out of CompileExpression')
                    if ')' in this_Token_split:
                        print('CompileDo - Got a ) ' + this_Token)
                        this_Token, blanks = self.space(this_Token, blanks, True, False, False)
                        FinalFile.write(this_Token)
                        this_Token, this_Token_split, Tokencount = self.advanceline(TToken, Tokencount)
                        print('CompileDo - Next token is ' + this_Token)
                        if ';' in this_Token_split:
                            print('CompileDo- Got a symbol  ; ' + this_Token)
                            this_Token, blanks = self.space(this_Token, blanks, True, False, False)
                            FinalFile.write(this_Token)
                            this_Token, this_Token_split, Tokencount = self.advanceline(TToken, Tokencount)
                            print('CompileDo - Next token is ' + this_Token)

                elif '.' in this_Token_split:
                    print('CompileDo - Got a . ' + this_Token)
                    this_Token, blanks = self.space(this_Token, blanks, True, False, False)
                    FinalFile.write(this_Token)
                    this_Token, this_Token_split, Tokencount = self.advanceline(TToken, Tokencount)
                    print('CompileDo - Next token is ' + this_Token)
                    if '<identifier>' in this_Token_split:
                        print('CompileDo - Got a identifier ' + this_Token)
                        this_Token, blanks = self.space(this_Token, blanks, True, False, False)
                        FinalFile.write(this_Token)
                        this_Token, this_Token_split, Tokencount = self.advanceline(TToken, Tokencount)
                        print('CompileDo - Next token is ' + this_Token)
                        if '(' in this_Token_split:
                            print('CompileDo - Got a ( ' + this_Token)
                            this_Token, blanks = self.space(this_Token, blanks, True, False, False)
                            FinalFile.write(this_Token)
                            this_Token, this_Token_split, Tokencount = self.advanceline(TToken, Tokencount)
                            print('CompileDo - Next token is ' + this_Token)
                            this_Token, this_Token_split, Tokencount, blanks = self.CompileExpressionList(Tokencount, this_Token, this_Token_split, FinalFile, TToken, classname, blanks)
                            print('CompileDo - Out of CompileExpression')
                            if ')' in this_Token_split:
                                print('CompileDo - Got a ) ' + this_Token)
                                this_Token, blanks = self.space(this_Token, blanks, True, False, False)
                                FinalFile.write(this_Token)
                                this_Token, this_Token_split, Tokencount = self.advanceline(TToken, Tokencount)
                                print('CompileDo - Next token is ' + this_Token)
                                if ';' in this_Token_split:
                                    print('CompileDo- Got a symbol  ; ' + this_Token)
                                    this_Token, blanks = self.space(this_Token, blanks, True, False, False)
                                    FinalFile.write(this_Token)
                                    this_Token, this_Token_split, Tokencount = self.advanceline(TToken, Tokencount)
                                    print('CompileDo - Next token is ' + this_Token)
        code = '</doStatement>' + '\n'
        code, blanks = self.space(code, blanks, False, False, True)
        FinalFile.write(code)
        return this_Token, this_Token_split, Tokencount, blanks

    def CompileReturn(self, Tokencount, this_Token, this_Token_split, FinalFile, TToken, classname, blanks):
        code = '<returnStatement>' + '\n'
        code, blanks = self.space(code, blanks, True, False, False)
        FinalFile.write(code)

        print('In CompileReturn - Received token - ' + this_Token)
        if 'return' in this_Token_split:
            print('CompileReturn - Got a keyword return ' + this_Token)
            this_Token, blanks = self.space(this_Token, blanks, False, True, False)
            FinalFile.write(this_Token)
            this_Token, this_Token_split, Tokencount = self.advanceline(TToken, Tokencount)
            print('CompileReturn - Next token is ' + this_Token)
            if ';' not in this_Token_split:
                this_Token, this_Token_split, Tokencount, blanks = self.CompileExpression(Tokencount, this_Token, this_Token_split, FinalFile, TToken, classname, blanks)
                print("CompileReturn - Out of CompileExpressions")
                if ';' in this_Token_split:
                    print('CompileReturn - Got a symbol ; ' + this_Token)
                    this_Token, blanks = self.space(this_Token, blanks, True, False, False)
                    FinalFile.write(this_Token)
                    this_Token, this_Token_split, Tokencount = self.advanceline(TToken, Tokencount)
                    print('CompileReturn - Next token is ' + this_Token)
            if ';' in this_Token_split:
                print('CompileReturn - Got a symbol ; ' + this_Token)
                this_Token, blanks = self.space(this_Token, blanks, True, False, False)
                FinalFile.write(this_Token)
                this_Token, this_Token_split, Tokencount = self.advanceline(TToken, Tokencount)
                print('CompileReturn - Next token is ' + this_Token)

        code = '</returnStatement>' + '\n'
        code, blanks = self.space(code, blanks, False, False, True)
        FinalFile.write(code)
        return this_Token, this_Token_split, Tokencount, blanks

    def CompileLet(self, Tokencount, this_Token, this_Token_split, FinalFile, TToken, classname, blanks):
        code = '<letStatement>' + '\n'
        code, blanks = self.space(code, blanks, True, False, False)
        FinalFile.write(code)

        print('In CompileLet - Received token - ' + this_Token)
        if 'let' in this_Token_split:
            print('CompileLet - Got a keyword let ' + this_Token)
            this_Token, blanks = self.space(this_Token, blanks, False, True, False)
            FinalFile.write(this_Token)
            this_Token, this_Token_split, Tokencount = self.advanceline(TToken, Tokencount)
            print('CompileLet - Next token is ' + this_Token)
            if '<identifier>' in this_Token_split:
                print('CompileLet - Got an identifier ' + this_Token)
                this_Token, blanks = self.space(this_Token, blanks, True, False, False)
                FinalFile.write(this_Token)
                this_Token, this_Token_split, Tokencount = self.advanceline(TToken, Tokencount)
                print('CompileLet -  Next token is ' + this_Token)
                if '[' in this_Token_split:
                    print('CompileLet - Got a symbol ' + this_Token)
                    this_Token, blanks = self.space(this_Token, blanks, True, False, False)
                    FinalFile.write(this_Token)
                    this_Token, this_Token_split, Tokencount = self.advanceline(TToken, Tokencount)
                    print('CompileLet - Next token is ' + this_Token)

                    this_Token, this_Token_split, Tokencount, blanks = self.CompileExpression(Tokencount, this_Token, this_Token_split, FinalFile, TToken, classname, blanks)
                    print("CompileLet - Out of CompileExpressions")

                    if ']' in this_Token_split:
                        print('CompileLet - Got a symbol ' + this_Token)
                        this_Token, blanks = self.space(this_Token, blanks, True, False, False)
                        FinalFile.write(this_Token)
                        this_Token, this_Token_split, Tokencount = self.advanceline(TToken, Tokencount)
                        print('CompileLet - Next token is ' + this_Token)
                        if '=' in this_Token_split:
                            print('CompileLet - Got a symbol ' + this_Token)
                            this_Token, blanks = self.space(this_Token, blanks, True, False, False)
                            FinalFile.write(this_Token)
                            this_Token, this_Token_split, Tokencount = self.advanceline(TToken, Tokencount)
                            print('CompileLet - Next token is ' + this_Token)

                            this_Token, this_Token_split, Tokencount, blanks = self.CompileExpression(Tokencount, this_Token, this_Token_split, FinalFile, TToken, classname, blanks)
                            print("CompileLet - Out of CompileExpressions")

                            if ';' in this_Token_split:
                                print('CompileLet - Got a symbol ' + this_Token)
                                this_Token, blanks = self.space(this_Token, blanks, True, False, False)
                                FinalFile.write(this_Token)
                                this_Token, this_Token_split, Tokencount = self.advanceline(TToken, Tokencount)
                                print('CompileLet - Next token is ' + this_Token)

                if '=' in this_Token_split:
                    print('CompileLet - Got a symbol ' + this_Token)
                    this_Token, blanks = self.space(this_Token, blanks, True, False, False)
                    FinalFile.write(this_Token)
                    this_Token, this_Token_split, Tokencount = self.advanceline(TToken, Tokencount)
                    print('CompileLet - Next token is ' + this_Token)

                    this_Token, this_Token_split, Tokencount, blanks = self.CompileExpression(Tokencount, this_Token, this_Token_split, FinalFile, TToken, classname, blanks)
                    print("CompileLet - Out of CompileExpressions")

                    if ';' in this_Token_split:
                        print('CompileLet - Got a symbol ' + this_Token)
                        this_Token, blanks = self.space(this_Token, blanks, True, False, False)
                        FinalFile.write(this_Token)
                        this_Token, this_Token_split, Tokencount = self.advanceline(TToken, Tokencount)
                        print('CompileLet - Next token is ' + this_Token)

        code = '</letStatement>' + '\n'
        code, blanks = self.space(code, blanks, False, False, True)
        FinalFile.write(code)

        return this_Token, this_Token_split, Tokencount, blanks

    def CompileExpression(self, Tokencount, this_Token, this_Token_split, FinalFile, TToken, classname, blanks):
        op = ['+', '-', '*', '/', '&', '|', '<', '>', '=']

        code = '<expression>' + '\n'
        code, blanks = self.space(code, blanks, True, False, False)
        FinalFile.write(code)

        code, blanks = self.space(code, blanks, False, True, False)
        print('In CompileExpression - Received token - ' + this_Token)
        this_Token, this_Token_split, Tokencount, blanks = self.CompileTerm(Tokencount, this_Token, this_Token_split, FinalFile, TToken, classname, blanks)
        print('CompileExpression - Out of CompileTerm')

        while any(item in op for item in this_Token_split):
            print('In while of CompileExpression')
            if any(item in op for item in this_Token_split):
                print('CompileExpression- Got a op ' + this_Token)
                this_Token, blanks = self.space(this_Token, blanks, True, False, False)
                FinalFile.write(this_Token)
                this_Token, this_Token_split, Tokencount = self.advanceline(TToken, Tokencount)
                print('CompileExpression - Next token is ' + this_Token)

                this_Token, this_Token_split, Tokencount, blanks = self.CompileTerm(Tokencount, this_Token, this_Token_split, FinalFile, TToken, classname, blanks)

        code = '</expression>' + '\n'
        code, blanks = self.space(code, blanks, False, False, True)
        FinalFile.write(code)

        return this_Token, this_Token_split, Tokencount, blanks

    def CompileTerm(self, Tokencount, this_Token, this_Token_split, FinalFile, TToken, classname, blanks):
        KeywordConstant = ['true', 'false', 'null', 'this']
        unaryOp = ['-', '~']

        code = '<term>' + '\n'
        code, blanks = self.space(code, blanks,True, False, False)
        FinalFile.write(code)

        print('In CompileTerm - Received token - ' + this_Token)
        if '<integerConstant>' in this_Token_split:
            print('CompileTerm - Got a integerConstant ' + this_Token)
            this_Token, blanks = self.space(this_Token, blanks, False, True, False)
            FinalFile.write(this_Token)
            this_Token, this_Token_split, Tokencount = self.advanceline(TToken, Tokencount)
            print('CompileTerm - Next token is ' + this_Token)
        elif '<stringConstant>' in this_Token_split:
            print('CompileTerm- Got a stringConstant ' + this_Token)
            this_Token, blanks = self.space(this_Token, blanks, False, True, False)
            FinalFile.write(this_Token)
            this_Token, this_Token_split, Tokencount = self.advanceline(TToken, Tokencount)
            print('CompileTerm - Next token is ' + this_Token)
        elif any(item in KeywordConstant for item in this_Token_split):
            print('CompileTerm- Got a KeywordConstant ' + this_Token)
            this_Token, blanks = self.space(this_Token, blanks, False, True, False)
            FinalFile.write(this_Token)
            this_Token, this_Token_split, Tokencount = self.advanceline(TToken, Tokencount)
            print('CompileTerm - Next token is ' + this_Token)
        elif any(item in unaryOp for item in this_Token_split):
            print('CompileTerm- Got a unaryOp ' + this_Token)
            this_Token, blanks = self.space(this_Token, blanks, False, True, False)
            FinalFile.write(this_Token)
            this_Token, this_Token_split, Tokencount = self.advanceline(TToken, Tokencount)
            print('CompileTerm - Next token is ' + this_Token)

            this_Token, this_Token_split, Tokencount, blanks = self.CompileTerm(Tokencount, this_Token, this_Token_split, FinalFile, TToken, classname, blanks)
            print('CompileTerm - Out of CompileTerm')
        elif '<identifier>' in this_Token_split:
            print('CompileTerm- Got a identifier ' + this_Token)
            this_Token, blanks = self.space(this_Token, blanks, False, True, False)
            FinalFile.write(this_Token)
            this_Token, this_Token_split, Tokencount = self.advanceline(TToken, Tokencount)
            print('CompileTerm - Next token is ' + this_Token)
            if '[' in this_Token_split:
                print('CompileTerm- Got a [ ' + this_Token)
                this_Token, blanks = self.space(this_Token, blanks, True, False, False)
                FinalFile.write(this_Token)
                this_Token, this_Token_split, Tokencount = self.advanceline(TToken, Tokencount)
                print('CompileTerm - Next token is ' + this_Token)

                this_Token, this_Token_split, Tokencount, blanks = self.CompileExpression(Tokencount, this_Token, this_Token_split, FinalFile, TToken, classname, blanks)
                print('CompileTerm - Out of CompileExpression')
                if ']' in this_Token_split:
                    print('CompileTerm- Got a ] ' + this_Token)
                    this_Token, blanks = self.space(this_Token, blanks, True, False, False)
                    FinalFile.write(this_Token)
                    this_Token, this_Token_split, Tokencount = self.advanceline(TToken, Tokencount)
                    print('CompileTerm - Next token is ' + this_Token)

            elif '(' in this_Token_split:
                print('CompileTerm- Got a ( ' + this_Token)
                this_Token, blanks = self.space(this_Token, blanks, True, False, False)
                FinalFile.write(this_Token)
                this_Token, this_Token_split, Tokencount = self.advanceline(TToken, Tokencount)
                print('CompileTerm - Next token is ' + this_Token)

                this_Token, this_Token_split, Tokencount, blanks = self.CompileExpressionList(Tokencount, this_Token, this_Token_split, FinalFile, TToken, classname, blanks)
                print('CompileTerm - Out of CompileExpression')
                if ')' in this_Token_split:
                    print('CompileTerm- Got a ) ' + this_Token)
                    this_Token, blanks = self.space(this_Token, blanks, True, False, False)
                    FinalFile.write(this_Token)
                    this_Token, this_Token_split, Tokencount = self.advanceline(TToken, Tokencount)
                    print('CompileTerm - Next token is ' + this_Token)

            elif '.' in this_Token_split:
                print('CompileTerm- Got a . ' + this_Token)
                this_Token, blanks = self.space(this_Token, blanks, True, False, False)
                FinalFile.write(this_Token)
                this_Token, this_Token_split, Tokencount = self.advanceline(TToken, Tokencount)
                print('CompileTerm - Next token is ' + this_Token)
                if '<identifier>' in this_Token_split:
                    print('CompileTerm- Got a identifier ' + this_Token)
                    this_Token, blanks = self.space(this_Token, blanks, True, False, False)
                    FinalFile.write(this_Token)
                    this_Token, this_Token_split, Tokencount = self.advanceline(TToken, Tokencount)
                    print('CompileTerm - Next token is ' + this_Token)
                    if '(' in this_Token_split:
                        print('CompileTerm- Got a (' + this_Token)
                        this_Token, blanks = self.space(this_Token, blanks, True, False, False)
                        FinalFile.write(this_Token)
                        this_Token, this_Token_split, Tokencount = self.advanceline(TToken, Tokencount)
                        print('CompileTerm - Next token is ' + this_Token)
                        this_Token, this_Token_split, Tokencount, blanks = self.CompileExpressionList(Tokencount, this_Token, this_Token_split, FinalFile, TToken, classname, blanks)
                        print('CompileTerm - Out of CompileExpression')
                        if ')' in this_Token_split:
                            print('CompileTerm- Got a ) ' + this_Token)
                            this_Token, blanks = self.space(this_Token, blanks, True, False, False)
                            FinalFile.write(this_Token)
                            this_Token, this_Token_split, Tokencount = self.advanceline(TToken, Tokencount)
                            print('CompileTerm - Next token is ' + this_Token)

        elif '(' in this_Token_split:
            print('CompileTerm- Got a ( ' + this_Token)
            this_Token, blanks = self.space(this_Token, blanks, False, True, False)
            FinalFile.write(this_Token)
            this_Token, this_Token_split, Tokencount = self.advanceline(TToken, Tokencount)
            print('CompileTerm - Next token is ' + this_Token)

            this_Token, this_Token_split, Tokencount, blanks = self.CompileExpression(Tokencount, this_Token, this_Token_split, FinalFile, TToken, classname, blanks)
            print('CompileTerm - Out of CompileExpression')

            if ')' in this_Token_split:
                print('CompileTerm- Got a ) ' + this_Token)
                this_Token, blanks = self.space(this_Token, blanks, True, False, False)
                FinalFile.write(this_Token)
                this_Token, this_Token_split, Tokencount = self.advanceline(TToken, Tokencount)
                print('CompileTerm - Next token is ' + this_Token)

        code = '</term>' + '\n'
        code, blanks = self.space(code, blanks, False, False, True)
        FinalFile.write(code)

        return this_Token, this_Token_split, Tokencount, blanks

    def CompileExpressionList(self, Tokencount, this_Token, this_Token_split, FinalFile, TToken, classname, blanks):
        code = '<expressionList>' + '\n'
        code, blanks = self.space(code, blanks, True, False, False)
        FinalFile.write(code)

        print('In CompileExpressionList - Received token - ' + this_Token)
        code, blanks = self.space(code, blanks, False, True, False)
        if ')' not in this_Token_split:
            this_Token, this_Token_split, Tokencount, blanks = self.CompileExpression(Tokencount, this_Token, this_Token_split, FinalFile, TToken, classname, blanks)
            while ',' in this_Token_split:
                print('In while of CompileExpressionList')
                if ',' in this_Token_split:
                    print('CompileExpressionList- Got a , ' + this_Token)
                    this_Token, blanks = self.space(this_Token, blanks, True, False, False)
                    FinalFile.write(this_Token)
                    this_Token, this_Token_split, Tokencount = self.advanceline(TToken, Tokencount)
                    print('CompileExpressionList - Next token is ' + this_Token)

                    this_Token, this_Token_split, Tokencount, blanks = self.CompileExpression(Tokencount, this_Token, this_Token_split, FinalFile, TToken, classname, blanks)

        code = '</expressionList>' + '\n'
        code, blanks = self.space(code, blanks, False, False, True)
        FinalFile.write(code)
        return this_Token, this_Token_split, Tokencount, blanks






if __name__ == "__main__":
    compiler_input_file = sys.argv[-1]
    if sys.argv[-1] == 'comp':
        # Opening the file containing the JACk program
        path = 'D:/nand2tetris/projects/10/ExpressionLessSquare/SquareGame.jack'
        dirname = os.path.dirname(path)
        basename = os.path.splitext(os.path.basename(path))[0]
        with open(path, 'r') as rawprogram:
            print(basename + " opened")  # file opened confirmation
            x = Cleanup(rawprogram)
            x.cleanup(rawprogram)  # Call for cleanup
        with open("D:/nand2tetris/projects/sampleparsed.txt", "a+") as cleanedupprogram:
            print("sampleparsed.txt opened")
            y = Tokenizer(cleanedupprogram)
            y.has_more_tokens(cleanedupprogram)
        with open("D:/nand2tetris/projects/token.xml", "a+") as TokenProgram:
            print("token.txt opened")
            z = CompilationEngine(TokenProgram)
            z.read(TokenProgram)
            #TODO: Colour text in terminal use coloroma print(f"{fore.GREEN}, text)