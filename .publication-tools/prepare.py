"""Prepare an attributed, English-only release; upload Git objects, never move refs."""
from pathlib import Path
import argparse, base64, hashlib, json, os, subprocess, urllib.request

REPO='DenisUkranian/erdos-634-tilings'
BASE='052b654f4a04eee3a28ee449dfe1b02bbd19db32'
p=argparse.ArgumentParser();p.add_argument('root');p.add_argument('--upload',action='store_true');a=p.parse_args()
root=Path(a.root).resolve()
def eligible(f):
    r=f.relative_to(root)
    return f.is_file() and not any(x in {'.git','build','audit-output','__pycache__'} for x in r.parts) and f.suffix not in {'.aux','.log','.out','.pyc'}
def snapshot():return {f.relative_to(root).as_posix():hashlib.sha256(f.read_bytes()).hexdigest() for f in root.rglob('*') if eligible(f)}
before=snapshot()
def put(path,text):
    f=root/path;f.parent.mkdir(parents=True,exist_ok=True);f.write_text(text,encoding='utf-8')
def replace(path,old,new):
    f=root/path;t=f.read_text()
    if t.count(old)!=1:raise ValueError('Ambiguous edit '+path)
    f.write_text(t.replace(old,new))

put('.github/workflows/verify.yml', '''name: Full research verification
on:
  push:
    branches: [main]
  pull_request:
  workflow_dispatch:
permissions:
  contents: read
jobs:
  verify:
    runs-on: ubuntu-latest
    timeout-minutes: 35
    steps:
      - uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1
        with:
          persist-credentials: false
      - name: Record source commit
        run: |
          mkdir -p audit-output
          git rev-parse HEAD > audit-output/verified-commit.txt
          git archive --format=zip HEAD > audit-output/verified-source.zip
      - name: Replay every published finite suite
        run: |
          set -o pipefail
          python3 scripts/verify_all.py --jobs 2 2>&1 | tee audit-output/full-replay.log
      - name: Preserve exact verification evidence
        if: always()
        uses: actions/upload-artifact@ea165f8d65b6e75b540449e92b4886f43607fa02
        with:
          name: full-research-verification-${{ github.sha }}
          path: audit-output/
          retention-days: 30
''')

put('research/general-spectra/ATTRIBUTION.md', '''# Attribution addendum — 30 September 2026

A subsequent source comparison found that the 120-degree threshold refinement and the same fixed-tile example in this package were already written down by **Jan Philipp Harries**, *New constructions, obstructions, and multiplier structure for Erdős Problem 634*, version 0.5, dated 28 August 2026.

In its trapezoid section the manuscript proves

    R(a,b) = ceil(a/b) + ceil(b/a),     m >= 3R(a,b),

and explicitly gives the tile (32,45,67), multiplier m=9, and count 116640 below the printed conjectural cutoff 12. For A=max(a,b)>B>1, coprimality makes 3R=3(floor(A/B)+2), exactly the 120-degree bound derived here.

Source of record inspected: [progress634.tex](https://github.com/jphme/math-problems/blob/main/progress634/progress634.tex), lines 1080–1110 in the inspected file, blob SHA `85536aabe013ad393e33985cbfcadbae50722f08`. The [author's README](https://github.com/jphme/math-problems/blob/main/progress634/README.md) identifies version 0.5 and its date.

Accordingly, these mathematical conclusions and this example are **prior work, rederived and independently implemented here**, not first discoveries of this project. The package supplies its own inspectable macrocertificate, generator, expanded exact coordinates, and separate checking program. The integer 116640 was already globally admissible; the example concerns the specified tile and multiplier.

The direction-functional framework also predates this note: Laczkovich's signed specialization, later Laurent/signed-direction treatments by Harries and Bonfioli, and Zhang's constructive geometry are relevant. The existing note already credits Bonfioli for the isosceles/F1 necessary spectra and Zhang for the building blocks. No priority claim is made for any other statement in this package.

This addendum does not import unrelated claims from the earlier manuscripts. In particular, it does not validate the separate all-primes candidate, and it does not treat a finite generator window for each fixed ray as a finite global classification.
''')
replace('research/general-spectra/README.md', 'Read `PROOF.md` (English) or `RESULT_RU.md` (Russian). The typeset version is', 'Read the [attribution addendum](ATTRIBUTION.md) and `PROOF.md`. The typeset version is')
replace('research/general-spectra/PROOF.md', '## 1. Two boundary characters and one parity constraint', '''**Attribution addendum (30 September 2026).** Harries, version 0.5 (28 August 2026), already derives the same 120-degree threshold refinement and explicitly gives the (32,45,67), m=9, N=116640 example. These are rederived and independently implemented here, not first discoveries. See [the source comparison](ATTRIBUTION.md).

## 1. Two boundary characters and one parity constraint''')
replace('research/general-spectra/paper.tex', '\\section{Two characters and parity}', r'''\paragraph{Attribution addendum (30 September 2026).}
Harries~\cite{Harries}, version 0.5 dated 28 August 2026, already derives the same $120^\circ$ threshold refinement and explicitly records $(32,45,67)$ at multiplier $9$, with $116640$ tiles below the printed cutoff $12$. These conclusions and this example are prior work, rederived and independently implemented here. Our package supplies its own exact coordinates and checking programs, not a first-discovery claim.

\section{Two characters and parity}''')
replace('research/general-spectra/paper.tex', '\\end{thebibliography}', r'''\bibitem{Harries} Jan Philipp Harries, \emph{New constructions, obstructions, and multiplier structure for Erd\H{o}s Problem 634}, version 0.5, 28 August 2026, trapezoid section. Inspected source blob \texttt{85536aabe013ad393e33985cbfcadbae50722f08}. \url{https://github.com/jphme/math-problems/tree/main/progress634}.
\end{thebibliography}''')
replace('README.md', '## Verification', '''The 120-degree cutoff refinement and the (45,32,67), m=9 example are prior results in Harries's August 2026 manuscript, rederived and independently implemented here. Read the [attribution addendum](research/general-spectra/ATTRIBUTION.md) and [literature audit](docs/literature-audit-2026-09-30.md).

## Verification''')
put('docs/literature-audit-2026-09-30.md', '''# Literature and scope audit — 30 September 2026

This is a targeted comparison, not a claim of having independently re-proved every cited paper.

## Sources and consequences

- **Beeson–Zhang**, *Rationality of certain triangle tilings*, arXiv:2604.01314v1: the rationality theorem and angular classification table license integer normalization and the listed nonsimilar branches under their hypotheses. They do not decide all allowable multipliers.
- **Beeson**, *Tilings of an Isosceles Triangle*, arXiv:1206.1974v7: right-tile restrictions, double-angle necessary conditions, and the existing finite-search perspective. Decidability for each input N is not being presented as a new structural classification.
- **Zhang**, *Tiling Triangles with 2pi/3 Angles*, arXiv:2512.22696v4: trapezoid constructions and transfers supply sufficient large-scale existence. A sufficient cutoff must not be silently treated as necessary.
- **Harries**, *New constructions, obstructions, and multiplier structure for Erdős Problem 634*, v0.5, 28 August 2026: inspected source `progress634/progress634.tex`, blob `85536aabe013ad393e33985cbfcadbae50722f08`, including the introduction/import ledger, Laurent argument, trapezoid refinement, and multiplier-addition/generator-window results. It already contains R=ceil(a/b)+ceil(b/a), the tail m>=3R, and the same (32,45,67), m=9, N=116640 example. These are explicitly credited in [our addendum](../research/general-spectra/ATTRIBUTION.md). The manuscript also distinguishes certified refutations, one-implementation exhaustion, and conditional forcing. Its fixed-ray finite generator windows do not bound the union over infinitely many tiles.
- **Bonfioli**, `ElVec1o/erdos_634_proof`: the current detailed open-case discussion leaves the attachment of the base-beta forcing scheme to arbitrary tilings unresolved. Broad historical summary claims in the README must not override that explicit dependency. Our prime manuscript remains a candidate, not certified by the other modules.

Relevant primary sources: [Beeson–Zhang](https://arxiv.org/abs/2604.01314v1), [Beeson isosceles](https://arxiv.org/abs/1206.1974v7), [Zhang](https://arxiv.org/abs/2512.22696v4), [Harries source](https://github.com/jphme/math-problems/blob/main/progress634/progress634.tex), [Bonfioli status](https://github.com/ElVec1o/erdos_634_proof).

## Consequence for this repository

The complete N=105 package, necessary spectra, eventual constructions, and squarefree congruence obstructions remain separate claims with their own proof boundaries. This audit supplies **no new full solution**. The N=154 instance (8,7,13) on (91,91,154) remains INCOMPLETE in the included search record.

To finish the structural problem one still needs an exhaustive answer for the surviving small multipliers over all primitive tiles, or a different argument classifying the union of realizable count sets without solving every fixed-tile problem. No finite global exception list has been established here. More length-linear translation-invariant boundary weights alone cannot close the scale-one W/beta instances: the included uniform-reduction note gives formal correct-count boundary witnesses, not geometric tilings.

Historical source hashes refer to the original recovered entries before editorial attribution updates. They are not the current integrity manifest. The current file inventory is `verification/manifest.json` and is checked without rebuilding it during verification.
''')
pth=root/'verification/recovered-source-hashes.json';d=json.loads(pth.read_text());d['uniform_reduction_package_included']=True;d['uniform_source_provenance']='verification/uniform-source-provenance.json';d['scope']='Original recovered source entries before integration and attribution edits; current integrity is verification/manifest.json.';pth.write_text(json.dumps(d,indent=2)+'\n')
put('verification/publication.json', json.dumps({'base_verified_commit':BASE,'all_package_import_run':36760117141,'all_package_import_result':'success','integrated_modules':['legacy','n105','general-spectra','uniform-reduction','c-relations'],'final_main_ci':'Recorded by GitHub Actions on the final commit; this file does not pre-assert its success.','full_problem_solved':False,'external_referee_acceptance':False,'note':'English-only publication. Original source records preserved; attribution addendum credits Harries for the existing 120-degree cutoff and 116640 example.'},indent=2)+'\n')
replace('scripts/build_publication_outputs.py','Rebuild the two publication PDFs','Rebuild the three publication PDFs')
# Keep the bibliography change in the compiled publication as well as its sources.
s=root/'research/general-spectra';(s/'build').mkdir(exist_ok=True)
for _ in range(2):
    with (s/'build/compile.log').open('w') as log:
        subprocess.run(['pdflatex','-interaction=nonstopmode','-halt-on-error','-no-shell-escape','-output-directory=build','paper.tex'],cwd=s,stdout=log,stderr=subprocess.STDOUT,check=True)
(s/'paper.pdf').write_bytes((s/'build/paper.pdf').read_bytes())
subprocess.run(['python3','scripts/build_manifest.py'],cwd=root,check=True)
subprocess.run(['python3','scripts/check_repository.py','--output','audit-output/final-structure.json'],cwd=root,check=True)
after=snapshot();changed=[n for n,h in after.items() if before.get(n)!=h]
record={'base_commit':BASE,'files':[],'deleted_files':sorted(set(before)-set(after))}
for name in sorted(changed):
    data=(root/name).read_bytes();entry={'path':name,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()}
    if a.upload:
        request=urllib.request.Request('https://api.github.com/repos/'+REPO+'/git/blobs',data=json.dumps({'content':base64.b64encode(data).decode(),'encoding':'base64'}).encode(),method='POST',headers={'Authorization':'Bearer '+os.environ['GITHUB_TOKEN'],'Accept':'application/vnd.github+json','X-GitHub-Api-Version':'2022-11-28','Content-Type':'application/json'})
        with urllib.request.urlopen(request,timeout=60) as response:entry['git_blob_sha']=json.load(response)['sha']
    record['files'].append(entry)
out=root/'audit-output';out.mkdir(exist_ok=True);(out/'publication-objects.json').write_text(json.dumps(record,indent=2)+'\n')
subprocess.run(['zip','-q',str(out/'attributed-paper.zip'),'research/general-spectra/paper.pdf'],cwd=root,check=True)
print(json.dumps(record,indent=2))
