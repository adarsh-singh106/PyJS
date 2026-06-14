# Chapter 3: Syntax Analysis & AST Construction 🌳

After lexical analysis converts characters to tokens, the next phase is **Syntax Analysis** (also known as **Parsing**).

The component that executes this task is the **Parser**. Its job is to take a flat stream of tokens, validate that they conform to the language grammar rules, and structure them into a multi-dimensional **Abstract Syntax Tree (AST)**.

---

## 1. Context-Free Grammars (CFG) & EBNF

A grammar defines how expressions and statements are formed. We describe grammars using **Extended Backus-Naur Form (EBNF)**.

A grammar consists of a set of rules (productions):
* **Non-terminals:** Capitalized rules that expand into other rules (e.g., `expression`, `statement`).
* **Terminals:** Specific tokens (e.g., `+`, `number`, `let`).

### Example Arithmetic Grammar:
```text
expression → term ( ( "+" | "-" ) term )*
term       → factor ( ( "*" | "/" ) factor )*
factor     → NUMBER | "(" expression ")"
```
*(Here, `*` means "repeat zero or more times". This grammar structure naturally embeds **operator precedence**, ensuring `*` bind tighter than `+`).*

---

## 2. Parsing Strategy: Recursive Descent

A **Recursive Descent Parser** is a top-down parser. It starts at the top-most grammar rule (`expression`) and recursively calls functions corresponding to the grammar rules, descending down the tree.

It uses **one-token lookahead** (referred to as LL(1)) to decide which branch to take.

### Core Parser Loop
We keep a `current` index pointing to the token stream:

```python
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0

    def peek(self):
        return self.tokens[self.current]

    def is_at_end(self):
        return self.peek().type == "EOF"

    def advance(self):
        if not self.is_at_end():
            self.current += 1
        return self.tokens[self.current - 1]

    def check(self, type_):
        if self.is_at_end():
            return False
        return self.peek().type == type_

    def match(self, *types):
        for type_ in types:
            if self.check(type_):
                self.advance()
                return True
        return False
```

---

## 3. Hand-writing Recursive Descent parser methods

Let's translate the arithmetic grammar rules directly into Python methods.

### Rules Mapping:
1. `expression → term ( ("+" | "-") term )*`
```python
    def expression(self):
        expr = self.term()
        
        while self.match("PLUS", "MINUS"):
            operator = self.tokens[self.current - 1] # the matched token
            right = self.term()
            expr = BinaryExpr(expr, operator, right)
            
        return expr
```

2. `term → factor ( ("*" | "/") factor )*`
```python
    def term(self):
        expr = self.factor()
        
        while self.match("STAR", "SLASH"):
            operator = self.tokens[self.current - 1]
            right = self.factor()
            expr = BinaryExpr(expr, operator, right)
            
        return expr
```

3. `factor → NUMBER | "(" expression ")"`
```python
    def factor(self):
        if self.match("NUMBER"):
            return LiteralExpr(float(self.tokens[self.current - 1].lexeme))
            
        if self.match("LEFT_PAREN"):
            expr = self.expression()
            self.consume("RIGHT_PAREN", "Expect ')' after expression.")
            return expr
            
        raise SyntaxError(f"Expect expression at token '{self.peek().lexeme}'")
        
    def consume(self, type_, message):
        if self.check(type_):
            return self.advance()
        raise SyntaxError(message)
```

---

## 4. AST Nodes: The Structure of Meaning
The structures returned by these parser methods are **AST Nodes**. 

```python
class Expr:
    pass

class BinaryExpr(Expr):
    def __init__(self, left, operator, right):
        self.left = left          # Expr node
        self.operator = operator  # Token
        self.right = right        # Expr node

class LiteralExpr(Expr):
    def __init__(self, value):
        self.value = value        # Python float, string, etc.
```

If we parse `5 + 3 * 2`, the recursive descent parser executes calls:
1. Calls `expression()`
2. Calls `term()`, which calls `factor()` to parse `5`
3. Matches `+` in `expression()`
4. Calls `term()` on the right side.
5. In `term()`, calls `factor()` to parse `3`.
6. Matches `*` in `term()`
7. In `term()`, calls `factor()` to parse `2`.
8. Returns the nested tree:

```text
       BinaryExpr(+)
      /             \
Literal(5)        BinaryExpr(*)
                 /             \
           Literal(3)       Literal(2)
```

Notice how `3 * 2` is nested deeper in the tree. Because evaluating a tree happens from the bottom up, this ensures that the multiplication executes first, fulfilling mathematical precedence rules!

---

## 🧠 Systems Thinking: First-Principles Takeaway
Parsing converts a flat list of tokens into a **hierarchical tree**. 

In systems design, trees are the base data structures used to model nested contexts (like file directories, HTML DOM trees, XML configs, and JSON schemas). Mastering parsing teaches you how to map sequential operations to parent-child tree models.
