// Constructive lattice search of fan residues for a=q(3q+2),b=2q+1,c=3q^2+3q+1.
// Failure excludes only this finite placement list, not the unrestricted tiling.
// Search lattice g Z[rho], eta=(2q+1)-q*rho, g=eta^L/bar(eta)^U.
// Nonconvex residue completeness is not claimed; positive certificates require separate checking.
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
int family=argc>10?atoi(argv[10]):2, mode=argc>11?atoi(argv[11]):1;
int aa=family*(3*family+2),bb=2*family+1,cc=3*family*family+3*family+1,A=aa*bb,B=bb*bb;
P eta{2*family+1,-family},bareta{family+1,family};
P invg=prod(power(eta,-L),power(bareta,U));
P X{-aa*aa,0},Y{2*A,-2*A-B},K{2*A,A+2*B},R1{A,-A},R2{A+B,0},R3{0,A};
P E0{2*A,-2*A},E1{A+B,-A},E2{B,A},V{2*A,A};
auto ccw=[&](vector<P> p){I ar=0;for(int i=0;i<int(p.size());i++)ar+=cross(p[i],p[(i+1)%p.size()]);if(ar<0)reverse(p.begin(),p.end());return p;};
vector<P> domainCanonical=ccw({X,Y,K});
vector<vector<P>> obstacleCanonical={ccw({X,Y,R1}),ccw({X,R1,R2}),ccw({X,R2,R3})};
if(!mode){obstacleCanonical.push_back(ccw({Y,R1,E0}));obstacleCanonical.push_back(ccw({R1,R2,E1}));obstacleCanonical.push_back(ccw({R2,R3,E2}));obstacleCanonical.push_back(ccw({R3,K,V}));}
vector<P> canonical=mode?ccw({Y,R1,R2,R3,K}):ccw({E0,R1,E1,R2,E2,V});
if(mode==2){domainCanonical=canonical=ccw({{0,0},{A,0},{0,A}});obstacleCanonical.clear();}
if(control){domainCanonical=canonical=ccw({{0,0},{aa*control,0},{-bb*control,bb*control}});obstacleCanonical.clear();}
auto transformed=[&](P w){vector<P> t;for(auto p:canonical)t.push_back(prod(w,p));return t;};
int basisRotation=0;UI bestBox=~UI(0);P testInv=invg;
for(int r=0;r<6;r++){auto t=transformed(testInv);int lx=0,hx=0,ly=0,hy=0;for(P p:t){lx=min(lx,p.x);hx=max(hx,p.x);ly=min(ly,p.y);hy=max(hy,p.y);}UI box=UI((hx-lx+64)/64)*UI(hy-ly+1);if(box<bestBox){bestBox=box;basisRotation=r;}testInv=rot(testInv);}
for(int r=0;r<basisRotation;r++)invg=rot(invg);auto target=transformed(invg);int NS=target.size();
vector<P> domain;for(auto p:domainCanonical)domain.push_back(prod(invg,p));
vector<vector<P>> obstacles;for(auto poly:obstacleCanonical){vector<P> t;for(auto p:poly)t.push_back(prod(invg,p));obstacles.push_back(t);}

int xmin=domain[0].x,xmax=xmin,ymin=domain[0].y,ymax=ymin;for(P p:domain){xmin=min(xmin,p.x);xmax=max(xmax,p.x);ymin=min(ymin,p.y);ymax=max(ymax,p.y);}int H=ymax-ymin+1;if(H>65535)throw runtime_error("y index exceeds uint16");vector<int> left(H),right(H);vector<UI> offsets(H+1,0);
for(int yy=0;yy<H;yy++){int y=yy+ymin;I lo=xmin,hi=xmax;for(int k=0;k<int(domain.size());k++){P a=domain[k],d=sub(domain[(k+1)%domain.size()],a);I num=I(d.x)*(y-a.y)+I(d.y)*a.x;if(d.y>0)hi=min(hi,floordiv(num,d.y));else if(d.y<0)lo=max(lo,ceildiv(-num,-I(d.y)));else if(num<0)hi=lo-1;}left[yy]=lo;right[yy]=hi;offsets[yy+1]=offsets[yy]+max(I(0),hi-lo+1);}
UI NP=offsets.back();auto point=[&](int x,int yy)->I{if(yy<0||yy>=H||x<left[yy]||x>right[yy])return -1;return offsets[yy]+x-left[yy];};
vector<uint16_t> yof(NP);for(int yy=0;yy<H;yy++)fill(yof.begin()+offsets[yy],yof.begin()+offsets[yy+1],uint16_t(yy));
vector<Temp> temps;map<pair<int,int>,int> dids;vector<P> directions;auto direction=[&](P p){p=primitive(p);auto key=make_pair(p.x,p.y);auto it=dids.find(key);if(it!=dids.end())return it->second;int id=directions.size();directions.push_back(p);dids[key]=id;return id;};
for(int h=L;h<=U;h++){P u=prod(power(eta,h-L),power(bareta,U-h));for(int r=0;r<basisRotation;r++)u=rot(u);for(int order=0;order<2;order++){P a=mul(u,order?bb:aa),b=mul(rot(rot(u)),order?aa:bb);for(int r=0;r<6;r++){Temp t{{P{0,0},a,b},h,{}};for(int k=0;k<3;k++)t.dirs[k]=direction(sub(t.p[(k+1)%3],t.p[k]));temps.push_back(t);a=rot(a);b=rot(b);}}}
int NT=temps.size(),ND=directions.size();UI NR=NP*ND,NV=NP*NT;vector<vector<Term>> terms(ND);for(int o=0;o<NT;o++)for(int k=0;k<3;k++)for(int end=0;end<2;end++){P p=temps[o].p[(k+end)%3];terms[temps[o].dirs[k]].push_back({o,-p.x,-p.y,end?-1:1});}
vector<UI> corners(NS);vector<int> bd(NS);for(int k=0;k<NS;k++){corners[k]=point(target[k].x,target[k].y-ymin);bd[k]=direction(sub(target[(k+1)%NS],target[k]));if(bd[k]>=ND)throw runtime_error("unsupported boundary direction");}
auto rhs=[&](UI p,int d){int b=0;for(int k=0;k<NS;k++){if(p==corners[k]&&d==bd[k])b++;if(p==corners[(k+1)%NS]&&d==bd[k])b--;}return b;};
cerr<<"band=["<<L<<","<<U<<"] points="<<NP<<" variables_before_containment="<<NV<<" rows="<<NR<<" state_MB="<<NV/4/1000000<<"\n";

TwoBits states(NV);Bits queued(NR);deque<uint32_t> todo;UI valid=0;
if(argc<8)throw runtime_error("need bitmap remaining file as argument7");ifstream input(argv[7]);int readL,readU;UI count;input>>readL>>readU>>count;if(!input||readL!=L||readU!=U)throw runtime_error("remaining header mismatch");
for(UI i=0;i<count;i++){int o,x,y;input>>o>>x>>y;if(!input||o<0||o>=NT)throw runtime_error("remaining data invalid");I pi=point(x,y-ymin);if(pi<0)throw runtime_error("remaining anchor invalid");states.set(UI(pi)*NT+o,2);valid++;
for(int k=0;k<3;k++)for(int end=0;end<2;end++){P v=temps[o].p[(k+end)%3];I pp=point(x+v.x,y-ymin+v.y);if(pp<0)throw runtime_error("remaining vertex outside");UI row=UI(pp)*ND+temps[o].dirs[k];if(!queued.get(row)){queued.set(row);todo.push_back(uint32_t(row));}}}
for(int k=0;k<NS;k++)for(int end=0;end<2;end++){UI row=corners[(k+end)%NS]*ND+bd[k];if(!queued.get(row)){queued.set(row);todo.push_back(uint32_t(row));}}

cerr<<"contained="<<valid<<" initial_seconds="<<elapsed()<<"\n";UI forced=0,ones=0,processed=0,maxQueue=0,traceRows=0;bool conflict=false,incomplete=false;uint32_t badrow=0;ofstream trace;if(saveTrace)trace.open(prefix+".rows.bin",ios::binary);
if(argc>8){ifstream seeds(argv[8]);int n;seeds>>n;if(!seeds)throw runtime_error("seed file unavailable");for(int i=0;i<n;i++){int o,x,y;seeds>>o>>x>>y;I pi=point(x,y-ymin);if(!seeds||o<0||o>=NT||pi<0)throw runtime_error("invalid seed");UI v=UI(pi)*NT+o;if(states.get(v)!=2)throw runtime_error("seed was not available");states.set(v,1);forced++;ones++;}}
auto process=[&](uint32_t row){processed++;UI pi=row/ND;int d=row%ND,yy=yof[pi],x=left[yy]+pi-offsets[yy];int lo=0,hi=0,b=rhs(pi,d);for(auto t:terms[d]){I anchor=point(x+t.dx,yy+t.dy);if(anchor<0)continue;int v=states.get(UI(anchor)*NT+t.o);if(v==2){if(t.sign>0)hi++;else lo--;}else lo+=t.sign*v,hi+=t.sign*v;}if(b<lo||b>hi){conflict=true;badrow=row;return;}if(b!=lo&&b!=hi)return;bool wrote=false;
for(auto t:terms[d]){I anchor=point(x+t.dx,yy+t.dy);if(anchor<0)continue;UI var=UI(anchor)*NT+t.o;if(states.get(var)!=2)continue;if(!wrote){if(saveTrace)trace.write((char*)&row,sizeof(row));traceRows++;wrote=true;}int value=b==lo?(t.sign<0):(t.sign>0);states.set(var,value);forced++;ones+=value;for(int k=0;k<3;k++)for(int end=0;end<2;end++){P v=temps[t.o].p[(k+end)%3];I pp=point(x+t.dx+v.x,yy+t.dy+v.y);if(pp<0)throw runtime_error("assigned invalid tile");UI rr=UI(pp)*ND+temps[t.o].dirs[k];if(!queued.get(rr)){queued.set(rr);todo.push_back(uint32_t(rr));}}}maxQueue=max<UI>(maxQueue,todo.size());};
UI geometricRemoved=0;int geometricRounds=0;UI scanrow=NR;for(;;){while((scanrow<NR||!todo.empty())&&!conflict){if(processed%1000000==0){if(elapsed()>limit){incomplete=true;break;}if(processed%10000000==0)cerr<<"rows="<<processed<<" scan="<<scanrow<<" forced="<<forced<<" queue="<<todo.size()<<" seconds="<<elapsed()<<"\n";}
if(scanrow<NR)process(uint32_t(scanrow++));else{uint32_t row=todo.front();todo.pop_front();queued.reset(row);process(row);}}

if(conflict||incomplete||argc<10||!atoi(argv[9]))break;
struct Located{array<P,3> p;int x0,x1,y0,y1;};vector<Located> fixed;
for(int yy=0;yy<H;yy++)for(int x=left[yy];x<=right[yy];x++){UI pi=offsets[yy]+x-left[yy];for(int o=0;o<NT;o++)if(states.get(pi*NT+o)==1){Located t;for(int k=0;k<3;k++)t.p[k]=add({x,yy+ymin},temps[o].p[k]);t.x0=t.x1=t.p[0].x;t.y0=t.y1=t.p[0].y;for(P p:t.p){t.x0=min(t.x0,p.x);t.x1=max(t.x1,p.x);t.y0=min(t.y0,p.y);t.y1=max(t.y1,p.y);}fixed.push_back(t);}}
const int BS=128,BX=(xmax-xmin)/BS+1,BY=(ymax-ymin)/BS+1;vector<vector<int>> buckets(BX*BY);for(int k=0;k<int(fixed.size());k++)for(int by=(fixed[k].y0-ymin)/BS;by<=(fixed[k].y1-ymin)/BS;by++)for(int bx=(fixed[k].x0-xmin)/BS;bx<=(fixed[k].x1-xmin)/BS;bx++)buckets[by*BX+bx].push_back(k);
auto overlaps=[&](const Located&a,const Located&b){if(a.x1<=b.x0||b.x1<=a.x0||a.y1<=b.y0||b.y1<=a.y0)return false;for(int side=0;side<2;side++){const auto &t=side?b:a,&u=side?a:b;for(int k=0;k<3;k++){P v=sub(t.p[(k+1)%3],t.p[k]);bool sep=true;for(P p:u.p)if(cross(v,sub(p,t.p[k]))>0){sep=false;break;}if(sep)return false;}}return true;};
for(int i=0;i<int(fixed.size());i++)for(int j=0;j<i;j++)if(overlaps(fixed[i],fixed[j])){conflict=true;cerr<<"fixed overlap contradiction\n";}
if(conflict)break;
vector<UI> seen(fixed.size(),0);UI stamp=0,removedHere=0;
for(int yy=0;yy<H&&!incomplete;yy++){if(yy%128==0&&elapsed()>limit){incomplete=true;break;}for(int x=left[yy];x<=right[yy];x++){UI pi=offsets[yy]+x-left[yy];for(int o=0;o<NT;o++)if(states.get(pi*NT+o)==2){stamp++;Located t;for(int k=0;k<3;k++)t.p[k]=add({x,yy+ymin},temps[o].p[k]);t.x0=t.x1=x;t.y0=t.y1=yy+ymin;for(P p:t.p){t.x0=min(t.x0,p.x);t.x1=max(t.x1,p.x);t.y0=min(t.y0,p.y);t.y1=max(t.y1,p.y);}bool bad=false;
for(int by=(t.y0-ymin)/BS;by<=(t.y1-ymin)/BS&&!bad;by++)for(int bx=(t.x0-xmin)/BS;bx<=(t.x1-xmin)/BS&&!bad;bx++)for(int k:buckets[by*BX+bx])if(seen[k]!=stamp){seen[k]=stamp;if(overlaps(t,fixed[k])){bad=true;break;}}
if(bad){states.set(pi*NT+o,0);removedHere++;forced++;for(int k=0;k<3;k++)for(int end=0;end<2;end++){P v=temps[o].p[(k+end)%3];I pp=point(x+v.x,yy+v.y);UI row=UI(pp)*ND+temps[o].dirs[k];if(!queued.get(row)){queued.set(row);todo.push_back(uint32_t(row));}}}
}}}
geometricRemoved+=removedHere;geometricRounds++;cerr<<"geometry round="<<geometricRounds<<" fixed="<<fixed.size()<<" deleted="<<removedHere<<" queue="<<todo.size()<<" seconds="<<elapsed()<<"\n";
if(!removedHere||incomplete)break;
}
if(trace)trace.close();cerr<<"DONE forced="<<forced<<" remaining="<<valid-forced<<" ones="<<ones<<" conflict="<<conflict<<" incomplete="<<incomplete<<" seconds="<<elapsed()<<"\n";
ofstream report(prefix+".json");report<<"{\"scope\":\"finite constructive lattice endpoint currents\",\"L\":"<<L<<",\"U\":"<<U<<",\"control_scale\":"<<control<<",\"basis_rotation\":"<<basisRotation<<",\"points\":"<<NP<<",\"variables_before_containment\":"<<NV<<",\"candidate_placements\":"<<valid<<",\"forced\":"<<forced<<",\"remaining\":"<<valid-forced<<",\"ones\":"<<ones<<",\"processed_rows\":"<<processed<<",\"scan_rows\":"<<scanrow<<",\"maximum_queue\":"<<maxQueue<<",\"forcing_rows\":"<<traceRows<<",\"conflict\":"<<(conflict?"true":"false")<<",\"incomplete\":"<<(incomplete?"true":"false")<<",\"geometric_removed\":"<<geometricRemoved<<",\"geometric_rounds\":"<<geometricRounds<<",\"bad_row\":"<<badrow<<",\"seconds\":"<<elapsed()<<",\"unrestricted_F3_decided\":false}\n";
if(!conflict&&!incomplete){ofstream surv(prefix+".survivors.bin",ios::binary);for(int yy=0;yy<H;yy++)for(int x=left[yy];x<=right[yy];x++){UI pi=offsets[yy]+x-left[yy];for(int o=0;o<NT;o++){int st=states.get(pi*NT+o);if(st==0)continue;int32_t row[4]={st,o,x,yy+ymin};surv.write((char*)row,16);}}}

}catch(const exception&e){cerr<<"ERROR "<<e.what()<<'\n';return 1;}}
