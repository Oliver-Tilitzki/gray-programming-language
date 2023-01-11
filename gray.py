def run(code, main = True):
    try:
        import time
        line = 0
        varNames = []
        varValues = []
        def join(strings):
            try:
                splitted_strings = []
                chars = ""
                inString = False
                for i in strings:
                    if i == '"':
                        chars += i
                        if inString:
                            inString = False
                        else:
                            inString = True
                    elif i == " ":
                        if not inString:
                            splitted_strings.append(chars)
                            chars = ""
                        else:
                            chars += i
                    else:
                        chars += i
                splitted_strings.append(chars)
                joined_string = ""
                for i in splitted_strings:
                    joined_string += str(get_value(i))
                return joined_string
            except:
                print("error: can't join strings " + str(strings))
        def calculate(calculation):
            try:
                splitted_calculation = []
                arithmeticoperations = ["+","-","*","/","%"]
                chars = ""
                inString = False
                for i in calculation:
                    if i == '"':
                        chars += i
                        if inString:
                            inString = False
                        else:
                            inString = True
                    elif i in arithmeticoperations:
                        if not inString:
                            splitted_calculation.append(chars)
                            splitted_calculation.append(i)
                            chars = ""
                        else:
                            chars += i
                    else:
                        chars += i
                splitted_calculation.append(chars)
                for j,i in enumerate(splitted_calculation):
                    if not i in arithmeticoperations:
                        splitted_calculation[j] = get_value(i.replace(" ","").replace("\t",""))
                calculation = ""
                for i in splitted_calculation:
                    calculation += str(i)
                return eval(calculation)
            except Exception as e:
                print("error: can't calculate " + str(calculation) + ":" + str(e))
        def get_value(raw_value):
            try:
                if str(raw_value)[0] == '"' and str(raw_value)[-1] == '"':
                    return raw_value[1:len(raw_value)-1]
                elif str(raw_value)[0] == ':':
                    if get_value(raw_value[1:]) in varNames:
                        return varValues[varNames.index(get_value(raw_value[1:]))]
                elif str(raw_value)[0] == '(' and str(raw_value)[-1] == ')':
                    return calculate(raw_value[1:len(raw_value)-1])
                elif str(raw_value)[0] == '[' and str(raw_value)[-1] == ']':
                    return join(raw_value[1:len(raw_value)-1])
                else:
                    return raw_value
            except:
                if not raw_value == "":
                    print("error: can't get value of " + str(raw_value))
                else:
                    return ""
        def split_line(line):
            splitted_line = []
            chars = ""
            inString = False
            inBrackets = 0
            inSquareBrackets = 0
            for i in line:
                if i == '"':
                    chars += i
                    if inString:
                        inString = False
                    else:
                        inString = True
                elif i == "(":
                    chars += i
                    if not inString:
                        inBrackets += 1
                elif i == ")":
                    chars += i
                    if not inString:
                        inBrackets -= 1
                elif i == "[":
                    chars += i
                    if not inString:
                        inSquareBrackets += 1
                elif i == "]":
                    chars += i
                    if not inString:
                        inSquareBrackets -= 1
                elif i == " ":
                    if not inString and inBrackets == 0 and inSquareBrackets == 0:
                        splitted_line.append(chars)
                        chars = ""
                    else:
                        chars += i
                else:
                    chars += i
            splitted_line.append(chars)
            return splitted_line
        while(line < len(code)):
            try:
                i = code[line]
                if not i.replace(" ","").replace("\t","") == "":
                    if not i[0:2] == "//":
                        splitted_code_line = split_line(i)
                        if splitted_code_line[0] == "print":
                            print(get_value(splitted_code_line[1]))
                        elif splitted_code_line[0] == "set":
                            if get_value(splitted_code_line[1]) in varNames:
                                varValues[varNames.index(get_value(splitted_code_line[1]))] = get_value(splitted_code_line[2])
                            else:
                                varNames.append(get_value(splitted_code_line[1]))
                                varValues.append(get_value(splitted_code_line[2]))
                        elif splitted_code_line[0] == "goto":
                            if not str(splitted_code_line[1])[0] == "$":
                                line = int(get_value(splitted_code_line[1])) - 2
                            else:
                                line = int(code.index("$" + get_value(splitted_code_line[1][1:])))
                        elif splitted_code_line[0] == "wait":
                            time.sleep(int(get_value(splitted_code_line[1])))
                        elif splitted_code_line[0] == "if":
                            def equal_as_float():
                                boolean = False
                                try:
                                    boolean = float(get_value(splitted_code_line[1])) != float(get_value(splitted_code_line[2]))
                                except:
                                    boolean = False
                                return boolean
                            if splitted_code_line[2] == "==":
                                if get_value(splitted_code_line[1]) != get_value(splitted_code_line[3]):
                                    expected_ends = 1
                                    while expected_ends > 0:
                                        line += 1
                                        if split_line(code[line])[0] == "if":
                                             expected_ends += 1
                                        if split_line(code[line])[0] == "end_if" or split_line(code[line])[0] == "else":
                                            expected_ends -= 1
                            if splitted_code_line[2] == "!=":
                                if get_value(splitted_code_line[1]) == get_value(splitted_code_line[3]):
                                    expected_ends = 1
                                    while expected_ends > 0:
                                        line += 1
                                        if split_line(code[line])[0] == "if":
                                             expected_ends += 1
                                        if split_line(code[line])[0] == "end_if" or split_line(code[line])[0] == "else":
                                            expected_ends -= 1
                            if splitted_code_line[2] == ">":
                                if not get_value(splitted_code_line[1]) > get_value(splitted_code_line[3]):
                                    expected_ends = 1
                                    while expected_ends > 0:
                                        line += 1
                                        if split_line(code[line])[0] == "if":
                                             expected_ends += 1
                                        if split_line(code[line])[0] == "end_if" or split_line(code[line])[0] == "else":
                                            expected_ends -= 1
                            if splitted_code_line[2] == "<":
                                if not get_value(splitted_code_line[1]) < get_value(splitted_code_line[3]):
                                    expected_ends = 1
                                    while expected_ends > 0:
                                        line += 1
                                        if split_line(code[line])[0] == "if":
                                             expected_ends += 1
                                        if split_line(code[line])[0] == "end_if" or split_line(code[line])[0] == "else":
                                            expected_ends -= 1
                            if splitted_code_line[2] == "!>":
                                if get_value(splitted_code_line[1]) > get_value(splitted_code_line[3]):
                                    expected_ends = 1
                                    while expected_ends > 0:
                                        line += 1
                                        if split_line(code[line])[0] == "if":
                                             expected_ends += 1
                                        if split_line(code[line])[0] == "end_if" or split_line(code[line])[0] == "else":
                                            expected_ends -= 1
                            if splitted_code_line[2] == "!<":
                                if get_value(splitted_code_line[1]) < get_value(splitted_code_line[3]):
                                    expected_ends = 1
                                    while expected_ends > 0:
                                        line += 1
                                        if split_line(code[line])[0] == "if":
                                             expected_ends += 1
                                        if split_line(code[line])[0] == "end_if" or split_line(code[line])[0] == "else":
                                            expected_ends -= 1
                        elif splitted_code_line[0] == "input":
                            if get_value(splitted_code_line[2]) in varNames:
                                varValues[varNames.index(get_value(splitted_code_line[2]))] = input(get_value(splitted_code_line[1]))
                            else:
                                varNames.append(get_value(splitted_code_line[2]))
                                varValues.append(input(get_value(splitted_code_line[1])))
                        elif splitted_code_line[0] == "else":
                            cline = line + 1
                            expected_ends = 1
                            while expected_ends > 0:
                                line += 1
                                if split_line(code[line])[0] == "if":
                                    expected_ends += 1
                                if split_line(code[line])[0] == "end_if" or split_line(code[line])[0] == "else":
                                    expected_ends -= 1
                            line += 1
                        else:
                            if not splitted_code_line[0][0] == "$" and not splitted_code_line[0] in ["end_if"]:
                                print("error in line " + str(line + 1) + " unknown syntax: " + splitted_code_line[0])
            except Exception as e:
                print("runtime error in line " + str(line + 1) + ": " + str(e))
            line += 1
    except Exception as e:
        print("gray has crashed: " + str(e))
try:
    if __name__ == "__main__":
        import sys
        code = []
        try:
            filePath = r"" + str(sys.argv[1]) + ""
        except:
            filePath = input("filepath of your code: ")
        try:
            with open(filePath) as codeFile:
                for line in codeFile:
                    code.append(line.rstrip())
        except:
            print("error while trying to read file")
            exit()
        run(code)
except Exception as e:
    print("gray has crashed: " + str(e))
