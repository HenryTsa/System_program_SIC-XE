def sic_xe_assembler_pass1(input_filename, output_filename,output_filename_2):
    symtab = {}
    locctr = 0
    starting_address = 0
    program_length = 0
    ifFirst=0
    with open(input_filename, 'r') as input_file, open(output_filename, 'w') as output_file :
        for line in input_file:
            fields = line.split()
            label, opcode, operand = fields[:3] if len(fields) >= 3 else ('', fields[0], '')
            if opcode == 'START':
                starting_address = int(operand, 16)
                locctr = starting_address
                output_file.write(line)
                continue
            elif opcode == 'END':
                program_length = locctr - starting_address
                output_file.write(line)
                break
            if label:
                if label in symtab:
                    print(f"Error: Duplicate symbol '{label}'")
                    # Handle error as needed
                else:
                    symtab[label] = locctr

            output_file.write(line.rstrip() + ' ' + str(hex(locctr))+'\n')

            if opcode in ['WORD', 'RESW']:
                locctr += 3
            elif opcode == 'RESB':
                locctr += int(operand) if operand else 0
            elif opcode == 'BYTE':
                if operand.startswith('C'):
                    constant_length = len(operand) - 3
                    locctr += constant_length
                elif operand.startswith('X'):
                    constant_length = (len(operand) - 3)// 2
                    locctr += constant_length
            elif opcode.startswith("+"):
                locctr += 4
            elif opcode in  ['CLEAR', 'COMPR','TIXR']:
                locctr += 2
            elif opcode in  ['BASE']:
                locctr += 0
            else:
                locctr +=3
            
    with open(output_filename_2, 'w') as output_file_2:
        print("Pass 1 completed.")
        print("Symbol Table:")
        for symbol, address in symtab.items():
            formatted_hex = f"{address:#06x}"
            print(f"{symbol}: {formatted_hex.upper()}")
            output_file_2.write(f"{symbol}: {formatted_hex.upper()}\n")
        print(f"Program Length: {program_length}")

# 使用範例
input_filename = 'input.txt'  
output_filename = 'output.txt'  
output_filename_2 = 'output2.txt'
sic_xe_assembler_pass1(input_filename, output_filename,output_filename_2)
