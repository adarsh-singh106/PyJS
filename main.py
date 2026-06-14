import sys
import esprima
import argparse
from interpreter.evaluator import Evaluator

def print_ast_tree(node, indent="", is_last=True):
    if node is None:
        return
    
    node_type = getattr(node, "type", "Unknown")
    prefix = "+-- " if is_last else "|-- "
    
    detail = ""
    if node_type == "Identifier":
        detail = f" ({node.name})"
    elif node_type == "Literal":
        detail = f" ({node.value})"
    elif node_type in ("BinaryExpression", "AssignmentExpression", "UpdateExpression", "LogicalExpression", "UnaryExpression"):
        detail = f" ({node.operator})"
    
    print(indent + prefix + node_type + detail)
    
    children = []
    for field in ["body", "declarations", "init", "id", "test", "consequent", "alternate", "left", "right", "argument", "arguments", "callee", "properties", "elements", "expression", "cases", "params"]:
        val = getattr(node, field, None)
        if val is None:
            continue
        if isinstance(val, list):
            for item in val:
                if hasattr(item, "type"):
                    children.append(item)
        elif hasattr(val, "type"):
            children.append(val)
            
    child_indent = indent + ("    " if is_last else "|   ")
    for i, child in enumerate(children):
        is_last_child = (i == len(children) - 1)
        print_ast_tree(child, child_indent, is_last_child)

def run_code(code, print_ast=False, evaluate=True):
    try:
        ast = esprima.parseScript(code)
        
        if print_ast:
            print("=== Abstract Syntax Tree (AST) ===")
            print_ast_tree(ast)
            print("==================================\n")
            
        if evaluate:
            evaluator = Evaluator()
            evaluator.evaluate_in_env(ast, evaluator.global_env)
    except esprima.Error as e:
        print(f"SyntaxError: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(e, file=sys.stderr)
        sys.exit(1)

def run_repl():
    print("Welcome to PyJS Runtime REPL (v1.0)")
    print("Type '.exit' or press Ctrl+D to exit.\n")
    evaluator = Evaluator()
    buffer = ""
    
    while True:
        try:
            prompt = "... " if buffer else "pyjs> "
            line = input(prompt)
            if line.strip() == ".exit":
                break
            
            buffer += line + "\n"
            
            try:
                ast = esprima.parseScript(buffer)
                res = evaluator.evaluate_in_env(ast, evaluator.global_env)
                
                from interpreter.runtime import UNDEFINED, js_to_display_string
                if res is not UNDEFINED:
                    print(js_to_display_string(res))
                buffer = ""
            except esprima.Error as e:
                # If it's an unexpected end of input or open bracket, wait for more lines
                err_msg = str(e)
                if "Unexpected end of input" in err_msg or "Unexpected token" in err_msg:
                    continue
                else:
                    print(f"SyntaxError: {e}")
                    buffer = ""
        except KeyboardInterrupt:
            print("\nKeyboardInterrupt")
            buffer = ""
        except EOFError:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")
            buffer = ""

def main():
    parser = argparse.ArgumentParser(description="PyJS: A lightweight JavaScript interpreter built in Python.")
    parser.add_argument("file", nargs="?", help="Path to JavaScript file to execute")
    parser.add_argument("-c", "--code", help="JavaScript code snippet to execute directly")
    parser.add_argument("-a", "--ast", action="store_true", help="Print the AST structure")
    parser.add_argument("--no-eval", action="store_true", help="Parse and show AST without executing")
    
    args = parser.parse_args()
    
    if args.code:
        run_code(args.code, print_ast=args.ast, evaluate=not args.no_eval)
    elif args.file:
        try:
            with open(args.file, "r", encoding="utf-8") as f:
                code = f.read()
            run_code(code, print_ast=args.ast, evaluate=not args.no_eval)
        except FileNotFoundError:
            print(f"Error: File not found: {args.file}", file=sys.stderr)
            sys.exit(1)
    else:
        if not sys.stdin.isatty():
            code = sys.stdin.read()
            run_code(code, print_ast=args.ast, evaluate=not args.no_eval)
        else:
            if args.ast or args.no_eval:
                print("Error: --ast and --no-eval flags require a file or code snippet (-c)", file=sys.stderr)
                sys.exit(1)
            run_repl()

if __name__ == "__main__":
    main()
