// Exact endpoint-current reduction of a finite supplied placement pool.
// An infeasible pool says NOTHING about completeness or N=154 generally.
#include <algorithm>
#include <array>
#include <cstdint>
#include <cstdlib>
#include <deque>
#include <fstream>
#include <iostream>
#include <numeric>
#include <stdexcept>
#include <vector>
using namespace std;
using L=int64_t;using I=__int128_t;
struct P{L x,y;}; P sub(P a,P b){return {a.x-b.x,a.y-b.y};} I cross(P a,P b){return I(a.x)*b.y-I(a.y)*b.x;}
struct T{array<P,3> p; int source,h,mirror;};
struct E{L dx,dy; I offset;L pos;int var,sign;};
bool lesskey(const E&a,const E&b){if(a.dx!=b.dx)return a.dx<b.dx;if(a.dy!=b.dy)return a.dy<b.dy;if(a.offset!=b.offset)return a.offset<b.offset;return a.pos<b.pos;}
bool eqkey(const E&a,const E&b){return a.dx==b.dx&&a.dy==b.dy&&a.offset==b.offset&&a.pos==b.pos;}
int main(int argc,char**argv){try{
 if(argc<3)throw runtime_error("endpoint_pool geometry.txt output.txt [mirror=1]");bool mirror=argc>3?atoi(argv[3]):true;
 ifstream in(argv[1]);L D;int np,nt;in>>D>>np>>nt;vector<P> pts(np);for(auto&p:pts)in>>p.x>>p.y;vector<T> ts;
 for(int j=0;j<nt;j++){array<int,3> v;int h,g;in>>v[0]>>v[1]>>v[2]>>h>>g;if(abs(h)>4)continue;T t{{pts[v[0]],pts[v[1]],pts[v[2]]},j,h,0};ts.push_back(t);if(mirror){for(P&p:t.p)p={pts[1].x-p.x-p.y,p.y};t.mirror=1;t.h=-h;swap(t.p[1],t.p[2]);ts.push_back(t);}}
 if(!in)throw runtime_error("bad geometry");cerr<<"pool "<<ts.size()<<" placements\n";
 vector<E> events;events.reserve(6*(ts.size()+1));auto insert=[&](P a,P b,int var){P d=sub(b,a);L g=gcd(d.x,d.y);d.x/=g;d.y/=g;int sign=1;if(d.x<0||(d.x==0&&d.y<0)){d.x=-d.x;d.y=-d.y;sign=-1;}I off=cross(d,a);events.push_back({d.x,d.y,off,d.x?a.x:a.y,var,1});events.push_back({d.x,d.y,off,d.x?b.x:b.y,var,-1});};
 for(int j=0;j<(int)ts.size();j++){auto p=ts[j].p;if(cross(sub(p[1],p[0]),sub(p[2],p[0]))<=0)throw runtime_error("orientation");for(int k=0;k<3;k++)insert(p[k],p[(k+1)%3],j);}
 array<P,3> out{{pts[0],pts[1],pts[2]}};for(int k=0;k<3;k++)insert(out[k],out[(k+1)%3],-1);
 sort(events.begin(),events.end(),lesskey);cerr<<"sorted "<<events.size()<<" endpoint entries\n";
 vector<int> starts{0},lits,rhs; vector<array<int,6>> cols(ts.size());vector<int> colcount(ts.size());
 for(size_t a=0;a<events.size();){size_t b=a+1;while(b<events.size()&&eqkey(events[a],events[b]))++b;int r=rhs.size(),bval=0;for(size_t k=a;k<b;k++){auto e=events[k];if(e.var<0)bval+=e.sign;else{lits.push_back(e.sign*(e.var+1));cols[e.var][colcount[e.var]++]=r;}}starts.push_back(lits.size());rhs.push_back(bval);a=b;}
 vector<E>().swap(events);cerr<<"rows "<<rhs.size()<<" entries "<<lits.size()<<"\n";
 vector<int8_t> assignment(ts.size(),-1),queued(rhs.size(),1);deque<int> q;for(int r=0;r<(int)rhs.size();r++)q.push_back(r);int forced=0;bool conflict=false;int badrow=-1;
 auto assign=[&](int v,int x){if(assignment[v]>=0){if(assignment[v]!=x)throw runtime_error("assign conflict");return;}assignment[v]=x;forced++;for(int r:cols[v])if(!queued[r]){queued[r]=1;q.push_back(r);}};
 while(!q.empty()){int r=q.front();q.pop_front();queued[r]=0;int lo=0,hi=0;for(int k=starts[r];k<starts[r+1];k++){int z=lits[k],v=abs(z)-1,s=z>0?1:-1;if(assignment[v]<0){if(s>0)hi++;else lo--;}else lo+=s*assignment[v],hi+=s*assignment[v];}
 if(rhs[r]<lo||rhs[r]>hi){conflict=true;badrow=r;break;}if(rhs[r]==lo||rhs[r]==hi)for(int k=starts[r];k<starts[r+1];k++){int z=lits[k],v=abs(z)-1;if(assignment[v]<0)assign(v,rhs[r]==lo?(z<0):(z>0));}}
 cerr<<"forced "<<forced<<" conflict "<<conflict<<"\n";ofstream report(string(argv[2])+".json");report<<"{\"pool_placements\":"<<ts.size()<<",\"input_placements\":"<<nt<<",\"mirrored\":"<<(mirror?"true":"false")<<",\"rows\":"<<rhs.size()<<",\"nonzeros\":"<<lits.size()<<",\"forced\":"<<forced<<",\"restricted_pool_conflict\":"<<(conflict?"true":"false")<<",\"N154_decided\":false,\"bad_row\":"<<badrow<<"}\n";
 if(conflict)return 0;
 vector<int> remap(ts.size(),-1),selected;int nv=0;for(int v=0;v<(int)ts.size();v++){if(assignment[v]<0)remap[v]=nv++;else if(assignment[v])selected.push_back(v);}ofstream f(argv[2]);f<<nv<<' '<<selected.size()<<'\n';for(int v=0;v<(int)ts.size();v++)if(assignment[v]<0||assignment[v]==1)f<<remap[v]<<' '<<ts[v].source<<' '<<ts[v].mirror<<' '<<ts[v].h<<'\n';
 for(int r=0;r<(int)rhs.size();r++){int b=rhs[r],n=0;for(int k=starts[r];k<starts[r+1];k++){int z=lits[k],v=abs(z)-1;if(assignment[v]<0)n++;else b-=(z>0?1:-1)*assignment[v];}if(!n){if(b)throw runtime_error("late conflict");continue;}f<<b<<' '<<n;for(int k=starts[r];k<starts[r+1];k++){int z=lits[k],v=abs(z)-1;if(assignment[v]<0)f<<' '<<(z>0?1:-1)*(remap[v]+1);}f<<'\n';}
 cerr<<"reduced variables "<<nv<<" selected "<<selected.size()<<"\n";
 }catch(const exception&e){cerr<<e.what()<<'\n';return 1;}}
