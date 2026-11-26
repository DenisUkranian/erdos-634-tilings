"""Slow independent finite proof. The join key uses exact integers and no fingerprints."""
from collections import Counter
import subprocess
from tempfile import TemporaryDirectory
from pathlib import Path
from terminal import HERE,UNITS,add,scale,word_from_codes,width_obstruction


def exact_endpoint_test(a,b,c,word):
    for modulus in (a,b):
        rows=Counter()
        p=(0,0)
        for token in word:
            j=token%6
            pieces=[(j,a),((j-1)%6,b)] if token<6 else [(j,c)]
            for k,length in pieces:
                q=add(p,scale(length,UNITS[k]))
                rows[k%3,p[0]%modulus,p[1]%modulus]-=1
                rows[k%3,q[0]%modulus,q[1]%modulus]+=1
                p=q
        if any(rows.values()):
            return False
    return True


def run():
    with TemporaryDirectory() as tmp:
        binary=str(Path(tmp)/"area_review")
        subprocess.run(["c++","-O3","-std=c++17",str(HERE/"area_review.cpp"),"-o",binary],check=True)
        for a,b,c,depths in [(33,7,37,(5,6,7)),(35,13,43,(6,7))]:
            for r in depths:
                candidates=0
                for multiple in (2,4):
                    run=subprocess.run([binary,*map(str,(a,b,c,r,multiple))],
                                       check=True,text=True,capture_output=True)
                    for line in run.stdout.splitlines():
                        left,right=map(int,line.split())
                        word=word_from_codes(left,right,r)
                        if word[-1]<6 or any(u//6==v//6 and (u-v)%6==3
                                             for u,v in zip(word,word[1:]+word[:1])):
                            continue
                        if exact_endpoint_test(a,b,c,word):
                            candidates+=1
                            assert width_obstruction(a,b,c,word)
                assert candidates==(44 if (c,r)==(37,7) else 0)
                print("Independent integer join:",c,2*r,candidates,flush=True)


if __name__=="__main__":
    run()
