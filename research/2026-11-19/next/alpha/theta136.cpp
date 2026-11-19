// Exact corner-fan replay, tile (3,8,9), theta_t for t=1,2,3.
// Argument 0 replays a nine-tile similar positive control.
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
constexpr L scale = 564859072962LL; // 2 * 3^24
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
const int length_[3]={3,8,9};
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
// Add a clockwise boundary segment by a signed interval sweep on its
// supporting line. Contacts on separate parallel lines are never merged.
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
void fan_choices(P p,D d,D end,std::vector<Tri>& current,
                 std::vector<std::vector<Tri>>& ans,size_t cap){
    if(d==end){ans.push_back(current);return;}
    D gap=minus(end,d);
    for(int j=0;j<3;j++){
        if(!fans.count(minus(gap,angle[j])))continue;
        for(int swap=0;swap<2;swap++){
            int i=(j+1+swap)%3,k=3-i-j;
            Tri t=make_tri(p,d,j,i,k);
            if(!inside(t))continue;
            if(std::any_of(placed.begin(),placed.end(),[&](const Tri& z){return !compatible(z,t);}))continue;
            // Interior-disjoint wedge sectors; integer common subdivisions
            // between the corner tiles are also required.
            if(std::any_of(current.begin(),current.end(),[&](const Tri& z){return !compatible(z,t);}))continue;
            current.push_back(t);fan_choices(p,plus(d,angle[j]),end,current,ans,cap);current.pop_back();
            if(ans.size()>=cap)return;
        }
    }
}
void init(bool control){
    using cpp_int=mpz_class;
    cpp_int sx=1,sy=0;
    for(int k=0;k<=angle_range;k++){
        auto sign=[](const cpp_int& n)->int{return n==0?0:(n>0?1:-1);};
        signs[angle_range+k]={sign(sx),sign(sy)};
        signs[angle_range-k]={sign(sx),-sign(sy)};
        cpp_int nx=-sx-35*sy,ny=sx-sy;sx=nx;sy=ny;
    }
    units[K]={scale,0};
    for(int k=1;k<=K;k++){
        auto [x,y]=units[K+k-1]; units[K+k]={(-x-35*y)/6,(x-y)/6};
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
        int th=target_n;
        P a{0,0},b{8*th*scale,0},c{4*th*scale,4*th*scale};
        outer={{a,b,{0,0}},{b,c,{1,0}},{c,a,{-1,0}}};
        target_n=8*th*th;
    }
    semigroup.assign(550,false);semigroup[0]=true;
    for(size_t n=0;n<semigroup.size();n++)if(semigroup[n])for(int l:length_)
        if(n+l<semigroup.size())semigroup[n+l]=true;
    for(int j=0;j<3;j++){
        auto e=outer[j];side_lengths[j]=distance(e.a,e.b,e.d);
        if(e.a+unit(e.d)*side_lengths[j]!=e.b)throw std::logic_error("target direction");
    }
}
uint64_t visited=0;
bool search(const Boundary& boundary){
    ++visited;
    if(boundary.empty()){
        if(int(placed.size())!=target_n)throw std::logic_error("area mismatch");
        return true;
    }
    std::vector<Sector> sectors;
    if(!describe(boundary,sectors))return false;
    if(sectors.empty())throw std::logic_error("no convex sector");
    std::stable_sort(sectors.begin(),sectors.end(),[](Sector a,Sector b){
        return angular(minus(a.finish,a.start),minus(b.finish,b.start));
    });
    std::vector<std::vector<Tri>> best;
    size_t limit=65536;
    for(Sector s:sectors){
        std::vector<Tri> partial; std::vector<std::vector<Tri>> options;
        fan_choices(s.p,s.start,s.finish,partial,options,limit);
        if(options.empty())return false;
        if(options.size()<limit){limit=options.size();best=std::move(options);}
    }
    if(best.empty())throw Limit("fan_count_limit");
    for(const auto& fan:best){
        size_t old=placed.size();
        Boundary next=boundary;
        for(const Tri& t:fan){
            for(Edge e:t.edges)add_edge(next,flipped(e));
            placed.push_back(t);
        }
        if(search(next))return true;
        placed.resize(old);
    }
    return false;
}
int main(int argc,char**argv){
    if(argc!=2)return 2;
    target_n=std::stoi(argv[1]);
    if(target_n<0||target_n>3)return 2;
    try{init(target_n==0);bool found=search(outer);
        std::cout<<"N="<<target_n<<" nodes="<<visited<<" result="<<(found?"TILABLE":"EXHAUSTED")<<"\n";
    }catch(const Limit& e){std::cout<<"UNKNOWN "<<e.what()<<"\n";return 3;}
}
