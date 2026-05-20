def calculate(expression: str) -> str:
    """Evaluate mathematical expression"""
    try:
        res = eval(expression)
        return str(res)
    except SyntaxError:
        return f"Error: invalid expression '{expression}'"
    except Exception as e:
        return f"Error: {e}"