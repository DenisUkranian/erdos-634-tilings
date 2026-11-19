// Reverse dependency extraction for the equilateral (33,7,37) proof.
#include <algorithm>
#include <array>
#include <cstdint>
#include <cstdlib>
#include <fstream>
#include <iostream>
#include <map>
#include <numeric>
#include <stdexcept>
#include <vector>
#include <sys/mman.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>
using namespace std;using I=int64_t;using UI=uint64_t;
struct P{int x,y;};P add(P a,P b){return {a.x+b.x,a.y+b.y};}P sub(P a,P b){return {a.x-b.x,a.y-b.y};}P mul(P p,int n){return {p.x*n,p.y*n};}P prod(P a,P b){return {a.x*b.x-a.y*b.y,a.x*b.y+a.y*b.x+a.y*b.y};}P power(P p,int n){P r{1,0};for(int i=0;i<n;i++)r=prod(r,p);return r;}P rot(P p){return {-p.y,p.x+p.y};}I cross(P a,P b){return I(a.x)*b.y-I(a.y)*b.x;}P primitive(P d){int g=gcd(d.x,d.y);d.x/=g;d.y/=g;if(d.x<0||(d.x==0&&d.y<0)){d.x=-d.x;d.y=-d.y;}return d;}
I floordiv(I a,I b){I q=a/b,r=a%b;return q-(r<0);}I ceildiv(I a,I b){return -floordiv(-a,b);}
struct Temp{array<P,3>p;int h;array<int,3>dirs;};struct Term{int o,dx,dy,sign;};
int main(int argc,char**argv){try{
if(argc!=7)throw runtime_error("L U trace_prefix root_direction_index root_y_index root_word");
int L=atoi(argv[1]),U=atoi(argv[2]);string prefix=argv[3];
if(!((L==0&&U==2)||(L==-1&&U==1)))throw runtime_error("unsupported band");
P invg=prod(power({7,-3},-L),power({4,3},U));array<P,3> target{{P{0,0},mul(invg,231),prod(invg,{0,231})}};
int xmin=target[0].x,xmax=xmin,ymin=target[0].y,ymax=ymin;for(P p:target){xmin=min(xmin,p.x);xmax=max(xmax,p.x);ymin=min(ymin,p.y);ymax=max(ymax,p.y);}int H=ymax-ymin+1;if(H>65535)throw runtime_error("y index exceeds uint16");vector<int> left(H),right(H);vector<UI> offsets(H+1,0);
for(int yy=0;yy<H;yy++){int y=yy+ymin;I lo=xmin,hi=xmax;for(int k=0;k<3;k++){P a=target[k],d=sub(target[(k+1)%3],a);I num=I(d.x)*(y-a.y)+I(d.y)*a.x;if(d.y>0)hi=min(hi,floordiv(num,d.y));else if(d.y<0)lo=max(lo,ceildiv(-num,-I(d.y)));else if(num<0)hi=lo-1;}left[yy]=lo;right[yy]=hi;offsets[yy+1]=offsets[yy]+max(I(0),hi-lo+1);}
UI NP=offsets.back();auto point=[&](int x,int yy)->I{if(yy<0||yy>=H||x<left[yy]||x>right[yy])return -1;return offsets[yy]+x-left[yy];};
vector<Temp> temps;map<pair<int,int>,int> dids;vector<P> directions;auto direction=[&](P p){p=primitive(p);auto key=make_pair(p.x,p.y);auto it=dids.find(key);if(it!=dids.end())return it->second;int id=directions.size();directions.push_back(p);dids[key]=id;return id;};
for(int h=L;h<=U;h++){P u=prod(power({7,-3},h-L),power({4,3},U-h));for(int order=0;order<2;order++){P a=mul(u,order?7:33),b=mul(rot(rot(u)),order?33:7);for(int r=0;r<6;r++){Temp t{{P{0,0},a,b},h,{}};for(int k=0;k<3;k++)t.dirs[k]=direction(sub(t.p[(k+1)%3],t.p[k]));temps.push_back(t);a=rot(a);b=rot(b);}}}
int NT=temps.size(),ND=directions.size();UI NR=NP*ND,NV=NP*NT;vector<vector<Term>> terms(ND);for(int o=0;o<NT;o++)for(int k=0;k<3;k++)for(int end=0;end<2;end++){P p=temps[o].p[(k+end)%3];terms[temps[o].dirs[k]].push_back({o,-p.x,-p.y,end?-1:1});}
array<UI,3> corners;array<int,3> bd;for(int k=0;k<3;k++){corners[k]=point(target[k].x,target[k].y-ymin);bd[k]=direction(sub(target[(k+1)%3],target[k]));if(bd[k]>=ND)throw runtime_error("unsupported boundary direction");}
auto rhs=[&](UI p,int d){int b=0;for(int k=0;k<3;k++){if(p==corners[k]&&d==bd[k])b++;if(p==corners[(k+1)%3]&&d==bd[k])b--;}return b;};
cerr<<"band=["<<L<<","<<U<<"] points="<<NP<<" variables_before_containment="<<NV<<" rows="<<NR<<" state_MB="<<NV/4/1000000<<"\n";

const int WP=(xmax-xmin+64)/64;const size_t NW=size_t(H)*WP;vector<vector<UI>> bitmap(NT,vector<UI>(NW,0));
struct Range{int lo,hi;};vector<vector<Range>> validRanges(NT,vector<Range>(H));
for(int o=0;o<NT;o++)for(int y=0;y<H;y++){
 int lo=left[y],hi=right[y];for(int k=1;k<3;k++){P v=temps[o].p[k];int yy=y+v.y;if(yy<0||yy>=H){hi=lo-1;break;}lo=max(lo,left[yy]-v.x);hi=min(hi,right[yy]-v.x);}
 validRanges[o][y]={lo-xmin,hi-xmin};}
struct ShiftTerm{int o,dy,q,k,sign;};vector<vector<ShiftTerm>> shifts(ND);for(int d=0;d<ND;d++)for(auto t:terms[d]){int q=int(floordiv(t.dx,64)),k=t.dx-64*q;shifts[d].push_back({t.o,t.dy,q,k,t.sign});}
auto read=[&](const ShiftTerm&t,int y,int w)->UI{int yy=y+t.dy,ww=w+t.q;if(yy<0||yy>=H)return 0;UI a=ww>=0&&ww<WP?bitmap[t.o][size_t(yy)*WP+ww]:0;if(!t.k)return a;UI b=ww+1>=0&&ww+1<WP?bitmap[t.o][size_t(yy)*WP+ww+1]:0;return (a>>t.k)|(b<<(64-t.k));};
auto erase=[&](const ShiftTerm&t,int y,int w,UI mask)->UI{if(!mask)return 0;int yy=y+t.dy,ww=w+t.q;if(yy<0||yy>=H)return 0;UI deleted=0;if(ww>=0&&ww<WP){UI&m=bitmap[t.o][size_t(yy)*WP+ww],cut=mask<<t.k;deleted+=__builtin_popcountll(m&cut);m&=~cut;}if(t.k&&ww+1>=0&&ww+1<WP){UI&m=bitmap[t.o][size_t(yy)*WP+ww+1],cut=mask>>(64-t.k);deleted+=__builtin_popcountll(m&cut);m&=~cut;}return deleted;};

struct Row{uint32_t d,y,w;UI p,n;}__attribute__((packed));
int badD=atoi(argv[4]),badY=atoi(argv[5]),badW=atoi(argv[6]);string path=prefix+".bitmap_trace.bin";
int fd=open(path.c_str(),O_RDONLY);struct stat st;if(fd<0||fstat(fd,&st)||st.st_size%28)throw runtime_error("trace");
Row* rows=(Row*)mmap(0,st.st_size,PROT_READ,MAP_PRIVATE,fd,0);if(rows==MAP_FAILED)throw runtime_error("mmap");
const size_t nrec=st.st_size/28;size_t nsel=0,nbits=0;
ofstream f(prefix+".backtrace.bin",ios::binary);
auto add_need=[&](const ShiftTerm&t,int y,int w,UI mask){
 if(!mask)return;int yy=y+t.dy,ww=w+t.q;if(yy<0||yy>=H)return;
 auto r=validRanges[t.o][yy];
 auto addw=[&](int w,UI bits){
  if(!bits||w<0||w>=WP||r.lo>r.hi)return;int start=64*w,stop=start+63;
  if(stop<r.lo||start>r.hi)return;if(start<r.lo)bits&=~UI(0)<<(r.lo-start);if(stop>r.hi)bits&=~UI(0)>>(stop-r.hi);
  bitmap[t.o][size_t(yy)*WP+w]|=bits;};
 addw(ww,mask<<t.k);if(t.k)addw(ww+1,mask>>(64-t.k));
};
int rootSign=rhs(point(xmin+64*badW,badY),badD);
if(abs(rootSign)!=1)throw runtime_error("root");
for(auto t:shifts[badD])if(t.sign==rootSign)add_need(t,badY,badW,1);
// Only retain endpoint directions where at least one still-needed tile occurs.
for(size_t k=nrec;k-->0;){auto r=rows[k];UI p=0,n=0;
 if(r.d>=unsigned(ND)||r.y>=unsigned(H)||r.w>=unsigned(WP))throw runtime_error("malformed trace");
 for(const auto&t:shifts[r.d]){UI q=read(t,r.y,r.w);if(t.sign>0)p|=(r.p&q);else n|=(r.n&q);}
 if(!(p|n))continue;
 // Each deleted placement now has its reason. Add every geometrically eligible
 // placement which could have provided the missing opposite endpoint.
 for(const auto&t:shifts[r.d])erase(t,r.y,r.w,t.sign>0?p:n);
 for(const auto&t:shifts[r.d])add_need(t,r.y,r.w,t.sign>0?n:p);
 Row selected{r.d,r.y,r.w,p,n};f.write((char*)&selected,sizeof(selected));++nsel;nbits+=__builtin_popcountll(p)+__builtin_popcountll(n);
}
for(auto& v:bitmap)for(auto w:v)if(w)throw runtime_error("unjustified surviving dependency");
cerr<<"verified reverse completeness: "<<nsel<<" "<<nbits<<" row bits"<<endl;
f.close();if(!f)throw runtime_error("could not save certificate");return 0;
}catch(const exception&e){cerr<<"ERROR "<<e.what()<<endl;return 1;}}
