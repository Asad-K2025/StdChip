import sys
import os

MAGIC = [0xF2, 0xC3, 0x38]
VERSION = [0x01]


def get_header():  # Helper for verification header
    return MAGIC + VERSION


# Instructions in binary format
OPCODES = {
    "SET": 0b00000001,
    "MOV": 0b00000010,
    "ADD": 0b00000011,
    "SUB": 0b00000100,
    "READ": 0b00001000,
    "PUT": 0b00001001,
    "JMP": 0b00010000,
    "JEQ": 0b00010001,
    "JGT": 0b00010010,
    "CALL": 0b00100000,
    "EXIT": 0b00100001,
}


def parse_value(value):  # Helper function converts values to base 10 and returns
    value = value.strip()

    if len(value) == 3 and value.startswith("'") and value.endswith("'"): # ASCII character in single quotes
        return ord(value[1])
    elif value.startswith("0b"):  # Binary
        return int(value, 2)
    elif value.startswith("0x"):  # Hex
        return int(value, 16)
    elif value.startswith("0o"):
        return int(value, 8)
    else:
        return int(value)


def process_instruction(op, operand, line_no):  # Process line based on opcode instruction
    try:
        if op == "SET":
            destination, value = map(parse_value, operand)  # Covert strings to integers with helper function
            return [OPCODES[op], destination & 0xFF, value & 0xFF, 0x00]  # Return line as array to write to bin and hex files

        elif op == "MOV":
            destination, source = map(parse_value, operand)
            return [OPCODES[op], destination & 0xFF, source & 0xFF, 0x00]

        elif op == "ADD":
            destination, addr_a, addr_b = map(parse_value, operand)
            return [OPCODES[op], destination & 0xFF, addr_a & 0xFF, addr_b & 0xFF]

        elif op == "SUB":
            destination, addr_a, addr_b = map(parse_value, operand)
            return [OPCODES[op], destination & 0xFF, addr_a & 0xFF, addr_b & 0xFF]

        elif op == "READ":
            if len(operand) == 2 and operand[1].upper() == "N":
                destination = parse_value(operand[0])
                return [OPCODES[op], destination & 0xFF, 0x01, 0x00]
            elif len(operand) == 3 and operand[1].upper() == "S":
                destination = parse_value(operand[0])
                count = parse_value(operand[2])
                return [OPCODES[op], destination & 0xFF, 0x02, count & 0xFF]
            else:
                raise ValueError

        elif op == "PUT":
            if len(operand) == 3 and operand[1] == "N":
                source = parse_value(operand[0])
                format = ord(operand[2]) & 0x7F
                return [OPCODES[op], source & 0xFF, format, 0x00]
            elif len(operand) == 3 and operand[1] == "S":
                source = parse_value(operand[0])
                count = parse_value(operand[2])
                return [OPCODES[op], source & 0xFF, 0x80, count & 0xFF]
            else:
                raise ValueError

        elif op == "JMP":
            label = parse_value(operand[0])
            return [OPCODES[op], label & 0xFF, 0x00, 0x00]

        elif op == "JEQ":
            label, addr_a, addr_b = map(parse_value, operand)
            return [OPCODES[op], label & 0xFF, addr_a & 0xFF, addr_b & 0xFF]

        elif op == "JGT":
            label, addr_a, addr_b = map(parse_value, operand)
            return [OPCODES[op], label & 0xFF, addr_a & 0xFF, addr_b & 0xFF]

        elif op == "CALL":
            destination, pointer = map(parse_value, operand)
            return [OPCODES[op], destination & 0xFF, pointer & 0xFF, 0x00]

        elif op == "EXIT":
            source = parse_value(operand[0])
            return [OPCODES[op], source & 0xFF, 0x00, 0x00]
        else:
            raise KeyError  # None of the instructions were matched
    except ValueError:
        sys.stderr.write(f"assembler.py: Malformed instruction on line {line_no}")
        sys.exit(1)
    except KeyError:
        sys.stderr.write(f"assembler.py: Unknown operation '{op}' on line {line_no}")
        sys.exit(1)


def main(args: list[str]):
    hex_output = False  # Flag to determine hex output

    if len(args) == 3 and args[0] == "--hex":
        hex_output = True
        in_file, out_file = args[1], args[2]
    elif len(args) == 2:
        in_file, out_file = args[0], args[1]
    else:
        print("Usage: python3 assembler.py [--hex] <in_file.asm> <out_file.bin>")
        sys.exit(0)

    if not os.path.exists(in_file):
        sys.stderr.write(f"assembler.py: File {in_file} does not exist.")
        sys.exit(1)
    elif not os.access(in_file, os.R_OK):
        sys.stderr.write(f"assembler.py: File {in_file} cannot be read.")
        sys.exit(1)
    elif os.path.exists(out_file) and not os.access(out_file, os.W_OK):
        sys.stderr.write(f"assembler.py: File {out_file} cannot be written to.")
        sys.exit(1)

    labels = {}  # Stores labels with their instruction index
    instruction_lines = []  # Holds (line_no, op, operands) as tuple
    instruction_index = 0  # Tracks how many isntructions have been processed

    with open(in_file, "r") as file:  # Store instructions in array
        for line_no, line in enumerate(file, start=1):
            line = line.split("//")[0].strip()  # Remove comments and blank whitespaces
            if not line or line.startswith("//"):  # Ignore full-comment and blank line
                continue
            if line.startswith(":") and line.endswith(":"):  # Label managing
                label_name = line[1:-1].strip()
                labels[label_name] = instruction_index
                continue
            line_parts = line.split()
            op = line_parts[0].upper()  # Op = operation, eg. ADD
            operands = line_parts[1:]  # Rest of the instruction
            instruction_lines.append((line_no, op, operands))
            instruction_index += 1

    instructions = []

    for line_no, op, operands in instruction_lines:  # loop 2 for label managing
        if op in ("JMP", "JEQ", "JGT"):  # Jump instructions
            if operands[0] in labels:  # Check for labels name in instruction and replace it with its instruction code
                operands[0] = str(labels[operands[0]])
            else:
                sys.stderr.write(f"assembler.py: Undefined label name: {operands[0]}")
                sys.exit(1)
        instructions.extend(process_instruction(op, operands, line_no))

    with open(out_file, "wb") as f:
        f.write(bytearray(get_header() + instructions))

    if hex_output:
        hex_filename = out_file.split(".")[0] + ".hex"
        with open(hex_filename, "w", encoding="ascii", newline="\n") as hex_file:
            for (line_no, op, operands), i in zip(instruction_lines, range(0, len(instructions), 4)):
                # Iterates over instruction and byte offset
                four_bytes_line = instructions[i:i + 4]
                hex_bytes = "".join(f"{byte:02X}" for byte in four_bytes_line)  # Convert each byte to hex and join
                original_line = f"{op} {' '.join(operands)}"
                hex_file.write(f"{original_line}: {hex_bytes}\n")


if __name__ == "__main__":
    main(sys.argv[1:])

