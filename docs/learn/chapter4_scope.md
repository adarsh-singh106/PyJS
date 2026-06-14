# Chapter 4: Environments, Scopes, & Symbol Resolution 🔒

A programming language needs a way to store data in variables and look them up when requested. 

In runtime systems, this state management is handled by **Environments** (also called **Symbol Tables** or **Activation Records**).

---

## 1. What is an Environment?

An environment is essentially a dictionary mapping variable names (keys) to their current values. 

However, variables are not all global. They are scoped. To support nested scoping (such as inside blocks or functions), environments are organized as a **Parent-Pointer Tree** (or a **Lexical Environment Chain**).

Each local environment has a reference (pointer) to its enclosing (`outer`) environment:

```text
┌──────────────────────────────────────────────┐
│ Global Scope: let x = 1, let y = 2           │
└──────────────────────▲───────────────────────┘
                       │ [outer pointer]
┌──────────────────────┴───────────────────────┐
│ Function Scope: let x = 10                   │
│ (Sees local x=10, sees global y=2)           │
└──────────────────────────────────────────────┘
```

---

## 2. Implementing the Scope Chain

We represent environments as objects with a dictionary `bindings` and a pointer `outer`:

```python
class Environment:
    def __init__(self, outer=None):
        self.bindings = {}
        self.outer = outer  # Link to parent environment

    def declare(self, name, value):
        # Always declare in the immediate current scope
        self.bindings[name] = value

    def get(self, name):
        # Resolve by climbing the environment chain
        if name in self.bindings:
            return self.bindings[name]
            
        if self.outer is not None:
            return self.outer.get(name)
            
        raise NameError(f"ReferenceError: {name} is not defined")

    def assign(self, name, value):
        # Update existing variable by finding where it was declared
        if name in self.bindings:
            self.bindings[name] = value
            return
            
        if self.outer is not None:
            self.outer.assign(name, value)
            return
            
        raise NameError(f"ReferenceError: {name} is not defined")
```

---

## 3. Scoping Paradigms

Languages manage scope transitions in two primary ways:

### Lexical Scoping (Static Scoping)
* **Rule:** A variable is resolved based on where the code is **written** (lexical structure).
* **Behavior:** If a function looks up a variable, it searches the environment where it was *defined*, not where it was *called*.
* **Examples:** JavaScript, Python, C++, Java, Rust.
* **Why it matters:** Lexical scoping makes code predictable and enables **closures**.

### Dynamic Scoping
* **Rule:** A variable is resolved based on where the function is **called** (call stack history).
* **Behavior:** The runtime searches the environment of the caller function, and then the caller's caller, climbing the call stack.
* **Examples:** Bash, early versions of Lisp, Perl (optional).

---

## 4. The Magic of Closures

A **Closure** is a function that remembers and accesses variables from its outer lexical scope even when executed outside that scope.

### JavaScript Example:
```javascript
function makeCounter() {
    let count = 0;
    return function() {
        count++;
        return count;
    };
}
let counter = makeCounter();
console.log(counter()); // 1
console.log(counter()); // 2
```

### How Closures Work under the Hood:
When `makeCounter()` is called:
1. A new environment `E1` is created. Its outer pointer points to the `Global Environment`.
2. Inside `E1`, the variable `count` is initialized to `0`.
3. The nested function is created. At creation time, **the function captures a reference to the environment it was defined in (`E1`)**.
4. The function object is returned and stored in `counter`.
5. `E1` is **not garbage collected** because the function object holds a live reference to it!
6. When `counter()` is called, its execution environment `E2` is created. The parent of `E2` is set to the *captured* environment `E1` (not the global environment!).
7. When `count++` executes, it searches `E2` (doesn't find it), searches its parent `E1` (finds it), and increments it.

---

## 🧠 Systems Thinking: First-Principles Takeaway
Environments teach you how **garbage collectors** and **memory managers** operate. 

You learn that variables are not magic symbols; they are memory locations linked by runtime structures. Understanding environments demystifies how scoping prevents name collisions, how scopes are cleaned up, and how memory leaks occur when closures keep references alive unnecessarily.
