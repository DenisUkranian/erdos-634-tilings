#include <algorithm>
#include <array>
#include <cassert>
#include <cmath>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <map>
#include <set>
#include <string>
#include <vector>
#include <chrono>
#include <numeric>
#include <unordered_set>
#include <queue>
using namespace std;using I=int64_t;using W=__int128_t;
struct P{I x,y;auto operator<=>(P const&)const=default;};
P operator+(P p,P q){return{p.x+q.x,p.y+q.y};}P operator-(P p,P q){return{p.x-q.x,p.y-q.y};}P operator*(I k,P p){return{k*p.x,k*p.y};}
P mul(P p,P q){return{p.x*q.x-p.y*q.y,p.y*q.x+p.x*q.y+p.y*q.y};}W det(P p,P q){return W(p.x)*q.y-W(p.y)*q.x;}
P rot(P p,int j){j=(j%6+6)%6;while(j--)p={-p.y,p.x+p.y};return p;}
P primitive(P p){I g=gcd(p.x,p.y);return{p.x/g,p.y/g};}
struct Dir{int h,j;auto operator<=>(Dir const&)const=default;};
struct E{P p,q;auto operator<=>(E const&)const=default;};
struct Block{vector<P>p;int area;char kind;int m,n;};
int a,b,c,H=5,limit=40,N;I D=1,A,B;vector<P> units;map<P,Dir> dirs;map<Dir,P> uv;
map<Dir,vector<array<P,3>>> forms;vector<Block> chosen;vector<int> coin;long long nodes=0,maxnodes=1000000;int filled=0;double timeout=40;auto st=chrono::steady_clock::now();
P unit(Dir d){return uv.at({d.h,(d.j%6+6)%6});}Dir heading(P p){return dirs.at(primitive(p));}
I len(P p){auto d=heading(p);P u=unit(d);I m=u.x?p.x/u.x:p.y/u.y;return m*u==p?m:-1;}
bool legal(Dir s,Dir t){int dh=t.h-s.h;double beta=atan2(b*sqrt(3.)/2.,a+b/2.);for(int m=0;m<=8;m++){int n=m+dh;if(n<0||(s.j+m-t.j)%6)continue;double angle=m*M_PI/3.+dh*beta;if(angle>=-1e-9&&angle<=M_PI+1e-9)return true;}return false;}
bool inside(P p){return p.x>=0&&p.y>=0&&W(A)*p.x+W(B)*p.y<=W(A)*B;}
bool separates(vector<P>const&t,vector<P>const&u){for(int i=0;i<int(t.size());i++){P p=t[i],d=t[(i+1)%t.size()]-p;bool yes=true;for(P q:u)if(det(d,q-p)>0){yes=false;break;}if(yes)return true;}return false;}
bool phase(vector<P>const&t,vector<P>const&u){for(int i=0;i<int(t.size());i++){P p=t[i],q=t[(i+1)%t.size()];for(P v:u)if(min(p,q)<v&&v<max(p,q)&&!det(q-p,v-p))if(len(v-p)<0)return false;}return true;}
bool fits(Block const&t){for(P p:t.p)if(!inside(p))return false;for(auto const&u:chosen){if(!separates(t.p,u.p)&&!separates(u.p,t.p))return false;if(!phase(t.p,u.p)||!phase(u.p,t.p))return false;}return true;}
vector<E> update(vector<E>old,vector<P>const&t){for(int j=0;j<int(t.size());j++){P p=t[(j+1)%t.size()],q=t[j],d=q-p;map<P,int>event;event[p]++;event[q]--;vector<E>keep;for(auto e:old){if(det(e.q-e.p,d)||det(e.p-p,d))keep.push_back(e);else{event[e.p]++;event[e.q]--;}}int n=0;P prev;for(auto [x,v]:event)if(v){if(n==1)keep.push_back({prev,x});if(n==-1)keep.push_back({x,prev});n+=v;if(abs(n)>1)abort();prev=x;}old=move(keep);}return old;}
bool iscoin(I x){return x>=0&&x<int(coin.size())&&coin[x];}
uint64_t hashEdges(vector<E>ed,int depth){sort(ed.begin(),ed.end());uint64_t h=depth+752201;for(auto e:ed)for(I v:{e.p.x,e.p.y,e.q.x,e.q.y})h=(h^uint64_t(v))*1099511628211ULL;return h;}
unordered_set<uint64_t> failed;int mode=0,rectLimit=3;
vector<Block> choices(vector<E>const&edges){
 map<P,vector<P>> in,out;for(auto e:edges){in[e.q].push_back(e.q-e.p);out[e.p].push_back(e.q-e.p);}set<P>clamps;
 for(auto const&[p,r]:out){if(r.size()!=1||in[p].size()!=1||det(in[p][0],r[0])<=0)continue;bool through=false;for(auto e:edges)if(min(e.p,e.q)<p&&p<max(e.p,e.q)&&!det(e.q-e.p,p-e.p)){through=true;break;}if(!through)clamps.insert(p);}
 for(P p:clamps)if(!legal(heading(out[p][0]),heading(-1*in[p][0])))return {};
 for(auto e:edges)if(clamps.count(e.p)&&clamps.count(e.q)&&!iscoin(len(e.q-e.p)))return {};
 vector<Block>best;bool hasbest=false;long long bestweight=0;
 for(P p:clamps){P aim=out[p][0],end=-1*in[p][0];Dir startdir=heading(aim),enddir=heading(end);vector<Block>cand;int maxsc=sqrt(N-filled);auto it=forms.find(startdir);if(it!=forms.end())for(auto const&t:it->second){
   if(det(aim,t[1])<0||det(aim,t[2])<0||det(in[p][0],t[1])<0||det(in[p][0],t[2])<0)continue;
   if(!legal(heading(t[2]),enddir))continue;
   int top=maxsc;for(P v:{t[1],t[2]}){if(v.x<0)top=min<I>(top,p.x/(-v.x));if(v.y<0)top=min<I>(top,p.y/(-v.y));W rat=W(A)*v.x+W(B)*v.y;if(rat>0)top=min<W>(top,(W(A)*B-W(A)*p.x-W(B)*p.y)/rat);}
   for(int k=top;k>=1;k--){Block z{{p,p+k*t[1],p+k*t[2]},k*k,'T',k,0};bool ok=true;for(auto e:edges){if(!clamps.count(e.p)&&!clamps.count(e.q))continue;P d=e.q-e.p;for(P v:z.p)if(min(e.p,e.q)<v&&v<max(e.p,e.q)&&!det(d,v-e.p)){if(clamps.count(e.p)&&!iscoin(len(v-e.p)))ok=false;if(clamps.count(e.q)&&!iscoin(len(e.q-v)))ok=false;}}if(ok&&fits(z))cand.push_back(move(z));}
 }
 // Every two-edge parallelogram of the tile, in either diagonal orientation.
 for(int ell:{a,b,c})for(int rr:{a,b,c})if(ell!=rr){
  P x=ell*unit(startdir),y=rr*unit(enddir);int ss=a+b+c-ell-rr;
  auto norm=[](P z){return W(z.x)*z.x+W(z.x)*z.y+W(z.y)*z.y;};
  if(norm(x-y)!=W(ss)*ss*D*D&&norm(x+y)!=W(ss)*ss*D*D)continue;
  int maxm=1;for(;maxm*2<=N-filled;maxm++)if(!inside(p+maxm*x))break;maxm--;
  for(int m=1;m<=maxm;m++){
   int top=(N-filled)/(2*m);
   for(P v:{p+m*x,p}){if(y.x<0)top=min<I>(top,v.x/(-y.x));if(y.y<0)top=min<I>(top,v.y/(-y.y));W rat=W(A)*y.x+W(B)*y.y;if(rat>0)top=min<W>(top,(W(A)*B-W(A)*v.x-W(B)*v.y)/rat);}
   for(int n=top;n>=max(1,top-rectLimit);n--){Block z{{p,p+m*x,p+m*x+n*y,p+n*y},2*m*n,'P',m,n};if(fits(z))cand.push_back(move(z));}
  }
 }

 if(cand.empty())return {};long long w=cand.size();if(mode==1){int ma=0;for(auto const&t:cand)ma=max(ma,t.area);w=1000000LL-ma*100+min<size_t>(99,cand.size());}
 if(!hasbest||w<bestweight){bestweight=w;best=move(cand);hasbest=true;}
 }
 if(!hasbest)return {};
return best;
}

struct State{vector<E>edges;vector<Block>blocks;int filled;double score;uint64_t key;};
struct Worse{bool operator()(State const&a,State const&b)const{return a.score<b.score;}};
double score(vector<E>const&edges,int fill,int style){double per=0;for(auto e:edges){I n=len(e.q-e.p);if(n<0)return 1e12;per+=n;}int rem=N-fill;if(!rem)return -1e12; if(style==0)return -double(fill)+2.0*edges.size()+per*0.05; if(style==1)return per*per/(double(a*b)*rem)+edges.size()*0.6+rem*0.003;return per+5*c*edges.size()+0.05*c*rem;}
bool beam(vector<E>const&initial,int width,int style){vector<State>active{{initial,{},0,0,0}};long long generated=0;for(int depth=0;depth<limit;depth++){
 map<uint64_t,priority_queue<State,vector<State>,Worse>> queues;unordered_set<uint64_t> seen;
 for(auto const&state:active){chosen=state.blocks;filled=state.filled;auto cand=choices(state.edges);nodes++;
  for(auto t:cand){int nf=filled+t.area;auto edges=update(state.edges,t.p);auto blocks=chosen;blocks.push_back(t);generated++;
   if(nf==N){if(!edges.empty())abort();cout<<"YES "<<N<<" "<<D<<" "<<blocks.size()<<"\n";for(auto const&q:blocks){cout<<q.kind<<" "<<q.m<<" "<<q.n<<" "<<q.area<<" "<<q.p.size();for(auto p:q.p)cout<<" "<<p.x<<" "<<p.y;cout<<"\n";}return true;}
   auto key=hashEdges(edges,0);if(!seen.insert(key).second)continue;auto const&first=blocks[0].p;vector<E> root;for(int ii=0;ii<int(first.size());ii++)root.push_back({first[ii],first[(ii+1)%first.size()]});auto group=hashEdges(root,0);auto&best=queues[group];double value=score(edges,nf,style);if(best.size()>=size_t(width)&&value>=best.top().score)continue;
   best.push({move(edges),move(blocks),nf,value,key});if(best.size()>size_t(width))best.pop();
  }
  if(chrono::duration<double>(chrono::steady_clock::now()-st).count()>timeout){cerr<<"BUDGET depth "<<depth<<" nodes "<<nodes<<" generated "<<generated<<"\n";return false;}
 }
 if(queues.empty()){cerr<<"DEAD depth "<<depth<<" nodes "<<nodes<<"\n";return false;}active.clear();int lo=N,hi=0;double minscore=1e100;
 for(auto&[group,best]:queues)while(!best.empty()){active.push_back(best.top());auto const&z=active.back();lo=min(lo,z.filled);hi=max(hi,z.filled);minscore=min(minscore,z.score);best.pop();}
 cerr<<"depth "<<depth+1<<" states "<<active.size()<<" area "<<lo<<"-"<<hi<<" score "<<minscore<<" generated "<<generated<<"\n";
 }return false;}

int main(int ac,char**av){if(ac<4)return 1;a=atoi(av[1]);b=atoi(av[2]);c=atoi(av[3]);if(ac>4)timeout=atof(av[4]);if(ac>5)limit=atoi(av[5]);if(ac>6)mode=atoi(av[6]);if(ac>7)rectLimit=atoi(av[7]);for(int i=0;i<H;i++)D*=c;B=D*b*(2*a+b);A=D*a*(a+2*b);N=(a+2*b)*(2*a+b);for(int h=-H;h<=H;h++){P u{1,0};I pow=1;for(int i=0;i<abs(h);i++){u=mul(u,h>0?P{a,b}:P{a+b,-b});pow*=c;}u=(D/pow)*u;for(int j=0;j<6;j++){P v=rot(u,j);uv[{h,j}]=v;dirs[primitive(v)]={h,j};}}
 for(int h=-H+1;h<=H-1;h++)for(int j=0;j<6;j++)for(int e:{-1,1}){array<P,3>t{P{0,0},a*unit({h,j}),b*unit({h,(j+2*e+6)%6})};if(det(t[1],t[2])<0)swap(t[1],t[2]);for(int k=0;k<3;k++){P v=t[(k+1)%3]-t[k],w=t[(k+2)%3]-t[k];forms[heading(v)].push_back({P{0,0},v,w});}}
 int cap=4*(c*c+a*b);coin.resize(cap);coin[0]=1;for(int i=1;i<cap;i++)for(int s:{a,b,c})if(i>=s&&coin[i-s])coin[i]=1;
 vector<E>edges{{{0,0},{B,0}},{{B,0},{0,A}},{{0,A},{0,0}}};st=chrono::steady_clock::now();bool yes=beam(edges,ac>8?atoi(av[8]):500,ac>9?atoi(av[9]):0);if(!yes)cout<<"NO IN THIS SEARCH "<<nodes<<"\n";
}
