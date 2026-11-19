#define WIDE_INIT
// Independent integer/GMP implementation of the outward-rounded star criterion.
// g++ -std=c++20 -O3 mesh_replay.cpp -lgmpxx -lgmp -o mesh_replay
#include <algorithm>
#include <array>
#include <cassert>
#include <cstdint>
#include <cstdlib>
#include <gmpxx.h>
#include <iostream>
#include <fstream>
#include <string>
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
vector<Off> cover(int k,P v){
 vector<Off> a;for(int x=floor_div(Q*v.x,S);x<=ceil_div(Q*v.x,S);x++)
 for(int y=floor_div(Q*v.y,S);y<=ceil_div(Q*v.y,S);y++)a.push_back({k,x,y});return a;
}
Z lower_bits(int n){Z z=0;if(n>0){mpz_setbit(z.get_mpz_t(),n);z-=1;}return z;}
int par_e=4,par_f=5,vertical=1;
int radicand,surd_factor,short_len,middle_len,long_len,base_len,axial_height,leg_len;
void init(){
 int e=par_e, v=par_f;
 int rad=4*v*v-e*e;surd_factor=1;for(int s=1;s*s<=rad;s++)if(rad%(s*s)==0)surd_factor=s;
 radicand=rad/(surd_factor*surd_factor);short_len=v*v-e*e;middle_len=e*v;long_len=v*v;
 assert(0<short_len&&short_len<middle_len&&middle_len<long_len);
 base_len=scale*e*(3*v*v-e*e);
 assert((scale*short_len*surd_factor*vertical)%2==0 && base_len%2==0);
 axial_height=scale*short_len*surd_factor*vertical/2;leg_len=scale*v*v*v;
 int K=max(3,B+2);S=4*v*v*v*vertical*vertical;for(int j=0;j<K;j++)S*=2*v;
 map<int,P> base;base[0]={S,0};for(int j=1;j<=K;j++){
 auto [x,y]=base[j-1];base[j]={(-e*vertical*x-radicand*surd_factor*y)/(2*v*vertical),(surd_factor*vertical*x-e*y)/(2*v)};base[-j]={base[j].x,-base[j].y};}
 for(auto [h,v]:base)for(int sign:{1,-1})rays.push_back(sign*v);
 sort(rays.begin(),rays.end(),angle);R=rays.size();N=R/2;
 for(int r=0;r<R;r++)rank_dir[rays[r]]=r;
 target={{0,0},{base_len,0},{base_len/2,axial_height}};W=base_len*Q+1;H=axial_height*Q+1;limit=lower_bits(W);
 vector<bool> sem(base_len+1);sem[0]=true;
 for(int j=1;j<(int)sem.size();j++)for(int n:{short_len,middle_len,long_len})if(j>=n&&sem[j-n])sem[j]=true;
 for(int i=0;i<3;i++){
  P a=target[i],d=target[(i+1)%3]-a;int len=(i?leg_len:base_len);
  P dir={S*d.x/len,S*d.y/len};int r=rank_dir.at(dir);
  Wall w{a,d,len,r,{}};
  for(int l=0;l<=len;l++)if(sem[l]&&sem[len-l]){
   P p=S*a+l*dir;w.joints.push_back(p);
   if(l&&l<len){int n=arcid((r+N)%R,r);mpz_setbit(exterior[n][floor_div(Q*p.y,S)].get_mpz_t(),floor_div(Q*p.x,S));}
  }
  walls.push_back(w);
 }
 for(int i=0;i<3;i++){
  int id=arcid((walls[(i+2)%3].ray+N)%R,walls[i].ray);uses[id]=true;
  int x=small(Q*target[i].x),y=small(Q*target[i].y);mpz_setbit(exterior[id][y].get_mpz_t(),x);corner.emplace_back(id,x,y);
 }
 for(int h=-B;h<=B;h++)for(int sign:{1,-1})for(int hand:{0,1}){
  int k=shapes.size();Shape f;P d=sign*base[h];f.v[0]={0,0};f.v[1]=short_len*d;
  int cx=hand==0?-par_e*par_e:2*short_len+par_e*par_e;
  int cy=par_e*surd_factor;
  f.v[2]={(cx*vertical*d.x-radicand*cy*d.y)/(2*vertical),(cy*vertical*d.x+cx*d.y)/2};
  f.len[0]=short_len;f.len[1]=hand==0?long_len:middle_len;f.len[2]=hand==0?middle_len:long_len;
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
   I c=det(d,v)+S*(max(I(0),d.x)+max(I(0),I(-d.y)));
   if(use_clearance)c-=parallel?vertical*short_len*par_e*surd_factor*I(w.len)*Q*(S/(2*long_len)):vertical*short_len*short_len*surd_factor*I(w.len)*Q*(S/(2*par_f*par_f*par_f));
   map<int,Z> specials;
   for(auto p:w.joints){
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
#ifdef PACKING_CAP
#include "packing.hpp"
#endif
#ifdef MIRROR_CELLS
#include "mirror_cells.hpp"
#endif
#ifdef FULL_CONTACTS
#include "full_contacts.hpp"
#endif
#ifdef WALL_WORDS
#ifdef EXACT_WALL_FANS
#include "exact_wall_fans.hpp"
#include "wall_fan_words.hpp"
#else
#include "wall_words.hpp"
#endif
#endif
#ifdef HALF_EDGES
#include "half_edges.hpp"
#endif
int main(int argc,char**argv){
 if(argc<5||argc>9)return 2;
 B=atoi(argv[1]);Q=atoi(argv[2]);par_e=atoi(argv[3]);par_f=atoi(argv[4]);int cap=argc>=6?atoi(argv[5]):1000;
 freeze_h=argc>=7?atoi(argv[6]):5000;scale=argc>=9?atoi(argv[8]):2;use_clearance=true;vertical=argc>=8?atoi(argv[7]):1;assert(vertical>=1&&vertical<=20);
 if(B<1||Q<1||Q>150||par_e<1||par_f<=par_e)return 2;
 init();
#ifdef PACKING_CAP
 std::vector<int> caps;prepare_packing();
#endif
#ifdef MIRROR_CELLS
 prepare_mirrors();
#endif
#ifdef FULL_CONTACTS
 prepare_contacts();
#endif
#ifdef WALL_WORDS
 prepare_word_options();
#endif
#ifdef HALF_EDGES
 prepare_half_edges();
#endif
 std::vector<std::tuple<int,int,int>> witness;
 if(const char* file=std::getenv("BETA_MESH_WITNESS")) {
   std::ifstream inp(file);int k,x,y;
   while(inp>>k>>x>>y)witness.emplace_back(k,x,y);
   assert(witness.size()==1475);
 }
 auto verify_real=[&](){ for(auto [k,x,y]:witness)assert(mpz_tstbit(poses.at(k).at(y).get_mpz_t(),x)); };
 verify_real();
 auto prev=count();cout<<0<<" "<<prev<<endl;
 for(int g=1;g<=cap;g++){
  bool ok=pass();
#ifdef WALL_WORDS
 if(ok)ok=prune_wall_words();
#endif
#ifdef HALF_EDGES
 if(ok)prune_half_edges();
#endif
 #ifdef FULL_CONTACTS
 if(ok)prune_contacts();
#endif
 #ifdef MIRROR_CELLS
 if(ok)prune_mirrors();
#endif
 #ifdef PACKING_CAP
 if(ok&&(g%4==0||count()==prev))prune_packing(caps);
#endif
 verify_real();auto next=count();cout<<g<<" "<<next<<" "<<ok<<endl;
  if(!ok||prev==next)break;prev=next;
 }
 for(int h=-B;h<=B;++h){
   uint64_t n=0;
   for(int i=0;i<4;++i)for(const auto& row:poses.at(4*(h+B)+i))n+=mpz_popcount(row.get_mpz_t());
   #ifdef PACKING_CAP
   cout<<"capacity "<<h<<" "<<packing_cap(h)<<'\n';
#endif
   cout<<"height "<<h<<" "<<n<<'\n';
 }
 if(const char* path=std::getenv("BETA_POSES_DUMP")){
   std::ofstream file(path);assert(file.good());
   file<<B<<" "<<Q<<" "<<vertical<<" "<<par_e<<" "<<par_f<<" "<<scale<<'\n';
   for(int k=0;k<(int)shapes.size();++k)for(int y=0;y<H;++y)
     if(poses[k][y]!=0)file<<k<<" "<<y<<" "<<poses[k][y].get_str(16)<<'\n';
 }
}
