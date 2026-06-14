from interpreter.runtime import (
    UNDEFINED, ArrayConstructor, ObjectConstructor, DateConstructor,
    MathObject, ConsoleObject, JSBuiltinFunction, js_parse_int,
    js_parse_float, js_is_nan, js_is_finite, FunctionPrototype,
    NumberConstructor, StringConstructor, BooleanConstructor
)

class Environment:
    def __init__(self, outer=None, is_function_scope=False):
        self.bindings = {}
        self.constants = set()
        self.outer = outer
        self.is_function_scope = is_function_scope
        
    def declare(self, name, value, is_const=False):
        self.bindings[name] = value
        if is_const:
            self.constants.add(name)
            
    def get(self, name):
        if name in self.bindings:
            return self.bindings[name]
        if self.outer is not None:
            return self.outer.get(name)
        raise NameError(f"ReferenceError: {name} is not defined")
        
    def assign(self, name, value):
        if name in self.bindings:
            if name in self.constants:
                raise TypeError(f"TypeError: Assignment to constant variable '{name}'")
            self.bindings[name] = value
            return
        if self.outer is not None:
            self.outer.assign(name, value)
            return
        # Create global variable implicitly in non-strict mode
        curr = self
        while curr.outer is not None:
            curr = curr.outer
        curr.declare(name, value)
        
    def declare_var(self, name, value):
        # Find the nearest function scope or global scope
        curr = self
        while curr.outer is not None and not curr.is_function_scope:
            curr = curr.outer
        curr.declare(name, value)

def create_global_environment():
    env = Environment()
    env.declare("Array", ArrayConstructor)
    env.declare("Object", ObjectConstructor)
    env.declare("Date", DateConstructor)
    env.declare("Number", NumberConstructor)
    env.declare("String", StringConstructor)
    env.declare("Boolean", BooleanConstructor)
    env.declare("Math", MathObject)
    env.declare("console", ConsoleObject)
    
    env.declare("parseInt", JSBuiltinFunction("parseInt", js_parse_int, prototype=FunctionPrototype))
    env.declare("parseFloat", JSBuiltinFunction("parseFloat", js_parse_float, prototype=FunctionPrototype))
    env.declare("isNaN", JSBuiltinFunction("isNaN", js_is_nan, prototype=FunctionPrototype))
    env.declare("isFinite", JSBuiltinFunction("isFinite", js_is_finite, prototype=FunctionPrototype))
    
    env.declare("undefined", UNDEFINED)
    env.declare("null", None)
    env.declare("NaN", float('nan'))
    env.declare("Infinity", float('inf'))
    
    return env
