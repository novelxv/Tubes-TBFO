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
    with open(file_path, 'r') as file:
        lines = file.readlines()
    # Menghapus karakter newline dan menggabungkan baris
    html_code = ''.join(line.strip() for line in lines)
    return html_code
    
def convert_html_symbols(html_code):
    # Mengonversi simbol-simbol dalam HTML
    symbol_mapping = {
        '/html' : 'c1', 'html' : 'c', 
        '/head' : 'd1', 'head' : 'd',
        '/body' : 'e1', 'body' : 'e3',
        '/title' : 'f1', 'title' : 'f',
        'link' : 'g', 
        '/h1' : 'i1', 'h1' : 'i',
        '/h2' : 'j1', 'h2' : 'j',
        '/h3' : 'k1', 'h3' : 'k',
        '/h4' : 'l1', 'h4' : 'l',
        '/h5' : 'm1', 'h5' : 'm',
        '/h6' : 'n1', 'h6' : 'n',
        '/script' : 'h1', 'script' : 'h',
        'em' : 'o', 'abbr' : 'q', 'strong' : 'r',
        'small' : 's', 'br' : 't', 'hr' : 't',
        'div' : 'u', 'img' : 'v', 'button' : 'w',
        'form' : 'x', 'input' : 'y', 'table' : 'z',
        'tr' : 'aa', 'td' : 'ab', 'th' : 'ac',
        '/a' : 'a1', '/b' : 'b1', 
        '/em' : 'o1', '/p' : 'p1',
        '/abbr' : 'q1', '/strong' : 'r1', '/small' : 's1',
        '/div' : 'u1', '/button' : 'w1', '/form' : '/x1',
        '/table' : 'z1', '/tr' : 'aa1', '/td' : 'ab1', 
        '/th' : 'ac1', 'id=' : 'a2', 'class=' : 'a2',
        'style=' : 'a2', 'rel=' : 'b2', 'href=' : 'c2',
        'src=' : 'd2', 'alt=' : 'e2', 'type=' : 'f2',
        'action=' : 'g2', 'method=' : 'h2', 'submit' : 'l3',
        'reset' : 'l3', 'button' : 'l3', 'GET' : 'm3', 
        'POST' : 'm3', 'text' : 'n3', 'password' : 'n3',
        'email' : 'n3', 'number' : 'n3', 'checkbox' : 'n3', 
    }

    converted_code = html_code
    for original_symbol, new_symbol in symbol_mapping.items():
        converted_code = converted_code.replace(original_symbol, new_symbol)
    print(converted_code)
    return converted_code
    
def evaluate_html_with_pda(html_code, pda_definition):
    # Mengevaluasi kode HTML dengan menggunakan PDA
    states = pda_definition['states']
    input_symbols = pda_definition['input_symbols']
    stack_symbols = pda_definition['stack_symbols']
    start_state = pda_definition['start_state']
    start_stack = pda_definition['start_stack']
    accepting_states = pda_definition['accepting_states']
    accept_condition = pda_definition['accept_condition']
    productions = pda_definition['productions']

    current_state = start_state[0]
    stack = [start_stack[0]]
    print("STACK\n", stack[0])
    i = 0
    for char in html_code:
        found_production = False
        print(f"current_state: {current_state}, char: {char}, stack: {stack}")
        for production in productions:
            # print(production)
            # print(f"curr_state: {production[0]}, readfw: {production[1]}, takefs: {production[2]}")
            if (
                production[0] == current_state and
                (production[1] == char or production[1] == 'e') and
                production[2] == stack[0]
            ):
                print("masuk")
                # print(production[4])
                current_state = production[3]
                # stack.pop(0)
                # print(stack)
                # print("Setelah pop", stack)
                if production[1] != 'e':
                    if production[4] == 'e':
                        stack.pop(0)
                    else:
                        stack.insert(0, production[4][0])
                print(stack)
                # if production[4] != 'e':
                #     # stack.extend(list(production[4]))
                #     # print(stack)
                #     for symbol in production[4]:
                #         stack.insert(-1, symbol)
                #     print(stack)
                
                found_production = True
                break
        print(i)
        i += 1
        if not found_production:
            print(f"Syntax Error at character '{char}'")
            return False

    # Cek final state
    if current_state in accepting_states:
        return True
    else:
        return False

def main():
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