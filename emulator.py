import sys
import os

MAGIC = [0xF2, 0xC3, 0x38]
VERSION = [0x01]  # Header section for validating binary file


def main(args: list[str], registers=None):
    if len(args) < 1:
        sys.stderr.write("Usage: python3 emulator.py <executable>")
        sys.exit(1)

    filename = args[0]

    if not os.path.exists(filename):
        sys.stderr.write(f"emulator.py: File {filename} does not exist.")
        sys.exit(1)
    elif not os.access(filename, os.R_OK):
        sys.stderr.write(f"emulator.py: File {filename} cannot be read.")
        sys.exit(1)

    with open(filename, "rb") as f:
        data = list(f.read())

    if data[:4] != MAGIC + VERSION:  # Read first 4 bytes for veifictaion
        sys.stderr.write(f"emulator.py: File {filename} is not a valid StdChip executable.")
        sys.exit(1)

    instructions = data[4:]
    if registers is None:  # Used to chekc if this is not a child process (otherwise it needs to share memory)
        registers = [0] * 256
    pc = 0

    while pc < len(instructions):
        opcode = instructions[pc]
        a, b, c = instructions[pc+1], instructions[pc+2], instructions[pc+3]

        if opcode == 0x01:  # SET
            registers[a] = b

        elif opcode == 0x02:  # MOV
            registers[a] = registers[b]

        elif opcode == 0x03:  # ADD
            registers[a] = (registers[b] + registers[c]) & 0xFF  # 0xFF bitwise operation for restiricting till 255

        elif opcode == 0x04:  # SUB
            registers[a] = (registers[b] - registers[c]) & 0xFF

        elif opcode == 0x08:  # READ
            if b == 0x01:  # READ N
                try:
                    value = int(input())
                    registers[a] = value & 0xFF
                except ValueError:
                    registers[a] = 0
            elif b == 0x02:  # READ S
                try:
                    text = input()
                    for i in range(c):
                        if i < len(text):
                            registers[a + i] = ord(text[i]) & 0xFF
                        else:
                            registers[a + i] = 0
                except Exception:
                    for i in range(c):
                        registers[a + i] = 0

        elif opcode == 0x09:  # PUT
            if b == 0x80:  # PUT S
                output = ''.join(
                    chr(registers[a + i]) if registers[a + i] != 0 else ' '
                    for i in range(c)
                )  # Join to print as single string
                print(output, end="")
            else:  # PUT N
                format_char = chr(b)
                value = registers[a]
                if format_char == 'd':
                    print(f"{value}", end="")
                elif format_char == 'x':
                    print(f"{value:x}", end="")
                elif format_char == 'X':
                    print(f"{value:X}", end="")
                elif format_char == 'b':
                    print(f"{value:b}", end="")
                else:
                    print(f"{value}", end="")

        elif opcode == 0x10:  # JMP
            pc = a * 4
            continue

        elif opcode == 0x11:  # JEQ
            if registers[b] == registers[c]:
                pc = a * 4
                continue

        elif opcode == 0x12:  # JGT
            if registers[b] > registers[c]:
                pc = a * 4
                continue

        elif opcode == 0x20:  # CALL
            # Extract string from registers starting at b
            filename_chars = []
            i = b
            while registers[i] != 0:
                filename_chars.append(chr(registers[i]))
                i += 1
            child_filename = ''.join(filename_chars)

            pid = os.fork()
            if pid == 0:
                # Child process
                try:
                    main([child_filename], registers)  # Call child process with shared memory through same registers
                    sys.exit(0)
                except Exception:
                    sys.stderr.write(f"emulator.py: File {child_filename} is not a valid StdChip executable.")
                    sys.exit(1)
            else:
                # Parent process
                _, status = os.wait()
                exit_code = os.WEXITSTATUS(status)
                registers[a] = exit_code & 0xFF

        elif opcode == 0x21:  # EXIT
            sys.exit(registers[a])

        else:
            sys.stderr.write(f"emulator.py: Unknown opcode {opcode:02X} at pc={pc}")
            sys.exit(1)

        pc += 4

if __name__ == "__main__":
    main(sys.argv[1:])

