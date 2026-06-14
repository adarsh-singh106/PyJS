from interpreter.runtime import (
    UNDEFINED, ReturnException, BreakException, ContinueException,
    JSObject, JSArray, JSFunction, JSBuiltinFunction, JSConstructor,
    js_to_boolean, to_number, to_integer, js_to_string, js_to_primitive,
    js_strict_equal, js_loose_equal, js_add, js_subtract, js_multiply,
    js_divide, js_modulo, js_exponent, js_less_than, js_less_equal,
    js_greater_than, js_greater_equal, to_int32, to_uint32, js_in, js_instanceof,
    ArrayPrototype, StringPrototype, ObjectPrototype, FunctionPrototype
)
from interpreter.environment import Environment, create_global_environment

class Evaluator:
    def __init__(self):
        self.global_env = create_global_environment()
        
    def evaluate_in_env(self, node, env):
        if node is None:
            return UNDEFINED
        method_name = f"visit_{node.type}"
        visitor = getattr(self, method_name, None)
        if visitor is None:
            raise NotImplementedError(f"Visitor for AST node type '{node.type}' is not implemented.")
        return visitor(node, env)
        
    def execute_in_env(self, node, env):
        self.evaluate_in_env(node, env)
        
    def hoist_declarations(self, statements, env):
        for stmt in statements:
            if stmt is None:
                continue
            if stmt.type == "FunctionDeclaration":
                name = stmt.id.name
                func = JSFunction(name, stmt.params, stmt.body, env, is_arrow=False, prototype=FunctionPrototype)
                env.declare(name, func)
            elif stmt.type == "VariableDeclaration" and stmt.kind == "var":
                for decl in stmt.declarations:
                    name = decl.id.name
                    curr = env
                    while curr.outer is not None and not curr.is_function_scope:
                        curr = curr.outer
                    if name not in curr.bindings:
                        curr.declare(name, UNDEFINED)

    def execute_block(self, body_nodes, env):
        self.hoist_declarations(body_nodes, env)
        for stmt in body_nodes:
            self.execute_in_env(stmt, env)
            
    # --- Visitor Methods ---
    def visit_Program(self, node, env):
        self.hoist_declarations(node.body, env)
        res = UNDEFINED
        for stmt in node.body:
            res = self.evaluate_in_env(stmt, env)
        return res
        
    def visit_BlockStatement(self, node, env):
        block_env = Environment(outer=env)
        self.hoist_declarations(node.body, block_env)
        res = UNDEFINED
        for stmt in node.body:
            res = self.evaluate_in_env(stmt, block_env)
        return res
        
    def visit_EmptyStatement(self, node, env):
        return UNDEFINED
        
    def visit_ExpressionStatement(self, node, env):
        return self.evaluate_in_env(node.expression, env)
        
    def visit_VariableDeclaration(self, node, env):
        is_const = (node.kind == "const")
        is_var = (node.kind == "var")
        for decl in node.declarations:
            name = decl.id.name
            if decl.init is not None:
                val = self.evaluate_in_env(decl.init, env)
            else:
                val = UNDEFINED
                
            if is_var:
                env.declare_var(name, val)
            else:
                env.declare(name, val, is_const=is_const)
        return UNDEFINED
        
    def visit_Identifier(self, node, env):
        return env.get(node.name)
        
    def visit_Literal(self, node, env):
        return node.value
        
    def visit_ThisExpression(self, node, env):
        try:
            return env.get('this')
        except NameError:
            return UNDEFINED
            
    def visit_ArrayExpression(self, node, env):
        elements = []
        for el in node.elements:
            if el is None:
                elements.append(UNDEFINED)
            elif el.type == "SpreadElement":
                spread_val = self.evaluate_in_env(el.argument, env)
                if isinstance(spread_val, JSArray):
                    elements.extend(spread_val.elements)
                elif isinstance(spread_val, str):
                    elements.extend(list(spread_val))
                elif hasattr(spread_val, 'elements'):
                    elements.extend(spread_val.elements)
                else:
                    raise TypeError(f"TypeError: {spread_val} is not iterable")
            else:
                elements.append(self.evaluate_in_env(el, env))
        return JSArray(elements, prototype=ArrayPrototype)
        
    def visit_ObjectExpression(self, node, env):
        obj = JSObject(prototype=ObjectPrototype)
        for prop in node.properties:
            if prop.type == "SpreadElement":
                spread_val = self.evaluate_in_env(prop.argument, env)
                if isinstance(spread_val, JSObject):
                    for k, v in spread_val.properties.items():
                        obj.set_property(k, v)
            else:
                if prop.computed:
                    key_val = self.evaluate_in_env(prop.key, env)
                    key_name = js_to_string(key_val)
                else:
                    if prop.key.type == "Identifier":
                        key_name = prop.key.name
                    else:
                        key_name = js_to_string(prop.key.value)
                        
                val = self.evaluate_in_env(prop.value, env)
                obj.set_property(key_name, val)
        return obj
        
    def visit_FunctionDeclaration(self, node, env):
        # Function declarations are hoisted at the start of block/program execution.
        # So we do nothing during normal execution.
        return UNDEFINED
        
    def visit_FunctionExpression(self, node, env):
        name = node.id.name if node.id is not None else None
        return JSFunction(name, node.params, node.body, env, is_arrow=False, prototype=FunctionPrototype)
        
    def visit_ArrowFunctionExpression(self, node, env):
        return JSFunction(None, node.params, node.body, env, is_arrow=True, prototype=FunctionPrototype)
        
    def visit_BinaryExpression(self, node, env):
        left_val = self.evaluate_in_env(node.left, env)
        right_val = self.evaluate_in_env(node.right, env)
        op = node.operator
        
        if op == "+":
            return js_add(left_val, right_val)
        elif op == "-":
            return js_subtract(left_val, right_val)
        elif op == "*":
            return js_multiply(left_val, right_val)
        elif op == "/":
            return js_divide(left_val, right_val)
        elif op == "%":
            return js_modulo(left_val, right_val)
        elif op == "**":
            return js_exponent(left_val, right_val)
        elif op == "==":
            return js_loose_equal(left_val, right_val)
        elif op == "!=":
            return not js_loose_equal(left_val, right_val)
        elif op == "===":
            return js_strict_equal(left_val, right_val)
        elif op == "!==":
            return not js_strict_equal(left_val, right_val)
        elif op == "<":
            return js_less_than(left_val, right_val)
        elif op == "<=":
            return js_less_equal(left_val, right_val)
        elif op == ">":
            return js_greater_than(left_val, right_val)
        elif op == ">=":
            return js_greater_equal(left_val, right_val)
        elif op == "&":
            return to_int32(left_val) & to_int32(right_val)
        elif op == "|":
            return to_int32(left_val) | to_int32(right_val)
        elif op == "^":
            return to_int32(left_val) ^ to_int32(right_val)
        elif op == "<<":
            return to_int32(left_val) << (to_int32(right_val) & 0x1f)
        elif op == ">>":
            return to_int32(left_val) >> (to_int32(right_val) & 0x1f)
        elif op == ">>>":
            return to_uint32(left_val) >> (to_int32(right_val) & 0x1f)
        elif op == "in":
            return js_in(left_val, right_val)
        elif op == "instanceof":
            return js_instanceof(left_val, right_val)
        else:
            raise ValueError(f"Unknown binary operator: {op}")
            
    def visit_LogicalExpression(self, node, env):
        left_val = self.evaluate_in_env(node.left, env)
        if node.operator == "&&":
            if not js_to_boolean(left_val):
                return left_val
            return self.evaluate_in_env(node.right, env)
        elif node.operator == "||":
            if js_to_boolean(left_val):
                return left_val
            return self.evaluate_in_env(node.right, env)
        else:
            raise ValueError(f"Unknown logical operator: {node.operator}")
            
    def visit_UnaryExpression(self, node, env):
        op = node.operator
        if op == "void":
            self.evaluate_in_env(node.argument, env)
            return UNDEFINED
        elif op == "delete":
            if node.argument.type == "MemberExpression":
                obj_val, prop_name = self.evaluate_MemberExpression_ref(node.argument, env)
                if isinstance(obj_val, JSObject):
                    return obj_val.delete_property(prop_name)
                return True
            return True
        elif op == "typeof":
            if node.argument.type == "Identifier":
                try:
                    val = env.get(node.argument.name)
                except NameError:
                    return "undefined"
            else:
                val = self.evaluate_in_env(node.argument, env)
                
            if val is None:
                return "object"
            if val is UNDEFINED:
                return "undefined"
            if isinstance(val, bool):
                return "boolean"
            if isinstance(val, (int, float)):
                return "number"
            if isinstance(val, str):
                return "string"
            if isinstance(val, JSFunction) or isinstance(val, JSBuiltinFunction):
                return "function"
            return "object"
        elif op == "+":
            return to_number(self.evaluate_in_env(node.argument, env))
        elif op == "-":
            return -to_number(self.evaluate_in_env(node.argument, env))
        elif op == "!":
            return not js_to_boolean(self.evaluate_in_env(node.argument, env))
        elif op == "~":
            return ~to_int32(self.evaluate_in_env(node.argument, env))
        else:
            raise ValueError(f"Unknown unary operator: {op}")
            
    def visit_UpdateExpression(self, node, env):
        op = node.operator
        prefix = node.prefix
        if node.argument.type == "Identifier":
            name = node.argument.name
            old_val = to_number(env.get(name))
            new_val = old_val + 1 if op == "++" else old_val - 1
            env.assign(name, new_val)
            return old_val if not prefix else new_val
        elif node.argument.type == "MemberExpression":
            obj_val, prop_name = self.evaluate_MemberExpression_ref(node.argument, env)
            if isinstance(obj_val, JSObject):
                old_val = to_number(obj_val.get_property(prop_name))
                new_val = old_val + 1 if op == "++" else old_val - 1
                obj_val.set_property(prop_name, new_val)
                return old_val if not prefix else new_val
            else:
                raise TypeError("TypeError: Cannot update property of non-object")
        else:
            raise SyntaxError("ReferenceError: Invalid left-hand side in update expression")
            
    def visit_AssignmentExpression(self, node, env):
        op = node.operator
        val = self.evaluate_in_env(node.right, env)
        if op == "=":
            return self.assign_to_ref(node.left, val, env)
        else:
            return self.assign_to_ref(node.left, val, env, op=op)
            
    def visit_MemberExpression(self, node, env):
        obj_val, prop_name = self.evaluate_MemberExpression_ref(node, env)
        if isinstance(obj_val, str):
            if prop_name == "length":
                return len(obj_val)
            try:
                idx = int(prop_name)
                if 0 <= idx < len(obj_val):
                    return obj_val[idx]
                return UNDEFINED
            except ValueError:
                pass
            return StringPrototype.get_property(prop_name)
        elif isinstance(obj_val, JSObject):
            return obj_val.get_property(prop_name)
        else:
            raise TypeError(f"TypeError: Cannot read property '{prop_name}' of {obj_val}")
            
    def visit_CallExpression(self, node, env):
        if node.callee.type == "MemberExpression":
            obj_val = self.evaluate_in_env(node.callee.object, env)
            if obj_val is None or obj_val is UNDEFINED:
                prop_name = "..." if node.callee.computed else node.callee.property.name
                raise TypeError(f"TypeError: Cannot read property '{prop_name}' of {obj_val}")
                
            if node.callee.computed:
                prop_name = js_to_string(self.evaluate_in_env(node.callee.property, env))
            else:
                prop_name = node.callee.property.name
                
            if isinstance(obj_val, str):
                func = StringPrototype.get_property(prop_name)
            elif isinstance(obj_val, JSObject):
                func = obj_val.get_property(prop_name)
            else:
                raise TypeError(f"TypeError: Cannot read property '{prop_name}' of {obj_val}")
                
            this_val = obj_val
        else:
            func = self.evaluate_in_env(node.callee, env)
            this_val = UNDEFINED
            
        if func is None or func is UNDEFINED or not hasattr(func, 'call'):
            name_str = node.callee.name if node.callee.type == 'Identifier' else 'callee'
            raise TypeError(f"TypeError: {name_str} is not a function")
            
        args = []
        for arg in node.arguments:
            if arg.type == "SpreadElement":
                spread_val = self.evaluate_in_env(arg.argument, env)
                if isinstance(spread_val, JSArray):
                    args.extend(spread_val.elements)
                elif isinstance(spread_val, str):
                    args.extend(list(spread_val))
                elif hasattr(spread_val, 'elements'):
                    args.extend(spread_val.elements)
            else:
                args.append(self.evaluate_in_env(arg, env))
                
        return func.call(self, this_val, args)
        
    def visit_NewExpression(self, node, env):
        func = self.evaluate_in_env(node.callee, env)
        if not isinstance(func, JSConstructor):
            name_str = node.callee.name if node.callee.type == 'Identifier' else 'callee'
            raise TypeError(f"TypeError: {name_str} is not a constructor")
            
        args = []
        for arg in node.arguments:
            if arg.type == "SpreadElement":
                spread_val = self.evaluate_in_env(arg.argument, env)
                if isinstance(spread_val, JSArray):
                    args.extend(spread_val.elements)
                elif isinstance(spread_val, str):
                    args.extend(list(spread_val))
                elif hasattr(spread_val, 'elements'):
                    args.extend(spread_val.elements)
            else:
                args.append(self.evaluate_in_env(arg, env))
                
        return func.construct(self, args)
        
    def visit_IfStatement(self, node, env):
        test_val = self.evaluate_in_env(node.test, env)
        if js_to_boolean(test_val):
            return self.evaluate_in_env(node.consequent, env)
        elif node.alternate is not None:
            return self.evaluate_in_env(node.alternate, env)
        return UNDEFINED
        
    def visit_SwitchStatement(self, node, env):
        disc_val = self.evaluate_in_env(node.discriminant, env)
        matched = False
        default_idx = -1
        case_idx = -1
        
        for i, case in enumerate(node.cases):
            if case.test is None:
                default_idx = i
                continue
            test_val = self.evaluate_in_env(case.test, env)
            if js_strict_equal(disc_val, test_val):
                case_idx = i
                matched = True
                break
                
        if not matched and default_idx != -1:
            case_idx = default_idx
            
        if case_idx != -1:
            try:
                for i in range(case_idx, len(node.cases)):
                    for stmt in node.cases[i].consequent:
                        self.execute_in_env(stmt, env)
            except BreakException:
                pass
        return UNDEFINED
        
    def visit_ForStatement(self, node, env):
        loop_env = Environment(outer=env)
        if node.init:
            self.execute_in_env(node.init, loop_env)
            
        while True:
            if node.test:
                test_val = self.evaluate_in_env(node.test, loop_env)
                if not js_to_boolean(test_val):
                    break
                    
            try:
                self.execute_in_env(node.body, loop_env)
            except BreakException:
                break
            except ContinueException:
                pass
                
            if node.update:
                self.evaluate_in_env(node.update, loop_env)
        return UNDEFINED
        
    def visit_WhileStatement(self, node, env):
        while js_to_boolean(self.evaluate_in_env(node.test, env)):
            try:
                self.execute_in_env(node.body, env)
            except BreakException:
                break
            except ContinueException:
                continue
        return UNDEFINED
        
    def visit_DoWhileStatement(self, node, env):
        while True:
            try:
                self.execute_in_env(node.body, env)
            except BreakException:
                break
            except ContinueException:
                pass
                
            if not js_to_boolean(self.evaluate_in_env(node.test, env)):
                break
        return UNDEFINED
        
    def visit_ReturnStatement(self, node, env):
        val = self.evaluate_in_env(node.argument, env) if node.argument is not None else UNDEFINED
        raise ReturnException(val)
        
    def visit_BreakStatement(self, node, env):
        raise BreakException()
        
    def visit_ContinueStatement(self, node, env):
        raise ContinueException()
        
    def visit_ConditionalExpression(self, node, env):
        test_val = self.evaluate_in_env(node.test, env)
        if js_to_boolean(test_val):
            return self.evaluate_in_env(node.consequent, env)
        return self.evaluate_in_env(node.alternate, env)
        
    # --- Helper methods ---
    def evaluate_MemberExpression_ref(self, node, env):
        obj_val = self.evaluate_in_env(node.object, env)
        if obj_val is None or obj_val is UNDEFINED:
            prop_name = "..." if node.computed else node.property.name
            raise TypeError(f"TypeError: Cannot read property '{prop_name}' of {obj_val}")
            
        if node.computed:
            prop_val = self.evaluate_in_env(node.property, env)
            prop_name = js_to_string(prop_val)
        else:
            prop_name = node.property.name
            
        return obj_val, prop_name
        
    def assign_to_ref(self, left_node, value, env, op=None):
        if left_node.type == "Identifier":
            name = left_node.name
            if op is not None:
                old_val = env.get(name)
                value = self.apply_assignment_operator(op, old_val, value)
            env.assign(name, value)
            return value
        elif left_node.type == "MemberExpression":
            obj_val, prop_name = self.evaluate_MemberExpression_ref(left_node, env)
            if isinstance(obj_val, str):
                raise TypeError("TypeError: Cannot assign to read-only property of string")
            elif isinstance(obj_val, JSObject):
                if op is not None:
                    old_val = obj_val.get_property(prop_name)
                    value = self.apply_assignment_operator(op, old_val, value)
                obj_val.set_property(prop_name, value)
                return value
            else:
                raise TypeError(f"TypeError: Cannot set property '{prop_name}' of {obj_val}")
        else:
            raise SyntaxError("ReferenceError: Invalid left-hand side in assignment")
            
    def apply_assignment_operator(self, op, old_val, right_val):
        if op == "+=":
            return js_add(old_val, right_val)
        elif op == "-=":
            return js_subtract(old_val, right_val)
        elif op == "*=":
            return js_multiply(old_val, right_val)
        elif op == "/=":
            return js_divide(old_val, right_val)
        elif op == "%=":
            return js_modulo(old_val, right_val)
        elif op == "**=":
            return js_exponent(old_val, right_val)
        elif op == "&=":
            return to_int32(old_val) & to_int32(right_val)
        elif op == "|=":
            return to_int32(old_val) | to_int32(right_val)
        elif op == "^=":
            return to_int32(old_val) ^ to_int32(right_val)
        elif op == "<<=":
            return to_int32(old_val) << (to_int32(right_val) & 0x1f)
        elif op == ">>=":
            return to_int32(old_val) >> (to_int32(right_val) & 0x1f)
        elif op == ">>>=":
            return to_uint32(old_val) >> (to_int32(right_val) & 0x1f)
        else:
            raise ValueError(f"Unknown assignment operator: {op}")
