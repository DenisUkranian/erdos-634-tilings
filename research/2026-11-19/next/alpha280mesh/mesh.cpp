// Specialization of the beta mesh to (6,5,9), axial unit sqrt(-2). Input target 2 = alpha-280, 3 = theta-6, 4 = quadratic grid control.
// See README.md for build and replay commands.
#include <algorithm>
#include <array>
#include <cassert>
#include <cstdint>
#include <cstdlib>
#include <gmpxx.h>
#include <iostream>
#include <map>
#include <set>
#include <tuple>
#include <vector>
using Z=mpz_class;
#ifdef WIDE_INIT
using I=mpz_class;
long small(const I& v){return v.get_si();}
#else
using I=__int128_t;
long small(I v){return (long)v;}
#endif
using namespace std;
struct P{I x,y;bool operator<(const P& o)const{return x<o.x||(x==o.x&&y<o.y);}};
P operator+(P a,P b){return{a.x+b.x,a.y+b.y};}
P operator-(P a,P b){return{a.x-b.x,a.y-b.y};}
P operator*(I s,P a){return{s*a.x,s*a.y};}
I det(P a,P b){return a.x*b.y-a.y*b.x;}
#ifdef WIDE_INIT
const I& big(const I& x){return x;}
#else
Z big(I x){Z g;__uint128_t y=x<0?-(static_cast<__uint128_t>(x)):static_cast<__uint128_t>(x);
mpz_import(g.get_mpz_t(),1,1,sizeof(y),0,0,&y);if(x<0)g=-g;return g;}
#endif
int floor_div(I x,I s){assert(s>0);I q=x/s,r=x%s;if(r<0)--q;assert(q>=INT32_MIN&&q<=INT32_MAX);return(int)small(q);}
int ceil_div(I x,I s){return-floor_div(-x,s);}
bool angle(P x,P y){auto half=[](P u){return u.y<0||(u.y==0&&u.x<0);};if(half(x)!=half(y))return half(x)<half(y);
return big(x.x)*big(y.y)>big(x.y)*big(y.x);}
struct Off{int k,x,y;auto operator<=>(const Off&)const=default;};
struct Wall{P a,d;int len,ray;vector<P> joints;};
struct Shape{P v[3];int ray[3],len[3],arc[3];vector<Off> off[3];};
struct Steps{int j;vector<pair<int,int>> in;};
int R,W,H,Q,B,N,scale,freeze_h=500,use_clearance=1;
I S=1;
vector<P> rays;
map<P,int> rank_dir;
vector<Shape> shapes;
vector<Wall> walls;
vector<P> target;
map<pair<int,int>,int> arc;
vector<pair<int,int>> arc_index;
vector<set<Off>> moves;
vector<map<int,Z>> exterior;
vector<tuple<int,int,int>> corner;
vector<vector<Steps>> path;
vector<vector<int>> wanted;
vector<bool> uses;
vector<vector<Z>> poses;
Z limit;
void clip(Z& v){mpz_and(v.get_mpz_t(),v.get_mpz_t(),limit.get_mpz_t());}
void shift(Z& out,const Z& a,int steps){
 if(steps==0)mpz_set(out.get_mpz_t(),a.get_mpz_t());
 else if(steps>0)mpz_mul_2exp(out.get_mpz_t(),a.get_mpz_t(),steps);
 else mpz_fdiv_q_2exp(out.get_mpz_t(),a.get_mpz_t(),-steps);
}
void add_or(Z& a,const Z& b){mpz_ior(a.get_mpz_t(),a.get_mpz_t(),b.get_mpz_t());}
int arcid(int a,int b){
 auto [it,yes]=arc.emplace(pair{a,b},arc.size());
 if(yes){arc_index.push_back({a,b});moves.push_back({});exterior.push_back({});uses.push_back(false);}
 return it->second;
}
bool lattice_only=false;
vector<Off> cover(int k,P v){
 if(lattice_only&&((Q*v.x)%S!=0||(Q*v.y)%S!=0))return{};
 vector<Off> a;for(int x=floor_div(Q*v.x,S);x<=ceil_div(Q*v.x,S);x++)
 for(int y=floor_div(Q*v.y,S);y<=ceil_div(Q*v.y,S);y++)a.push_back({k,x,y});return a;
}
Z lower_bits(int n){Z z=0;if(n>0){mpz_setbit(z.get_mpz_t(),n);z-=1;}return z;}
void init(){
 int K=max(3,B+2);for(int j=0;j<K;j++)S*=3;
 map<int,P> base;base[0]={S,0};for(int j=1;j<=K;j++){
 auto [x,y]=base[j-1];base[j]={(-x-4*y)/3,(2*x-y)/3};base[-j]={base[j].x,-base[j].y};}
 for(auto [h,v]:base)for(int sign:{1,-1})rays.push_back(sign*v);
 sort(rays.begin(),rays.end(),angle);R=rays.size();N=R/2;
 for(int r=0;r<R;r++)rank_dir[rays[r]]=r;
 int base_length=scale==2?140:scale==3?60:20;
 int apex_x=scale==2?70:scale==3?30:28;
 int apex_y=scale==2?40:scale==3?60:16;
 target={{0,0},{base_length,0},{apex_x,apex_y}};
 W=max(base_length,apex_x)*Q+1; H=apex_y*Q+1;limit=lower_bits(W);
 vector<bool> sem(141);sem[0]=true;
 for(int j=1;j<(int)sem.size();j++)for(int n:{5,6,9})if(j>=n&&sem[j-n])sem[j]=true;
 for(int i=0;i<3;i++){
  P a=target[i],d=target[(i+1)%3]-a;int len=scale<4?(i?90:base_length):(i==0?20:i==1?24:36);
  P dir={S*d.x/len,S*d.y/len};int r=rank_dir.at(dir);
  Wall w{a,d,len,r,{}};
  for(int l=0;l<=len;l++)if(sem[l]&&sem[len-l]){
   P p=S*a+l*dir;w.joints.push_back(p);
   if(l&&l<len&&(!lattice_only||((Q*p.x)%S==0&&(Q*p.y)%S==0))){int n=arcid((r+N)%R,r);mpz_setbit(exterior[n][floor_div(Q*p.y,S)].get_mpz_t(),floor_div(Q*p.x,S));}
  }
  walls.push_back(w);
 }
 for(int i=0;i<3;i++){
  int id=arcid((walls[(i+2)%3].ray+N)%R,walls[i].ray);uses[id]=true;
  int x=small(Q*target[i].x),y=small(Q*target[i].y);mpz_setbit(exterior[id][y].get_mpz_t(),x);corner.emplace_back(id,x,y);
 }
 for(int h=-B;h<=B;h++)for(int sign:{1,-1})for(int cx:{-2,7}){
  int k=shapes.size();Shape f;P d=sign*base[h];f.v[0]={0,0};f.v[1]=5*d;f.v[2]={cx*d.x-8*d.y,4*d.x+cx*d.y};
  f.len[0]=5;f.len[1]=cx==-2?9:6;f.len[2]=cx==-2?6:9;
  for(int i=0;i<3;i++){P delta=f.v[(i+1)%3]-f.v[i];f.ray[i]=rank_dir.at({delta.x/f.len[i],delta.y/f.len[i]});}
  for(int i=0;i<3;i++){
   int id=arcid(f.ray[i],(f.ray[(i+2)%3]+N)%R);f.arc[i]=id;uses[id]=true;
   f.off[i]=cover(k,f.v[i]);for(auto off:f.off[i])moves[id].insert(off);
   id=arcid(f.ray[i],(f.ray[i]+N)%R);
   for(int m=1;m<f.len[i];m++)for(auto off:cover(k,f.v[i]+m*rays[f.ray[i]]))moves[id].insert(off);
  }
  vector<Z> rows(H,limit);
  for(auto& w:walls)for(int i=0;i<3;i++){
   P d=w.d,v=Q*f.v[i]-Q*S*w.a;
   bool parallel=(f.ray[i]%N==w.ray%N)||(f.ray[(i+2)%3]%N==w.ray%N);
   // For x,y in the given cell, largest possible signed wall determinant
   // differs from its lower-left evaluation by max(0,dx)+max(0,-dy).
   I c=det(d,v);if(!lattice_only)c+=S*(max(I(0),d.x)+max(I(0),I(-d.y)));
   if(use_clearance)c-=parallel?20*I(w.len)*Q*(S/9):50*I(w.len)*Q*(S/27);
   map<int,Z> specials;
   for(auto p:w.joints){
    if(lattice_only&&((Q*(p.x-f.v[i].x))%S!=0||(Q*(p.y-f.v[i].y))%S!=0))continue;
    int x=floor_div(Q*(p.x-f.v[i].x),S),y=floor_div(Q*(p.y-f.v[i].y),S);
    if(x>=0&&x<W&&y>=0&&y<H)mpz_setbit(specials[y].get_mpz_t(),x);
   }
   for(int y=0;y<H;y++){
    if(rows[y]==0)continue;
    I n=c+S*d.x*y;Z useful;
    if(d.y>0){int r=min(W-1,floor_div(n,S*d.y));useful=lower_bits(r+1);}
    else if(d.y<0){int l=max(0,ceil_div(-n,-S*d.y));useful=l<W?limit^lower_bits(l):Z(0);}
    else if(n>=0)useful=limit;
    auto it=specials.find(y);if(it!=specials.end())add_or(useful,it->second);
    rows[y]&=useful;
   }
  }
  shapes.push_back(f);poses.push_back(move(rows));
 }
 path.resize(R);wanted.resize(R);
 for(int a=0;a<(int)uses.size();a++)if(uses[a])wanted[arc_index[a].second].push_back(a);
 for(int start=0;start<R;start++){
  vector<bool> seen(R);seen[start]=true;
  for(int m=1;m<R;m++){
   int j=(start+m)%R;Steps s{j,{}};
   for(int i=0;i<R;i++)if(seen[i]&&arc.contains({i,j}))s.in.emplace_back(i,arc.at({i,j}));
   if(!s.in.empty()){seen[j]=true;path[start].push_back(move(s));}
  }
 }
}
uint64_t count(){uint64_t n=0;for(auto& sh:poses)for(auto& r:sh)n+=mpz_popcount(r.get_mpz_t());return n;}
bool pass(){
 int A=arc.size();vector<vector<Z>> supports(A);for(int i=0;i<A;i++)if(uses[i])supports[i].resize(H);
 vector<Z> avail(A),reach(R);Z temp,part;
 for(int y=0;y<H;y++){
  for(int a=0;a<A;a++){
   auto it=exterior[a].find(y);if(it==exterior[a].end())avail[a]=0;else avail[a]=it->second;
   for(auto off:moves[a]){
    int v=y-off.y;if(v<0||v>=H||poses[off.k][v]==0)continue;
    shift(temp,poses[off.k][v],off.x);add_or(avail[a],temp);
   }
   clip(avail[a]);
  }
  for(int start=0;start<R;start++)if(!wanted[start].empty()){
   for(auto& arr:reach)arr=0;reach[start]=limit;
   for(auto& s:path[start])for(auto [i,arcid]:s.in)if(reach[i]!=0&&avail[arcid]!=0){
    mpz_and(part.get_mpz_t(),reach[i].get_mpz_t(),avail[arcid].get_mpz_t());add_or(reach[s.j],part);
   }
   for(int id:wanted[start])supports[id][y]=reach[arc_index[id].first];
  }
 }
 bool ok=true;
 for(auto [a,x,y]:corner)if(!mpz_tstbit(supports[a][y].get_mpz_t(),x)){
  cerr<<"missing "<<x<<" "<<y<<'\n';ok=false;
 }
 for(int k=0;k<(int)shapes.size();k++){
  if(abs(k/4-B)>freeze_h)continue;
  auto& f=shapes[k];
  for(int c=0;c<3;c++)for(int y=0;y<H;y++){
   if(poses[k][y]==0)continue;part=0;
   for(auto off:f.off[c]){int v=y+off.y;if(v<0||v>=H)continue;
    shift(temp,supports[f.arc[c]][v],-off.x);add_or(part,temp);
   }
   poses[k][y]&=part;
  }
 }
 return ok;
}
#ifdef HALF_EDGES
#include "half_edges.hpp"
#endif
#ifdef MIRROR_CELLS
#include "mirror_cells.hpp"
#endif
#ifdef TERMINAL_PACKING
#include "terminal_packing.hpp"
#endif
int main(int argc,char**argv){
 if(argc<3||argc>7)return 2;B=atoi(argv[1]);Q=atoi(argv[2]);int cap=argc>=4?atoi(argv[3]):1000;scale=argc>=5?atoi(argv[4]):2;freeze_h=argc>=6?atoi(argv[5]):500;use_clearance=argc>=7?atoi(argv[6]):1;
 if(B<0||Q<1||Q>243||scale<2||scale>4)return 2;
#ifndef WIDE_INIT
 if(B>39)return 2;
#endif
 lattice_only=(getenv("EXACT_LATTICE")!=nullptr);
 if(lattice_only){long d=1;for(int k=0;k<B;k++){if(d>Q)return 2;d*=3;}if(Q%d)return 2;}
 init();
#ifdef HALF_EDGES
 prepare_half_edges();
#endif
#ifdef MIRROR_CELLS
 if(scale!=4)prepare_mirrors();
#endif
 auto prev=count();cout<<0<<" "<<prev<<endl;
 for(int g=1;g<=cap;g++){
  bool ok=pass();
#ifdef HALF_EDGES
 if(ok)prune_half_edges();
#endif
#ifdef MIRROR_CELLS
 if(ok&&scale!=4)prune_mirrors();
#endif
#ifdef TERMINAL_PACKING
 if(ok&&scale!=4)prune_unoccupied_terminal();
#endif
 auto next=count();cout<<g<<" "<<next<<" "<<ok<<endl;
  if(!ok||prev==next||g==cap){
   if(const char* filename=getenv("DUMP_CELLS")) {
    FILE* stream=fopen(filename,"w");if(!stream)return 3;
    fprintf(stream,"%d %d %d %d %d\n",B,Q,scale,W,H);
    for(int k=0;k<(int)poses.size();++k)for(int y=0;y<H;++y)if(poses[k][y]!=0){
     fprintf(stream,"%d %d ",k,y);mpz_out_str(stream,16,poses[k][y].get_mpz_t());fputc('\n',stream);
    }
    if(fclose(stream)!=0)return 3;
   }
   for(int h=-B;h<=B;h++){
    uint64_t count_h=0;
    for(int k=(h+B)*4;k<(h+B+1)*4;k++)for(auto& row:poses[k])count_h+=mpz_popcount(row.get_mpz_t());
    cout<<"height "<<h<<" "<<count_h<<endl;
   }
   break;
  }
  prev=next;
 }
}
