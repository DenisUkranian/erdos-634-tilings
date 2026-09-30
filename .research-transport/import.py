from pathlib import Path
import json,lzma,hashlib,sys
HERE=Path(__file__).resolve().parent
root=Path(sys.argv[1]).resolve()
def entries(prefix,count):
    raw=lzma.LZMADecompressor().decompress(b''.join((HERE/f'{prefix}{i:02}').read_bytes() for i in range(count)))
    text=raw.decode('utf8','ignore');pos=text.index('"files":[')+9;dec=json.JSONDecoder();out=[]
    while True:
        try:e,end=dec.raw_decode(text,pos)
        except json.JSONDecodeError:break
        out.append(e);pos=end+1
    return out

def decode(c,dfs=False):
    d=dict(c['data']);nodes=[]
    for i,row in enumerate(d['nodes']):
        n=dict(zip(c['schemas'][row[0]],row[1:]))
        for k,v in list(n.items()):
            if k=='tiles':
                delta,added=v;n[k]=sorted(nodes[i-delta]['tiles']+added) if delta else added
            elif k in ('child','ref'):n[k]=v+i
            elif k=='children':n[k]=[j+i for j in v]
            elif k=='reason':n[k]=c['reasons'][v]
        nodes.append(n)
    if dfs:
        order=d.pop('_order',None)
        if order is None:order=sorted(range(len(nodes)),key=lambda i:(len(nodes[i]['tiles']),nodes[i]['tiles']))
        renumber={old:new for new,old in enumerate(order)};old=nodes;nodes=[]
        for oi in order:
            n=dict(old[oi])
            for k in ('child','ref'):
                if k in n:n[k]=renumber[n[k]]
            if 'children' in n:n['children']=[renumber[j] for j in n['children']]
            nodes.append(n)
    d['nodes']=nodes;return d

def put(path,b):
    p=(root/path).resolve()
    if root not in p.parents or '.git' in p.relative_to(root).parts:raise ValueError('Unsafe path')
    p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b)
old=entries('p',16);new=entries('new',14)
if len(old)!=45 or len(new)!=23:raise ValueError(('Unexpected recovered entry count',len(old),len(new)))
records=[]
for e in old+new:
    b=e['content'].encode() if e['kind']=='text' else (json.dumps(decode(e['content'],e['kind']=='node-dfs-v1'),separators=(',',':'))+'\n').encode()
    if len(b)!=e['bytes'] or hashlib.sha256(b).hexdigest()!=e['sha256']:raise ValueError('Hash mismatch '+e['path'])
    records.append({k:e[k] for k in ('path','bytes','sha256')})
    if e['path']=='README.ru.md' or e['path'].endswith('/RESULT_RU.md'):continue
    put(e['path'],b)
for path,text in json.loads(lzma.decompress((HERE/'utilities.xz').read_bytes())).items():put(path,text.encode())
(root/'README.ru.md').unlink(missing_ok=True)
for p in root.rglob('*.md'):
    if '.git' in p.parts:continue
    t=p.read_text();t=t.replace('[Русское описание](README.ru.md) · ','')
    p.write_text(t)
put('.github/ABOUT.txt',b'Erdos Problem 634 - congruent triangle tilings.\n')
put('verification/recovered-source-hashes.json',(json.dumps({'source_entries_hash_verified':len(records),'entries':records,'excluded_translations':['README.ru.md','RESULT_RU.md'],'source_date':'2026-09-30','uniform_reduction_package_included':False},indent=2)+'\n').encode())
print('RECOVERED_SOURCE_HASHES=PASS',len(records),flush=True)
