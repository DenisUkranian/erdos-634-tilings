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
int family=argc>8?atoi(argv[8]):2, mode=argc>9?atoi(argv[9]):1;
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

if(argc<8)throw runtime_error("need survivors.bin as argument7");
vector<int32_t> index(NV,-1);vector<UI> original;UI fixed=0;Bits active(NR);vector<uint32_t> rows;
ifstream input(argv[7],ios::binary);int32_t record[4];while(input.read((char*)record,16)){int st=record[0],o=record[1],x=record[2],y=record[3];I pi=point(x,y-ymin);if(pi<0||o<0||o>=NT||(st!=1&&st!=2))throw runtime_error("bad record");UI v=UI(pi)*NT+o;if(st==1){index[v]=-2;fixed++;}else{index[v]=original.size();original.push_back(v);}for(int k=0;k<3;k++)for(int end=0;end<2;end++){P z=temps[o].p[(k+end)%3];I pp=point(x+z.x,y-ymin+z.y);if(pp<0)throw runtime_error("bad contained tile");UI row=UI(pp)*ND+temps[o].dirs[k];if(!active.get(row)){active.set(row);rows.push_back(row);}}}
for(int k=0;k<NS;k++)for(int end=0;end<2;end++){UI row=corners[(k+end)%NS]*ND+bd[k];if(!active.get(row)){active.set(row);rows.push_back(row);}}
int N=original.size();vector<int> parent(N),weight(N,1);vector<int8_t> value(N,-1);iota(parent.begin(),parent.end(),0);auto find=[&](int x){int r=x;while(parent[r]!=r)r=parent[r];while(parent[x]!=x){int q=parent[x];parent[x]=r;x=q;}return r;};
UI merges=0,assignments=0;bool conflict=false,incomplete=false;int passes=0;int64_t selected=fixed;int desired=control?control*control:(mode==2?aa*bb:(mode?3*bb*(2*aa+bb):2*bb*(3*aa-2*bb)));
auto assign=[&](int r,int v){r=find(r);if(value[r]>=0){if(value[r]!=v)conflict=true;return;}value[r]=v;assignments++;selected+=I(weight[r])*v;if(selected>desired)conflict=true;};
auto unite=[&](int a,int b){a=find(a);b=find(b);if(a==b)return;if(value[a]>=0||value[b]>=0)throw runtime_error("assigned root in union");if(weight[a]<weight[b])swap(a,b);parent[b]=a;weight[a]+=weight[b];merges++;if(weight[a]>desired-selected)assign(a,0);};
vector<pair<int,int>> eq;eq.reserve(64);
auto equation=[&](uint32_t row){eq.clear();UI pi=row/ND;int d=row%ND,yy=yof[pi],x=left[yy]+pi-offsets[yy];int b=rhs(pi,d);for(auto t:terms[d]){I anchor=point(x+t.dx,yy+t.dy);if(anchor<0)continue;int ix=index[UI(anchor)*NT+t.o];if(ix==-1)continue;if(ix==-2){b-=t.sign;continue;}int r=find(ix);if(value[r]>=0){b-=t.sign*value[r];continue;}bool found=false;for(auto &e:eq)if(e.first==r){e.second+=t.sign;found=true;break;}if(!found)eq.push_back({r,t.sign});}eq.erase(remove_if(eq.begin(),eq.end(),[](auto a){return a.second==0;}),eq.end());return b;};
cerr<<"variables="<<N<<" fixed="<<fixed<<" active_rows="<<rows.size()<<" initialization="<<elapsed()<<"\n";
for(;;){UI before=merges+assignments;passes++;for(UI j=0;j<rows.size()&&!conflict;j++){if(j%100000==0&&elapsed()>limit){incomplete=true;break;}int b=equation(rows[j]),lo=0,hi=0;for(auto e:eq){lo+=min(0,e.second);hi+=max(0,e.second);}if(b<lo||b>hi){conflict=true;break;}if(b==lo||b==hi){bool low=b==lo;for(auto e:eq)assign(e.first,low?(e.second<0):(e.second>0));}
else if(eq.size()==2&&b==0&&eq[0].second==-eq[1].second)unite(eq[0].first,eq[1].first);}
if(!conflict&&!incomplete)for(int r=0;r<N;r++)if(parent[r]==r&&value[r]<0&&weight[r]>desired-selected)assign(r,0);
cerr<<"pass="<<passes<<" merged="<<merges<<" assigned="<<assignments<<" selected_tiles="<<selected<<" seconds="<<elapsed()<<"\n";
if(conflict||incomplete||before==merges+assignments)break;}
vector<int> rid(N,-1);int groups=0;for(int r=0;r<N;r++)if(parent[r]==r&&value[r]<0)rid[r]=groups++;
if(!conflict&&!incomplete){ofstream model(prefix+".pbtxt");for(int k=0;k<groups;k++)model<<"variables { domain:0 domain:1 }\n";
for(auto row:rows){int b=equation(row);if(eq.empty()){if(b)throw runtime_error("nonzero empty final row");continue;}model<<"constraints { linear { vars:[";bool first=true;for(auto e:eq){if(!first)model<<',';first=false;model<<rid[find(e.first)];}model<<"] coeffs:[";first=true;for(auto e:eq){if(!first)model<<',';first=false;model<<e.second;}model<<"] domain:["<<b<<','<<b<<"] }}\n";}
model<<"constraints { linear { vars:[";bool first=true;for(int r=0;r<N;r++)if(rid[r]>=0){if(!first)model<<',';first=false;model<<rid[r];}model<<"] coeffs:[";first=true;for(int r=0;r<N;r++)if(rid[r]>=0){if(!first)model<<',';first=false;model<<weight[r];}model<<"] domain:["<<desired-selected<<','<<desired-selected<<"] }}\n";model.close();
ofstream mapping(prefix+".mapping.bin",ios::binary);for(UI pi=0;pi<NP;pi++){int yy=yof[pi],x=left[yy]+pi-offsets[yy];for(int o=0;o<NT;o++){int ix=index[pi*NT+o],group=-2;if(ix==-1)continue;if(ix>=0){int r=find(ix);if(value[r]==0)continue;group=value[r]==1?-1:rid[r];}else if(ix==-2)group=-1;int32_t line[4]={group,o,x,yy+ymin};mapping.write((char*)line,16);}}
}
ofstream report(prefix+".json");report<<"{\"L\":"<<L<<",\"U\":"<<U<<",\"basis_rotation\":"<<basisRotation<<",\"initial_unknown\":"<<N<<",\"initial_fixed\":"<<fixed<<",\"merges\":"<<merges<<",\"assignments\":"<<assignments<<",\"selected_tiles\":"<<selected<<",\"groups\":"<<groups<<",\"conflict\":"<<(conflict?"true":"false")<<",\"incomplete\":"<<(incomplete?"true":"false")<<",\"seconds\":"<<elapsed()<<",\"scope\":\"Constructive fan residue model; no full F3 exclusion\"}\n";
}catch(const exception&e){cerr<<"ERROR "<<e.what()<<'\n';return 1;}}
