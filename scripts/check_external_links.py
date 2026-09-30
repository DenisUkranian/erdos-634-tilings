#!/usr/bin/env python3
"""Diagnostic HTTP checks. 403/429/timeouts are not treated as mathematical or link failures."""
from concurrent.futures import ThreadPoolExecutor
import argparse,json,re,time,urllib.request,urllib.error
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def check(url):
    headers={'User-Agent':'erdos-634-tilings-publication-audit/0.2.0'}
    try:
        req=urllib.request.Request(url,headers=headers,method='HEAD')
        try:r=urllib.request.urlopen(req,timeout=15)
        except urllib.error.HTTPError as e:
            if e.code not in (405,501):raise
            r=urllib.request.urlopen(urllib.request.Request(url,headers=headers),timeout=15)
        with r:return {'url':url,'status':r.status,'final_url':r.url,'classification':'reachable'}
    except urllib.error.HTTPError as e:return {'url':url,'status':e.code,'classification':'not_found' if e.code in (404,410) else 'blocked_or_other_http'}
    except Exception as e:return {'url':url,'classification':'unverified_network','error':str(e)}

def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--output',type=Path,default=ROOT/'audit-output/external-links.json');args=ap.parse_args()
    urls=set()
    # Canonical source/document links; image badges are not research dependencies.
    for p in ROOT.rglob('*.md'):
        if any(x in {'.git','audit-output','build','.publication'} for x in p.relative_to(ROOT).parts):continue
        urls.update(u.rstrip('.,;') for u in re.findall(r'https?://[^\s<>"\]\)]+',p.read_text()))
    urls={u for u in urls if not any(x in u for x in ('sandbox:','img.shields.io','/badge.svg'))}
    with ThreadPoolExecutor(max_workers=4) as pool:out=list(pool.map(check,sorted(urls)))
    result={'diagnostic_only':True,'checked':len(out),'results':out,'note':'403, rate limiting and timeouts do not establish absence. Results do not validate the mathematics of the linked source.'}
    args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'checked':len(out),'not_found':[x['url'] for x in out if x['classification']=='not_found'],'unverified':sum(x['classification']!='reachable' for x in out)},indent=2))
if __name__=='__main__':main()
