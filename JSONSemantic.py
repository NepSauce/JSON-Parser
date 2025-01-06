# Author: Zawad Atif
# ID: B00947033
# Import Block
import os

# Token class to represent a Token
# Most of the code was taken from my Parser from part 2.
# Key change are the SemanticError() and polishing out
# Some of my node() methods with conditional checks
class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

# Custom semantic exception
class SemanticError(Exception):
    def __init__(self, message, token, type_number= 0):
        self.message = f"Error type <Type{type_number}> at <{token.type}, {token.value}>: {message}"
        super().__init__(self.message)

# Custom syntax exception
class SyntaxError(Exception):
    def __init__(self, message, token, type_number=1):
        self.message = f"Error type <Type{type_number}> at <{token.type}, {token.value}>: {message}"
        super().__init__(self.message)

# Represents a node in the JSON syntax tree
class JSONNode:
    def __init__(self, value=None, node_type=None):
        self.value = value
        self.node_type = node_type
        self.children = {} if node_type == 'object' else [] if node_type == 'array' else None

    def add_child(self, key, child):
        if self.node_type == 'object':
            if key in self.children:
                raise SemanticError(f"Duplicate key '{key}' in object.", Token("STRING", key), 5)
            self.children[key] = child
        elif self.node_type == 'array':
            self.children.append(child)

    def write_tree(self, file, depth=0):
        indent = "  " * depth
        if self.node_type == 'object':
            file.write(f"{indent}Object:\n")
            for key, child in self.children.items():
                file.write(f"{indent}  Pair:\n")
                file.write(f"{indent}    Key: {key}\n")
                child.write_tree(file, depth + 2)
        elif self.node_type == 'array':
            file.write(f"{indent}Array:\n")
            for child in self.children:
                file.write(f"{indent}  Element:\n")
                child.write_tree(file, depth + 2)
        elif self.node_type == 'string':
            file.write(f"{indent}String: {self.value}\n")
        elif self.node_type == 'number':
            file.write(f"{indent}Number: {self.value}\n")
        elif self.node_type == 'boolean':
            file.write(f"{indent}Boolean: {self.value}\n")
        elif self.node_type == 'null':
            file.write(f"{indent}Null\n")

# JSON parser class
class JSONParser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token = None
        self.index = -1
        self.get_next_token()

    def get_next_token(self):
        self.index += 1
        if self.index < len(self.tokens):
            self.current_token = self.tokens[self.index]
        else:
            self.current_token = Token("EOF", None)

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.get_next_token()
        else:
            if self.current_token.type == "EOF":
                raise SyntaxError(f"Unexpected EOF. Expected {token_type}.", self.current_token, type_number=1)
            raise SyntaxError(f"Expected {token_type}, but got {self.current_token.type}.", self.current_token, type_number=1)

    def parse(self):
        if not self.tokens:
            raise SyntaxError("No tokens provided for parsing.", Token("EOF", None), type_number=1)
        return self.json_value()

    def json_value(self):
        if self.current_token.type == 'LBRACE':
            return self.json_object()
        elif self.current_token.type == 'LBRACKET':
            return self.json_array()
        elif self.current_token.type == 'STRING':
            return self.json_string()
        elif self.current_token.type == 'NUMBER':
            return self.json_number()
        elif self.current_token.type in {'TRUE', 'FALSE'}:
            return self.json_boolean()
        elif self.current_token.type == 'NULL':
            return self.json_null()
        else:
            raise SyntaxError(f"Unexpected token {self.current_token.type}.", self.current_token, type_number=1)

    def json_object(self):
        node = JSONNode(node_type='object')
        self.eat('LBRACE')
        if self.current_token.type == 'RBRACE':
            self.eat('RBRACE')
            return node
        while True:
            if self.current_token.type != 'STRING':
                raise SyntaxError("Object keys must be strings.", self.current_token, type_number=1)
            key = self.current_token.value
            if key.strip() == "":
                raise SemanticError("Empty dictionary keys are not allowed", self.current_token, type_number=2)
            if key.lower() in {"true", "false"}:
                raise SemanticError(f"Reserved word '{key}' cannot be used as a key", self.current_token, type_number=4)
            self.eat('STRING')
            self.eat('COLON')
            value = self.json_value()
            node.add_child(key, value)
            if self.current_token.type == 'RBRACE':
                break
            if self.current_token.type != 'COMMA':
                raise SyntaxError("Expected ',' or '}'.", self.current_token, type_number=1)
            self.eat('COMMA')
        self.eat('RBRACE')
        return node

    # For parsing JSON array
    # Finds a few semantic and syntax errors
    def json_array(self):
        node = JSONNode(node_type='array')
        self.eat('LBRACKET')
        element_type = None
        if self.current_token.type == 'RBRACKET':
            self.eat('RBRACKET')
            return node
        while True:
            value = self.json_value()
            if element_type is None:
                element_type = value.node_type
            elif value.node_type != element_type:
                raise SemanticError("All elements in an array must be of the same type", self.current_token, type_number=6)
            node.add_child(None, value)
            if self.current_token.type == 'RBRACKET':
                break
            if self.current_token.type != 'COMMA':
                raise SyntaxError("Expected ',' or ']'.", self.current_token, type_number=1)
            self.eat('COMMA')
        self.eat('RBRACKET')
        return node

    def json_string(self):
        value = self.current_token.value
        self.eat('STRING')
        if value.lower() in {"true", "false"}:
            raise SemanticError(f"Reserved word '{value}' cannot be used as a string value", self.current_token, type_number=7)
        if value == "":
            raise SemanticError("String values must not be empty", self.current_token, type_number=2)
        return JSONNode(value=value, node_type='string')

    def json_number(self):
        value = self.current_token.value
        if value.startswith('0') and len(value) > 1 and not value.startswith("0."):
            raise SemanticError(f"Invalid number format: Leading zeros are not allowed", self.current_token, type_number=3)
        if value.startswith('+') and not ('e' in value or 'E' in value):
            raise SemanticError(f"Invalid number format: Leading '+' is not allowed", self.current_token, type_number=3)
        if value.count('.') == 1 and (value.startswith('.') or value.endswith('.')):
            raise SemanticError(f"Invalid decimal number format", self.current_token, type_number=1)
        try:
            number = float(value)
            self.eat('NUMBER')
            return JSONNode(value=number, node_type='number')
        except ValueError:
            raise SemanticError(f"Invalid number format: {value}", self.current_token, type_number=3)

    def json_boolean(self):
        value = True if self.current_token.type == 'TRUE' else False
        self.eat(self.current_token.type)
        return JSONNode(value=value, node_type='boolean')

    def json_null(self):
        self.eat('NULL')
        return JSONNode(value=None, node_type='null')

# Load tokens from file
def load_tokens_from_file(filename):
    tokens = []
    with open(filename, "r") as file:
        for line in file:
            parts = line.strip("<>\n").split(", ")
            token_type = parts[0]
            token_value = None if parts[1] == "None" else parts[1]
            tokens.append(Token(token_type, token_value))
    return tokens

# Parse files and handles output
def parse_files(input_files):
    for input_file in input_files:
        print(f"Processing {input_file}...")
        try:
            tokens = load_tokens_from_file(input_file)
            parser = JSONParser(tokens)
            json_tree = parser.parse()
            output_file = f"output_{os.path.basename(input_file)}"
            with open(output_file, "w") as file:
                json_tree.write_tree(file)
            print(f"Successfully processed {input_file}. Output written to {output_file}.")
        except (SemanticError, SyntaxError) as e:
            output_file = f"output_{os.path.basename(input_file)}"
            with open(output_file, "w") as file:
                file.write(f"{e.message}")
            print(f"Error in {input_file}: {e.message}. Output written to {output_file}.")


# Main method
# This spaghetti code works
# Last 3 files are comprised of valid JSON structures
# Used Generative Tools to create edge cases to test my program
if __name__ == "__main__":
    input_files = [
        "test1.txt", 
        "test1(2).txt",
        "test2.txt",  
        "test3.txt",
        "test3(2).txt",
        "test4.txt",
        "test5.txt",
        "test6.txt",
        "test7.txt",
        "valid1.txt",      # Valid file
        "valid2.txt",      # Valid file
        "valid3.txt",      # Valid file
    ]
    parse_files(input_files)
