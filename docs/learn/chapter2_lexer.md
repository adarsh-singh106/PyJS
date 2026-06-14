# Chapter 2: Lexical Analysis & Tokenization 🔍

The first phase of the language compiler is **Lexical Analysis**. The component that executes this task is called a **Lexer** or **Scanner**.

The lexer's sole purpose is to convert a flat sequence of characters into a structured sequence of **Tokens**.

---

## 1. What is a Token?
A token is a object/struct grouping character sequences that represent a single unit of meaning. 

In a lexer, a token usually contains:
1. **Type:** A category identifier (e.g., `LET`, `NUMBER`, `IDENTIFIER`, `PLUS`).
2. **Lexeme:** The actual string representation from the source code (e.g., `let`, `42`, `x`, `+`).
3. **Metadata:** Line and column numbers for error tracking.

```python
class Token:
    def __init__(self, type_, lexeme, line):
        self.type = type_
        self.lexeme = lexeme
        self.line = line

    def __repr__(self):
        return f"Token({self.type}, '{self.lexeme}')"
```

---

## 2. Theoretical Foundations: State Machines

A lexer maps text using **Regular Languages**. Mathematically, it operates as a **Deterministic Finite Automaton (DFA)**. 

A DFA is a state machine with:
* A set of input symbols (characters).
* A set of states.
* State transition functions.
* An initial state and one or more acceptance states.

### State Diagram for an Identifier/Keyword:
```text
           [Letter / _]
(Start) ────────────────► (Identifier State) ──[Letter/Digit/_]──┐
                            ▲                                    │
                            └────────────────────────────────────┘
```
If the state machine halts on a boundary character (like a space or operator) while in the `Identifier State`, it spits out an `IDENTIFIER` token (and later checks if the lexeme matches a reserved keyword like `let` or `while`).

---

## 3. Implementing a Hand-Written Scanner (First Principles)

Instead of using code generators, writing a scanner by hand helps you understand string cursor traversal. 

### The Cursor Pattern
We maintain a `source` string, a `current` index pointer, a `start` index representing the beginning of the current lexeme, and the current `line` number.

```python
class Lexer:
    def __init__(self, source):
        self.source = source
        self.tokens = []
        self.start = 0
        self.current = 0
        self.line = 1
        
        # Reserved keywords mapping
        self.keywords = {
            "let": "LET", "const": "CONST", "function": "FUNCTION",
            "if": "IF", "else": "ELSE", "while": "WHILE", "return": "RETURN"
        }

    def is_at_end(self):
        return self.current >= len(self.source)

    def advance(self):
        char = self.source[self.current]
        self.current += 1
        return char

    def peek(self):
        if self.is_at_end():
            return '\0'
        return self.source[self.current]
```

### Scanning Tokens Loop
We read characters, mapping matching cases to identify tokens:

```python
    def scan_tokens(self):
        while not self.is_at_end():
            self.start = self.current
            self.scan_token()
        return self.tokens

    def scan_token(self):
        c = self.advance()
        
        # Skip Whitespace
        if c in (' ', '\r', '\t'):
            return
        elif c == '\n':
            self.line += 1
            return
            
        # Single Character Operators
        elif c == '+':
            self.add_token("PLUS")
        elif c == '-':
            self.add_token("MINUS")
        elif c == ';':
            self.add_token("SEMICOLON")
            
        # Literals
        elif c.isdigit():
            self.number()
        elif c.isalpha() or c == '_':
            self.identifier()
        else:
            raise SyntaxError(f"Unexpected character on line {self.line}: '{c}'")

    def add_token(self, type_, literal=None):
        text = self.source[self.start:self.current]
        self.tokens.append(Token(type_, text, self.line))
```

### Scanning Multi-character Literals
* **Numbers:** Keep advancing as long as the character is a digit.
* **Identifiers & Keywords:** Read alphanumeric strings. Check if they exist in `self.keywords` to output keywords, else output identifiers:

```python
    def number(self):
        while self.peek().isdigit():
            self.advance()
        # Decimal part support
        if self.peek() == '.' and self.peek_next().isdigit():
            self.advance() # consume '.'
            while self.peek().isdigit():
                self.advance()
        self.add_token("NUMBER")

    def identifier(self):
        while self.peek().isalnum() or self.peek() == '_':
            self.advance()
            
        text = self.source[self.start:self.current]
        type_ = self.keywords.get(text, "IDENTIFIER")
        self.add_token(type_)
        
    def peek_next(self):
        if self.current + 1 >= len(self.source):
            return '\0'
        return self.source[self.current + 1]
```

---

## 🧠 Systems Thinking: First-Principles Takeaway
By scanning tokens, you have collapsed raw 1-dimensional text data into localized semantic units. 

Instead of reading `"l"`, `"e"`, `"t"`, your interpreter can now reason at a higher level of abstraction: **Variable Declarations**. This reduction of complexity is the baseline pattern for all layers of system architecture.
