import subprocess
import sys

TESTS = [
    {
        "file": "tests/test_1.js",
        "expected": "7 is Odd\n"
    },
    {
        "file": "tests/test_2.js",
        "expected": "*\n**\n***\n****\n*****\n"
    },
    {
        "file": "tests/test_3.js",
        "expected": "true\nfalse\n"
    },
    {
        "file": "tests/test_4.js",
        "expected": "Original: 1, 2, 3, 4, 5\nReversed: 5, 4, 3, 2, 1\n"
    },
    {
        "file": "tests/test_5.js",
        "expected": "racecar is a Palindrome\n"
    },
    {
        "file": "tests/hoisting_test.js",
        "expected": "Hello\n42\n42\nfalse\n"
    },
    {
        "file": "tests/comprehensive_test.js",
        "expected": "Doubled: 2, 4, 6, 8, 10\nEvens: 2, 4\nSum: 15\nFound > 3: 4\nSome > 4: true\nEvery > 0: true\nTrimmed: 'JavaScript Interpreter'\nUpper: JAVASCRIPT INTERPRETER\nLower: javascript interpreter\nSlice: Java\nSubstring: Script\nIncludes Java: true\nStarts with Java: true\nEnds with Interpreter: true\nIndexOf Script: 4\nReplace: JavaJS Interpreter\nReplaceAll: baz-bar-baz\nMath.PI check: true\nMath.abs: 5\nMath.ceil: 5\nMath.floor: 4\nMath.round: 5\nMath.sqrt: 4\nMath.pow: 8\nMath.max: 5\nMath.min: 1\nYear: 2024\nMonth: 5\nDate: 14\nRest param sum: 10\nIt's an apple\nDo-while count: 3\n"
    }
]

def run_test(test):
    file_path = test["file"]
    expected = test["expected"].strip()
    
    # Run main.py using python
    result = subprocess.run(
        [sys.executable, "main.py", file_path],
        capture_output=True,
        text=True
    )
    
    stdout = result.stdout.strip()
    stderr = result.stderr.strip()
    
    # Standardize windows newlines
    stdout = stdout.replace("\r\n", "\n").strip()
    expected = expected.replace("\r\n", "\n").strip()
    
    if result.returncode != 0:
        return False, f"Process exited with code {result.returncode}. Stderr: {stderr}"
        
    if stdout == expected:
        return True, "PASSED"
    else:
        return False, f"FAILED. Expected:\n{expected}\nActual:\n{stdout}"

def main():
    passed_all = True
    print("=== PyJS Interpreter Test Runner ===")
    for i, test in enumerate(TESTS, 1):
        print(f"Running Test {i} ({test['file']})... ", end="")
        success, msg = run_test(test)
        if success:
            print("\033[92mPASSED\033[0m")
        else:
            print("\033[91mFAILED\033[0m")
            print(msg)
            passed_all = False
    
    if passed_all:
        print("\nAll tests PASSED successfully!")
        sys.exit(0)
    else:
        print("\nSome tests FAILED.")
        sys.exit(1)

if __name__ == "__main__":
    main()
