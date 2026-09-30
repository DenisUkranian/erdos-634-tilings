#!/usr/bin/env python3
"""Offline integrity, syntax, local-link and claim-scope audit; not a proof assistant."""
from __future__ import annotations
import argparse, ast, gzip, hashlib, json, re, sys
from pathlib import Path
from urllib.parse import unquote, urlsplit
ROOT=Path(__file__).resolve().parents[1]
SKIP={'.git','__pycache__','.pytest_cache','audit-output','build','dist','.publication'}
TEXT={'.md','.tex','.yml','.yaml','.cff','.txt','.py'}

def files(root:Path):
    return sorted(p for p in root.rglob('*') if p.is_file() and not any(x in SKIP for x in p.relative_to(root).parts) and p.suffix not in {'.pyc','.aux','.log','.out','.toc','.fls','.fdb_latexmk'})

def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--skip-manifest',action='store_true');ap.add_argument('--output',type=Path)
    args=ap.parse_args();errors=[];warnings=[];inventory=[];urls=set();links=0;pycount=jsoncount=0
    tracked=files(ROOT)
    for p in tracked:
        rel=p.relative_to(ROOT).as_posix();raw=p.read_bytes()
        inventory.append({'path':rel,'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()})
        if p.suffix=='.py':
            pycount+=1
            try:ast.parse(raw,filename=rel)
            except Exception as e:errors.append({'path':rel,'syntax':str(e)})
        if p.suffix=='.json':
            jsoncount+=1
            try:json.loads(raw)
            except Exception as e:errors.append({'path':rel,'json':str(e)})
        if p.suffix in TEXT:
            try:text=raw.decode('utf-8')
            except UnicodeError as e:errors.append({'path':rel,'utf8':str(e)});continue
            urls.update(x.rstrip('.,;') for x in re.findall(r'https?://[^\s<>"\]\)]+',text))
            # Search only falsely labelled project identities, not legitimate history or arithmetic 506.
            if p.name in {'README.md','README.ru.md','CITATION.cff','ABOUT.txt'} and re.search(r'(?:proof of|доказательство задачи) (?:Erd[oő]s Problem )?506',text,re.I):
                errors.append({'path':rel,'wrong_project_identity':True})
            if p.suffix=='.md':
                clean=re.sub(r'```.*?```','',text,flags=re.S)
                targets=re.findall(r'!?\[[^\]\n]*\]\(([^\s)]+)(?:\s+"[^"\n]*")?\)',clean)
                targets += re.findall(r'^\[[^\]\n]+\]:\s*(\S+)',clean,flags=re.M)
                for target in targets:
                    target=target.strip('<>');u=urlsplit(target)
                    if u.scheme or target.startswith('//'):continue
                    links+=1
                    path=(ROOT/unquote(u.path.lstrip('/'))) if u.path.startswith('/') else p.parent/unquote(u.path)
                    if not u.path:path=p
                    if not path.exists():errors.append({'path':rel,'broken_local_link':target});continue
                    if ROOT.resolve() not in [path.resolve(),*path.resolve().parents]:errors.append({'path':rel,'escaping_link':target})
                    # GitHub's exact heading IDs for math/punctuation can vary; record but do not invent certainty.
                    if u.fragment and path.suffix=='.md':
                        headings=re.findall(r'^#{1,6}\s+(.+?)\s*#*$',path.read_text(),re.M)
                        def slug(s):
                            s=re.sub(r'<[^>]+>','',s).lower();s=re.sub(r'[^\w\- ]','',s);return s.replace(' ','-')
                        anchors={slug(h) for h in headings}
                        if unquote(u.fragment) not in anchors:warnings.append({'path':rel,'anchor_requires_render_check':target})
    manifest_path=ROOT/'verification/manifest.json'
    if not args.skip_manifest:
        manifest=json.loads(manifest_path.read_text()); entries=manifest['files']
        for rel,entry in entries.items():
            p=ROOT/rel
            if not p.exists():errors.append({'missing_manifest_file':rel});continue
            raw=p.read_bytes()
            if len(raw)!=entry['bytes'] or hashlib.sha256(raw).hexdigest()!=entry['sha256']:errors.append({'manifest_mismatch':rel})
        actual={p.relative_to(ROOT).as_posix() for p in tracked}-{'verification/manifest.json','verification/replay.json'}
        if actual!=set(entries):errors.append({'manifest_missing_entries':sorted(actual-set(entries)),'manifest_extra_entries':sorted(set(entries)-actual)})
    # Strong scope sentinels keep particular verified results separate from the all-integer problem.
    for rel in ['research/n105/VERIFIED_RESULTS.json','research/general-spectra/VERIFIED_RESULTS.json']:
        d=json.loads((ROOT/rel).read_text())
        if d.get('full_Erdos634_solved') is not False:errors.append({'invalid_all_problem_scope':rel})
    cff=(ROOT/'CITATION.cff').read_text()
    if 'version: 0.2.0' not in cff or '634' not in cff:errors.append({'citation_identity_or_version':False})
    # Check generated coordinate stream against the frozen, uncompressed content hash.
    p=ROOT/'research/general-spectra/tiles_116640.jsonl.gz'
    if p.exists():
        digest=hashlib.sha256();n=0
        with gzip.open(p,'rb') as stream:
            for line in stream:digest.update(line);n+=1
        if n!=116640 or digest.hexdigest()!='86710b7ea51c174e070bf1cc4cda6860815f9e9c790529008caca53d49bf0f23':errors.append({'expanded_coordinates_mismatch':True})
    else:errors.append({'missing_expanded_coordinates':p.relative_to(ROOT).as_posix()})
    report={'status':'PASS' if not errors else 'FAIL','tracked_files':len(tracked),'python_files':pycount,'json_files':jsoncount,'local_links_checked':links,'external_urls_found':sorted(urls),'warnings':warnings,'errors':errors,'inventory':inventory,'scope':'File coverage, integrity, syntax, local targets and declared scopes only. No formal verification of universal mathematics.'}
    text=json.dumps(report,ensure_ascii=False,indent=2)+'\n'
    if args.output:args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(text)
    print(json.dumps({k:v for k,v in report.items() if k not in {'inventory','external_urls_found'}},ensure_ascii=False,indent=2))
    if errors:raise SystemExit(1)
if __name__=='__main__':main()
