# PyJS Runtime: Technical Architecture & System Design Spec 🏗️

This document outlines the internal design, architecture patterns, and technical execution details of the **PyJS Runtime**—a lightweight, pure-Python JavaScript interpreter.

---

## 1. System Pipeline Architecture

PyJS Runtime executes code in three distinct stages:

```text
Source Code ──► Lexer/Parser (Esprima) ──► AST (ESTree JSON) ──► Evaluator (Visitor Pattern)
                                                                       │
                                                   ┌───────────────────┴───────────────────┐
                                                   ▼                                       ▼
                                          Environment Chain                         Stdout (console.log)
```

1. **Syntactic Translation (Frontend):** 
   The JavaScript source code is parsed into a standardized **ESTree-compliant Abstract Syntax Tree (AST)** using `esprima`. This translates raw text into a hierarchical, object-oriented node structure.
2. **State & Binding Records (Context):** 
   The runtime manages scope lookups, constants, and variable declarations using a custom parent-pointer scope environment.
3. **AST Visitation (Execution Engine):** 
   The `Evaluator` class traverses the generated AST recursively using dynamic visitor dispatching.

---

## 2. Core Execution Subsystems

### A. The Environment Scope Chain
To model standard JavaScript lexical scoping rules (including closures, block scoping, and global hoisting), the interpreter implements the [Environment](file:///D:/CSE57_26-27_3rd-year/Strike's-Thunder-Series-Hackathons/02-hackathon/interpreter/environment.py) class.

* **Block Scopes (`let`, `const`):** Created as fresh `Environment` instances nested within the active scope, pointing to the enclosing environment via the `outer` pointer.
* **Function/Global Scopes (`var`):** Hoisted to the closest enclosing function or global environment by climbing up the environment chain until `is_function_scope` is `True` or `outer` is `None`.
* **Lexical Closures:** Functions (`JSFunction`) maintain a pointer to their **definition-time** environment (`closure_env`), ensuring static scoping is preserved when called out of context.

### B. Double-Pass Scoping (Declaration Hoisting)
Before executing any block statement or program, the evaluator performs a pre-execution sweep to scan for:
1. **Function Declarations:** Instantiated and bound to their identifiers in the local environment immediately.
2. **`var` Declarations:** Registered and bound to `undefined` in the closest function or global scope.

This double-pass mechanism ensures calling functions or referencing `var` variables before their physical code location behaves in compliance with standard JavaScript.

---

## 3. Custom Value & Type System

Since Python primitives behave differently from JavaScript, PyJS implements a custom boxing and translation layer inside [interpreter/runtime.py](file:///D:/CSE57_26-27_3rd-year/Strike's-Thunder-Series-Hackathons/02-hackathon/interpreter/runtime.py):

* **Undefined:** Represented by a singleton object `UNDEFINED`.
* **Null:** Represented natively by Python's `None`.
* **Objects (`JSObject`):** Model properties and inherit properties from parent structures via prototype-chain lookups.
* **Arrays (`JSArray`):** Subclass `JSObject` to manage length indices dynamically and expose array manipulation methods.
* **Functions (`JSFunction` / `JSBuiltinFunction`):** Encapsulate parameters, body statements, and call boundaries.
* **Constructors (`JSConstructor`):** Subclass functions to handle `new` operations by instantiating raw object frames and binding context prototype links.

---

## 4. Control Flow Stack Unwinding

Python's execution stacks are linear. When a JS control statement (like a function `return` or a loop `break`/`continue`) is hit inside deep nested subtrees, the interpreter must immediately unwind the Python call stack back to the enclosing boundary.

This is implemented using **low-overhead Python Exceptions** acting as control signals:

* `ReturnException(value)`: Caught at the function invocation boundary to return values.
* `BreakException`: Caught at loop structures (`for`, `while`, `do...while`, `switch`) to terminate execution loops.
* `ContinueException`: Caught at loop structures to skip remaining statements and trigger update phases.

---

## 5. Type Coercion Matrix

Operations mimic JavaScript's standard coercion algorithms:
* **Strict Equality (`===`):** Compares data type and value (or reference identity for reference objects).
* **Loose Equality (`==`):** Coerces mismatched types (e.g. converting strings to numbers or boolean states to numeric values) dynamically before evaluation.
* **Binary Addition (`+`):** If either operand is an object/string, both are converted to string primitives and concatenated; otherwise, they are treated as numbers.
* **Mathematical Operations (`/`, `%`, `**`):** Handle division-by-zero bounds gracefully (returning `Infinity` or `NaN`) and remainder operators mimic JavaScript's floating-point modulo (`math.fmod`).
