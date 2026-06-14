# PyJS Runtime

### A Lightweight JavaScript Interpreter Built in Python

---

# Thunder Hackathon 2.0 Submission

> **Build Your Own JavaScript**

PyJS Runtime is a lightweight JavaScript interpreter developed entirely in Python without relying on Node.js, V8, Deno, Bun, or any existing JavaScript runtime.

The project accepts JavaScript source code as input, parses it into an Abstract Syntax Tree (AST), and executes it using a custom-built runtime environment.

The primary objective of this project is to demonstrate a deep understanding of programming language implementation while providing a robust execution engine capable of passing the hackathon test cases.

---

# Executive Summary

Modern developers use programming languages every day but rarely explore how those languages work internally.

When JavaScript code is written, several stages occur behind the scenes before the final output is produced:

```text
Source Code
    ↓
Lexical Analysis
    ↓
Parsing
    ↓
Abstract Syntax Tree
    ↓
Runtime Execution
    ↓
Program Output
```

PyJS Runtime aims to recreate this process from scratch.

Rather than using existing JavaScript engines, the project implements the core execution mechanisms independently, providing both an educational exploration of compiler design principles and a practical runtime capable of executing JavaScript programs.

---

# Project Motivation

The goal of this project extends beyond simply passing test cases.

This project was designed to achieve four objectives:

## 1. Understand Programming Languages Internally

Most programmers learn how to use a language.

Few learn how a language works.

Building an interpreter provides insight into:

* How variables are stored.
* How expressions are evaluated.
* How functions create new scopes.
* How control flow statements alter execution.
* How built-in objects behave.

---

## 2. Demonstrate Systems Thinking

Programming language implementation requires combining multiple concepts:

* Data structures
* Algorithms
* Software architecture
* Recursive problem solving
* State management

This project serves as evidence of the ability to design and build complex systems from specifications.

---

## 3. Create a Meaningful Portfolio Project

Machine learning notebooks and tutorial projects often demonstrate usage of existing tools.

PyJS Runtime demonstrates the ability to:

* Design architectures.
* Build interpreters.
* Implement execution environments.
* Translate theoretical concepts into functioning software.

---

## 4. Learn Through Construction

Many compiler concepts remain abstract until implemented.

By constructing a runtime system, these ideas become tangible:

* Tokens become actual objects.
* AST nodes become executable structures.
* Scopes become environment chains.
* Functions become runtime entities.

---

# Problem Statement

Develop a JavaScript execution engine that:

* Accepts JavaScript code as input.
* Parses the source code.
* Executes the program correctly.
* Produces output matching JavaScript semantics.
* Operates independently of Node.js or existing JavaScript runtimes.

---

# Why Build an Interpreter Instead of a Compiler?

Programming languages are commonly implemented in two ways:

---

## Compiler

A compiler translates source code into another representation before execution.

Example:

```text
JavaScript
    ↓
Machine Code / Bytecode
    ↓
Execution
```

Advantages:

* Faster execution.
* Better optimization opportunities.
* Suitable for production systems.

Disadvantages:

* More implementation complexity.
* Requires code generation phases.
* Harder to debug during development.

---

## Interpreter

An interpreter executes programs directly from an intermediate representation.

Example:

```text
JavaScript
    ↓
AST
    ↓
Interpreter
    ↓
Execution
```

Advantages:

* Easier to develop.
* Simpler debugging.
* Faster iteration during implementation.
* Excellent for educational purposes.

Disadvantages:

* Slower execution.
* Fewer optimization opportunities.

---

## Why an Interpreter Was Chosen

Given the constraints of the hackathon:

* Limited development time.
* Requirement for correctness.
* Emphasis on code quality.
* Need for extensibility.

An interpreter provides the best balance between:

```text
Learning Value
        +
Implementation Speed
        +
Feature Completeness
```

---

# System Overview

The runtime follows a classical language implementation pipeline.

```text
JavaScript Source Code
            ↓
     Lexer / Tokenizer
            ↓
         Parser
            ↓
   Abstract Syntax Tree
            ↓
      Interpreter
            ↓
      Environment
            ↓
   Built-in Functions
            ↓
          stdout
```

Each stage has a clearly defined responsibility.

---

# Architectural Philosophy

The project was designed using the following principles.

---

## 1. Separation of Concerns

Each subsystem performs a single responsibility.

| Component   | Responsibility                   |
| ----------- | -------------------------------- |
| Lexer       | Convert characters into tokens   |
| Parser      | Convert tokens into AST          |
| Interpreter | Execute AST nodes                |
| Environment | Manage scopes and variables      |
| Built-ins   | Provide JavaScript functionality |

Benefits:

* Easier testing.
* Improved maintainability.
* Reduced coupling.

---

## 2. Extensibility

The architecture should support gradual feature additions.

Example:

Adding support for a new array method should not require modifying the interpreter core.

Instead:

```text
Interpreter
    ↓
Method Registry
    ↓
Implementation
```

Benefits:

* Easier hidden test adaptation.
* Cleaner code organization.

---

## 3. Incremental Development

The runtime is developed in phases.

Phase 1:

```javascript
console.log(5 + 3);
```

Phase 2:

```javascript
if (x > 0) {
    console.log(x);
}
```

Phase 3:

```javascript
function add(a, b) {
    return a + b;
}
```

Benefits:

* Faster feedback cycles.
* Earlier detection of architectural flaws.
* Reduced implementation risk.

---

# Technology Choices

## Programming Language

Python

Reasoning:

* Fast development speed.
* Excellent readability.
* Rich ecosystem.
* Suitable for recursive algorithms.
* Familiar development environment.

---

## Parsing Strategy

Generic parser generators (Lark / PLY)

Reasoning:

* Permitted by hackathon rules.
* Reduce parser boilerplate.
* Allow focus on runtime implementation.
* Improve reliability.

Trade-Off:

```text
Less educational than handwritten parsing
            vs
Faster development and reduced bugs
```

The latter was prioritized due to the hackathon timeline.

---

# Scope Definition

This project intentionally focuses on a subset of JavaScript.

The objective is not:

> Reimplement the entire ECMAScript specification.

The objective is:

> Design a robust interpreter architecture capable of supporting the JavaScript features required by the hackathon.

---

# Success Criteria

Minimum Success:

* Pass all visible test cases.

Target Success:

* Pass visible and hidden test cases.

Stretch Goal:

* Deliver educational tooling and innovation features that improve judge experience.

Examples include:

* AST visualization.
* Execution tracing.
* Interactive REPL support.
* Enhanced error reporting.

---

# Guiding Principle

> "Build something small enough to finish, but structured enough to grow."

The value of this project lies not only in the final result, but in the understanding gained throughout the process of building it.

--- 
# Part 2: Lexical Analysis, Parsing, and AST Construction

---

# From Text to Executable Structures

When developers write JavaScript, they see code like this:

```javascript
let x = 5 + 3;
console.log(x);
```

To a human, this is meaningful.

To a computer, this is simply a sequence of characters:

```text
l e t   x   =   5   +   3 ; ...
```

The primary challenge of programming language implementation is:

> **How do we transform raw text into something a machine can understand and execute?**

This transformation happens in several stages.

```text
Source Code
     ↓
Lexical Analysis
     ↓
Token Stream
     ↓
Parsing
     ↓
Parse Tree
     ↓
Abstract Syntax Tree (AST)
     ↓
Interpreter
```

---

# Stage 1: Lexical Analysis (Tokenization)

---

## What is Lexical Analysis?

Lexical analysis converts raw source code into meaningful units called **tokens**.

Tokens are the smallest meaningful pieces of a programming language.

Example:

Source Code:

```javascript
let x = 5 + 3;
```

Token Stream:

```text
LET
IDENTIFIER(x)
ASSIGN
NUMBER(5)
PLUS
NUMBER(3)
SEMICOLON
```

---

# Why Do We Need Tokens?

Without tokenization, the parser would need to reason about individual characters.

Example:

Instead of processing:

```text
l e t x = 5 + 3 ;
```

it processes:

```text
LET IDENTIFIER ASSIGN NUMBER PLUS NUMBER
```

Benefits:

* Simplifies parsing.
* Improves readability.
* Separates concerns.

---

# Common Token Types

PyJS Runtime defines tokens for:

## Keywords

```javascript
let
const
function
if
else
for
while
return
```

---

## Literals

```javascript
123
3.14
"hello"
true
false
null
```

---

## Operators

```javascript
+
-
*
/
%
==
===
!=
>
<
>=
<=
&&
||
!
```

---

## Delimiters

```javascript
(
)
{
}
[
]
;
,
.
```

---

## Identifiers

Variable names:

```javascript
x
userName
calculateSum
```

---

# Lexer Design Trade-Offs

---

## Handwritten Lexer

Advantages:

* Maximum learning value.
* Full control.

Disadvantages:

* More development time.
* Greater risk of bugs.

---

## Generated Lexer

Advantages:

* Faster implementation.
* Better reliability.

Disadvantages:

* Slightly reduced educational depth.

---

# Decision for PyJS Runtime

We chose:

```text
Generic Parser Tools
        +
Custom Runtime Logic
```

Reason:

The educational value lies primarily in:

* AST design,
* scope handling,
* interpreter execution,

rather than writing hundreds of regular expressions.

---

# Stage 2: Parsing

---

# What is Parsing?

Parsing determines whether the sequence of tokens follows the language grammar.

Example:

Tokens:

```text
LET IDENTIFIER ASSIGN NUMBER PLUS NUMBER
```

Parser Output:

```text
VariableDeclaration
    Identifier(x)
    BinaryExpression(+)
```

---

# Grammar

A grammar defines the valid structure of a language.

Example:

```text
expression
    : expression "+" term
    | term
```

Meaning:

An expression can be:

* another expression plus a term, or
* simply a term.

---

# Why Use Grammars?

Grammars provide:

* Predictability,
* Consistency,
* Formal definitions of syntax.

Without grammars:

Programming languages would become ambiguous.

---

# Parse Trees

A parse tree captures every detail of the grammar.

Example:

```javascript
5 + 3
```

Parse Tree:

```text
Expression
├── Expression
│   └── Term
│       └── Number(5)
├── +
└── Term
    └── Number(3)
```

---

# Problems with Parse Trees

Parse trees contain excessive information.

Examples:

* Parentheses,
* Grammar rules,
* Intermediate nodes.

Interpreters rarely need these details.

---

# Abstract Syntax Trees (AST)

ASTs remove unnecessary information.

Example:

```javascript
5 + 3
```

AST:

```text
BinaryExpression(+)
├── Literal(5)
└── Literal(3)
```

---

# Why ASTs Matter

ASTs provide:

* Simpler structures,
* Easier evaluation,
* Cleaner architecture.

Almost all interpreters and compilers rely on ASTs.

---

# AST Example

Source Code:

```javascript
let x = 5 + 3;
```

AST:

```text
Program
└── VariableDeclaration
    ├── Identifier(x)
    └── BinaryExpression(+)
        ├── Literal(5)
        └── Literal(3)
```

---

# PyJS AST Philosophy

PyJS prioritizes:

```text
Simplicity
      +
Extensibility
```

Each AST node represents a meaningful runtime concept.

---

# Core AST Nodes

---

## Program

Represents the entire JavaScript file.

Example:

```text
Program
```

Contains:

```python
body = [...]
```

---

## Literal

Examples:

```javascript
5
"hello"
true
```

Represents:

Constant values.

---

## Identifier

Examples:

```javascript
x
name
sum
```

Represents:

Variable references.

---

## VariableDeclaration

Example:

```javascript
let x = 10;
```

Represents:

Variable creation.

---

## BinaryExpression

Examples:

```javascript
a + b
x > y
```

Represents:

Operations involving two operands.

---

## AssignmentExpression

Example:

```javascript
x = x + 1;
```

Represents:

Variable updates.

---

## CallExpression

Example:

```javascript
console.log(x);
```

Represents:

Function invocation.

---

## FunctionDeclaration

Example:

```javascript
function add(a,b) {}
```

Represents:

Function definitions.

---

## IfStatement

Example:

```javascript
if (x > 0) {}
```

Represents:

Conditional execution.

---

## ForStatement

Represents:

Iteration using initialization, condition, and update phases.

---

## WhileStatement

Represents:

Condition-driven repetition.

---

# AST Benefits

---

## Separation of Syntax and Semantics

Syntax:

```javascript
5 + 3
```

Semantics:

```text
Add two numbers.
```

AST bridges this gap.

---

## Easier Execution

Interpreters evaluate nodes directly.

Example:

```text
BinaryExpression
    ↓
Evaluate Left
Evaluate Right
Apply Operator
Return Result
```

---

## Easier Debugging

ASTs allow:

* Visualization,
* Tracing,
* Inspection.

---

# Innovation: AST Visualization

One of PyJS Runtime's educational innovations is AST visualization.

Example:

```text
Program
├── VariableDeclaration
│   ├── Identifier(x)
│   └── Literal(5)
└── CallExpression
    └── console.log
```

---

# Why Include AST Visualization?

Educational Benefits:

* Makes compiler concepts tangible.
* Helps beginners understand execution.

Practical Benefits:

* Simplifies debugging.
* Demonstrates architectural transparency.

Hackathon Benefits:

* Provides an impressive visual demonstration.
* Differentiates the project from standard submissions.

---

# Design Trade-Off Summary

| Decision                    | Option Chosen                | Reason                |
| --------------------------- | ---------------------------- | --------------------- |
| Tokenization                | Generic parser tools         | Faster implementation |
| Parsing                     | Grammar-driven parsing       | Reliability           |
| Intermediate Representation | AST                          | Simplifies execution  |
| Parse Trees                 | Discarded after AST creation | Reduced complexity    |
| AST Visualization           | Included                     | Educational value     |

---

# Key Takeaways

By the end of this stage:

Raw text has become structured data.

```text
Characters
     ↓
Tokens
     ↓
Grammar Validation
     ↓
Abstract Syntax Tree
```

The interpreter no longer deals with source code.

Instead, it operates on a well-defined representation of the program.

This abstraction is one of the most important ideas in compiler and interpreter design.

It allows the execution engine to focus entirely on:

> **What the program means, rather than how the program was written.**

--- 
Suggestions to Complete the Draft
Here is how you might want to complete that final section that got cut off:

Project Motivation
The goal of this project extends beyond simply passing test cases. This project was designed to achieve four objectives:

1. Understand Programming Languages Internally
Most programmers learn how to use a language, but few learn how a language works. Building an interpreter provides deep insight into how variables are stored in memory, how scopes are resolved, and how control flow is managed.

2. Bridge the Gap Between Python and JS
(Example objective) To demonstrate interoperability by recreating the syntax and behavior of the web's most popular language using Python's object-oriented paradigms.

3. Demystify the Abstract Syntax Tree (AST)
(Example objective) To build a visual and functional understanding of how raw text is tokenized and structured into machine-readable trees.

4. Deliver a Functional Proof-of-Concept
(Example objective) To successfully pass the provided hackathon test cases, proving the logic handles edge cases, nested functions, and mathematical operations correctly.

Overall Verdict: You have a fantastic foundation here. Once you finish out the missing bullet points and clearly define exactly which JavaScript features your interpreter supports, this will be a top-tier executive summary for your hackathon submission.
