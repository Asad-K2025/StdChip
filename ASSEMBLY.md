## Values

Values used in instructions can be written in multiple formats:

| Format      | Example    | Description                   |
|-------------|------------|-------------------------------|
| Decimal     | `42`       | Base 10                       |
| Binary      | `0b101010` | Base 2                        |
| Octal       | `0o52`     | Base 8                        |
| Hexadecimal | `0x2A`     | Base 16                       |
| ASCII char  | `'A'`      | Uses ASCII value of character |

All values must fit in **one byte** (`0–255`).

## Addresses

- Addresses are always written in **decimal**
- Valid range: `0–255`

## Labels

Labels are used for control flow (jumps and branches).

### Defining a Label
A label is written on its own line and enclosed in colons:

```
:loop_start:
```

The label refers to the **instruction immediately following it**.

### Using a Label
Labels are referenced by name **without colons**:

```
JMP loop_start
```

### Rules
- Label names may contain letters and underscores
- Label names must be unique
- Labels are resolved during assembly and do not appear in the executable

## Instructions

### SET
**Syntax:**  
`SET <address> <value>`

**Description:**  
Store a value in a memory address.

**Examples:**
```
SET 10 65
SET 11 'A'
```

### MOV
**Syntax:**  
`MOV <address_to> <address_from>`

**Description:**  
Copy the value in address `<address_from>` to `<address_to>`.

### ADD
**Syntax:**  
`ADD <d> <a> <b>`

**Description:**  
Add the two memory values at `<a>` and `<b>`, and store result at address `<d>`.

### SUB
**Syntax:**  
`SUB <d> <a> <b>`

**Description:**  
Subtract the value at memory address `<b>` from the value at address `<a>` and store at address `<d>`.

### READ (Number)
**Syntax:**  
`READ <d> N`

**Description:**  
Read a number from standard input and store it in memory at address `<d>`.

Input may be in binary, octal, decimal, or hexadecimal.
Reading stops at newline, null character, or EOF.

### READ (String)
**Syntax:**  
`READ <d> S <c>`

**Description:**  
Read up to `<c>` bytes from standard input and store them starting at address `<d>`.

Reading stops early on newline, null character, or EOF.
The terminator is not stored.

### PUT (Number)
**Syntax:**  
`PUT <s> N <f>`

**Description:**  
Output the value at memory address `<s>` as a number.

`<f>` specifies the output format:
- `b` – binary
- `o` – octal
- `d` – decimal
- `h` – hexadecimal

No newline is printed.

### PUT (String)
**Syntax:**  
`PUT <s> S <c>`

**Description:**  
Read `<c>` bytes from memory starting at `<s>`, interpret them as ASCII,
and print them to standard output.

No newline is printed.

### JMP
**Syntax:**  
`JMP <label>`

**Description:**  
Unconditionally jump to the instruction following the given `<label>`.

### JEQ
**Syntax:**  
`JEQ <label> <a> <b>`

**Description:**  
Jump to `<label>`if the values at `<a>` and `<b>` are equal.

### JGT
**Syntax:**  
`JGT <label> <a> <b>`

**Description:**  
Jump if the value at `<a>` is greater than the value at `<b>`.

### CALL
**Syntax:**  
`CALL <d> <p>`

**Description:**  
Execute another StdChip executable whose file path is stored as a null-terminated
string starting at `<p>`.

The program is executed in a child process. The exit code of the child is stored at `<d>`.

### EXIT
**Syntax:**  
`EXIT <s>`

**Description:**  
Terminate execution with the exit code stored at address `<s>`.

## Notes

- All arithmetic is performed modulo 256
- No instruction implicitly prints a newline
- Behaviour outside the documented rules is undefined and not guaranteed
