# StdChip Assembler & Emulator

This project implements a complete toolchain for **StdChip**, a fictional 8-bit computer architecture.

It consists of:
- A **Python assembler** that converts the custom StdChip assembly language into executable machine code
- A **Python emulator** that executes machine code produced by the assembler
- Bash-based **test cases**

The implementation contains instruction encodings, memory constraints, I/O behaviour, and error handling.

## Architecture Overview

**StdChip characteristics:**
- 256 memory cells
- Each cell is **1 byte**, unsigned values only (`0–255`)
- Instructions are **4 bytes** each
- Supports arithmetic, memory manipulation, control flow, I/O, and process execution

## Assembler (`assembler.py`)

The assembler converts human-readable StdChip assembly into executable machine code.

### Features
- Supports following instructions:
  - `SET`, `MOV`, `ADD`, `SUB`
  - `READ`, `PUT`
  - `JMP`, `JEQ`, `JGT`
  - `CALL`, `EXIT`
- Resolves **labels** to instruction indices
- Handles values in:
  - Decimal
  - Binary (`0b`)
  - Octal (`0o`)
  - Hexadecimal (`0x`)
  - ASCII characters (`'A'`)
- Generates:
  - **Binary executables** (default `.bin` files)
  - **Hex output** (`.hex` files)

### Usage

```bash
python3 assembler.py [--hex] <input_file> <output_file>
```

To generate a hex file as the output, run the command with the optional `--hex` flag.

## Emulator (`emulator.py`)

The emulator runs executable (`.bin`) files produced by the assembler.

### Features

- Verifies executable header and version
- Implements a full 256-byte memory model
- Executes instructions sequentially with correct control flow
- Correctly handles:
  - Arithmetic overflow and underflow
  - Conditional jumps
  - Console I/O
  - Process forking via CALL

### Usage
```bash
python3 emulator.py <executable>
```

## Testcases

The testcases cover:

- Instruction correctness
- Arithmetic overflow and underflow
- Label resolution and branching
- Loops and conditional jumps
- Input/output operations
- End-to-end assembler and emulator execution

### Running Test

```bash
bash tests/run_tests.sh
```

