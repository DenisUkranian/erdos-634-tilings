// Matrix-free exact endpoint-current propagation on the complete denominator7
// lattice for short-edge heights {-1,0,1}. The equilateral N=135 problem is NOT decided by a bounded direction failure.
#include <algorithm>
#include <array>
#include <chrono>
#include <cstdint>
#include <cstdlib>
#include <deque>
#include <fstream>
#include <iostream>
#include <map>
#include <numeric>
#include <vector>
using namespace std;using Clock=chrono::steady_clock;struct P{int x,y;};P add(P a,P b){return {a.x+b.x,a.y+b.y};}P sub(P a,P b){return {a.x-b.x,a.y-b.y};}P mul(P p,int n){return {p.x*n,p.y*n};}P rot(P p){return {-p.y,p.x+p.y};}int64_t cross(P a,P b){return int64_t(a.x)*b.y-int64_t(a.y)*b.x;}P primitive(P d){int g=gcd(d.x,d.y);d.x/=g;d.y/=g;if(d.x<0||(d.x==0&&d.y<0)){d.x=-d.x;d.y=-d.y;}return d;}
struct Temp{array<P,3>p;int h;array<int,3>dirs;};struct Term{int o,dx,dy,sign,offset;};
int main(int argc,char**argv){auto start=Clock::now();double limit=argc>1?atof(argv[1]):120;string prefix=argc>2?argv[2]:"/tmp/634-full3";int center=argc>3?atoi(argv[3]):0;array<P,3> target=center==0?array<P,3>{{{0,0},{315,0},{0,315}}}:array<P,3>{{{0,0},{360,-225},{225,135}}};
int xmin=target[0].x,xmax=xmin,ymin=target[0].y,ymax=ymin;for(P p:target){xmin=min(xmin,p.x);xmax=max(xmax,p.x);ymin=min(ymin,p.y);ymax=max(ymax,p.y);}int W=xmax-xmin+1,H=ymax-ymin+1;
auto inside=[&](P p){for(int k=0;k<3;k++)if(cross(sub(target[(k+1)%3],target[k]),sub(p,target[k]))<0)return false;return true;};
vector<Temp> temps;map<pair<int,int>,int> dids;vector<P> directions;auto direction=[&](P p){p=primitive(p);auto key=make_pair(p.x,p.y);auto it=dids.find(key);if(it!=dids.end())return it->second;int id=directions.size();directions.push_back(p);dids[key]=id;return id;};
for(int h=-1;h<=1;h++){P u=h==0?P{7,0}:h==1?P{3,5}:P{8,-5};for(int order=0;order<2;order++){P a=mul(u,order?5:3),b=mul(rot(rot(u)),order?3:5);for(int r=0;r<6;r++){Temp t{{P{0,0},a,b},h,{}};for(int k=0;k<3;k++)t.dirs[k]=direction(sub(t.p[(k+1)%3],t.p[k]));temps.push_back(t);a=rot(a);b=rot(b);}}}
const int NT=temps.size(),ND=directions.size(),NP=W*H;vector<vector<Term>> terms(ND);
for(int o=0;o<NT;o++)for(int k=0;k<3;k++)for(int end=0;end<2;end++){P p=temps[o].p[(k+end)%3];terms[temps[o].dirs[k]].push_back({o,-p.x,-p.y,end?-1:1,NT*(-p.y*W-p.x)+o});}
vector<uint8_t> states(size_t(NP)*NT,0),queued(size_t(NP)*ND,0);vector<int8_t> rhs(size_t(NP)*ND,0);deque<int> todo;int valid=0;auto pid=[&](P p){return (p.y-ymin)*W+p.x-xmin;};
for(int k=0;k<3;k++){int d=direction(sub(target[(k+1)%3],target[k]));if(d>=ND){cerr<<"Boundary direction outside templates\n";return 1;}rhs[pid(target[k])*ND+d]++;rhs[pid(target[(k+1)%3])*ND+d]--;}
for(int y=ymin;y<=ymax;y++)for(int x=xmin;x<=xmax;x++){P p{x,y};if(!inside(p))continue;int pi=pid(p);for(int o=0;o<NT;o++)if(inside(add(p,temps[o].p[1]))&&inside(add(p,temps[o].p[2]))){states[size_t(pi)*NT+o]=2;valid++;}for(int d=0;d<ND;d++){todo.push_back(pi*ND+d);queued[pi*ND+d]=1;}}
cerr<<"valid="<<valid<<" points_rectangle="<<NP<<" directions="<<ND<<" rows_initial="<<todo.size()<<"\n";int forced=0,ones=0;uint64_t processed=0;bool conflict=false,incomplete=false;int badrow=-1;vector<int> assignments;assignments.reserve(valid);
while(!todo.empty()){if((processed%100000)==0){double elapsed=chrono::duration<double>(Clock::now()-start).count();if(elapsed>limit){incomplete=true;break;}if(processed%5000000==0)cerr<<"rows="<<processed<<" forced="<<forced<<" queue="<<todo.size()<<" seconds="<<elapsed<<"\n";}
int row=todo.front();todo.pop_front();queued[row]=0;processed++;int pi=row/ND,d=row%ND,x=pi%W+xmin,y=pi/W+ymin,base=pi*NT,lo=0,hi=0;
for(auto t:terms[d]){int ax=x+t.dx,ay=y+t.dy;if(ax<xmin||ax>xmax||ay<ymin||ay>ymax)continue;uint8_t v=states[base+t.offset];if(v==2){if(t.sign>0)hi++;else lo--;}else lo+=t.sign*v,hi+=t.sign*v;}
if(rhs[row]<lo||rhs[row]>hi){conflict=true;badrow=row;break;}
if(rhs[row]==lo||rhs[row]==hi)for(auto t:terms[d]){int ax=x+t.dx,ay=y+t.dy;if(ax<xmin||ax>xmax||ay<ymin||ay>ymax)continue;int v=base+t.offset;if(states[v]!=2)continue;int value=rhs[row]==lo?(t.sign<0):(t.sign>0);states[v]=value;forced++;ones+=value;assignments.push_back(value?v+1:-v-1);int o=v%NT,anchor=v/NT;for(int k=0;k<3;k++)for(int end=0;end<2;end++){P p=temps[o].p[(k+end)%3];int rr=(anchor+p.y*W+p.x)*ND+temps[o].dirs[k];if(!queued[rr]){queued[rr]=1;todo.push_back(rr);}}}
}
double elapsed=chrono::duration<double>(Clock::now()-start).count();cerr<<"DONE forced="<<forced<<" remaining="<<valid-forced<<" ones="<<ones<<" conflict="<<conflict<<" incomplete="<<incomplete<<" elapsed="<<elapsed<<"\n";
ofstream report(prefix+".json");report<<"{\"scope\":\"complete three-height lattice endpoint currents\",\"center_height\":"<<center<<",\"candidate_placements\":"<<valid<<",\"forced\":"<<forced<<",\"remaining\":"<<valid-forced<<",\"ones\":"<<ones<<",\"processed_rows\":"<<processed<<",\"conflict\":"<<(conflict?"true":"false")<<",\"incomplete\":"<<(incomplete?"true":"false")<<",\"bad_row\":"<<badrow<<",\"seconds\":"<<elapsed<<",\"N135_decided\":false}\n";
if(conflict){ofstream trace(prefix+".assignments.bin",ios::binary);trace.write((char*)assignments.data(),assignments.size()*sizeof(int));return 0;}
if(incomplete)return 0;
vector<int> remap(states.size(),-1),selected;int nv=0;for(size_t v=0;v<states.size();v++)if(states[v]==2)remap[v]=nv++;else if(states[v])selected.push_back(v);
ofstream f(prefix+".model.txt");f<<nv<<' '<<selected.size()<<' '<<center<<'\n';for(int v=0;v<(int)states.size();v++)if(states[v]){int o=v%NT,pi=v/NT;f<<remap[v]<<' '<<pi%W+xmin<<' '<<pi/W+ymin<<' '<<o<<' '<<temps[o].h+center<<'\n';}
for(int pi=0;pi<NP;pi++){P p{pi%W+xmin,pi/W+ymin};if(!inside(p))continue;for(int d=0;d<ND;d++){int b=rhs[pi*ND+d];vector<int> ls;for(auto t:terms[d]){int ax=p.x+t.dx,ay=p.y+t.dy;if(ax<xmin||ax>xmax||ay<ymin||ay>ymax)continue;int v=pi*NT+t.offset;if(states[v]==2)ls.push_back(t.sign*(remap[v]+1));else b-=t.sign*states[v];}if(ls.empty()){if(b){cerr<<"Export inconsistency\n";return 1;}continue;}f<<b<<' '<<ls.size();for(int z:ls)f<<' '<<z;f<<'\n';}}
}
