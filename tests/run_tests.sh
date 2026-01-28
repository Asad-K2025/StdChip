PASSED=0
FAILED=0

echo "----------------------------------------"

# Assembler tests
for asm_path in tests/*.asm; do  # looping through all .asm input files for assembler
    asm_file="$(basename "$asm_path")"  # extracting file_name from tests/file_name.asm
    test_name="${asm_file%.asm}"

    output_bin="tests/${test_name}.bin"
    output_hex="tests/${test_name}.hex"  # Output files produced by runnign tests
    expected_file="tests/${test_name}.expected"

    is_hex=false
    if [[ "$asm_file" == *_hex.asm ]]; then  # Check if file has ..._hex.asm meaning a .hex file is compared form output
        is_hex=true
    fi

    if $is_hex; then
        assembler_stderr=$(python assembler.py --hex "$asm_path" "$output_hex" 2>&1 1>/dev/null)
        assembler_exit=$?
        output_file="$output_hex"
    else
        assembler_stderr=$(python assembler.py "$asm_path" "$output_bin" 2>&1 1>/dev/null)
        assembler_exit=$?
        output_file="$output_bin"
    fi

    # Assembler tests output messages
    if [[ $assembler_exit -eq 0 && -f "$output_file" ]]; then
        if diff "$output_file" "$expected_file" >/dev/null 2>&1; then
            echo "$test_name PASSED: Assembler output matches expected"
            ((PASSED++))
        else
            echo "$test_name FAILED: Assembler output differs"
            diff -u <(xxd "$expected_file") <(xxd "$output_file") | sed 's/^/    /'
            echo ""
            ((FAILED++))
        fi
    else
        if diff <(echo "$assembler_stderr") "$expected_file" >/dev/null 2>&1; then
            echo "$test_name PASSED: Assembler stderr matches expected"
            ((PASSED++))
        else
            echo "$test_name FAILED: Assembler stderr differs"
            diff -u "$expected_file" <(echo "$assembler_stderr") | sed 's/^/    /'
            echo ""
            ((FAILED++))
        fi
    fi
done

# emulator tests
for emulator_input in tests/*_emulator.bin; do
    input_file="$(basename "$emulator_input")"
    test_name="${input_file%.bin}"
    expected_file="tests/${test_name}.expected"

    if [[ ! -f "$expected_file" ]]; then
        echo "$test_name FAILED: Missing expected file for emulator"
        ((FAILED++))
        continue
    fi

    emulator_stderr=$(python emulator.py "$emulator_input" 2>/dev/null)  # Stadard error output stored in variable

    # Emulator output messages
    if diff <(echo "$emulator_stderr") "$expected_file" >/dev/null 2>&1; then
        echo "$test_name PASSED: Emulator output matches"
        ((PASSED++))
    else
        echo "$test_name FAILED: Emulator output differs"
        diff -u "$expected_file" <(echo "$emulator_stderr") | sed 's/^/    /'
        echo ""
        ((FAILED++))
    fi
done

echo "----------------------------------------"
echo "Summary: $PASSED passed, $FAILED failed."
