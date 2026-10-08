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
int main(int argc,char**argv){try{
if(argc<4)throw runtime_error("full_band_packed L U prefix [seconds=180] [trace=0] [control_scale=0]");int L=atoi(argv[1]),U=atoi(argv[2]);string prefix=argv[3];double limit=argc>4?atof(argv[4]):180;bool saveTrace=argc>5?atoi(argv[5]):false;int control=argc>6?atoi(argv[6]):0;if(L>0||U<0||U<L||U-L>6)throw runtime_error("support outside supported bounds");auto start=Clock::now();auto elapsed=[&](){return chrono::duration<double>(Clock::now()-start).count();};
P invg=prod(power({2,1},-L),power({3,-1},U));int basisRotation=0;UI bestBox=~UI(0);P testInv=invg;for(int r=0;r<6;r++){array<P,3> t{{P{0,0},mul(testInv,45),mul(rot(testInv),45)}};if(control)t={P{0,0},mul(testInv,3*control),mul(rot(rot(testInv)),5*control)};int lx=0,hx=0,ly=0,hy=0;for(P p:t){lx=min(lx,p.x);hx=max(hx,p.x);ly=min(ly,p.y);hy=max(hy,p.y);}UI box=UI((hx-lx+64)/64)*UI(hy-ly+1);if(box<bestBox){bestBox=box;basisRotation=r;}testInv=rot(testInv);}for(int r=0;r<basisRotation;r++)invg=rot(invg);array<P,3> target{{P{0,0},mul(invg,45),mul(rot(invg),45)}};if(control)target={P{0,0},mul(invg,3*control),mul(rot(rot(invg)),5*control)};
int xmin=target[0].x,xmax=xmin,ymin=target[0].y,ymax=ymin;for(P p:target){xmin=min(xmin,p.x);xmax=max(xmax,p.x);ymin=min(ymin,p.y);ymax=max(ymax,p.y);}int H=ymax-ymin+1;if(H>65535)throw runtime_error("y index exceeds uint16");vector<int> left(H),right(H);vector<UI> offsets(H+1,0);
for(int yy=0;yy<H;yy++){int y=yy+ymin;I lo=xmin,hi=xmax;for(int k=0;k<3;k++){P a=target[k],d=sub(target[(k+1)%3],a);I num=I(d.x)*(y-a.y)+I(d.y)*a.x;if(d.y>0)hi=min(hi,floordiv(num,d.y));else if(d.y<0)lo=max(lo,ceildiv(-num,-I(d.y)));else if(num<0)hi=lo-1;}left[yy]=lo;right[yy]=hi;offsets[yy+1]=offsets[yy]+max(I(0),hi-lo+1);}
UI NP=offsets.back();auto point=[&](int x,int yy)->I{if(yy<0||yy>=H||x<left[yy]||x>right[yy])return -1;return offsets[yy]+x-left[yy];};
vector<Temp> temps;map<pair<int,int>,int> dids;vector<P> directions;auto direction=[&](P p){p=primitive(p);auto key=make_pair(p.x,p.y);auto it=dids.find(key);if(it!=dids.end())return it->second;int id=directions.size();directions.push_back(p);dids[key]=id;return id;};
for(int h=L;h<=U;h++){P u=prod(power({2,1},h-L),power({3,-1},U-h));for(int r=0;r<basisRotation;r++)u=rot(u);for(int order=0;order<2;order++){P a=mul(u,order?5:3),b=mul(rot(rot(u)),order?3:5);for(int r=0;r<6;r++){Temp t{{P{0,0},a,b},h,{}};for(int k=0;k<3;k++)t.dirs[k]=direction(sub(t.p[(k+1)%3],t.p[k]));temps.push_back(t);a=rot(a);b=rot(b);}}}
int NT=temps.size(),ND=directions.size();UI NR=NP*ND,NV=NP*NT;if(NR>UINT32_MAX)throw runtime_error("row index exceeds uint32");vector<vector<Term>> terms(ND);for(int o=0;o<NT;o++)for(int k=0;k<3;k++)for(int end=0;end<2;end++){P p=temps[o].p[(k+end)%3];terms[temps[o].dirs[k]].push_back({o,-p.x,-p.y,end?-1:1});}
array<UI,3> corners;array<int,3> bd;for(int k=0;k<3;k++){corners[k]=point(target[k].x,target[k].y-ymin);bd[k]=direction(sub(target[(k+1)%3],target[k]));if(bd[k]>=ND)throw runtime_error("unsupported boundary direction");}
auto rhs=[&](UI p,int d){int b=0;for(int k=0;k<3;k++){if(p==corners[k]&&d==bd[k])b++;if(p==corners[(k+1)%3]&&d==bd[k])b--;}return b;};
cerr<<"band=["<<L<<","<<U<<"] points="<<NP<<" variables_before_containment="<<NV<<" rows="<<NR<<" state_MB="<<NV/4/1000000<<"\n";

const int WP=(xmax-xmin+64)/64;const size_t NW=size_t(H)*WP;vector<vector<UI>> bitmap(NT,vector<UI>(NW,0));UI valid=0;
for(int o=0;o<NT;o++)for(int y=0;y<H;y++){int lo=left[y],hi=right[y];for(int k=1;k<3;k++){P v=temps[o].p[k];int yy=y+v.y;if(yy<0||yy>=H){hi=lo-1;break;}lo=max(lo,left[yy]-v.x);hi=min(hi,right[yy]-v.x);}if(lo>hi)continue;valid+=hi-lo+1;int a=lo-xmin,b=hi-xmin,wa=a/64,wb=b/64;UI low=~UI(0)<<(a%64),high=~UI(0)>>(63-b%64);if(wa==wb)bitmap[o][size_t(y)*WP+wa]=low&high;else{bitmap[o][size_t(y)*WP+wa]=low;for(int w=wa+1;w<wb;w++)bitmap[o][size_t(y)*WP+w]=~UI(0);bitmap[o][size_t(y)*WP+wb]=high;}}
cerr<<"bitmap contained="<<valid<<" MB="<<UI(NW)*NT*8/1000000<<" initialization="<<elapsed()<<"\n";
struct ShiftTerm{int o,dy,q,k,sign;};vector<vector<ShiftTerm>> shifts(ND);for(int d=0;d<ND;d++)for(auto t:terms[d]){int q=int(floordiv(t.dx,64)),k=t.dx-64*q;shifts[d].push_back({t.o,t.dy,q,k,t.sign});}
auto read=[&](const ShiftTerm&t,int y,int w)->UI{int yy=y+t.dy,ww=w+t.q;if(yy<0||yy>=H)return 0;UI a=ww>=0&&ww<WP?bitmap[t.o][size_t(yy)*WP+ww]:0;if(!t.k)return a;UI b=ww+1>=0&&ww+1<WP?bitmap[t.o][size_t(yy)*WP+ww+1]:0;return (a>>t.k)|(b<<(64-t.k));};
auto erase=[&](const ShiftTerm&t,int y,int w,UI mask)->UI{if(!mask)return 0;int yy=y+t.dy,ww=w+t.q;if(yy<0||yy>=H)return 0;UI deleted=0;if(ww>=0&&ww<WP){UI&m=bitmap[t.o][size_t(yy)*WP+ww],cut=mask<<t.k;deleted+=__builtin_popcountll(m&cut);m&=~cut;}if(t.k&&ww+1>=0&&ww+1<WP){UI&m=bitmap[t.o][size_t(yy)*WP+ww+1],cut=mask>>(64-t.k);deleted+=__builtin_popcountll(m&cut);m&=~cut;}return deleted;};
struct Special{int y,w,b;UI mask;};vector<vector<Special>> special(ND);for(int k=0;k<3;k++)for(int end=0;end<2;end++){P p=target[(k+end)%3];int xx=p.x-xmin;special[bd[k]].push_back({p.y-ymin,xx/64,end?-1:1,UI(1)<<(xx%64)});}
ofstream trace;if(saveTrace)trace.open(prefix+".bitmap_trace.bin",ios::binary);UI removed=0,traceRecords=0;int passes=0;bool conflict=false,incomplete=false;int badD=-1,badY=-1,badW=-1;UI badMask=0;UI before;
do{before=removed;passes++;for(int d=0;d<ND&&!conflict&&!incomplete;d++)for(int y=0;y<H&&!conflict&&!incomplete;y++){if(y%128==0&&elapsed()>limit){incomplete=true;break;}for(int w=0;w<WP;w++){UI pos=0,neg=0;for(auto t:shifts[d]){UI v=read(t,y,w);if(t.sign>0)pos|=v;else neg|=v;}UI badP=pos&~neg,badN=neg&~pos;for(auto s:special[d])if(s.y==y&&s.w==w){if((s.b>0?pos:neg)&s.mask){badP&=~s.mask;badN&=~s.mask;}else{conflict=true;badD=d;badY=y;badW=w;badMask=s.mask;break;}}if(conflict)break;if(!badP&&!badN)continue;if(saveTrace){uint32_t dd=d,yy=y,ww=w;trace.write((char*)&dd,4);trace.write((char*)&yy,4);trace.write((char*)&ww,4);trace.write((char*)&badP,8);trace.write((char*)&badN,8);}traceRecords++;for(auto t:shifts[d])removed+=erase(t,y,w,t.sign>0?badP:badN);}}
cerr<<"pass="<<passes<<" removed="<<removed<<" remaining="<<valid-removed<<" seconds="<<elapsed()<<"\n";}while(removed>before&&!conflict&&!incomplete);
if(trace)trace.close();ofstream report(prefix+".json");report<<"{\"scope\":\"complete band lattice zero support propagation\",\"L\":"<<L<<",\"U\":"<<U<<",\"control_scale\":"<<control<<",\"basis_rotation\":"<<basisRotation<<",\"candidate_placements\":"<<valid<<",\"removed\":"<<removed<<",\"remaining\":"<<valid-removed<<",\"passes\":"<<passes<<",\"trace_records\":"<<traceRecords<<",\"conflict\":"<<(conflict?"true":"false")<<",\"incomplete\":"<<(incomplete?"true":"false")<<",\"bad_direction\":"<<badD<<",\"bad_y\":"<<badY<<",\"bad_word\":"<<badW<<",\"bad_mask\":"<<badMask<<",\"seconds\":"<<elapsed()<<",\"equilateral_135_decided\":false}\n";
if(!conflict&&!incomplete){ofstream geom(prefix+".remaining.txt");geom<<L<<' '<<U<<' '<<valid-removed<<'\n';for(int o=0;o<NT;o++)for(int y=0;y<H;y++)for(int w=0;w<WP;w++){UI v=bitmap[o][size_t(y)*WP+w];while(v){int bit=__builtin_ctzll(v);v&=v-1;geom<<o<<' '<<xmin+64*w+bit<<' '<<y+ymin<<'\n';}}}
}catch(const exception&e){cerr<<"ERROR "<<e.what()<<'\n';return 1;}}
