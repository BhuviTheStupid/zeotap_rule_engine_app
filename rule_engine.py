# import re
from models import Node
import re

def create_rule(rule_string):
    if(rule_string == ""):
        return
    tokens = rule_string.replace('(', ' ( ').replace(')', ' ) ').split()
    ast, _ = parse_expression(tokens)  # We only need the AST, ignore the index
    return ast

def parse_expression(tokens):
    stack = []
    current = []
    operators = []

    i = 0
    while i < len(tokens):
        token = tokens[i]

        if token == '(':
            # Start of a new sub-expression
            sub_expr, sub_expr_end = parse_expression(tokens[i + 1:])  # Recursively parse
            current.append(sub_expr)
            i += sub_expr_end + 1  # Move past the sub-expression
        elif token == ')':
            # End of the current sub-expression
            break
        elif token in ('AND', 'OR'):
            if current:
                stack.append(current)
                current = []
            operators.append(token)
            i += 1
        else:
            # It's an operand
            if i + 2 < len(tokens) and tokens[i + 1] in ('>', '<', '=', '>=', '<=', '!='):
                operand = f"{token} {tokens[i + 1]} {tokens[i + 2]}"
                current.append(Node('operand', value=operand))
                i += 3  # Skip the next two tokens
            else:
                raise ValueError(f"Invalid operand format: {token}")

    # Handle remaining conditions
    if current:
        stack.append(current)

    while operators:
        left = stack.pop(0) if stack else current
        operator = operators.pop(0)
        right = stack.pop(0) if stack else current

        left_node = left[0] if len(left) == 1 else Node('operator', left=left[0], right=None, value=operator)
        current = [Node('operator', left=left_node, right=right[0], value=operator)]

    if len(current) == 1:
        return current[0], i  # Return the single root node and the index

    raise ValueError("Invalid expression: unable to construct AST.")

# def evaluate_rule(ast, user_data):
    if ast is None:
        raise ValueError("AST is None, cannot evaluate.")

    # Debugging output
    print(f"Evaluating AST: {ast}") 

    if ast.type == 'operator':
        left_result = evaluate_rule(ast.left, user_data)
        right_result = evaluate_rule(ast.right, user_data)

        if ast.value == 'AND':
            return left_result and right_result
        elif ast.value == 'OR':
            return left_result or right_result
        else:
            raise ValueError(f"Unknown operator: {ast.value}")

    elif ast.type == 'operand':
        condition_parts = ast.value.split(' ')
        if len(condition_parts) != 3:
            raise ValueError(f"Invalid operand format: {ast.value}")

        field, operator, value = condition_parts[0], condition_parts[1], condition_parts[2].strip("'")

        # Check if the field exists in user_data
        if field not in user_data:
            raise ValueError(f"Field '{field}' not found in user data.")

        # Evaluate based on the operator
        if operator == '>':
            return user_data[field] > int(value)
        elif operator == '<':
            return user_data[field] < int(value)
        elif operator == '=':
            return user_data[field] == value
        elif operator == '>=':
            return user_data[field] >= int(value)
        elif operator == '<=':
            return user_data[field] <= int(value)
        elif operator == '!=':
            return user_data[field] != value
        else:
            raise ValueError(f"Unknown operator: {operator}")

    raise ValueError(f"Invalid AST node: {ast}")

def evaluate_rule(ast, user_data):
    if ast is None:
        raise ValueError("AST is None, cannot evaluate.")

    if ast.type == 'operator':
        left_result = evaluate_rule(ast.left, user_data)
        right_result = evaluate_rule(ast.right, user_data)

        if ast.value == 'AND':
            return left_result and right_result
        elif ast.value == 'OR':
            return left_result or right_result
        else:
            raise ValueError(f"Unknown operator: {ast.value}")

    elif ast.type == 'operand':
        condition_parts = ast.value.split(' ')
        if len(condition_parts) != 3:
            raise ValueError(f"Invalid operand format: {ast.value}")

        field = condition_parts[0]
        operator = condition_parts[1]
        value = condition_parts[2].strip("'")

        # Ensure the field exists in user_data
        if field not in user_data:
            raise ValueError(f"Field '{field}' not found in user data.")

        # Ensure the data type is correct for comparison
        user_value = user_data[field]
        try:
            if user_value.isdigit():
                user_value = int(user_value)
            value = int(value) if value.isdigit() else value
        except ValueError:
            raise ValueError(f"Data type mismatch for field '{field}'.")

        # Perform the comparison
        if operator == '>':
            return user_value > value
        elif operator == '<':
            return user_value < value
        elif operator == '=':
            return user_value == value
        elif operator == '>=':
            return user_value >= value
        elif operator == '<=':
            return user_value <= value
        elif operator == '!=':
            return user_value != value
        else:
            raise ValueError(f"Unknown operator: {operator}")

    raise ValueError(f"Invalid AST node: {ast}")