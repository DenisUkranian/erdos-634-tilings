// Integer-scaled triangle search for (90,90,140) by a (6,5,9) tile.
#include <algorithm>
#include <gmpxx.h>
#include <array>
#include <chrono>
#include <cstdint>
#include <deque>
#include <fstream>
#include <iostream>
#include <map>
#include <set>
#include <bitset>
#include <stdexcept>
#include <string>
#include <tuple>
#include <unordered_set>
#include <vector>
using I = __int128_t;
using L = int64_t;
constexpr int K = 24;
constexpr L scale = 282429536481LL; // 3^24
struct Limit : std::runtime_error {using std::runtime_error::runtime_error;};
struct P {
    L x,y;
    auto operator<=>(const P&) const = default;
};
P operator+(P a,P b){return {a.x+b.x,a.y+b.y};}
P operator-(P a,P b){return {a.x-b.x,a.y-b.y};}
P operator*(P a,L k){return {a.x*k,a.y*k};}
I cross(P a,P b){return I(a.x)*b.y-I(a.y)*b.x;}
I orient(P a,P b,P c){return cross(b-a,c-a);}
struct D {int k,neg; auto operator<=>(const D&) const = default;};
D plus(D a,D b){return {a.k+b.k,a.neg^b.neg};}
D minus(D a,D b){return {a.k-b.k,a.neg^b.neg};}
D reverse(D a){return {a.k,a.neg^1};}
std::array<P,2*K+1> units;
P unit(D d){
    if(abs(d.k)>K)throw Limit("orientation_limit");
    return units[d.k+K]*(d.neg?-1:1);
}
constexpr int angle_range=100;
std::array<P,2*angle_range+1> signs;
P axis_signs(D d){
    if(abs(d.k)>angle_range)throw Limit("angle_inventory_limit");
    return signs[angle_range+d.k]*(d.neg?-1:1);
}
int half(D d){auto p=axis_signs(d);return (p.y>0||(p.y==0&&p.x>=0))?0:1;}
bool angular(D a,D b){
    return half(a)!=half(b)?half(a)<half(b):axis_signs(minus(b,a)).y>0;
}
const int length_[3]={6,5,9};
const D angle[3]={{2,1},{-3,0},{1,0}};
std::set<D> fans;
struct Edge {
    P a,b;D d;
    auto operator<=>(const Edge&) const = default;
};
Edge flipped(Edge e){return {e.b,e.a,reverse(e.d)};}
bool on(P p,Edge e){
    return orient(e.a,e.b,p)==0 && std::min(e.a,e.b)<=p && p<=std::max(e.a,e.b);
}
int distance(P a,P b,D d){
    P u=unit(d),v=b-a;
    L w=u.x?u.x:u.y, s=u.x?v.x:v.y;
    if(s%w)return -1;
    return static_cast<int>(s/w);
}
struct Tri {std::array<Edge,3> edges;L xmin,xmax,ymin,ymax;};
Tri make_tri(P p,D d,int corner,int first,int second){
    D other=plus(d,angle[corner]);
    D transverse=plus(d,reverse(minus({0,0},angle[second])));
    P q=p+unit(d)*length_[first],r=p+unit(other)*length_[second];
    if(q+unit(transverse)*length_[corner]!=r)throw std::logic_error("angle mismatch");
    return {{{{p,q,d},{q,r,transverse},{r,p,reverse(other)}}},
        std::min({p.x,q.x,r.x}),std::max({p.x,q.x,r.x}),
        std::min({p.y,q.y,r.y}),std::max({p.y,q.y,r.y})};
}
using Boundary=std::vector<Edge>;
struct Sector{P p;D start,finish;};
struct Rays{D d;bool out;};
std::vector<Edge> outer;
int side_lengths[3], target_n;
std::vector<bool> semigroup;
std::vector<Tri> placed,solution;
bool disjoint(const Tri& a,const Tri& b){
    for(const Tri* first:{&a,&b}){
        const Tri& second=first==&a?b:a;
        for(Edge e:first->edges){
            if(std::all_of(second.edges.begin(),second.edges.end(),
                    [&](Edge f){return orient(e.a,e.b,f.a)<=0;}))return true;
        }
    }
    return false;
}
bool compatible(const Tri& a,const Tri& b){
    if(a.xmax<b.xmin||b.xmax<a.xmin||a.ymax<b.ymin||b.ymax<a.ymin)return true;
    if(!disjoint(a,b))return false;
    for(const Tri* first:{&a,&b}){
        const Tri& second=first==&a?b:a;
        for(Edge e:first->edges)for(Edge f:second.edges)
            if(on(f.a,e)&&distance(e.a,f.a,e.d)<0)return false;
    }
    return true;
}
bool inside(const Tri& t){
    for(int i=0;i<3;i++){
        Edge e=outer[i];
        for(Edge f:t.edges){
            I c=orient(e.a,e.b,f.a);
            if(c<0)return false;
            if(c==0){
                int n=distance(e.a,f.a,e.d);
                if(n<0||n>side_lengths[i]||!semigroup[n]||!semigroup[side_lengths[i]-n])return false;
            }
        }
    }
    return true;
}
void add_edge(Boundary& b,Edge e){
    std::map<P,int> events;
    auto add=[&](Edge f){events[f.a]++;events[f.b]--;};
    add(e);
    auto it=std::remove_if(b.begin(),b.end(),[&](Edge f){
        if(e.d.k==f.d.k&&orient(e.a,e.b,f.a)==0){add(f);return true;}
        return false;
    });
    b.erase(it,b.end());
    int count=0;P start{};
    D positive=e.a<e.b?e.d:reverse(e.d);
    for(auto [p,delta]:events){
        if(!delta)continue;
        if(count==1)b.push_back({start,p,positive});
        if(count==-1)b.push_back({p,start,reverse(positive)});
        count+=delta;start=p;
        if(abs(count)>1)throw std::logic_error("boundary multiplicity");
    }
    if(count!=0)throw std::logic_error("interval imbalance");
}
bool describe(const Boundary& b,std::vector<Sector>& corners){
    std::map<P,std::vector<Rays>> rays;
    for(Edge e:b){
        if(distance(e.a,e.b,e.d)<0)return false;
        rays[e.a].push_back({e.d,true});
        rays[e.b].push_back({reverse(e.d),false});
    }
    std::set<std::pair<P,D>> convex_out,convex_in;
    for(auto& [p,list]:rays){
        for(Edge e:b)if(e.a!=p&&e.b!=p&&on(p,e)){
            if(distance(e.a,p,e.d)<0)return false;
            list.push_back({e.d,true});list.push_back({reverse(e.d),false});
        }
        std::sort(list.begin(),list.end(),[](Rays a,Rays b){return angular(a.d,b.d);});
        for(size_t j=0;j<list.size();j++){
            Rays a=list[j],c=list[(j+1)%list.size()];
            if(a.out==c.out||a.d==c.d)throw std::logic_error("nonalternating local rays");
            if(a.out&&cross(unit(a.d),unit(c.d))>0){
                if(!fans.count(minus(c.d,a.d)))return false;
                corners.push_back({p,a.d,c.d});
                convex_out.insert({p,a.d});convex_in.insert({p,c.d});
            }
        }
    }
    // A straight stretch with two convex ends must consist of whole new
    // tile edges. The same holds unconditionally along the target boundary.
    for(Edge e:b){
        bool exterior=false;
        for(Edge f:outer)if(e.d.k==f.d.k&&orient(f.a,f.b,e.a)==0)exterior=true;
        std::vector<P> cuts{e.a,e.b};
        for(auto& [p,list]:rays)if(p!=e.a&&p!=e.b&&on(p,e))cuts.push_back(p);
        std::sort(cuts.begin(),cuts.end());
        if(e.b<e.a)std::reverse(cuts.begin(),cuts.end());
        for(size_t j=1;j<cuts.size();j++){
            if(exterior||(convex_out.count({cuts[j-1],e.d})&&convex_in.count({cuts[j],reverse(e.d)}))){
                int n=distance(cuts[j-1],cuts[j],e.d);
                if(n<0||n>=(int)semigroup.size()||!semigroup[n])return false;
            }
        }
    }
    return true;
}
std::unordered_set<std::string> seen;
// Translation-normalized oriented boundary; direction and exact length
// recover the other endpoint. The set compares complete keys after hashing.
std::string boundary_key(const Boundary& b){
    std::vector<Edge> ordered=b;
    std::sort(ordered.begin(),ordered.end());
    P origin=ordered.front().a;
    std::string key;
    key.reserve(20*b.size());
    for(auto e:ordered){
        P offset=e.a-origin;
        key.append(reinterpret_cast<const char*>(&offset.x),sizeof(L));
        key.append(reinterpret_cast<const char*>(&offset.y),sizeof(L));
        int n=distance(e.a,e.b,e.d);
        if(n<0)return {};
        uint16_t len=static_cast<uint16_t>(n);
        key.append(reinterpret_cast<const char*>(&len),sizeof(len));
        key.push_back(static_cast<char>(e.d.k+K));key.push_back(static_cast<char>(e.d.neg));
    }
    return key;
}
std::chrono::steady_clock::time_point stop_time;
uint64_t max_nodes=0;
void init(bool control){
    using cpp_int=mpz_class;
    cpp_int sx=1,sy=0;
    for(int k=0;k<=angle_range;k++){
        auto sign=[](const cpp_int& n)->int{return n==0?0:(n>0?1:-1);};
        signs[angle_range+k]={sign(sx),sign(sy)};
        signs[angle_range-k]={sign(sx),-sign(sy)};
        cpp_int nx=-sx-4*sy,ny=2*sx-sy;sx=nx;sy=ny;
    }
    units[K]={scale,0};
    for(int k=1;k<=K;k++){
        auto [x,y]=units[K+k-1]; units[K+k]={(-x-4*y)/3,(2*x-y)/3};
        units[K-k]={units[K+k].x,-units[K+k].y};
    }
    fans.insert({0,0});std::vector<D> queue{{0,0}};
    for(size_t i=0;i<queue.size();i++)for(D a:angle){
        D d=plus(queue[i],a);
        if(axis_signs(d).y>0&&fans.insert(d).second)queue.push_back(d);
    }

    if(control){
        Tri t=make_tri({0,0},{0,0},0,2,1);
        for(int j=0;j<3;j++){Edge e=t.edges[j];outer.push_back({e.a*3,e.b*3,e.d});}
        target_n=9;
    }else{
P a{0,0},b{140*scale,0},c{70*scale,40*scale};
outer={{a,b,{0,0}},{b,c,{-2,0}},{c,a,{2,0}}};target_n=280;
    }
    semigroup.assign(550,false);semigroup[0]=true;
    for(size_t n=0;n<semigroup.size();n++)if(semigroup[n])for(int l:length_)
        if(n+l<semigroup.size())semigroup[n+l]=true;
    for(int j=0;j<3;j++){
        auto e=outer[j];side_lengths[j]=distance(e.a,e.b,e.d);
        if(e.a+unit(e.d)*side_lengths[j]!=e.b)throw std::logic_error("target direction");
    }
}

struct Choice {Tri tile;int size,sign;};
int pieces;
int calls=0,maxd=0;
std::vector<int> scales,best_scales;
std::vector<std::vector<std::bitset<161>>> reachable;
void prep(){
 reachable.resize(pieces+1,std::vector<std::bitset<161>>(target_n+1));
 reachable[0][0].set(80);
 for(int k=1;k<=pieces;k++)for(int a=0;a<=target_n;a++){
  for(int m=1;m*m<=a;m++){
   auto h=reachable[k-1][a-m*m];reachable[k][a]|=(h<<m)|(h>>m);
  }
 }
}
bool phase_ok(int k,int a,int b){return k>=0 && a>=0 && abs(b)<=80 && reachable[k][a][b+80];}
bool macros(const Boundary& outer_left,int k,int area,int signed_scale){
 if(++calls>max_nodes||(calls%1024==1 && std::chrono::steady_clock::now()>stop_time))throw Limit("budget");
 int depth=pieces-k;maxd=std::max(maxd,depth);
 if(!k){if(outer_left.empty()&&!area&&!signed_scale){solution=placed;best_scales=scales;return true;}return false;}
 if(!phase_ok(k,area,signed_scale)||outer_left.empty())return false;
 auto key=boundary_key(outer_left);key+=char(k);if(!seen.insert(key).second)return false;
 if(seen.size()>350000)seen.clear();
 std::vector<Sector> corners;if(!describe(outer_left,corners))return false;
 std::vector<Choice> best;unsigned bestlen=100000;
 for(auto s:corners){
  std::vector<Choice> candidates;D gap=minus(s.finish,s.start);
  for(int j=0;j<3;j++){
   if(!fans.count(minus(gap,angle[j])))continue;
   for(int j2=0;j2<2;j2++){
    int i=(j+1+j2)%3,l=3-i-j;auto unit_tile=make_tri(s.p,s.start,j,i,l);
    int sig=0;for(auto e:unit_tile.edges)sig+=(e.d.neg?-1:1)*distance(e.a,e.b,e.d);
    if(abs(sig)!=8)throw std::logic_error("sign invariant");
    sig/=8;
    for(int m=16;m>0;m--){
     if(!phase_ok(k-1,area-m*m,signed_scale-sig*m))continue;
     auto t=unit_tile;
     for(auto& e:t.edges){e.a=s.p+(e.a-s.p)*m;e.b=s.p+(e.b-s.p)*m;}
     t.xmin=t.xmax=s.p.x;t.ymin=t.ymax=s.p.y;
     for(auto e:t.edges){
      t.xmin=std::min(t.xmin,e.a.x);t.xmax=std::max(t.xmax,e.a.x);
      t.ymin=std::min(t.ymin,e.a.y);t.ymax=std::max(t.ymax,e.a.y);
     }
     if(!inside(t))continue;
     bool ok=true;for(const auto& q:placed)if(!compatible(t,q)){ok=false;break;}
     if(ok)candidates.push_back({t,m,sig});
    }
   }
  }
  if(candidates.empty())return false;
  if(candidates.size()<bestlen){bestlen=candidates.size();best=std::move(candidates);}
 }
 for(const auto& e:best){
  auto b=outer_left;
  for(const Edge& z:e.tile.edges)add_edge(b,flipped(z));
  placed.push_back(e.tile);scales.push_back(e.size);
  if(macros(b,k-1,area-e.size*e.size,signed_scale-e.sign*e.size))return true;
  placed.pop_back();scales.pop_back();
 }
 return false;
}
int main(int argc,char**argv){
 if(argc!=5)return 2;
 pieces=std::stoi(argv[1]);int seconds=std::stoi(argv[2]);max_nodes=std::stoull(argv[3]);
 init(std::getenv("ALPHA_CONTROL")!=nullptr);
 if(const char* shape=std::getenv("ALPHA_TARGET")){int target=std::atoi(shape);
  int b=target==180?60:80;
  P a{0,0},p{b*scale,0},q{b*scale/2,b*scale};
  outer={{a,p,{0,0}},{p,q,{1,0}},{q,a,{-1,0}}};target_n=target;
  for(int j=0;j<3;j++)side_lengths[j]=distance(outer[j].a,outer[j].b,outer[j].d);
 }
 int sm=0;for(auto e:outer)sm+=(e.d.neg?-1:1)*distance(e.a,e.b,e.d);
 if(sm%8)throw std::logic_error("target signature");sm/=8;prep();
 stop_time=std::chrono::steady_clock::now()+std::chrono::seconds(seconds);
 std::string status;
 try{status=macros(outer,pieces,target_n,sm)?"SAT":"EXHAUSTED";}
 catch(const Limit& e){status=e.what();}
 if(status=="SAT"){
  std::ofstream out(argv[4]);out<<scale<<"\n";
  for(unsigned i=0;i<solution.size();i++){out<<best_scales[i];for(auto e:solution[i].edges)out<<" "<<e.a.x<<" "<<e.a.y;out<<"\n";}
 }
 std::cout<<"{\"status\":\""<<status<<"\",\"pieces\":"<<pieces<<",\"calls\":"<<calls<<",\"depth\":"<<maxd<<"}\n";
}
