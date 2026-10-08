// Complete finite lattice endpoint currents for (8,7,13) tilings of (91,91,154).
// For support [L,U] containing0: eta=3+rho, g=eta^L/bar(eta)^U,
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
int main(int argc,char**argv){try{
if(argc<4)throw runtime_error("full_band_packed L U prefix [seconds=180] [trace=0] [control_scale=0]");int L=atoi(argv[1]),U=atoi(argv[2]);string prefix=argv[3];double limit=argc>4?atof(argv[4]):180;bool saveTrace=argc>5?atoi(argv[5]):false;int control=argc>6?atoi(argv[6]):0;if(L>0||U<0||U<L||U-L>4)throw runtime_error("support outside supported bounds");auto start=Clock::now();auto elapsed=[&](){return chrono::duration<double>(Clock::now()-start).count();};
P invg=prod(power({3,1},-L),power({4,-1},U));array<P,3> target{{P{0,0},mul(invg,154),prod(invg,{49,56})}};if(control)target={P{0,0},mul(invg,8*control),mul(rot(rot(invg)),7*control)};
int xmin=target[0].x,xmax=xmin,ymin=target[0].y,ymax=ymin;for(P p:target){xmin=min(xmin,p.x);xmax=max(xmax,p.x);ymin=min(ymin,p.y);ymax=max(ymax,p.y);}int H=ymax-ymin+1;if(H>65535)throw runtime_error("y index exceeds uint16");vector<int> left(H),right(H);vector<UI> offsets(H+1,0);
for(int yy=0;yy<H;yy++){int y=yy+ymin;I lo=xmin,hi=xmax;for(int k=0;k<3;k++){P a=target[k],d=sub(target[(k+1)%3],a);I num=I(d.x)*(y-a.y)+I(d.y)*a.x;if(d.y>0)hi=min(hi,floordiv(num,d.y));else if(d.y<0)lo=max(lo,ceildiv(-num,-I(d.y)));else if(num<0)hi=lo-1;}left[yy]=lo;right[yy]=hi;offsets[yy+1]=offsets[yy]+max(I(0),hi-lo+1);}
UI NP=offsets.back();auto point=[&](int x,int yy)->I{if(yy<0||yy>=H||x<left[yy]||x>right[yy])return -1;return offsets[yy]+x-left[yy];};vector<uint16_t> yof(NP);for(int yy=0;yy<H;yy++)fill(yof.begin()+offsets[yy],yof.begin()+offsets[yy+1],uint16_t(yy));
vector<Temp> temps;map<pair<int,int>,int> dids;vector<P> directions;auto direction=[&](P p){p=primitive(p);auto key=make_pair(p.x,p.y);auto it=dids.find(key);if(it!=dids.end())return it->second;int id=directions.size();directions.push_back(p);dids[key]=id;return id;};
for(int h=L;h<=U;h++){P u=prod(power({3,1},h-L),power({4,-1},U-h));for(int order=0;order<2;order++){P a=mul(u,order?7:8),b=mul(rot(rot(u)),order?8:7);for(int r=0;r<6;r++){Temp t{{P{0,0},a,b},h,{}};for(int k=0;k<3;k++)t.dirs[k]=direction(sub(t.p[(k+1)%3],t.p[k]));temps.push_back(t);a=rot(a);b=rot(b);}}}
int NT=temps.size(),ND=directions.size();UI NR=NP*ND,NV=NP*NT;if(NR>UINT32_MAX)throw runtime_error("row index exceeds uint32");vector<vector<Term>> terms(ND);for(int o=0;o<NT;o++)for(int k=0;k<3;k++)for(int end=0;end<2;end++){P p=temps[o].p[(k+end)%3];terms[temps[o].dirs[k]].push_back({o,-p.x,-p.y,end?-1:1});}
array<UI,3> corners;array<int,3> bd;for(int k=0;k<3;k++){corners[k]=point(target[k].x,target[k].y-ymin);bd[k]=direction(sub(target[(k+1)%3],target[k]));if(bd[k]>=ND)throw runtime_error("unsupported boundary direction");}
auto rhs=[&](UI p,int d){int b=0;for(int k=0;k<3;k++){if(p==corners[k]&&d==bd[k])b++;if(p==corners[(k+1)%3]&&d==bd[k])b--;}return b;};
cerr<<"band=["<<L<<","<<U<<"] points="<<NP<<" variables_before_containment="<<NV<<" rows="<<NR<<" state_MB="<<NV/4/1000000<<"\n";
TwoBits states(NV);Bits queued(NR);deque<uint32_t> todo;UI valid=0;for(int yy=0;yy<H;yy++)for(int x=left[yy];x<=right[yy];x++){UI pi=offsets[yy]+x-left[yy];for(int o=0;o<NT;o++)if(point(x+temps[o].p[1].x,yy+temps[o].p[1].y)>=0&&point(x+temps[o].p[2].x,yy+temps[o].p[2].y)>=0){states.set(pi*NT+o,2);valid++;}}
cerr<<"contained="<<valid<<" initial_seconds="<<elapsed()<<"\n";UI forced=0,ones=0,processed=0,maxQueue=0,traceRows=0;bool conflict=false,incomplete=false;uint32_t badrow=0;ofstream trace;if(saveTrace)trace.open(prefix+".rows.bin",ios::binary);
auto process=[&](uint32_t row){processed++;UI pi=row/ND;int d=row%ND,yy=yof[pi],x=left[yy]+pi-offsets[yy];int lo=0,hi=0,b=rhs(pi,d);for(auto t:terms[d]){I anchor=point(x+t.dx,yy+t.dy);if(anchor<0)continue;int v=states.get(UI(anchor)*NT+t.o);if(v==2){if(t.sign>0)hi++;else lo--;}else lo+=t.sign*v,hi+=t.sign*v;}if(b<lo||b>hi){conflict=true;badrow=row;return;}if(b!=lo&&b!=hi)return;bool wrote=false;
for(auto t:terms[d]){I anchor=point(x+t.dx,yy+t.dy);if(anchor<0)continue;UI var=UI(anchor)*NT+t.o;if(states.get(var)!=2)continue;if(!wrote){if(saveTrace)trace.write((char*)&row,sizeof(row));traceRows++;wrote=true;}int value=b==lo?(t.sign<0):(t.sign>0);states.set(var,value);forced++;ones+=value;for(int k=0;k<3;k++)for(int end=0;end<2;end++){P v=temps[t.o].p[(k+end)%3];I pp=point(x+t.dx+v.x,yy+t.dy+v.y);if(pp<0)throw runtime_error("assigned invalid tile");UI rr=UI(pp)*ND+temps[t.o].dirs[k];if(!queued.get(rr)){queued.set(rr);todo.push_back(uint32_t(rr));}}}maxQueue=max<UI>(maxQueue,todo.size());};
UI scanrow=0;while((scanrow<NR||!todo.empty())&&!conflict){if(processed%1000000==0){if(elapsed()>limit){incomplete=true;break;}if(processed%10000000==0)cerr<<"rows="<<processed<<" scan="<<scanrow<<" forced="<<forced<<" queue="<<todo.size()<<" seconds="<<elapsed()<<"\n";}
if(scanrow<NR)process(uint32_t(scanrow++));else{uint32_t row=todo.front();todo.pop_front();queued.reset(row);process(row);}}
if(trace)trace.close();cerr<<"DONE forced="<<forced<<" remaining="<<valid-forced<<" ones="<<ones<<" conflict="<<conflict<<" incomplete="<<incomplete<<" seconds="<<elapsed()<<"\n";
ofstream report(prefix+".json");report<<"{\"scope\":\"complete band lattice endpoint currents\",\"L\":"<<L<<",\"U\":"<<U<<",\"control_scale\":"<<control<<",\"points\":"<<NP<<",\"variables_before_containment\":"<<NV<<",\"candidate_placements\":"<<valid<<",\"forced\":"<<forced<<",\"remaining\":"<<valid-forced<<",\"ones\":"<<ones<<",\"processed_rows\":"<<processed<<",\"scan_rows\":"<<scanrow<<",\"maximum_queue\":"<<maxQueue<<",\"forcing_rows\":"<<traceRows<<",\"conflict\":"<<(conflict?"true":"false")<<",\"incomplete\":"<<(incomplete?"true":"false")<<",\"bad_row\":"<<badrow<<",\"seconds\":"<<elapsed()<<",\"N154_decided\":false}\n";
}catch(const exception&e){cerr<<"ERROR "<<e.what()<<'\n';return 1;}}
