#!/usr/bin/env python3
"""Deterministic CNF export for the owned search's restricted Boolean grammar.

This does not validate the geometric necessity of source assertions.  It
retains all source assertions, explicit root assumptions, and the finite-pool
count bound.  No Z3 code is used by this encoder.
"""
from __future__ import annotations

import argparse
import hashlib
import gzip
import json
from pathlib import Path
import re

if not __debug__:
    raise SystemExit('Run without -O: exact encoding assertions are required.')


def parse(source):
    tokens = re.findall(r'\(|\)|[^\s()]+', source)
    at = 0

    def item():
        nonlocal at
        if at >= len(tokens):
            raise ValueError('Truncated expression')
        token = tokens[at]
        at += 1
        if token == '(':
            out = []
            while at < len(tokens) and tokens[at] != ')':
                out.append(item())
            if at == len(tokens):
                raise ValueError('Unclosed expression')
            at += 1
            return tuple(out)
        if token == ')':
            raise ValueError('Unexpected closing parenthesis')
        return token

    result = item()
    if at != len(tokens):
        raise ValueError('More than one expression')
    if isinstance(result, tuple) and result and result[0] == 'assert':
        if len(result) != 2:
            raise ValueError('Malformed assertion')
        result = result[1]
    return result


def negate(literal):
    return not literal if isinstance(literal, bool) else -literal


class Encoder:
    def __init__(self):
        self.variables = 0
        self.symbols = {}
        self.clauses = []
        self.memo = {}

    def fresh(self):
        self.variables += 1
        return self.variables

    def clause(self, literals):
        out = []
        seen = set()
        for literal in literals:
            if literal is True:
                return
            if literal is False:
                continue
            if -literal in seen:
                return
            if literal not in seen:
                seen.add(literal)
                out.append(literal)
        self.clauses.append(tuple(out))

    def conjunction(self, literals):
        out = []
        seen = set()
        for literal in literals:
            if literal is False:
                return False
            if literal is True:
                continue
            if -literal in seen:
                return False
            if literal not in seen:
                seen.add(literal)
                out.append(literal)
        if not out:
            return True
        if len(out) == 1:
            return out[0]
        v = self.fresh()
        for literal in out:
            self.clause((-v, literal))
        self.clause((v, *(negate(x) for x in out)))
        return v

    def disjunction(self, literals):
        return negate(self.conjunction(negate(x) for x in literals))

    def xor(self, a, b):
        if a is False:
            return b
        if b is False:
            return a
        if a is True:
            return negate(b)
        if b is True:
            return negate(a)
        if a == b:
            return False
        if a == -b:
            return True
        v = self.fresh()
        for clause in ((-a, -b, -v), (a, b, -v),
                       (a, -b, v), (-a, b, v)):
            self.clause(clause)
        return v

    def add_bits(self, a, b):
        result = []
        carry = False
        for i in range(max(len(a), len(b))):
            x = a[i] if i < len(a) else False
            y = b[i] if i < len(b) else False
            result.append(self.xor(self.xor(x, y), carry))
            carry = self.disjunction((
                self.conjunction((x, y)),
                self.conjunction((x, carry)),
                self.conjunction((y, carry))))
        if carry is not False:
            result.append(carry)
        while result and result[-1] is False:
            result.pop()
        return result

    def count_bits(self, literals):
        level = [[literal] for literal in literals]
        return self.sum_vectors(level)

    def sum_vectors(self,level):
        while len(level) > 1:
            level = [self.add_bits(level[i], level[i + 1])
                     if i + 1 < len(level) else level[i]
                     for i in range(0, len(level), 2)]
        return level[0] if level else []

    def cardinality(self, op, bound, literals):
        return self.weighted(op,bound,literals,[1]*len(literals))

    def weighted(self, op, bound, literals, weights):
        assert len(weights) == len(literals) and all(w > 0 for w in weights)
        if bound < 0:
            return False
        maximum = sum(weights)
        if op in ('at-most','pble') and bound >= maximum:
            return True
        if bound > maximum:
            return False
        bits = self.sum_vectors([[literal if (weight>>k)&1 else False
                                  for k in range(weight.bit_length())]
                                 for literal,weight in zip(literals,weights)])
        if op == 'pbeq':
            if bound >> len(bits):
                return False
            return self.conjunction(bit if (bound >> i) & 1 else negate(bit)
                                    for i, bit in enumerate(bits))
        if bound >= 1 << len(bits):
            return True
        equal, lower = True, False
        for i in range(len(bits) - 1, -1, -1):
            bit = bits[i]
            if (bound >> i) & 1:
                lower = self.disjunction((lower, self.conjunction((equal, negate(bit)))))
                equal = self.conjunction((equal, bit))
            else:
                equal = self.conjunction((equal, negate(bit)))
        return self.disjunction((lower, equal))

    def literal(self, node):
        if node in self.memo:
            return self.memo[node]
        if isinstance(node, str):
            if node in ('true', 'false'):
                result = node == 'true'
            else:
                if not re.fullmatch(r'[A-Za-z_][A-Za-z_0-9.-]*', node):
                    raise ValueError('Unsupported symbol: ' + node)
                result = self.symbols.setdefault(node, 0)
                if not result:
                    result = self.symbols[node] = self.fresh()
        elif isinstance(node, tuple) and node:
            op, *args = node
            if isinstance(op, tuple):
                if len(op) < 3 or op[0] != '_' or op[1] not in ('at-most', 'pbeq', 'pble'):
                    raise ValueError('Unsupported indexed operator: ' + repr(op))
                if op[1] == 'at-most' and len(op) != 3:
                    raise ValueError('Malformed at-most')
                if op[1] == 'pbeq' and (len(op) != len(args) + 3 or any(w != '1' for w in op[3:])):
                    raise ValueError('Only unweighted pbeq is supported')
                literals = [self.literal(x) for x in args]
                if op[1] == 'pble':
                    if len(op) != len(args)+3:
                        raise ValueError('Malformed weighted pble')
                    weights = list(map(int,op[3:]))
                    if any(w <= 0 for w in weights):
                        raise ValueError('Only positive integer pble weights are supported')
                    result = self.weighted(op[1],int(op[2]),literals,weights)
                else:
                    result = self.cardinality(op[1], int(op[2]), literals)
            elif op == 'not' and len(args) == 1:
                result = negate(self.literal(args[0]))
            elif op == 'and':
                result = self.conjunction(self.literal(x) for x in args)
            elif op == 'or':
                result = self.disjunction(self.literal(x) for x in args)
            elif op == '=>' and len(args) == 2:
                result = self.disjunction((negate(self.literal(args[0])), self.literal(args[1])))
            elif op == '=' and len(args) == 2:
                result = negate(self.xor(self.literal(args[0]), self.literal(args[1])))
            else:
                raise ValueError('Unsupported Boolean operator: ' + repr(op))
        else:
            raise ValueError('Malformed Boolean expression')
        self.memo[node] = result
        return result


def encode_assertions(assertions):
    encoder = Encoder()
    for source in assertions:
        encoder.clause((encoder.literal(parse(source)),))
    return dict(variables=encoder.variables, clauses=[list(c) for c in encoder.clauses],
                symbols=encoder.symbols, source_assertions=assertions,
                source_sha256=hashlib.sha256(json.dumps(assertions, separators=(',', ':')).encode()).hexdigest())


def read_model(path):
    raw = Path(path).read_bytes()
    if raw.startswith(b'\x1f\x8b'):
        raw = gzip.decompress(raw)
    model = json.loads(raw)
    assertions = list(model['permanent_assertions'])
    assertions.extend(model.get('root_assumptions', []))
    if 'query_count_bound' not in model:
        raise ValueError('The explicit query_count_bound must be retained')
    assertions.append(model['query_count_bound'])
    if not all(isinstance(a, str) for a in assertions):
        raise ValueError('Assertions must be SMT Boolean terms')
    return model, encode_assertions(assertions)


def write_dimacs(record, path):
    with Path(path).open('w') as out:
        out.write(f"p cnf {record['variables']} {len(record['clauses'])}\n")
        for clause in record['clauses']:
            out.write(' '.join(map(str, clause)) + (' ' if clause else '') + '0\n')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('model', type=Path)
    parser.add_argument('output_prefix', type=Path)
    args = parser.parse_args()
    _, record = read_model(args.model)
    record['model_file_sha256'] = hashlib.sha256(args.model.read_bytes()).hexdigest()
    cnf = Path(str(args.output_prefix) + '.cnf')
    write_dimacs(record, cnf)
    Path(str(args.output_prefix) + '.cnf.json').write_text(json.dumps(record, separators=(',', ':')) + '\n')
    print(json.dumps(dict(status='ENCODED', variables=record['variables'], clauses=len(record['clauses']),
                          cnf=str(cnf), scope='Restricted Boolean encoding; geometric necessity remains a separate audit.')))


if __name__ == '__main__':
    main()
