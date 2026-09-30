#!/usr/bin/env python3
"""Rebuild the two publication PDFs and the deterministic expanded coordinate stream.

Verification itself needs only Python. This optional typesetting step needs pandoc,
XeLaTeX, pdfLaTeX, standard TeX packages, and DejaVu fonts installed locally.
No font files are copied into the repository.
"""
from pathlib import Path
import argparse,hashlib,gzip,json,subprocess,sys
ROOT=Path(__file__).resolve().parents[1]
def run(args,cwd):
    p=subprocess.run(args,cwd=cwd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
    if p.returncode:
        print(p.stdout);raise SystemExit(p.returncode)
def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--coordinates-only',action='store_true');ap.add_argument('--pdfs-only',action='store_true');args=ap.parse_args()
    if not args.coordinates_only:
        n=ROOT/'research/n105'
        run(['pandoc','paper/proof_pdf_source.md','-o','PROOF_N105.pdf','--pdf-engine=xelatex','-V','mainfont=DejaVu Serif','-V','monofont=DejaVu Sans Mono','-V','fontsize=10pt','-V','geometry:margin=20mm','-H','paper/header.tex'],n)
        s=ROOT/'research/general-spectra';(s/'build').mkdir(exist_ok=True)
        for _ in range(2):run(['pdflatex','-interaction=nonstopmode','-halt-on-error','-no-shell-escape','-output-directory=build','paper.tex'],s)
        (s/'paper.pdf').write_bytes((s/'build/paper.pdf').read_bytes())
        u=ROOT/'research/uniform-reduction';(u/'build').mkdir(exist_ok=True)
        for _ in range(2):run(['xelatex','-interaction=nonstopmode','-halt-on-error','-no-shell-escape','-output-directory=build','paper.tex'],u)
        (u/'paper.pdf').write_bytes((u/'build/paper.pdf').read_bytes())
        lines=[hashlib.sha256(f.read_bytes()).hexdigest()+'  '+f.name for f in sorted(u.iterdir()) if f.is_file() and f.name not in {'MANIFEST.sha256','SHA256SUMS.txt'}]
        (u/'MANIFEST.sha256').write_text('\n'.join(lines)+'\n')
    if not args.pdfs_only:
        s=ROOT/'research/general-spectra';run([sys.executable,'verify_certificate.py','construction_116640.json','--expand','--expanded-path','tiles_116640.jsonl.gz'],s)
        h=hashlib.sha256();count=0
        with gzip.open(s/'tiles_116640.jsonl.gz','rb') as f:
            for line in f:h.update(line);count+=1
        if h.hexdigest()!='86710b7ea51c174e070bf1cc4cda6860815f9e9c790529008caca53d49bf0f23' or count!=116640:raise SystemExit('Expanded coordinates do not match the frozen stream')
    print('PUBLICATION_OUTPUTS=PASS')
if __name__=='__main__':main()
