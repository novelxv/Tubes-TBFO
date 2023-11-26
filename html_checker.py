import sys

def read_pda_definition(file_path):
    # Membaca definisi PDA dari file eksternal
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Parsing PDA definition
    states = lines[0].strip().split()
    input_symbols = lines[1].strip().split()
    stack_symbols = lines[2].strip().split()
    start_state = lines[3].strip().split()
    start_stack = lines[4].strip().split()
    accepting_states = lines[5].strip().split()
    accept_condition = lines[6].strip().split()

    # Parsing productions
    productions = [line.strip().split() for line in lines[7:]]
    
    return {
        'states' : states,
        'input_symbols' : input_symbols,
        'stack_symbols' : stack_symbols,
        'start_state' : start_state,
        'start_stack' : start_stack,
        'accepting_states' : accepting_states,
        'accept_condition' : accept_condition,
        'productions' : productions
    } 

def read_html_code(file_path):
    # Membaca kode HTML dari file eksternal
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    # Menghapus karakter newline dan menggabungkan baris
    html_code = ''.join(line.strip() for line in lines)
    return html_code
    
def convert_html_symbols(html_code):
    # Mengonversi simbol-simbol dalam HTML
    symbol_mapping = {
        '/html': 'c1', 'html': 'c',
        '/head': 'd1', 'head': 'd',
        '/body': 'e1', '/button': 'w1', 'button' : 'w',
        '/b': 'b1', 'body': 'e3', 
        '/title': 'f1', 'title': 'f',
        'link': 'g',
        '/h1': 'i1', 'h1': 'i',
        '/h2': 'j1', 'h2': 'j',
        '/h3': 'k1', 'h3': 'k',
        '/h4': 'l1', 'h4': 'l',
        '/h5': 'm1', 'h5': 'm',
        '/h6': 'n1', 'h6': 'n',
        '/script': 'h1', 'script': 'h',
        '/em': 'o1', 'em': 'o',
        '/p': 'p1',
        '/abbr': 'q1', 'abbr': 'q',
        '/strong': 'r1', 'strong': 'r',
        '/small': 's1', 'small': 's',
        'br': 't', 
        ' href=' : '2c',
        'hr': 't',
        '/div': 'u1', 'div': 'u',
        'img': 'v', 
        '/form': 'x1', 'form': 'x',
        'input': 'y', '/table': 'z1', 'table': 'z',
        '/tr': 'aa1', 'tr': 'aa',
        '/td': 'ab1', 'td': 'ab',
        ' method=': '2h',
        '/th': 'ac1', 'th': 'ac',
        ' id=': '2a', ' class=': '2a',
        ' style=': '2a', ' rel=': '2b',
        ' src=': '2d', ' alt=': '2e', ' type=': '2f',
        ' action=': '2g', 'submit': 'w3',
        'reset': 'w3', 'GET': 'x3',
        'POST': 'x3', 'text': 'y3', 'password': 'y3',
        'email': 'y3', 'number': 'y3', 'checkbox': 'y3',
        '<!' : '$', '--' : '_',
        '/a': 'a1', '”' : '"'
    }

    converted_code = html_code
    for original_symbol, new_symbol in symbol_mapping.items():
        converted_code = converted_code.replace(original_symbol, new_symbol)
    print(converted_code) # debug
    return converted_code

def process_input_symbols(current_state, input, stack, productions, found_production):
    found_production = False
    print(f"current_state: {current_state}, input: {input}, top_stack: {stack[0]}")
    for production in productions:
        if (
            production[0] == current_state and
            (production[1] == input or production[1] == 'e') and
            production[2][0] == stack[0]
        ):
            print("masuk") # debug
            current_state = production[3]
            print("curr state: ", current_state) # debug

            if production[2] != production[4]:
                if production[1] != 'e':
                    if production[4] == 'e':
                        stack.pop(0)
                        if len(production[2]) > 1:
                            stack.pop(0)
                            if len(production[2]) == 3:
                                stack.pop(0)
                    else:
                        stack.insert(0, production[4][0])
            print(stack) # debug
            
            found_production = True
            break

    if not found_production:
        print(f"Syntax Error at character '{input}'")

    return current_state, stack, found_production
    
def evaluate_html_with_pda(html_code, pda_definition):
    # Mengevaluasi kode HTML dengan menggunakan PDA
    start_state = pda_definition['start_state']
    start_stack = pda_definition['start_stack']
    accepting_states = pda_definition['accepting_states']
    productions = pda_definition['productions']
    
    in_atribut = ['w', 'w3', 'x3', 'y3']

    current_state = start_state[0]
    stack = [start_stack[0]]
    found_production = True
    
    print("STACK\n", stack[0]) # debug

    if (html_code[0] != "<"):
        print("Kode HTML harus diawali '<'")
    else:
        input = ""
        inside_tag = False
        count_petik = 0
        count_underscore = 0
        comment = False
        i = 0

        if found_production:
            for char in html_code:
                # >|sss $ _ * _ > sss|<      debug
                # print(f"current_state: {current_state}, char: {char}, input: {input}, stack: {stack}")
                if (char == '<' and not inside_tag):
                    if i != 0 and input:
                        input = '*'
                        print("input:", input) # debug
                        if found_production:
                            current_state, stack, found_production = process_input_symbols(current_state, input, stack, productions, found_production)
                    inside_tag = True
                    if found_production:
                        current_state, stack, found_production = process_input_symbols(current_state, char, stack, productions, found_production)
                    input = ""
                elif (char != '>'): 
                    if char == '2' and inside_tag:
                        if input:
                            print("input:", input) # debug
                            if found_production:
                                current_state, stack, found_production = process_input_symbols(current_state, input, stack, productions, found_production)
                            print("stack setelah proses input: ", stack)  # debug
                        input = char
                    elif char == '"' and inside_tag:
                        count_petik += 1
                        if count_petik == 1:
                            if input:
                                print("input:", input) # debug
                                if found_production:
                                    current_state, stack, found_production = process_input_symbols(current_state, input, stack, productions, found_production)
                                print("stack setelah proses input: ", stack)  # debug
                        elif count_petik == 2:
                            count_petik = 0 
                            if input:
                                if input not in in_atribut:
                                    input = "*"
                                if found_production:
                                    current_state, stack, found_production = process_input_symbols(current_state, input, stack, productions, found_production)
                        if found_production: 
                            current_state, stack, found_production = process_input_symbols(current_state, char, stack, productions, found_production)    
                        input = ""   
                    elif (char == '$' or (char == '_' and count_underscore == 0 and comment)) and not inside_tag:
                        if char == '$':
                            comment = True
                        if char == '_':
                            count_underscore += 1
                        input = char
                        print("input:", input) # debug
                        if found_production:
                            current_state, stack, found_production = process_input_symbols(current_state, input, stack, productions, found_production)
                        print("stack setelah proses input: ", stack) # debug
                    elif char == '_' and count_underscore == 1 and not inside_tag:
                        input = '*'
                        print("string dalam komen") # debug
                        if found_production:
                            current_state, stack, found_production = process_input_symbols(current_state, input, stack, productions, found_production)
                        input = char
                        print("proses _ kedua komen") # debug
                        if found_production:
                            current_state, stack, found_production = process_input_symbols(current_state, char, stack, productions, found_production)
                    else: 
                        input += char
                elif (input == '_' and count_underscore == 1 and char == '>' and not inside_tag):
                    count_underscore = 0
                    print("proses > tutup komen") # debug
                    if found_production:
                        current_state, stack, found_production = process_input_symbols(current_state, char, stack, productions, found_production)
                    input = ""
                elif (char == '>' and inside_tag):
                    inside_tag = False
                    if input:
                        print("input:", input) # debug
                        if found_production:
                            current_state, stack, found_production = process_input_symbols(current_state, input, stack, productions, found_production)
                        print("stack setelah proses input: ", stack)   # debug             
                    if found_production:
                        current_state, stack, found_production = process_input_symbols(current_state, char, stack, productions, found_production)
                    print("current state: ", current_state) # debug
                    input = ""
                
                print(i) # debug
                i += 1
            
            if inside_tag:
                print("< tidak ditutup")
            else:
                if input:
                    print("Terdapat string bebas setelah '>' terakhir")

    # Cek final state
    if current_state in accepting_states:
        return True
    else:
        return False

def main():

    print("                                             Halo Kakak Asisten")
    print("")
    print("                             88888888888   888888b.     8888888888    .d88888b. ")
    print("                                 888       888  '88b    888          d88P' 'Y88b ")
    print("                                 888       888  .88P    8888888      888     888 ")
    print("                                 888       8888888K.    888          888     888 ")
    print("                                 888       888   Y88b   888          888     888 ")
    print("                                 888       888    888   888          888     888 ")
    print("                                 888       888   d88P   888          Y88b. .d88P  ")
    print("                                 888       8888888P'    888           'Y88888P'  ")
    print("")
    print("                                                Kami (dari)")
    print("")
    print("888b     d888                                888               888       888                                           ")
    print("8888b   d8888                          888   888               888   o   888                                           ")
    print("88888b.d88888                                888               888  d8b  888                                           ")
    print("888Y88888P888     8888b.   .d8888b     888   88888b.           888 d888b 888    8888b.    888d888     8888b.   .d8888b")
    print("888 Y888P 888       '88b   88K         888   888 '88b          888d88888b888       '88b   888P'         '88b   88K     ")
    print("888  Y8P  888   .d888888   'Y8888b.    888   888  888          88888P Y88888   .d888888   888       .d888888   'Y8888b.")
    print("888   '   888   888  888        X88    888   888  888          8888P   Y8888   888  888   888       888  888        X88")
    print("888       888   'Y888888    88888P'    888   888  888          888P     Y888   'Y888888   888       'Y888888    88888P'")

    if len(sys.argv) != 3:
        print("Usage: python html_checker.py <pda_definition_file> <html_file>")
        sys.exit(1)

    pda_definition_file = sys.argv[1]
    html_file = sys.argv[2]

    pda_definition = read_pda_definition(pda_definition_file)
    html_code = read_html_code(html_file)
    html_code = convert_html_symbols(html_code)
    result = evaluate_html_with_pda(html_code, pda_definition)

    if result:
        print("Accepted")
    else:
        print("Syntax Error")

if __name__ == "__main__":
    main()