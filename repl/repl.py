#!/usr/bin/env python3
import re
from operator import add, sub, mul, mod, truediv

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
        self.ops = { '*': mul, '/': truediv, '%': mod, '+': add, '-': sub, '=': self.assignment }
        self.priority = { '*': 1, '/': 1, '%': 1, '+': 2, '-': 2, '=': 3 }
        self.brackets = { '(', ')', '{', '}', '[', ']' }

    def assignment(self, a, b):
        self.vars[a] = b
        return b

    def interpret_val(self, val):
        if type(val).__name__ == 'int': return val, False
        if val in self.vars: return self.vars[val], False
        if val.isdigit(): return int(val), False
        if val in self.brackets: return val, False
        return val, True

    def eval_(self, tokens):
        i = 0
        while i < len(tokens):
            if ')' in tokens:
                j = k = tokens.index(')')
                if '(' not in tokens[:k]: return None
                while tokens[j] != '(': j -= 1
                r = self.eval_(tokens[j + 1:k].copy())
                if r is None: return None
                tokens[j:k + 1] = [r]
            elif tokens[i] in self.ops:
                if i == len(tokens) - 1: return None
                a, x, b = tokens[i - 1], tokens[i], tokens[i + 1]
                if i + 2 < len(tokens): y = tokens[i + 2]
                if i + 2 < len(tokens) and self.priority[x] > self.priority[y]:
                    if i + 2 == len(tokens) - 1: return None
                    tokens[i + 1] = self.ops[y](b, tokens[i + 3])
                    del tokens[i + 2:i + 4]
                else:
                    tokens[i - 1] = self.ops[x](a, b)
                    del tokens[i:i + 2]
            else:
                i += 1
        if len(tokens) == 1: return tokens[0]
        return None

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
        solution = self.eval_(self.t)
        if solution is not None:
            return int(solution)
        raise Exception('unrecognized input')

interpreter = Interpreter();
input_ = [
    "(  10  /  (  8  -  (  4  +  2  )  )  )  *  3",
    "x = 1",
    "( 8 - ( 4 + 2 ) ) * 3",
    "( 7 + 3 ) / ( 2 * 2 + 1 )",
    "1 + 1", "2 - 1", "2 * 3",
    "8 / 4", "7 % 4",
    "x", "", "4 + 2 * 3", "(1 + 5) * 3"
]
for i in input_:
    r = interpreter.input(i)
    print(r)
