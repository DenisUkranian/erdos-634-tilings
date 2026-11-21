#!/usr/bin/env python3
"""Compose exact geometric regeneration, CNF regeneration and DRAT checking.

No SMT or SAT library is imported. A root-conditioned result excludes only
that explicitly identified root. Exhaustive root coverage remains a separate
required verification before claiming a complete board exclusion.
"""
import argparse
import hashlib
import json
from pathlib import Path

from check_drat import check_files, check_with_propagation, read_dimacs
from proof_cnf import encode_assertions
from verify_snapshot import SnapshotAudit,read_snapshot_bytes


def verify(model_path,cnf_path,proof_path,reduced_path=None,verbose=False):
    raw = read_snapshot_bytes(model_path)
    model = json.loads(raw)
    semantic = SnapshotAudit(model).run(verbose)
    sources = list(model['permanent_assertions'])+list(model.get('root_assumptions',[]))
    sources.append(model['query_count_bound'])
    expected = encode_assertions(sources)
    variables,clauses = read_dimacs(cnf_path)
    assert variables == expected['variables'], 'CNF variable count mismatch'
    assert clauses == list(map(tuple,expected['clauses'])), 'CNF differs from exact source re-encoding'
    proof = (check_with_propagation(cnf_path,reduced_path,proof_path) if reduced_path is not None
             else check_files(cnf_path,proof_path))
    assert proof['status'] == 'VERIFIED_UNSAT'
    root = model['root']
    return dict(status='VERIFIED_ROOT_UNSAT' if root is not None else 'VERIFIED_UNRESTRICTED_MODEL_UNSAT',
                sides=model['sides'],N=model['N'],root=root,
                model_sha256=hashlib.sha256(raw).hexdigest(),semantic_audit=semantic,proof_audit=proof,
                scope='Only the explicitly recorded root is excluded; check exhaustive root coverage separately.'
                      if root is not None else
                      'The unrestricted finite necessary model is refuted, under the mathematical inputs stated in audit/README.md.')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('model',type=Path)
    parser.add_argument('cnf',type=Path)
    parser.add_argument('proof',type=Path)
    parser.add_argument('--propagated-cnf',type=Path)
    parser.add_argument('--verbose',action='store_true')
    parser.add_argument('--report',type=Path)
    args = parser.parse_args()
    report = verify(args.model,args.cnf,args.proof,args.propagated_cnf,args.verbose)
    text = json.dumps(report,indent=2)+'\n'
    if args.report:
        args.report.write_text(text)
    print(text,end='')


if __name__ == '__main__':
    main()
