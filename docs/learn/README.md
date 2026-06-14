# Compiler & Interpreter Design: First-Principles Curriculum 🎓

Welcome to the **Language Implementation & Systems Engineering Curriculum**!

Building an interpreter from scratch is one of the most transformative exercises a software engineer can undertake. It strips away the magic of programming languages and forces you to think from **first principles** about how text files become instructions executed by silicon gates.

This curriculum is structured to take you from a high-level conceptual understanding of computer systems to the construction of lexers, parsers, scoping environments, and execution runtimes.

---

## 🗺️ Curriculum Roadmap

This learning path is divided into **6 chapters**, each focusing on a fundamental phase of compiler/interpreter design and its connection to computer systems:

```text
Source Code (Text)
    │
    ▼ [Chapter 2: Lexical Analysis]
Token Stream
    │
    ▼ [Chapter 3: Syntactic Analysis]
Abstract Syntax Tree (AST)
    │
    ▼ [Chapter 4: Environment & Scopes]
Lexical Environments & Closures
    │
    ▼ [Chapter 5: Evaluation & Runtimes]
Visitor Pattern & Execution
    │
    ▼ [Chapter 6: Virtual Machines & Memory]
Bytecode VMs, Stack vs Heap, & Garbage Collection
```

### 📂 Syllabus Overview

### [Chapter 1: The Compilation Pipeline & Philosophy](./chapter1_pipeline.md)
* **First Principles:** What is code? Why do we need translators?
* **High-Level Flow:** Lexer, Parser, AST, Evaluator, Compiler vs. Interpreter.
* **Systems Connection:** How compilers bridge human thought models to CPU instruction sets.

### [Chapter 2: Lexical Analysis (Tokenizers)](./chapter2_lexer.md)
* **Concepts:** RegEx, State Machines, Deterministic Finite Automata (DFA).
* **Implementation:** Writing a scanner from scratch using the cursor pattern.
* **Mental Model:** Converting a 1D sequence of characters into a structured list of semantic units.

### [Chapter 3: Syntactic Analysis (Parsers & ASTs)](./chapter3_parser.md)
* **Concepts:** Context-Free Grammars (CFG), EBNF, Recursive Descent, Operator Precedence.
* **Implementation:** Building a hand-written recursive-descent parser to generate an AST.
* **Mental Model:** Translating a flat token list into a multi-dimensional nested tree structure.

### [Chapter 4: Environments, Scopes, & Symbol Tables](./chapter4_scope.md)
* **Concepts:** Lexical vs. Dynamic scoping, Closure binding, block scoping, symbol tables.
* **Implementation:** Modeling parent-pointer trees for scope chaining.
* **Mental Model:** How computer memory organizes variables, scopes, and functions during execution.

### [Chapter 5: Runtimes, Evaluation, & The Visitor Pattern](./chapter5_evaluator.md)
* **Concepts:** Tree-walking execution, the Visitor Pattern, type systems, and coercion logic.
* **Implementation:** Executing control flow (loops, conditionals, functions) via stack-unwinding exceptions.
* **Mental Model:** Giving "meaning" (semantics) to syntax trees.

### [Chapter 6: Virtual Machines, Bytecode, & Memory Management](./chapter6_memory.md)
* **Concepts:** Stack vs. Register machines, Bytecode compilation, stack frame layouts, heaps, and Garbage Collection (Mark-and-Sweep, Reference Counting).
* **Implementation:** Designing a minimal VM instructions format.
* **Mental Model:** Moving from tree evaluation to linear memory CPU emulator patterns.

### [Advanced Mastery: Beyond This Project](./advanced_mastery.md)
* **Concepts:** Static type checking (HM inference), SSA intermediate representation, native code generation (x86/ARM), Graph Coloring register allocation, JIT compilation (W^X memory protection), and generational garbage collection.
* **Next Steps:** Curated literature (SICP, Dragon Book, Crafting Interpreters) and open-source engine codebases to read.

---

## 🧠 Why Learn This? (The First-Principles Benefit)

1. **Master Systems Thinking:** You will learn how software interacts with hardware. You'll understand *why* call stacks overflow, *why* closures consume memory, and *how* loops translate to CPU jumps.
2. **Improve Problem Solving:** Translating string input to execution models develops your recursive thinking, tree structures mastery, and state machine designs.
3. **Write Optimized Code:** Knowing what happens under the hood helps you choose the right data patterns and avoid runtime bottlenecks.
