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
        self.assign_operators()

    def assign_operators(self):
        self.ops = {
            '*': self.mulitplication,
            '/': self.division,
            '%': self.modulo,
            '+': self.addition,
            '-': self.subtraction,
            '=': self.assignment
        }
        self.priority = {
            '*': 1,
            '/': 1,
            '%': 1,
            '+': 2,
            '-': 2,
            '=': 3
        }

    def is_float(self, n):
        try:
            float(n)
            return True
        except ValueError: return False

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

    def handle_single_token(self):
        void, unassigned = self.interpret_val(self.t[0])
        if unassigned is True:
            raise Exception("ERROR: Invalid identifier. No variable with name '{}' was found.".format(self.t[0]))
        return self.t[0]

    def evaluate_expression(self):
        i = 0
        while i < len(self.t):
            if self.t[i] in self.ops:
                if self.priority[self.t[i]]
                r = self.ops[self.t[i]](self.t[i - 1], self.t[i + 1])
                return r
            i += 1

    def input(self, expression):
        self.t = tokenize(expression)
        if len(self.t) == 0: return ""

        i = 0
        while i < len(self.t):
            if self.t[i] not in self.ops:
                self.t[i], unassigned = self.interpret_val(self.t[i])
                if unassigned is True and self.t[1] != '=':
                    raise Exception("ERROR: Invalid identifier. No variable with name '{}' was found.".format(self.t[i]))
            i += 1

        if len(self.t) == 1:
            return self.handle_single_token()

        evaluate = self.evaluate_expression()
        if evaluate is not None:
            return evaluate

        raise Exception('unrecognized input')

interpreter = Interpreter();
input_ = [
    "1 + 1", "2 - 1", "2 * 3",
    "8 / 4", "7 % 4", "x = 1",
    "x", "", "4 + 2 * 3"
]
for i in input_:
    r = interpreter.input(i)
    print(r)
