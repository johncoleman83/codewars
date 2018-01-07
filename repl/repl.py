#!/usr/bin/env python3
import re

def tokenize(expression):
    if expression == "":
        return []

    regex = re.compile("\s*(=>|[-+*\/\%=\(\)]|[A-Za-z_][A-Za-z0-9_]*|[0-9]*\.?[0-9]+)\s*")
    tokens = regex.findall(expression)
    return [s for s in tokens if not s.isspace()]

class Interpreter:
    def __init__(self):
        self.vars = {}
        self.assign_operator_functions()

    def assign_operator_functions(self):
        self.ops = {
            '*': self.mulitplication,
            '+': self.addition,
            '/': self.division,
            '%': self.modulo,
            '-': self.subtraction,
            '=': self.assignment
        }

    def is_float(self, n):
        try:
            float(n)
            return True
        except ValueError:
            return False

    def mulitplication(self, a, b): return a * b
    def addition(self, a, b): return a + b
    def division(self, a, b): return a // b
    def modulo(self, a, b): return a % b
    def subtraction(self, a, b): return a - b
    def assignment(self, a, b):
        self.vars[a] = b
        return b

    def interpret_val(self, val):
        if type(val).__name__ == 'int': return val, False
        if val in self.vars: return self.vars[val], False
        if val.isdigit(): return int(val), False
        if self.is_float(val): return float(val), False
        return val, True

    def input(self, expression):
        tokens = tokenize(expression)
        print(tokens)

        if len(tokens) == 0: return ""

        i = 0
        while i < len(tokens):
            if tokens[i] not in self.ops:
                tokens[i], unassigned = self.interpret_val(tokens[i])
            i += 1

        if len(tokens) == 1:
            void, unassigned = self.interpret_val(tokens[0])
            if unassigned is True:
                raise Exception("ERROR: Invalid identifier. No variable with name '{}' was found.".format(tokens[0]))
            return tokens[0]

        # NEED TO HANDLE MULTIPLE EXPRESSIONS
        i = 0
        while i < len(tokens):
            if tokens[i] in self.ops:
                if tokens[i] != '=':
                    void, unassigned = self.interpret_val(tokens[i - 1])
                    if unassigned is True:
                        raise Exception("ERROR: Invalid identifier. No variable with name '{}' was found.".format(tokens[i - 1]))
                    void, unassigned = self.interpret_val(tokens[i + 1])
                    if unassigned is True:
                        raise Exception("ERROR: Invalid identifier. No variable with name '{}' was found.".format(tokens[i + 1]))
                r = self.ops[tokens[i]](tokens[i - 1], tokens[i + 1])
                return r
            i += 1

        raise Exception('unrecognized input')

interpreter = Interpreter();
input_ = [
    "1 + 1", "2 - 1", "2 * 3",
    "8 / 4", "7 % 4", "x = 1",
    "x", ""
]
for i in input_:
    r = interpreter.input(i)
    print(r)
