## File Naming Convention

- `<name>.asm`: File automatically runs and generated `<name>.bin` (or stderr for errors) is compared with `<name>.expected`
- `<name>_hex.asm`: File runs the --hex command to compare the `<name>_hex.hex` file output with `<name>_hex.expected`
- `<name>_emulator.bin`: Binary file is tested by the emulator, and stderr output is compared against `<name>_emulator.expected`
