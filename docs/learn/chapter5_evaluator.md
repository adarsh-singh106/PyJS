# Chapter 5: Runtimes, Evaluation, & The Visitor Pattern ⚙️

Now that we have parsed our code into an Abstract Syntax Tree (AST) and understood how variables are scoped in Environments, we need to actually **execute** the AST. 

This phase is called **AST Evaluation**. The component that walks the tree and executes it is called a **Tree-Walking Interpreter**.

---

## 1. Tree-Walking & The Visitor Pattern

An AST is a composite structure of different node types (e.g. `BinaryExpression`, `IfStatement`, `Literal`). To evaluate the tree recursively, we need to run specific code for each node type.

The **Visitor Pattern** is a design pattern that separates algorithms (evaluation code) from the data structures (AST nodes) they operate on.

### The Dynamic Visitor in Python
In Python, we can dynamically dispatch AST nodes to their visitor methods using `getattr`:

```python
class Evaluator:
    def evaluate(self, node, env):
        if node is None:
            return None
            
        # Dynamically build the method name, e.g. "visit_BinaryExpression"
        method_name = f"visit_{node.type}"
        visitor = getattr(self, method_name, None)
        
        if visitor is None:
            raise NotImplementedError(f"No visitor method 'visit_{node.type}'")
            
        return visitor(node, env)
```

---

## 2. Implementing Visitor Methods

Let's look at how typical statements and expressions are evaluated.

### A. Evaluating Literals & Identifiers
```python
    def visit_Literal(self, node, env):
        return node.value

    def visit_Identifier(self, node, env):
        return env.get(node.name)
```

### B. Evaluating Binary Expressions
We evaluate the left subtree recursively, then the right, and combine them using the operator:

```python
    def visit_BinaryExpression(self, node, env):
        left_val = self.evaluate(node.left, env)
        right_val = self.evaluate(node.right, env)
        
        op = node.operator
        if op == '+':
            return left_val + right_val
        elif op == '-':
            return left_val - right_val
        elif op == '*':
            return left_val * right_val
        elif op == '/':
            return left_val / right_val
            
        raise ValueError(f"Unknown operator: {op}")
```

### C. Evaluating If Statements
```python
    def visit_IfStatement(self, node, env):
        test_val = self.evaluate(node.test, env)
        
        # Coerce to boolean (JS truthy/falsy rules)
        if bool(test_val):
            return self.evaluate(node.consequent, env)
        elif node.alternate is not None:
            return self.evaluate(node.alternate, env)
            
        return None
```

---

## 3. Controlling Stack Flow via Exceptions

How does the interpreter handle control flow statements like `return`, `break`, and `continue`? 

In Python, execution flows step-by-step. If we are deep inside a nested loop or recursive function, and we hit a `return` statement, we need to immediately exit (unwind) all the python call frames back to the function boundary.

We can implement this by raising **custom Python exceptions**.

```python
# Custom flow control exceptions
class ReturnException(Exception):
    def __init__(self, value):
        self.value = value

class BreakException(Exception):
    pass

class ContinueException(Exception):
    pass
```

### Supporting Returns in Functions
When evaluating a `ReturnStatement`, we throw a `ReturnException`:

```python
    def visit_ReturnStatement(self, node, env):
        val = self.evaluate(node.argument, env)
        raise ReturnException(val)
```

When calling a function, we wrap the body execution in a `try-except` block to catch this exception and return its value:

```python
    # Inside JSFunction.call():
    def call(self, interpreter, args):
        func_env = Environment(outer=self.closure_env)
        # bind arguments...
        
        try:
            interpreter.execute_block(self.body, func_env)
        except ReturnException as re:
            return re.value  # Exit here and return the value!
            
        return None # Return undefined if no return statement was hit
```

---

## 🧠 Systems Thinking: First-Principles Takeaway
Evaluating syntax trees teaches you how **execution states** are managed. 

You learn that control flow statements (like loops, loops breaks, and function returns) are not magic constructs. They are instructions that alter the **program counter** or unwind execution frames. By implementing them using Python's exception handling, you gain a clear mental model of call stacks and frame management.
