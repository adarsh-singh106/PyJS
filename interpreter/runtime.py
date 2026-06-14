import math
import datetime
import random

class UndefinedType:
    def __str__(self):
        return "undefined"
    def __repr__(self):
        return "undefined"

UNDEFINED = UndefinedType()

class ReturnException(Exception):
    def __init__(self, value):
        self.value = value

class BreakException(Exception):
    pass

class ContinueException(Exception):
    pass

class JSObject:
    def __init__(self, prototype=None):
        self.properties = {}
        self.prototype = prototype
        
    def get_property(self, name):
        curr = self
        while curr is not None:
            if name in curr.properties:
                return curr.properties[name]
            curr = curr.prototype
        return UNDEFINED
        
    def set_property(self, name, value):
        self.properties[name] = value
        
    def delete_property(self, name):
        if name in self.properties:
            del self.properties[name]
            return True
        return False
        
    def __str__(self):
        return "[object Object]"
        
    def __repr__(self):
        return self.__str__()

class JSArray(JSObject):
    def __init__(self, elements=None, prototype=None):
        super().__init__(prototype=prototype)
        self.elements = list(elements) if elements is not None else []
        
    @property
    def length(self):
        return len(self.elements)
        
    @length.setter
    def length(self, val):
        try:
            val = int(val)
        except (ValueError, TypeError):
            raise ValueError("RangeError: Invalid array length")
        if val < 0:
            raise ValueError("RangeError: Invalid array length")
        if val < len(self.elements):
            self.elements = self.elements[:val]
        elif val > len(self.elements):
            self.elements.extend([UNDEFINED] * (val - len(self.elements)))
            
    def get_property(self, name):
        if name == "length":
            return self.length
        try:
            idx = int(name)
            if idx >= 0 and str(idx) == name:
                if 0 <= idx < len(self.elements):
                    return self.elements[idx]
                return UNDEFINED
        except ValueError:
            pass
        return super().get_property(name)
        
    def set_property(self, name, value):
        if name == "length":
            self.length = value
            return
        try:
            idx = int(name)
            if idx >= 0 and str(idx) == name:
                if idx >= len(self.elements):
                    self.elements.extend([UNDEFINED] * (idx - len(self.elements) + 1))
                self.elements[idx] = value
                return
        except ValueError:
            pass
        super().set_property(name, value)
        
    def __str__(self):
        return ",".join(js_to_string(x) for x in self.elements)

class JSFunction(JSObject):
    def __init__(self, name, params, body, closure_env, is_arrow=False, prototype=None):
        super().__init__(prototype=prototype)
        self.name = name
        self.params = params
        self.body = body
        self.closure_env = closure_env
        self.is_arrow = is_arrow
        
    def call(self, interpreter, this_val, args):
        from interpreter.environment import Environment
        func_env = Environment(outer=self.closure_env, is_function_scope=True)
        func_env.declare('this', this_val)
        
        # Bind parameters
        for i, param in enumerate(self.params):
            if param.type == "RestElement":
                rest_name = param.argument.name
                rest_args = args[i:] if i < len(args) else []
                func_env.declare(rest_name, JSArray(rest_args, prototype=ArrayPrototype))
                break
            else:
                param_name = param.name
                val = args[i] if i < len(args) else UNDEFINED
                func_env.declare(param_name, val)
                
        try:
            if self.body.type == "BlockStatement":
                interpreter.execute_block(self.body.body, func_env)
            else:
                return interpreter.evaluate_in_env(self.body, func_env)
        except ReturnException as re:
            return re.value
            
        return UNDEFINED

class JSBuiltinFunction(JSObject):
    def __init__(self, name, func, prototype=None):
        super().__init__(prototype=prototype)
        self.name = name
        self.func = func
        
    def call(self, interpreter, this_val, args):
        return self.func(interpreter, this_val, args)

class JSConstructor(JSBuiltinFunction):
    def __init__(self, name, func, instance_class, prototype=None, instance_prototype=None):
        super().__init__(name, func, prototype=prototype)
        self.instance_class = instance_class
        self.instance_prototype = instance_prototype
        
    def construct(self, interpreter, args):
        new_instance = self.instance_class(prototype=self.instance_prototype)
        res = self.call(interpreter, new_instance, args)
        if isinstance(res, JSObject) and not isinstance(res, JSConstructor):
            return res
        return new_instance

class JSDate(JSObject):
    def __init__(self, dt=None, prototype=None):
        super().__init__(prototype=prototype)
        self.dt = dt if dt is not None else datetime.datetime.now()
        
    def __str__(self):
        return self.dt.strftime("%a %b %d %Y %H:%M:%S GMT")

# Coercion functions
def js_to_boolean(val):
    if val is None or val is UNDEFINED:
        return False
    if isinstance(val, bool):
        return val
    if isinstance(val, (int, float)):
        return val != 0 and not math.isnan(val)
    if isinstance(val, str):
        return len(val) > 0
    if isinstance(val, JSObject):
        return True
    return bool(val)

def to_number(val):
    if val is None:
        return 0
    if val is UNDEFINED:
        return float('nan')
    if isinstance(val, bool):
        return 1 if val else 0
    if isinstance(val, (int, float)):
        return val
    if isinstance(val, str):
        s = val.strip()
        if not s:
            return 0
        if s.lower() == "infinity" or s.lower() == "+infinity":
            return float('inf')
        if s.lower() == "-infinity":
            return float('-inf')
        try:
            if s.startswith(("0x", "0X")):
                return int(s, 16)
            if s.startswith(("0o", "0O")):
                return int(s, 8)
            if s.startswith(("0b", "0B")):
                return int(s, 2)
            return float(s)
        except ValueError:
            return float('nan')
    if isinstance(val, JSArray):
        return to_number(js_to_string(val))
    if isinstance(val, JSObject):
        return float('nan')
    return float('nan')

def to_integer(val):
    num = to_number(val)
    if math.isnan(num):
        return 0
    if math.isinf(num):
        return num
    return int(num)

def js_to_string(val):
    if val is None:
        return "null"
    if val is UNDEFINED:
        return "undefined"
    if isinstance(val, bool):
        return "true" if val else "false"
    if isinstance(val, (int, float)):
        if math.isnan(val):
            return "NaN"
        if math.isinf(val):
            return "Infinity" if val > 0 else "-Infinity"
        if isinstance(val, float) and val.is_integer():
            return str(int(val))
        return str(val)
    if isinstance(val, str):
        return val
    if isinstance(val, JSArray):
        return ",".join(js_to_string(x) for x in val.elements)
    if isinstance(val, JSObject):
        return "[object Object]"
    return str(val)

def js_to_primitive(val):
    if isinstance(val, JSObject):
        return js_to_string(val)
    return val

def js_strict_equal(left, right):
    if isinstance(left, (int, float)) and isinstance(right, (int, float)):
        if math.isnan(left) or math.isnan(right):
            return False
        return left == right
    if type(left) != type(right):
        return False
    if isinstance(left, (int, float)):
        if math.isnan(left) or math.isnan(right):
            return False
        return left == right
    if isinstance(left, JSObject):
        return left is right
    return left == right

def js_same_value_zero(left, right):
    if isinstance(left, (int, float)) and isinstance(right, (int, float)):
        if math.isnan(left) and math.isnan(right):
            return True
        return left == right
    return js_strict_equal(left, right)

def js_loose_equal(left, right):
    if (type(left) == type(right)) or (isinstance(left, (int, float)) and isinstance(right, (int, float))):
        return js_strict_equal(left, right)
    if (left is None or left is UNDEFINED) and (right is None or right is UNDEFINED):
        return True
    if left is None or left is UNDEFINED or right is None or right is UNDEFINED:
        return False
    if isinstance(left, (int, float)) and isinstance(right, str):
        return js_loose_equal(left, to_number(right))
    if isinstance(left, str) and isinstance(right, (int, float)):
        return js_loose_equal(to_number(left), right)
    if isinstance(left, bool):
        return js_loose_equal(1 if left else 0, right)
    if isinstance(right, bool):
        return js_loose_equal(left, 1 if right else 0)
    if isinstance(left, JSObject) and isinstance(right, (str, int, float)):
        return js_loose_equal(js_to_primitive(left), right)
    if isinstance(left, (str, int, float)) and isinstance(right, JSObject):
        return js_loose_equal(left, js_to_primitive(right))
    return False

def to_int32(val):
    num = to_number(val)
    if math.isnan(num) or math.isinf(num):
        return 0
    val32 = int(num) & 0xffffffff
    if val32 >= 0x80000000:
        val32 -= 0x100000000
    return val32

def to_uint32(val):
    num = to_number(val)
    if math.isnan(num) or math.isinf(num):
        return 0
    return int(num) & 0xffffffff

def js_add(left, right):
    lp = js_to_primitive(left)
    rp = js_to_primitive(right)
    if isinstance(lp, str) or isinstance(rp, str):
        return js_to_string(lp) + js_to_string(rp)
    return to_number(lp) + to_number(rp)

def js_subtract(left, right):
    return to_number(left) - to_number(right)

def js_multiply(left, right):
    return to_number(left) * to_number(right)

def js_divide(left, right):
    l = to_number(left)
    r = to_number(right)
    if math.isnan(l) or math.isnan(r):
        return float('nan')
    if r == 0:
        if l == 0:
            return float('nan')
        return float('inf') if l > 0 else float('-inf')
    return l / r

def js_modulo(left, right):
    l = to_number(left)
    r = to_number(right)
    if r == 0 or math.isinf(l) or math.isnan(l) or math.isnan(r):
        return float('nan')
    return math.fmod(l, r)

def js_exponent(left, right):
    l = to_number(left)
    r = to_number(right)
    if l < 0 and isinstance(r, float) and not r.is_integer():
        return float('nan')
    try:
        return l ** r
    except ZeroDivisionError:
        return float('inf')
    except OverflowError:
        return float('inf')

def js_less_than(left, right):
    l = js_to_primitive(left)
    r = js_to_primitive(right)
    if isinstance(l, str) and isinstance(r, str):
        return l < r
    ln = to_number(l)
    rn = to_number(r)
    if math.isnan(ln) or math.isnan(rn):
        return False
    return ln < rn

def js_less_equal(left, right):
    l = js_to_primitive(left)
    r = js_to_primitive(right)
    if isinstance(l, str) and isinstance(r, str):
        return l <= r
    ln = to_number(l)
    rn = to_number(r)
    if math.isnan(ln) or math.isnan(rn):
        return False
    return ln <= rn

def js_greater_than(left, right):
    l = js_to_primitive(left)
    r = js_to_primitive(right)
    if isinstance(l, str) and isinstance(r, str):
        return l > r
    ln = to_number(l)
    rn = to_number(r)
    if math.isnan(ln) or math.isnan(rn):
        return False
    return ln > rn

def js_greater_equal(left, right):
    l = js_to_primitive(left)
    r = js_to_primitive(right)
    if isinstance(l, str) and isinstance(r, str):
        return l >= r
    ln = to_number(l)
    rn = to_number(r)
    if math.isnan(ln) or math.isnan(rn):
        return False
    return ln >= rn

# Prototype Definitions
ObjectPrototype = JSObject(prototype=None)
ArrayPrototype = JSObject(prototype=ObjectPrototype)
StringPrototype = JSObject(prototype=ObjectPrototype)
DatePrototype = JSObject(prototype=ObjectPrototype)
FunctionPrototype = JSObject(prototype=ObjectPrototype)

# Array Prototype Methods
def array_push(interpreter, this_val, args):
    if not isinstance(this_val, JSArray):
        raise TypeError("TypeError: Array.prototype.push called on non-array")
    for arg in args:
        this_val.elements.append(arg)
    return this_val.length

def array_pop(interpreter, this_val, args):
    if not isinstance(this_val, JSArray):
        raise TypeError("TypeError: Array.prototype.pop called on non-array")
    if len(this_val.elements) == 0:
        return UNDEFINED
    return this_val.elements.pop()

def array_shift(interpreter, this_val, args):
    if not isinstance(this_val, JSArray):
        raise TypeError("TypeError: Array.prototype.shift called on non-array")
    if len(this_val.elements) == 0:
        return UNDEFINED
    return this_val.elements.pop(0)

def array_unshift(interpreter, this_val, args):
    if not isinstance(this_val, JSArray):
        raise TypeError("TypeError: Array.prototype.unshift called on non-array")
    for arg in reversed(args):
        this_val.elements.insert(0, arg)
    return this_val.length

def array_slice(interpreter, this_val, args):
    if not isinstance(this_val, JSArray):
        raise TypeError("TypeError: Array.prototype.slice called on non-array")
    n = len(this_val.elements)
    start = to_integer(args[0]) if len(args) > 0 and args[0] is not UNDEFINED else 0
    end = to_integer(args[1]) if len(args) > 1 and args[1] is not UNDEFINED else n
    
    if start < 0:
        start = max(n + start, 0)
    else:
        start = min(start, n)
        
    if end < 0:
        end = max(n + end, 0)
    else:
        end = min(end, n)
        
    if start >= end:
        return JSArray(prototype=ArrayPrototype)
    return JSArray(this_val.elements[start:end], prototype=ArrayPrototype)

def array_splice(interpreter, this_val, args):
    if not isinstance(this_val, JSArray):
        raise TypeError("TypeError: Array.prototype.splice called on non-array")
    n = len(this_val.elements)
    start = to_integer(args[0]) if len(args) > 0 else 0
    if start < 0:
        start = max(n + start, 0)
    else:
        start = min(start, n)
        
    delete_count = n - start
    if len(args) > 1:
        delete_count = to_integer(args[1])
        delete_count = max(0, min(delete_count, n - start))
        
    insert_items = args[2:] if len(args) > 2 else []
    deleted = this_val.elements[start:start+delete_count]
    this_val.elements[start:start+delete_count] = insert_items
    return JSArray(deleted, prototype=ArrayPrototype)

def array_concat(interpreter, this_val, args):
    res_elements = list(this_val.elements) if isinstance(this_val, JSArray) else [this_val]
    for arg in args:
        if isinstance(arg, JSArray):
            res_elements.extend(arg.elements)
        else:
            res_elements.append(arg)
    return JSArray(res_elements, prototype=ArrayPrototype)

def array_includes(interpreter, this_val, args):
    if not isinstance(this_val, JSArray):
        raise TypeError("TypeError: Array.prototype.includes called on non-array")
    search_element = args[0] if len(args) > 0 else UNDEFINED
    from_index = to_integer(args[1]) if len(args) > 1 else 0
    n = len(this_val.elements)
    if from_index < 0:
        from_index = max(n + from_index, 0)
    for i in range(from_index, n):
        if js_same_value_zero(this_val.elements[i], search_element):
            return True
    return False

def array_index_of(interpreter, this_val, args):
    if not isinstance(this_val, JSArray):
        raise TypeError("TypeError: Array.prototype.indexOf called on non-array")
    search_element = args[0] if len(args) > 0 else UNDEFINED
    from_index = to_integer(args[1]) if len(args) > 1 else 0
    n = len(this_val.elements)
    if from_index < 0:
        from_index = max(n + from_index, 0)
    for i in range(from_index, n):
        if js_strict_equal(this_val.elements[i], search_element):
            return i
    return -1

def array_sort(interpreter, this_val, args):
    if not isinstance(this_val, JSArray):
        raise TypeError("TypeError: Array.prototype.sort called on non-array")
    compare_fn = args[0] if len(args) > 0 and args[0] is not UNDEFINED else None
    
    from functools import cmp_to_key
    def default_compare(x, y):
        sx = js_to_string(x)
        sy = js_to_string(y)
        if sx < sy:
            return -1
        elif sx > sy:
            return 1
        return 0
        
    if compare_fn is None:
        this_val.elements.sort(key=cmp_to_key(default_compare))
    else:
        def custom_compare(x, y):
            res = compare_fn.call(interpreter, UNDEFINED, [x, y])
            return to_number(res)
        this_val.elements.sort(key=cmp_to_key(custom_compare))
    return this_val

def array_reverse(interpreter, this_val, args):
    if not isinstance(this_val, JSArray):
        raise TypeError("TypeError: Array.prototype.reverse called on non-array")
    this_val.elements.reverse()
    return this_val

def array_join(interpreter, this_val, args):
    if not isinstance(this_val, JSArray):
        raise TypeError("TypeError: Array.prototype.join called on non-array")
    separator = js_to_string(args[0]) if len(args) > 0 and args[0] is not UNDEFINED else ","
    parts = []
    for el in this_val.elements:
        if el is UNDEFINED or el is None:
            parts.append("")
        else:
            parts.append(js_to_string(el))
    return separator.join(parts)

def array_map(interpreter, this_val, args):
    if not isinstance(this_val, JSArray):
        raise TypeError("TypeError: Array.prototype.map called on non-array")
    callback = args[0] if len(args) > 0 else None
    if callback is None or not hasattr(callback, 'call'):
        raise TypeError("TypeError: callback is not a function")
    this_arg = args[1] if len(args) > 1 else UNDEFINED
    res_elements = []
    for i, el in enumerate(this_val.elements):
        res = callback.call(interpreter, this_arg, [el, i, this_val])
        res_elements.append(res)
    return JSArray(res_elements, prototype=ArrayPrototype)

def array_filter(interpreter, this_val, args):
    if not isinstance(this_val, JSArray):
        raise TypeError("TypeError: Array.prototype.filter called on non-array")
    callback = args[0] if len(args) > 0 else None
    if callback is None or not hasattr(callback, 'call'):
        raise TypeError("TypeError: callback is not a function")
    this_arg = args[1] if len(args) > 1 else UNDEFINED
    res_elements = []
    for i, el in enumerate(this_val.elements):
        res = callback.call(interpreter, this_arg, [el, i, this_val])
        if js_to_boolean(res):
            res_elements.append(el)
    return JSArray(res_elements, prototype=ArrayPrototype)

def array_reduce(interpreter, this_val, args):
    if not isinstance(this_val, JSArray):
        raise TypeError("TypeError: Array.prototype.reduce called on non-array")
    callback = args[0] if len(args) > 0 else None
    if callback is None or not hasattr(callback, 'call'):
        raise TypeError("TypeError: callback is not a function")
    has_initial = len(args) > 1
    accumulator = args[1] if has_initial else None
    start_idx = 0
    if not has_initial:
        if len(this_val.elements) == 0:
            raise TypeError("TypeError: Reduce of empty array with no initial value")
        accumulator = this_val.elements[0]
        start_idx = 1
    for i in range(start_idx, len(this_val.elements)):
        accumulator = callback.call(interpreter, UNDEFINED, [accumulator, this_val.elements[i], i, this_val])
    return accumulator

def array_find(interpreter, this_val, args):
    if not isinstance(this_val, JSArray):
        raise TypeError("TypeError: Array.prototype.find called on non-array")
    callback = args[0] if len(args) > 0 else None
    if callback is None or not hasattr(callback, 'call'):
        raise TypeError("TypeError: callback is not a function")
    this_arg = args[1] if len(args) > 1 else UNDEFINED
    for i, el in enumerate(this_val.elements):
        res = callback.call(interpreter, this_arg, [el, i, this_val])
        if js_to_boolean(res):
            return el
    return UNDEFINED

def array_some(interpreter, this_val, args):
    if not isinstance(this_val, JSArray):
        raise TypeError("TypeError: Array.prototype.some called on non-array")
    callback = args[0] if len(args) > 0 else None
    if callback is None or not hasattr(callback, 'call'):
        raise TypeError("TypeError: callback is not a function")
    this_arg = args[1] if len(args) > 1 else UNDEFINED
    for i, el in enumerate(this_val.elements):
        res = callback.call(interpreter, this_arg, [el, i, this_val])
        if js_to_boolean(res):
            return True
    return False

def array_every(interpreter, this_val, args):
    if not isinstance(this_val, JSArray):
        raise TypeError("TypeError: Array.prototype.every called on non-array")
    callback = args[0] if len(args) > 0 else None
    if callback is None or not hasattr(callback, 'call'):
        raise TypeError("TypeError: callback is not a function")
    this_arg = args[1] if len(args) > 1 else UNDEFINED
    for i, el in enumerate(this_val.elements):
        res = callback.call(interpreter, this_arg, [el, i, this_val])
        if not js_to_boolean(res):
            return False
    return True

def make_array_builtin(name, func):
    return JSBuiltinFunction(name, func, prototype=FunctionPrototype)

ArrayPrototype.set_property("push", make_array_builtin("push", array_push))
ArrayPrototype.set_property("pop", make_array_builtin("pop", array_pop))
ArrayPrototype.set_property("shift", make_array_builtin("shift", array_shift))
ArrayPrototype.set_property("unshift", make_array_builtin("unshift", array_unshift))
ArrayPrototype.set_property("slice", make_array_builtin("slice", array_slice))
ArrayPrototype.set_property("splice", make_array_builtin("splice", array_splice))
ArrayPrototype.set_property("concat", make_array_builtin("concat", array_concat))
ArrayPrototype.set_property("includes", make_array_builtin("includes", array_includes))
ArrayPrototype.set_property("indexOf", make_array_builtin("indexOf", array_index_of))
ArrayPrototype.set_property("sort", make_array_builtin("sort", array_sort))
ArrayPrototype.set_property("reverse", make_array_builtin("reverse", array_reverse))
ArrayPrototype.set_property("join", make_array_builtin("join", array_join))
ArrayPrototype.set_property("map", make_array_builtin("map", array_map))
ArrayPrototype.set_property("filter", make_array_builtin("filter", array_filter))
ArrayPrototype.set_property("reduce", make_array_builtin("reduce", array_reduce))
ArrayPrototype.set_property("find", make_array_builtin("find", array_find))
ArrayPrototype.set_property("some", make_array_builtin("some", array_some))
ArrayPrototype.set_property("every", make_array_builtin("every", array_every))

# String Prototype Methods
def string_split(interpreter, this_val, args):
    if not isinstance(this_val, str):
        raise TypeError("TypeError: String.prototype.split called on non-string")
    separator = js_to_string(args[0]) if len(args) > 0 and args[0] is not UNDEFINED else None
    limit = to_integer(args[1]) if len(args) > 1 and args[1] is not UNDEFINED else None
    if separator is None:
        return JSArray([this_val], prototype=ArrayPrototype)
    if separator == "":
        parts = list(this_val)
    else:
        parts = this_val.split(separator)
    if limit is not None:
        parts = parts[:limit]
    return JSArray(parts, prototype=ArrayPrototype)

def string_replace(interpreter, this_val, args):
    if not isinstance(this_val, str):
        raise TypeError("TypeError: String.prototype.replace called on non-string")
    search = js_to_string(args[0]) if len(args) > 0 else "undefined"
    replace_val = js_to_string(args[1]) if len(args) > 1 else "undefined"
    return this_val.replace(search, replace_val, 1)

def string_replace_all(interpreter, this_val, args):
    if not isinstance(this_val, str):
        raise TypeError("TypeError: String.prototype.replaceAll called on non-string")
    search = js_to_string(args[0]) if len(args) > 0 else "undefined"
    replace_val = js_to_string(args[1]) if len(args) > 1 else "undefined"
    return this_val.replace(search, replace_val)

def string_substring(interpreter, this_val, args):
    if not isinstance(this_val, str):
        raise TypeError("TypeError: String.prototype.substring called on non-string")
    start = to_integer(args[0]) if len(args) > 0 else 0
    end = to_integer(args[1]) if len(args) > 1 else len(this_val)
    start = max(0, start)
    end = max(0, end)
    if start > end:
        start, end = end, start
    start = min(start, len(this_val))
    end = min(end, len(this_val))
    return this_val[start:end]

def string_slice(interpreter, this_val, args):
    if not isinstance(this_val, str):
        raise TypeError("TypeError: String.prototype.slice called on non-string")
    n = len(this_val)
    start = to_integer(args[0]) if len(args) > 0 else 0
    end = to_integer(args[1]) if len(args) > 1 else n
    if start < 0:
        start = max(n + start, 0)
    else:
        start = min(start, n)
    if end < 0:
        end = max(n + end, 0)
    else:
        end = min(end, n)
    if start >= end:
        return ""
    return this_val[start:end]

def string_trim(interpreter, this_val, args):
    if not isinstance(this_val, str):
        raise TypeError("TypeError: String.prototype.trim called on non-string")
    return this_val.strip()

def string_to_upper_case(interpreter, this_val, args):
    if not isinstance(this_val, str):
        raise TypeError("TypeError: String.prototype.toUpperCase called on non-string")
    return this_val.upper()

def string_to_lower_case(interpreter, this_val, args):
    if not isinstance(this_val, str):
        raise TypeError("TypeError: String.prototype.toLowerCase called on non-string")
    return this_val.lower()

def string_includes(interpreter, this_val, args):
    if not isinstance(this_val, str):
        raise TypeError("TypeError: String.prototype.includes called on non-string")
    search = js_to_string(args[0]) if len(args) > 0 else "undefined"
    position = to_integer(args[1]) if len(args) > 1 else 0
    position = max(0, min(position, len(this_val)))
    return search in this_val[position:]

def string_starts_with(interpreter, this_val, args):
    if not isinstance(this_val, str):
        raise TypeError("TypeError: String.prototype.startsWith called on non-string")
    search = js_to_string(args[0]) if len(args) > 0 else "undefined"
    position = to_integer(args[1]) if len(args) > 1 else 0
    position = max(0, min(position, len(this_val)))
    return this_val.startswith(search, position)

def string_ends_with(interpreter, this_val, args):
    if not isinstance(this_val, str):
        raise TypeError("TypeError: String.prototype.endsWith called on non-string")
    search = js_to_string(args[0]) if len(args) > 0 else "undefined"
    end_pos = to_integer(args[1]) if len(args) > 1 and args[1] is not UNDEFINED else len(this_val)
    end_pos = max(0, min(end_pos, len(this_val)))
    return this_val[:end_pos].endswith(search)

def string_index_of(interpreter, this_val, args):
    if not isinstance(this_val, str):
        raise TypeError("TypeError: String.prototype.indexOf called on non-string")
    search = js_to_string(args[0]) if len(args) > 0 else "undefined"
    position = to_integer(args[1]) if len(args) > 1 else 0
    position = max(0, min(position, len(this_val)))
    return this_val.find(search, position)

def make_string_builtin(name, func):
    return JSBuiltinFunction(name, func, prototype=FunctionPrototype)

StringPrototype.set_property("replace", make_string_builtin("replace", string_replace))
StringPrototype.set_property("replaceAll", make_string_builtin("replaceAll", string_replace_all))
StringPrototype.set_property("substring", make_string_builtin("substring", string_substring))
StringPrototype.set_property("slice", make_string_builtin("slice", string_slice))
StringPrototype.set_property("split", make_string_builtin("split", string_split))
StringPrototype.set_property("trim", make_string_builtin("trim", string_trim))
StringPrototype.set_property("toUpperCase", make_string_builtin("toUpperCase", string_to_upper_case))
StringPrototype.set_property("toLowerCase", make_string_builtin("toLowerCase", string_to_lower_case))
StringPrototype.set_property("includes", make_string_builtin("includes", string_includes))
StringPrototype.set_property("startsWith", make_string_builtin("startsWith", string_starts_with))
StringPrototype.set_property("endsWith", make_string_builtin("endsWith", string_ends_with))
StringPrototype.set_property("indexOf", make_string_builtin("indexOf", string_index_of))

# Date Prototype Methods
def date_get_time(interpreter, this_val, args):
    if not isinstance(this_val, JSDate):
        raise TypeError("TypeError: Date.prototype.getTime called on non-date")
    return this_val.dt.timestamp() * 1000.0

def date_get_full_year(interpreter, this_val, args):
    if not isinstance(this_val, JSDate):
        raise TypeError("TypeError: Date.prototype.getFullYear called on non-date")
    return this_val.dt.year

def date_get_month(interpreter, this_val, args):
    if not isinstance(this_val, JSDate):
        raise TypeError("TypeError: Date.prototype.getMonth called on non-date")
    return this_val.dt.month - 1

def date_get_date(interpreter, this_val, args):
    if not isinstance(this_val, JSDate):
        raise TypeError("TypeError: Date.prototype.getDate called on non-date")
    return this_val.dt.day

def date_get_day(interpreter, this_val, args):
    if not isinstance(this_val, JSDate):
        raise TypeError("TypeError: Date.prototype.getDay called on non-date")
    return (this_val.dt.weekday() + 1) % 7

def date_get_hours(interpreter, this_val, args):
    if not isinstance(this_val, JSDate):
        raise TypeError("TypeError: Date.prototype.getHours called on non-date")
    return this_val.dt.hour

def date_get_minutes(interpreter, this_val, args):
    if not isinstance(this_val, JSDate):
        raise TypeError("TypeError: Date.prototype.getMinutes called on non-date")
    return this_val.dt.minute

def date_get_seconds(interpreter, this_val, args):
    if not isinstance(this_val, JSDate):
        raise TypeError("TypeError: Date.prototype.getSeconds called on non-date")
    return this_val.dt.second

def date_get_milliseconds(interpreter, this_val, args):
    if not isinstance(this_val, JSDate):
        raise TypeError("TypeError: Date.prototype.getMilliseconds called on non-date")
    return int(this_val.dt.microsecond / 1000)

def date_to_iso_string(interpreter, this_val, args):
    if not isinstance(this_val, JSDate):
        raise TypeError("TypeError: Date.prototype.toISOString called on non-date")
    return this_val.dt.isoformat()

def date_to_string(interpreter, this_val, args):
    if not isinstance(this_val, JSDate):
        raise TypeError("TypeError: Date.prototype.toString called on non-date")
    return this_val.__str__()

def make_date_builtin(name, func):
    return JSBuiltinFunction(name, func, prototype=FunctionPrototype)

DatePrototype.set_property("getTime", make_date_builtin("getTime", date_get_time))
DatePrototype.set_property("getFullYear", make_date_builtin("getFullYear", date_get_full_year))
DatePrototype.set_property("getMonth", make_date_builtin("getMonth", date_get_month))
DatePrototype.set_property("getDate", make_date_builtin("getDate", date_get_date))
DatePrototype.set_property("getDay", make_date_builtin("getDay", date_get_day))
DatePrototype.set_property("getHours", make_date_builtin("getHours", date_get_hours))
DatePrototype.set_property("getMinutes", make_date_builtin("getMinutes", date_get_minutes))
DatePrototype.set_property("getSeconds", make_date_builtin("getSeconds", date_get_seconds))
DatePrototype.set_property("getMilliseconds", make_date_builtin("getMilliseconds", date_get_milliseconds))
DatePrototype.set_property("toISOString", make_date_builtin("toISOString", date_to_iso_string))
DatePrototype.set_property("toString", make_date_builtin("toString", date_to_string))

# Constructors implementations
def array_constructor(interpreter, this_val, args):
    if this_val is not None and isinstance(this_val, JSArray):
        if len(args) == 1 and isinstance(args[0], (int, float)):
            this_val.length = int(args[0])
        else:
            this_val.elements = list(args)
        return this_val
    else:
        if len(args) == 1 and isinstance(args[0], (int, float)):
            arr = JSArray(prototype=ArrayPrototype)
            arr.length = int(args[0])
            return arr
        return JSArray(args, prototype=ArrayPrototype)

def object_constructor(interpreter, this_val, args):
    if this_val is not None and isinstance(this_val, JSObject):
        return this_val
    return JSObject(prototype=ObjectPrototype)

def date_constructor(interpreter, this_val, args):
    if this_val is not None and isinstance(this_val, JSDate):
        if len(args) > 0:
            val = args[0]
            if isinstance(val, (int, float)):
                this_val.dt = datetime.datetime.fromtimestamp(val / 1000.0)
            elif isinstance(val, str):
                try:
                    this_val.dt = datetime.datetime.fromisoformat(val.replace("Z", "+00:00"))
                except ValueError:
                    this_val.dt = datetime.datetime.now()
            else:
                this_val.dt = datetime.datetime.now()
        else:
            this_val.dt = datetime.datetime.now()
        return this_val
    else:
        return datetime.datetime.now().strftime("%a %b %d %Y %H:%M:%S GMT")

def number_constructor(interpreter, this_val, args):
    if len(args) == 0:
        return 0
    return to_number(args[0])

def string_constructor(interpreter, this_val, args):
    if len(args) == 0:
        return ""
    return js_to_string(args[0])

def boolean_constructor(interpreter, this_val, args):
    if len(args) == 0:
        return False
    return js_to_boolean(args[0])

NumberConstructor = JSConstructor("Number", number_constructor, JSObject, prototype=FunctionPrototype, instance_prototype=ObjectPrototype)
StringConstructor = JSConstructor("String", string_constructor, JSObject, prototype=FunctionPrototype, instance_prototype=ObjectPrototype)
BooleanConstructor = JSConstructor("Boolean", boolean_constructor, JSObject, prototype=FunctionPrototype, instance_prototype=ObjectPrototype)

ArrayConstructor = JSConstructor("Array", array_constructor, JSArray, prototype=FunctionPrototype, instance_prototype=ArrayPrototype)
def array_is_array(interpreter, this_val, args):
    if len(args) == 0:
        return False
    return isinstance(args[0], JSArray)
ArrayConstructor.set_property("isArray", JSBuiltinFunction("isArray", array_is_array, prototype=FunctionPrototype))

ObjectConstructor = JSConstructor("Object", object_constructor, JSObject, prototype=FunctionPrototype, instance_prototype=ObjectPrototype)
DateConstructor = JSConstructor("Date", date_constructor, JSDate, prototype=FunctionPrototype, instance_prototype=DatePrototype)

# Global Math Object
MathObject = JSObject(prototype=ObjectPrototype)

def math_floor(interpreter, this_val, args):
    val = to_number(args[0]) if len(args) > 0 else float('nan')
    if math.isnan(val) or math.isinf(val):
        return val
    return math.floor(val)

def math_random(interpreter, this_val, args):
    return random.random()

def math_abs(interpreter, this_val, args):
    val = to_number(args[0]) if len(args) > 0 else float('nan')
    if math.isnan(val):
        return val
    return abs(val)

def math_ceil(interpreter, this_val, args):
    val = to_number(args[0]) if len(args) > 0 else float('nan')
    if math.isnan(val) or math.isinf(val):
        return val
    return math.ceil(val)

def math_min(interpreter, this_val, args):
    if len(args) == 0:
        return float('inf')
    nums = [to_number(arg) for arg in args]
    if any(math.isnan(n) for n in nums):
        return float('nan')
    return min(nums)

def math_max(interpreter, this_val, args):
    if len(args) == 0:
        return float('-inf')
    nums = [to_number(arg) for arg in args]
    if any(math.isnan(n) for n in nums):
        return float('nan')
    return max(nums)

def math_pow(interpreter, this_val, args):
    base = to_number(args[0]) if len(args) > 0 else float('nan')
    exp = to_number(args[1]) if len(args) > 1 else float('nan')
    if math.isnan(base) or math.isnan(exp):
        return float('nan')
    if base < 0 and isinstance(exp, float) and not exp.is_integer():
        return float('nan')
    try:
        return base ** exp
    except ZeroDivisionError:
        return float('inf')
    except OverflowError:
        return float('inf')

def math_sqrt(interpreter, this_val, args):
    val = to_number(args[0]) if len(args) > 0 else float('nan')
    if val < 0 or math.isnan(val):
        return float('nan')
    return math.sqrt(val)

def math_round(interpreter, this_val, args):
    val = to_number(args[0]) if len(args) > 0 else float('nan')
    if math.isnan(val) or math.isinf(val):
        return val
    return math.floor(val + 0.5)

def make_math_builtin(name, func):
    return JSBuiltinFunction(name, func, prototype=FunctionPrototype)

MathObject.set_property("floor", make_math_builtin("floor", math_floor))
MathObject.set_property("random", make_math_builtin("random", math_random))
MathObject.set_property("abs", make_math_builtin("abs", math_abs))
MathObject.set_property("ceil", make_math_builtin("ceil", math_ceil))
MathObject.set_property("min", make_math_builtin("min", math_min))
MathObject.set_property("max", make_math_builtin("max", math_max))
MathObject.set_property("pow", make_math_builtin("pow", math_pow))
MathObject.set_property("sqrt", make_math_builtin("sqrt", math_sqrt))
MathObject.set_property("round", make_math_builtin("round", math_round))
MathObject.set_property("PI", 3.141592653589793)
MathObject.set_property("E", 2.718281828459045)

# Global Console Object
def js_to_display_string(val):
    if val is None:
        return "null"
    if val is UNDEFINED:
        return "undefined"
    if isinstance(val, bool):
        return "true" if val else "false"
    if isinstance(val, (int, float)):
        if math.isnan(val):
            return "NaN"
        if math.isinf(val):
            return "Infinity" if val > 0 else "-Infinity"
        if isinstance(val, float) and val.is_integer():
            return str(int(val))
        return str(val)
    if isinstance(val, str):
        return val
    if isinstance(val, JSArray):
        return "[" + ", ".join(js_to_display_string(x) if not isinstance(x, str) else f"'{x}'" for x in val.elements) + "]"
    if isinstance(val, JSObject):
        return "[object Object]"
    return str(val)

def console_log(interpreter, this_val, args):
    print_str = " ".join(js_to_display_string(arg) for arg in args)
    print(print_str)
    return UNDEFINED

ConsoleObject = JSObject(prototype=ObjectPrototype)
ConsoleObject.set_property("log", JSBuiltinFunction("log", console_log, prototype=FunctionPrototype))

# Global helper functions
def js_parse_int(interpreter, this_val, args):
    s = js_to_string(args[0]) if len(args) > 0 else "undefined"
    radix = to_number(args[1]) if len(args) > 1 and args[1] is not UNDEFINED else 10
    s = s.strip()
    import re
    match = re.match(r'^\s*[-+]?[0-9a-zA-Z]+', s)
    if not match:
        return float('nan')
    sub = match.group(0).strip()
    try:
        radix_val = int(radix)
        if radix_val < 2 or radix_val > 36:
            return float('nan')
        valid_chars = "0123456789abcdefghijklmnopqrstuvwxyz"[:radix_val]
        sign = 1
        if sub[0] in ('-', '+'):
            if sub[0] == '-':
                sign = -1
            sub = sub[1:]
        cleaned = ""
        for char in sub.lower():
            if char in valid_chars:
                cleaned += char
            else:
                break
        if not cleaned:
            return float('nan')
        return sign * int(cleaned, radix_val)
    except Exception:
        return float('nan')

def js_parse_float(interpreter, this_val, args):
    s = js_to_string(args[0]) if len(args) > 0 else "undefined"
    s = s.strip()
    import re
    match = re.match(r'^\s*[-+]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][-+]?\d+)?', s)
    if not match:
        if s.startswith("Infinity"):
            return float('inf')
        if s.startswith("-Infinity"):
            return float('-inf')
        return float('nan')
    try:
        return float(match.group(0))
    except ValueError:
        return float('nan')

def js_is_nan(interpreter, this_val, args):
    val = to_number(args[0]) if len(args) > 0 else float('nan')
    return math.isnan(val)

def js_is_finite(interpreter, this_val, args):
    val = to_number(args[0]) if len(args) > 0 else float('nan')
    return not (math.isnan(val) or math.isinf(val))

def js_in(left, right):
    if not isinstance(right, JSObject):
        raise TypeError("TypeError: Cannot use 'in' operator to search for property in non-object")
    prop = js_to_string(left)
    return right.get_property(prop) is not UNDEFINED or prop in right.properties

def js_instanceof(left, right):
    if not isinstance(right, JSObject) or not hasattr(right, 'call'):
        raise TypeError("TypeError: Right-hand side of 'instanceof' is not callable")
    if not isinstance(left, JSObject):
        return False
    proto = right.get_property("prototype")
    curr = left.prototype
    while curr is not None:
        if curr is proto:
            return True
        curr = curr.prototype
    return False
