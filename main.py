opcodes = {
    "ADD": "00",
    "MOVE": "01",
    "STORE": "01",
    "LOAD": "01",
    "JMP": "10000000",
    "JPZ": "10000001",
    "JPP": "10000010",
    "JPN": "10000011"
}

val_code = {
    "ADD": "101",
    "MOVE": "101",
    "STORE": "110",
    "LOAD": "110"
}

alpha_bin = {
    "A": "000",
    "B": "001",
    "C": "010",
    "D": "011",
    "E": "100",
}

hex_bin = {
    "0": "0000",
    "1": "0001",
    "2": "0010",
    "3": "0011",
    "4": "0100",
    "5": "0101",
    "6": "0110",
    "7": "0111",
    "8": "1000",
    "9": "1001",
    "A": "1010",
    "B": "1011",
    "C": "1100",
    "D": "1101",
    "E": "1110",
    "F": "1111",
}

bin_hex = {
    "0000": "0",
    "0001": "1",
    "0010": "2",
    "0011": "3",
    "0100": "4",
    "0101": "5",
    "0110": "6",
    "0111": "7",
    "1000": "8",
    "1001": "9",
    "1010": "A",
    "1011": "B",
    "1100": "C",
    "1101": "D",
    "1110": "E",
    "1111": "F",
}


# Convert number to binary with two's compliment
# https://stackoverflow.com/questions/21871829/twos-complement-of-numbers-in-python
def to_twoscomplement(bits, value):
    if value < 0:
        value = (1 << bits) + value
    formatstring = '{:0%ib}' % bits
    return formatstring.format(value)


def is_digit(n):
    try:
        int(n)
        return True
    except ValueError:
        return False


def encode(instruction):
    if not instruction.startswith(tuple(list(opcodes.keys()))):
        print(f"Invalid keyword: {instruction.split(' ')[0]}")
    else:
        # Separate the instruction into sections where there is a space.
        command = instruction.replace(",", "").split(" ")
        ext = ""

        output = ""

        # If the command length is less then 3 (Has no source registry or value) then default to 10 for opcode
        if len(command) <= 1:
            print(f"Invalid format. At least 1 argument is required.")
            return
        elif len(command) < 3:
            opcode_bin = opcodes[command[0]]
            if is_digit(command[1]):
                ext = command[1]
            else:
                print(f"Invalid argument: {instruction.split(' ')[1]}")
                return

            # Split the opcode into 2 4-bit binary digits
            output_bin_split = [opcode_bin[i:i + 4] for i in range(0, len(opcode_bin), 4)]

            # Convert each 4 bit binary digits into a hexadecimal
            output_hex = (''.join(hex(int(a, 2))[2:] for a in output_bin_split)).upper()

            # Split the address into 2 sections and reverse it
            ext_split = [ext[i:i + 2] for i in range(0, len(ext), 2)]
            ext_split.reverse()

            # Combine the output hexadecimal value and extension
            output = output_hex + ''.join(ext_split)

        else:
            # Get the binary opcode of the command from the opcodes dictionary
            opcode_bin = opcodes[command[0]]

            # Checks if destination is a value or a registry
            if is_digit(str(command[1])):
                # The destination has digits, therefor will require an extension
                dest_bin = val_code[command[0]]
                ext = command[1]
            else:
                # An address has been detected, will format the address to hex
                dest_bin = alpha_bin[command[1]]

            # Checks if source section is a value or a registry
            if is_digit(str(command[2])):
                # The destination has digits, therefor will require an extension
                src_bin = val_code[command[0]]
                # Checks if the digits is a negative
                if int(command[2]) < 0:
                    # Will perform a format into hexadecimal for the extension
                    ext_bin = to_twoscomplement(8, int(command[2]))
                    ext_bin_split = [ext_bin[i:i + 4] for i in range(0, len(ext_bin), 4)]
                    ext = (''.join(hex(int(a, 2))[2:] for a in ext_bin_split)).upper()
                else:
                    # Will use the number provided for the extension
                    ext = command[2]

            else:
                # An address has been detected, will format the address to hex
                src_bin = alpha_bin[command[2]]

            # Combine all binary numbers into one string
            output_bin = f"{opcode_bin}{dest_bin}{src_bin}"

            # Split the output into 2 4-bit binary numbers
            output_bin_split = [output_bin[i:i + 4] for i in range(0, len(output_bin), 4)]

            # Convert each 4 bit binary number into a hexadecimal
            output_hex = (''.join(hex(int(a, 2))[2:] for a in output_bin_split)).upper()

            # Split the address into 2 sections and reverse it
            ext_split = [ext[i:i + 2] for i in range(0, len(ext), 2)]
            ext_split.reverse()

            # Combine the output hexadecimal value and extension
            output = output_hex + ''.join(ext_split)

        return output


def decode(instruction):
    # Validates the instruction
    if not instruction[0].isdigit():
        print(f"Invalid format. Instruction must start with a number")
    else:
        import bitstring

        # Converts each character from the hexadecimal string into binary
        bin_str = ""
        for char in instruction:
            bin_str += hex_bin[char]

        # Splits the binary string into instruction and extension
        base_instruction = bin_str[:8]
        ext = bin_str[8:]

        # Splits the binary instruction into the opcode, destination and source sections
        opcode_ins = base_instruction[:2]
        dest_ins = base_instruction[2:5]
        src_ins = base_instruction[5:8]

        # Checks if there is an extension
        if ext:
            # Converts binary into positive digits and swaps the values
            if len(ext) != 8:
                ext_bin_4 = [ext[i:i + 4] for i in range(0, len(ext), 4)]
                ext_bin_1 = []
                for bin_val in ext_bin_4:
                    ext_bin_1.append(str(int(bin_val, 2)))

                ext_int_dual = [ext_bin_1[0] + ext_bin_1[1], ext_bin_1[2] + ext_bin_1[3]]
                ext_int_dual.reverse()
            else:
                # Converts binary into negative digits and swaps the values
                ext_int_dual = str(bitstring.BitArray(bin=str(ext)).int)
        else:
            # Converts binary hexadecimal
            ext_int_dual = list(alpha_bin.keys())[list(alpha_bin.values()).index(src_ins)]

        if base_instruction in list(opcodes.values()):
            # Perform JMPs
            output = f"{list(opcodes.keys())[list(opcodes.values()).index(base_instruction)]} {''.join(ext_int_dual)}"
        else:
            # Performs other commands
            if dest_ins in list(alpha_bin.values()):
                # Can perform LOAD, ADD or MOVE
                if src_ins == "110":
                    # Perform LOAD
                    output = f"LOAD {list(alpha_bin.keys())[list(alpha_bin.values()).index(dest_ins)]}, {''.join(ext_int_dual)}"
                    pass
                else:
                    if opcode_ins == "00":
                        # Perform ADD
                        output = f"ADD {list(alpha_bin.keys())[list(alpha_bin.values()).index(dest_ins)]}, {''.join(ext_int_dual)}"
                    else:
                        # Perform MOVE
                        output = f"MOVE {list(alpha_bin.keys())[list(alpha_bin.values()).index(dest_ins)]}, {''.join(ext_int_dual)}"
            else:
                # Can Perform STORE
                output = f"STORE {''.join(ext_int_dual)}, {list(alpha_bin.keys())[list(alpha_bin.values()).index(src_ins)]}"

        return output


def main():
    import os
    option = -1

    while option <= 0 or option >= 3:
        print("1. Encode")
        print("2. Decode")
        option = int(input("Pick an option: "))
        print()

    if option == 2:
        print("Enter an instruction to be encoded from hexadecimal into assembly (e.g. 5DFB)")
        print("Or enter a filename in the current directory (e.g. decode_me.txt)")
        instruction_str = str(input())
        if os.path.isfile(instruction_str):
            with open(instruction_str, "r") as file:
                for line in file:
                    decoded_line = decode(line.strip())
                    if decoded_line is not None:
                        print(f"[{line.strip()}] -> {decoded_line}")
            file.close()
        else:
            decoded_line = decode(instruction_str.strip())
            if decoded_line is not None:
                print(f"[{instruction_str.strip()}] -> {decoded_line}")
    else:
        print("Enter an instruction to be encoded from assembly into hexadecimal (e.g. MOVE D, -5)")
        print("Or enter a filename in the current directory (e.g. encode_me.txt)")
        instruction_str = str(input())
        if os.path.isfile(instruction_str):
            with open(instruction_str, "r") as file:
                for line in file:
                    encoded_line = encode(line.strip())
                    if encoded_line is not None:
                        print(f"[{line.strip()}] -> {encoded_line}")
            file.close()
        else:
            encoded_line = encode(instruction_str.strip())
            if encoded_line is not None:
                print(f"[{instruction_str.strip()}] -> {encoded_line}")


if __name__ == "__main__":
    main()
