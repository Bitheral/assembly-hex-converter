opcodes = {
    "ADD": "00",
    "MOVE": "01",
    "STORE": "01",
    "LOAD": "01",
    "JMP": "10",
    "JPZ": "10",
    "JPP": "10",
    "JPN": "10"
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

# def splitAt(w, n):
#     for i in range(0, len(w), n):
#         yield w[i:i + n]

def to_twoscomplement(bits, value):
    if value < 0:
        value = ( 1<<bits ) + value
    formatstring = '{:0%ib}' % bits
    return formatstring.format(value)

def isBinary(num):
    for i in str(int(num)):
        if i in ("0","1") == False:
            return False
    return True

def is_digit(n):
    try:
        int(n)
        return True
    except ValueError:
        return False


def encode(instruction):
    command = instruction.replace(",", "").split(" ")
    opcode = ""
    dest = ""
    src = ""
    ext = ""
    output = ""

    if len(command) < 3:
        opcode = "10"
    else:
        opcode = opcodes[command[0]]
        if is_digit(command[2]):
            src = val_code[command[0]]
            value = ""
            if command[2].startswith('-'):
                value = to_twoscomplement(8, int(command[2]))
            else:
                value = command[2]

            hexval_str = ""
            if isBinary(value):
                hexval_split = [value[i:i + 4] for i in range(0, len(value), 4)]
                hexval_str = (''.join(hex(int(a, 2))[2:] for a in hexval_split)).upper()
            else:
                ext_temp = [value[i:i + 2] for i in range(0, len(value), 2)]
                ext_temp.reverse()
            ext = hexval_str if isBinary(value) else ''.join(ext_temp)
        else:
            for index, char in enumerate(command[2]):
                src += alpha_bin[char]

    if command[1].isnumeric():
        dest = val_code[command[0]]
        ext_temp = [command[1][i:i + 2] for i in range(0, len(command[1]), 2)]
        ext_temp.reverse()
        ext = ''.join(ext_temp)
    else:
        for index, char in enumerate(command[1]):
            dest += alpha_bin[char]

    hexcode = (opcode + dest + src)
    hexcode_split = [hexcode[i:i + 4] for i in range(0, len(hexcode), 4)]

    hexcode_str = (''.join(hex(int(a, 2))[2:] for a in hexcode_split)).upper()

    output = hexcode_str + ext  # hexcode_split + ext

    print(output)


def decode(instruction):
    import struct
    import bitstring
    command_hex = [instruction[:2], instruction[2:4]]

    command = ["", ""]

    bin_str = ""
    for char in command_hex[0]:
        bin_str += hex_bin[char]

    if bin_str[2:5] in list(val_code.values()):
        if opcodes[list(val_code.keys())[list(val_code.values()).index(bin_str[2:5])]] == bin_str[:2]:
            command[0] = list(val_code.keys())[list(val_code.values()).index(bin_str[2:5])]
            command[1] = list(alpha_bin.keys())[list(alpha_bin.values()).index(bin_str[5:])]
            ext = [instruction[i:i + 2] for i in range(2, len(instruction), 2)]
            ext.reverse()
            command.append(''.join(ext))
    else:
        command[0] = list(opcodes.keys())[list(opcodes.values()).index(bin_str[:2])]
        if bin_str[2:5] not in list(alpha_bin.values()):
            command[1] = list(alpha_bin.keys())[list(alpha_bin.values()).index(bin_str[5:])]
        else:
            command[1] = list(alpha_bin.keys())[list(alpha_bin.values()).index(bin_str[2:5])]
            value_bin = ""
            for char in instruction[-2:]:
                value_bin += hex_bin[char]

            command.append(str(bitstring.BitArray(bin=value_bin).int))

    command_word = command[0]
    command_src = command[1]
    command_req = command_word + " " + command_src

    command_str = command_req if len(instruction) < 3 else command_req + ", " + command[2]
    print(command_str)



def main():
    print("1. Decode")
    print("2. Encode")
    option = int(input("Pick an option: "))

    optionState = option - 1
    if optionState:
        print("Enter an instruction to be decoded from hexadecimal into assembly (e.g. MOVE D, -5)")
        instruction_str = str(input())
        encode(instruction_str)
    else:
        print("Enter an instruction to be encoded from hexadecimal into assembly (e.g. 5DFB)")
        instruction_str = str(input())
        decode(instruction_str)


main()

# a map for the other way


def hexToBin(hexString):
    # can validate the string here if needed

    # start with an empty output
    binaryString = ""

    # loop through mapping each digit to the dictionary and retrieving the associated binary
    marker = 0

    while marker < len(hexString):
        # add the next four digits onto the string
        binaryString += hexToBinDictionary.get(hexString[marker])
        # move the marker so we are looking at the next digit
        marker += 1

    return binaryString


def binToHex(binaryString):
    # make sure the string has blocks of 4 bits
    while len(binaryString)%4 != 0:
        binaryString = "0"+binaryString

    # now go through the string and convert each 4 blocks to a Hex digit using the dictionary defined at the start of this file.
    marker = 0
    returnString = ""
    while marker < len(binaryString):
        returnString += binToHexDictionary.get(binaryString[marker:marker+4])
        marker += 4

    return returnString

