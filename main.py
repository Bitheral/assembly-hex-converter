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

alpha_bin = {
    "A": "000",
    "B": "001",
    "C": "010",
    "D": "011",
    "E": "100"
}

numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]


def splitAt(w, n):
    for i in range(0, len(w), n):
        yield w[i:i + n]


def encode(instruction):
    instruction_bits = [0, 0, 0, 0, 0, 0, 0, 0]
    sectors = instruction.replace(",", "").split(" ")
    for index, bit in enumerate(opcodes[sectors[0]]):
        instruction_bits[int(index)] = int(bit)

    if sectors[0] == "STORE":
        instruction_bits[2] = 1
        instruction_bits[3] = 1
        instruction_bits[4] = 0
    else:
        pass

    if not sectors[2].replace('-', '').isdigit():
        # Address
        if sectors[0] == "STORE":
            bits = alpha_bin[sectors[2]]
            for index, bit in enumerate(bits):
                instruction_bits[int(index) + 5] = int(bit)
    else:
        # Value
        #if sectors[0] == "ADD":

        pass

    instruction_bit_str = ""
    for index, bit in enumerate(instruction_bits):
        instruction_bit_str += str(bit)
        if index == 3:
            instruction_bit_str += " "

    instruction_hex = []
    instruction_bit_hex = instruction_bit_str.split(" ")
    for hex_bits in instruction_bit_hex:
        instruction_hex.append(str(int(hex_bits, 2)))

    addr = sectors[1]
    temp_addr = [addr[i:i + 2] for i in range(0, len(addr), 2)]
    temp_addr.reverse()
    for addr_split in temp_addr:
        instruction_hex.append(addr_split)

    print(''.join(instruction_hex))


def decode():
    pass


def main():
    print("1. Decode")
    print("2. Encode")
    option = int(input("Pick an option: "))

    optionState = option - 1
    if optionState:
        print("Enter an insturction to be encoded into hexadecimal")
        instruction_str = str(input())
        encode(instruction_str)
    else:
        decode()


main()
