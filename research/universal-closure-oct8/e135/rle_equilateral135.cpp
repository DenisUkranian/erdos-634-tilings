// Complete finite lattice endpoint currents for equilateral side45 by (3,5,7).
// For support [L,U] containing0: eta=2+rho, g=eta^L/bar(eta)^U,
// vertices lie in g Z[rho], and unit_h/g=eta^(h-L)bar(eta)^(U-h).
// Two-bit placements; dense scanline point indexing; exact integer propagation.
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
#include <stdexcept>
#include <vector>
using namespace std;using Clock=chrono::steady_clock;using I=int64_t;using UI=uint64_t;
struct P{int x,y;};P add(P a,P b){return {a.x+b.x,a.y+b.y};}P sub(P a,P b){return {a.x-b.x,a.y-b.y};}P mul(P p,int n){return {p.x*n,p.y*n};}P prod(P a,P b){return {a.x*b.x-a.y*b.y,a.x*b.y+a.y*b.x+a.y*b.y};}P power(P p,int n){P r{1,0};for(int i=0;i<n;i++)r=prod(r,p);return r;}P rot(P p){return {-p.y,p.x+p.y};}I cross(P a,P b){return I(a.x)*b.y-I(a.y)*b.x;}P primitive(P d){int g=gcd(d.x,d.y);d.x/=g;d.y/=g;if(d.x<0||(d.x==0&&d.y<0)){d.x=-d.x;d.y=-d.y;}return d;}
I floordiv(I a,I b){I q=a/b,r=a%b;return q-(r<0);}I ceildiv(I a,I b){return -floordiv(-a,b);}
struct Temp{array<P,3>p;int h;array<int,3>dirs;};struct Term{int o,dx,dy,sign;};
struct TwoBits{vector<UI>b;explicit TwoBits(UI n):b((n+31)/32,0){}int get(UI v)const{return (b[v>>5]>>(2*(v&31)))&3;}void set(UI v,int x){UI shift=2*(v&31),&w=b[v>>5];w=(w&~(UI(3)<<shift))|(UI(x)<<shift);}};
struct Bits{vector<UI>b;explicit Bits(UI n):b((n+63)/64,0){}bool get(UI v)const{return (b[v>>6]>>(v&63))&1;}void set(UI v){b[v>>6]|=UI(1)<<(v&63);}void reset(UI v){b[v>>6]&=~(UI(1)<<(v&63));}};

struct Span{int lo,hi;};using Runs=vector<Span>;
UI cardinality(const Runs&a){UI n=0;for(auto s:a)n+=UI(s.hi-s.lo+1);return n;}
void append(Runs&out,int lo,int hi){if(lo>hi)return;if(!out.empty()&&lo<=out.back().hi+1)out.back().hi=max(out.back().hi,hi);else out.push_back({lo,hi});}
void unite(Runs&a,const Runs&b,int shift,Runs&work){work.clear();size_t i=0,j=0;while(i<a.size()||j<b.size()){Span s;if(j==b.size()||(i<a.size()&&a[i].lo<=b[j].lo+shift))s=a[i++];else{s=b[j++];s.lo+=shift;s.hi+=shift;}append(work,s.lo,s.hi);}a.swap(work);}
UI difference(const Runs&a,const Runs&b,int shift,Runs&out){out.clear();size_t j=0;UI deleted=0;for(auto s:a){deleted+=UI(s.hi-s.lo+1);int x=s.lo;while(j<b.size()&&b[j].hi+shift<x)j++;size_t k=j;while(k<b.size()&&b[k].lo+shift<=s.hi){int lo=b[k].lo+shift,hi=b[k].hi+shift;if(lo>x){int end=min(s.hi,lo-1);append(out,x,end);deleted-=UI(end-x+1);}x=max(x,hi+1);if(x>s.hi)break;k++;}if(x<=s.hi){append(out,x,s.hi);deleted-=UI(s.hi-x+1);}}return deleted;}
bool contains(const Runs&a,int x){auto i=lower_bound(a.begin(),a.end(),x,[](Span s,int p){return s.hi<p;});return i!=a.end()&&i->lo<=x;}
void removePoint(Runs&a,int x){auto i=lower_bound(a.begin(),a.end(),x,[](Span s,int p){return s.hi<p;});if(i==a.end()||i->lo>x)return;if(i->lo==i->hi)a.erase(i);else if(x==i->lo)i->lo++;else if(x==i->hi)i->hi--;else{Span tail{x+1,i->hi};i->hi=x-1;a.insert(i+1,tail);}}
int main(int argc,char**argv){try{
if(argc<4)throw runtime_error("full_band_packed L U prefix [seconds=180] [trace=0] [control_scale=0]");int L=atoi(argv[1]),U=atoi(argv[2]);string prefix=argv[3];double limit=argc>4?atof(argv[4]):180;bool saveTrace=argc>5?atoi(argv[5]):false;int control=argc>6?atoi(argv[6]):0;if(L>0||U<0||U<L||U-L>8)throw runtime_error("support outside supported bounds");auto start=Clock::now();auto elapsed=[&](){return chrono::duration<double>(Clock::now()-start).count();};
P invg=prod(power({2,1},-L),power({3,-1},U));int basisRotation=0;UI bestBox=~UI(0);P testInv=invg;for(int r=0;r<6;r++){array<P,3> t{{P{0,0},mul(testInv,45),mul(rot(testInv),45)}};if(control)t={P{0,0},mul(testInv,3*control),mul(rot(rot(testInv)),5*control)};int lx=0,hx=0,ly=0,hy=0;for(P p:t){lx=min(lx,p.x);hx=max(hx,p.x);ly=min(ly,p.y);hy=max(hy,p.y);}UI box=UI((hx-lx+64)/64)*UI(hy-ly+1);if(box<bestBox){bestBox=box;basisRotation=r;}testInv=rot(testInv);}for(int r=0;r<basisRotation;r++)invg=rot(invg);array<P,3> target{{P{0,0},mul(invg,45),mul(rot(invg),45)}};if(control)target={P{0,0},mul(invg,3*control),mul(rot(rot(invg)),5*control)};
int xmin=target[0].x,xmax=xmin,ymin=target[0].y,ymax=ymin;for(P p:target){xmin=min(xmin,p.x);xmax=max(xmax,p.x);ymin=min(ymin,p.y);ymax=max(ymax,p.y);}int H=ymax-ymin+1;vector<int> left(H),right(H);vector<UI> offsets(H+1,0);
for(int yy=0;yy<H;yy++){int y=yy+ymin;I lo=xmin,hi=xmax;for(int k=0;k<3;k++){P a=target[k],d=sub(target[(k+1)%3],a);I num=I(d.x)*(y-a.y)+I(d.y)*a.x;if(d.y>0)hi=min(hi,floordiv(num,d.y));else if(d.y<0)lo=max(lo,ceildiv(-num,-I(d.y)));else if(num<0)hi=lo-1;}left[yy]=lo;right[yy]=hi;offsets[yy+1]=offsets[yy]+max(I(0),hi-lo+1);}
UI NP=offsets.back();auto point=[&](int x,int yy)->I{if(yy<0||yy>=H||x<left[yy]||x>right[yy])return -1;return offsets[yy]+x-left[yy];};
vector<Temp> temps;map<pair<int,int>,int> dids;vector<P> directions;auto direction=[&](P p){p=primitive(p);auto key=make_pair(p.x,p.y);auto it=dids.find(key);if(it!=dids.end())return it->second;int id=directions.size();directions.push_back(p);dids[key]=id;return id;};
for(int h=L;h<=U;h++){P u=prod(power({2,1},h-L),power({3,-1},U-h));for(int r=0;r<basisRotation;r++)u=rot(u);for(int order=0;order<2;order++){P a=mul(u,order?5:3),b=mul(rot(rot(u)),order?3:5);for(int r=0;r<6;r++){Temp t{{P{0,0},a,b},h,{}};for(int k=0;k<3;k++)t.dirs[k]=direction(sub(t.p[(k+1)%3],t.p[k]));temps.push_back(t);a=rot(a);b=rot(b);}}}
int NT=temps.size(),ND=directions.size();UI NR=NP*ND,NV=NP*NT;vector<vector<Term>> terms(ND);for(int o=0;o<NT;o++)for(int k=0;k<3;k++)for(int end=0;end<2;end++){P p=temps[o].p[(k+end)%3];terms[temps[o].dirs[k]].push_back({o,-p.x,-p.y,end?-1:1});}
array<UI,3> corners;array<int,3> bd;for(int k=0;k<3;k++){corners[k]=point(target[k].x,target[k].y-ymin);bd[k]=direction(sub(target[(k+1)%3],target[k]));if(bd[k]>=ND)throw runtime_error("unsupported boundary direction");}
auto rhs=[&](UI p,int d){int b=0;for(int k=0;k<3;k++){if(p==corners[k]&&d==bd[k])b++;if(p==corners[(k+1)%3]&&d==bd[k])b--;}return b;};
cerr<<"band=["<<L<<","<<U<<"] points="<<NP<<" variables_before_containment="<<NV<<" rows="<<NR<<" state_MB="<<NV/4/1000000<<"\n";


vector<Runs> rows(size_t(NT)*H);UI valid=0,totalRuns=0,maxRuns=0;
for(int o=0;o<NT;o++)for(int y=0;y<H;y++){int lo=left[y],hi=right[y];for(int k=1;k<3;k++){P v=temps[o].p[k];int yy=y+v.y;if(yy<0||yy>=H){hi=lo-1;break;}lo=max(lo,left[yy]-v.x);hi=min(hi,right[yy]-v.x);}if(lo>hi)continue;valid+=UI(hi-lo+1);rows[size_t(o)*H+y].push_back({lo,hi});totalRuns++;}maxRuns=totalRuns;
cerr<<"RLE contained="<<valid<<" initial_runs="<<totalRuns<<" row_objects="<<rows.size()<<" initialization="<<elapsed()<<"\n";
struct Special{int y,x,b;};vector<vector<Special>> special(ND);for(int k=0;k<3;k++)for(int end=0;end<2;end++){P p=target[(k+end)%3];special[bd[k]].push_back({p.y-ymin,p.x,end?-1:1});}
ofstream trace;if(saveTrace)trace.open(prefix+".rle_trace.bin",ios::binary);UI removed=0,traceRecords=0;int passes=0;bool conflict=false,incomplete=false;int badD=-1,badY=-1,badX=-1;UI before;Runs pos,neg,work,badP,badN,eraseWork;
do{before=removed;passes++;for(int d=0;d<ND&&!conflict&&!incomplete;d++)for(int y=0;y<H&&!conflict&&!incomplete;y++){if(y%128==0&&elapsed()>limit){incomplete=true;break;}pos.clear();neg.clear();for(auto t:terms[d]){int yy=y+t.dy;if(yy<0||yy>=H)continue;const auto&r=rows[size_t(t.o)*H+yy];if(!r.empty())unite(t.sign>0?pos:neg,r,-t.dx,work);}difference(pos,neg,0,badP);difference(neg,pos,0,badN);for(auto s:special[d])if(s.y==y){if(!contains(s.b>0?pos:neg,s.x)){conflict=true;badD=d;badY=y;badX=s.x;break;}removePoint(badP,s.x);removePoint(badN,s.x);}if(conflict)break;if(badP.empty()&&badN.empty())continue;
for(int sign:{1,-1})for(auto r:sign>0?badP:badN){if(saveTrace){array<int32_t,5>record{{d,y,r.lo,r.hi,sign}};trace.write((char*)record.data(),sizeof(record));}traceRecords++;}
for(auto t:terms[d]){int yy=y+t.dy;if(yy<0||yy>=H)continue;auto&r=rows[size_t(t.o)*H+yy];const auto&bad=t.sign>0?badP:badN;if(r.empty()||bad.empty())continue;UI deleted=difference(r,bad,t.dx,eraseWork);if(deleted){removed+=deleted;totalRuns-=r.size();r.swap(eraseWork);totalRuns+=r.size();maxRuns=max(maxRuns,totalRuns);}}
}
cerr<<"pass="<<passes<<" removed="<<removed<<" remaining="<<valid-removed<<" runs="<<totalRuns<<" max_runs="<<maxRuns<<" seconds="<<elapsed()<<"\n";}while(removed>before&&!conflict&&!incomplete);
if(trace)trace.close();ofstream report(prefix+".json");report<<"{\"scope\":\"complete band lattice run-length zero support propagation\",\"L\":"<<L<<",\"U\":"<<U<<",\"control_scale\":"<<control<<",\"basis_rotation\":"<<basisRotation<<",\"candidate_placements\":"<<valid<<",\"removed\":"<<removed<<",\"remaining\":"<<valid-removed<<",\"passes\":"<<passes<<",\"trace_records\":"<<traceRecords<<",\"remaining_runs\":"<<totalRuns<<",\"max_runs\":"<<maxRuns<<",\"conflict\":"<<(conflict?"true":"false")<<",\"incomplete\":"<<(incomplete?"true":"false")<<",\"bad_direction\":"<<badD<<",\"bad_y\":"<<badY<<",\"bad_x\":"<<badX<<",\"seconds\":"<<elapsed()<<",\"equilateral_135_decided\":false}\n";
if(!conflict&&!incomplete){ofstream geom(prefix+".remaining.txt");geom<<L<<' '<<U<<' '<<valid-removed<<'\n';for(int o=0;o<NT;o++)for(int y=0;y<H;y++)for(auto s:rows[size_t(o)*H+y])for(int x=s.lo;x<=s.hi;x++)geom<<o<<' '<<x<<' '<<y+ymin<<'\n';}
}catch(const exception&e){cerr<<"ERROR "<<e.what()<<'\n';return 1;}}
