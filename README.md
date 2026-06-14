# PyJS Runtime 🚀

### A Lightweight, Pure-Python JavaScript Interpreter & AST Visualizer

PyJS Runtime is a lightweight JavaScript execution engine developed entirely in Python. It parses JavaScript source code into an Abstract Syntax Tree (AST) using a compliant ECMA parser, and interprets it using a custom-built, standard-compliant runtime environment. 

This project operates completely independently of Node.js, V8, Deno, Bun, or any other existing JavaScript engine.

---

## 📖 Table of Contents
1. [Core Features](#-core-features)
2. [Architectural Overview](#-architectural-overview)
3. [Installation](#-installation)
4. [Usage Instructions](#-usage-instructions)
    - [Running a JavaScript File](#1-running-a-javascript-file)
    - [Running Code Snippets Directly](#2-running-code-snippets-directly)
    - [AST Visualization](#3-ast-visualization)
    - [Interactive REPL](#4-interactive-repl)
5. [Running the Test Suite](#-running-the-test-suite)
6. [Implementation Details](#-implementation-details)

---

## ✨ Core Features

PyJS Runtime fully implements the subset of JavaScript required for the hackathon, including:
* **Variables & Scopes:** Block-scoping (`let`, `const`), function-scoping (`var`), and lexical hoisting for function declarations and variables.
* **Primitives:** `number`, `string`, `boolean`, `null`, `undefined` with JavaScript type coercion semantics.
* **Complex Data Structures:** Full support for `Object` and `Array` literals, property access, and method calls.
* **Control Flow:** `if-else if-else` statements, `switch-case` statements with fall-through, `for` loops, `while` loops, and `do...while` loops (supporting `break` and `continue`).
* **Functions & Closures:** Function declarations, function expressions, lexical scopes, closures, callback functions, arrow functions, and the REST parameter (`...args`).
* **Array Methods:** `push()`, `pop()`, `shift()`, `unshift()`, `slice()`, `splice()`, `concat()`, `includes()`, `indexOf()`, `sort()`, `reverse()`, `join()`, and callback-based methods `map()`, `filter()`, `reduce()`, `find()`, `some()`, `every()`.
* **String Operations:** `replace()`, `replaceAll()`, `substring()`, `slice()`, `split()`, `trim()`, `toUpperCase()`, `toLowerCase()`, `includes()`, `startsWith()`, `endsWith()`, and `indexOf()`.
* **Standard Built-ins:**
  - `Math` object (constants `PI`, `E`, and methods `floor()`, `random()`, `abs()`, `ceil()`, `min()`, `max()`, `pow()`, `sqrt()`, `round()`).
  - `Date` constructor and instance getters (`getTime()`, `getFullYear()`, `getMonth()`, `getDate()`, `getDay()`, `getHours()`, `getMinutes()`, `getSeconds()`, `getMilliseconds()`, `toISOString()`).
  - Global functions `parseInt()`, `parseFloat()`, `isNaN()`, `isFinite()`, and type casting functions `Number()`, `String()`, `Boolean()`.
* **Operator Spread:** Array and Object spread syntax (`[...arr]`, `{...obj}`).

---

## 🏗️ Architectural Overview

The execution pipeline consists of three core components:

```text
JS Source Code ──► Lexer/Parser (Esprima) ──► AST (ESTree JSON) ──► Evaluator (Visitor Pattern) ──► Output
```

1. **Parser & Tokenizer:** Leverages a pure-Python port of `esprima` to tokenize and compile source JavaScript code into standard ESTree Abstract Syntax Trees.
2. **Environment Record:** Resolves scope lookups using an environment chain modeling lexical scoping and closures.
3. **AST Evaluator:** Traverses the parsed AST nodes using the Visitor Pattern, executing JS statements and expressions with JavaScript-specific semantics (coercion rules, truthiness/falsiness, mathematical operations).

---

## 🛠️ Installation & Setup

Ensure you have **Python 3.10+** installed. Depending on your operating system, use:
* **Windows:** `python` and `pip`
* **macOS / Linux:** `python3` and `pip3`

### 1. Clone the Repository
Clone the repository from GitHub and navigate into the project directory:
```bash
git clone https://github.com/adarsh-singh106/PyJS.git
cd PyJS
```

### 2. Install Dependencies
You can install dependencies globally:
```bash
pip install -r requirements.txt   # Or: pip3 install -r requirements.txt
```

Or set up and install using a virtual environment:
```bash
# Create environment
python -m venv venv   # Or: python3 -m venv venv

# Activate environment
source venv/bin/activate  # On Windows (cmd/PowerShell): venv\Scripts\activate

# Install requirements
pip install -r requirements.txt
```

---

## 🚀 Usage Instructions

### 1. Running a JavaScript File
Execute any JavaScript file by passing the path as a positional argument (use `python3` on macOS/Linux):
```bash
python main.py path/to/file.js   # Or: python3 main.py path/to/file.js
```
Example:
```bash
python main.py tests/test_1.js
```

### 2. Running Code Snippets Directly
Execute JavaScript code snippets directly in your shell using the `-c` or `--code` flag:
```bash
python main.py -c "let nums = [1, 2, 3]; console.log(nums.map(x => x ** 2).join(' - '));"
```

### 3. AST Visualization
PyJS includes a stretch-goal AST Visualizer that renders ASCII tree hierarchies of the compiled code. Use the `-a` or `--ast` flag to print the tree structure:
```bash
python main.py tests/test_1.js -a
```
This produces a clear structural overview of statements and expressions before running:
```text
=== Abstract Syntax Tree (AST) ===
+-- Program
    |-- VariableDeclaration
    |   +-- VariableDeclarator
    |       |-- Literal (7)
    |       +-- Identifier (num)
    +-- IfStatement
...
```

You can also parse and output the AST without executing the code using the `--no-eval` flag:
```bash
python main.py tests/test_1.js -a --no-eval
```

### 4. Interactive REPL
Start an interactive read-eval-print loop (REPL) by running `main.py` without arguments:
```bash
python main.py
```
Type expressions and press enter to evaluate them dynamically:
```text
Welcome to PyJS Runtime REPL (v1.0)
Type '.exit' or press Ctrl+D to exit.

pyjs> let x = [1, 2, 3]
pyjs> x.push(4)
4
pyjs> x.join(' -> ')
1 -> 2 -> 3 -> 4
pyjs> .exit
```

---

## 🧪 Running the Test Suite

We provide an automated test runner that validates the implementation against the 5 visible hackathon test cases and 2 additional custom test suites (hoisting and comprehensive feature checks):

```bash
python tests/run_tests.py
```

Expected Output:
```text
=== PyJS Interpreter Test Runner ===
Running Test 1 (tests/test_1.js)... PASSED
Running Test 2 (tests/test_2.js)... PASSED
Running Test 3 (tests/test_3.js)... PASSED
Running Test 4 (tests/test_4.js)... PASSED
Running Test 5 (tests/test_5.js)... PASSED
Running Test 6 (tests/hoisting_test.js)... PASSED
Running Test 7 (tests/comprehensive_test.js)... PASSED

All tests PASSED successfully!
```

---

## 💡 Implementation Details
* **Type Coercion & Comparisons:** All operators implement standard JavaScript behaviors (e.g. `===` checks reference identity or strict type equality, `==` triggers coercion paths, string additions concatenate objects whereas standard additions trigger numeric conversions).
* **Control Flows via Python Exceptions:** Evaluates loop control flow blocks utilizing custom exceptions (`BreakException`, `ContinueException`, `ReturnException`) to emulate lexical stack exits.
