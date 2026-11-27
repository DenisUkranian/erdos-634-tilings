#pragma once
// Section endpoints carry the lift of the side met by the probe.
#include "section_geometry.hpp"
#include <limits>
#include <tuple>

struct Mesh {Point basis, origin; int height;};
struct Shape {
    std::array<Point,4> p;
    int size, cell, long_cell;
};
using Shapes=std::vector<Shape>;
constexpr I infinity=std::numeric_limits<I>::max()/4;
I resolution;

bool belongs(Point p,const Mesh& m) {
    Point uv=product(p-m.origin,{m.basis.x+m.basis.y,-m.basis.y});
    return uv.x%(resolution*resolution)==0 && uv.y%(resolution*resolution)==0;
}
Shapes catalog(const Polygon& polygon,Mesh m,int id,
               const std::vector<std::pair<int,Mesh>>& neighbors,bool pairs) {
    Point conjugate{m.basis.x+m.basis.y,-m.basis.y};
    I lx=infinity,ly=infinity,hx=-infinity,hy=-infinity,norm=resolution*resolution;
    for (Point p:polygon) {
        Point v=product(p-m.origin,conjugate);
        lx=std::min(lx,v.x/norm-1); hx=std::max(hx,v.x/norm+1);
        ly=std::min(ly,v.y/norm-1); hy=std::max(hy,v.y/norm+1);
    }
    I pad=a+b+1,stride=hy-ly+2*pad+1;
    std::vector<bool> legal((hx-lx+1+2*pad)*stride);
    auto index=[&](I x,I y){return (x-lx+pad)*stride+y-ly+pad;};
    for (I x=lx;x<=hx;++x) for (I y=ly;y<=hy;++y)
        legal[index(x,y)]=inside(m.origin+product(m.basis,{x,y}),polygon);
    Shapes out;
    for (I x=lx;x<=hx;++x) for (I y=ly;y<=hy;++y) {
        if (!legal[index(x,y)]) continue;
        Point q=m.origin+product(m.basis,{x,y});
        for (int h:{-1,1}) for (int j=0;j<6;++j) {
            Point du=(-a)*unit[j],dv=b*unit[(j+h+6)%6];
            if (!legal[index(x+du.x,y+du.y)] || !legal[index(x+dv.x,y+dv.y)]) continue;
            Point u=q+product(m.basis,du),v=q+product(m.basis,dv);
            if (pairs && j<3 && legal[index(x+du.x+dv.x,y+du.y+dv.y)])
                out.push_back({{u,q,v,u+v-q},4,id,id});
            for (auto [k,other]:neighbors) if (other.height==m.height+h && belongs(u,other)) {
                assert(belongs(v,other));
                out.push_back({{u,q,v,u},3,id,k});
            }
        }
    }
    return out;
}

bool disjoint(const Shape& a,const Shape& b) {
    for (auto p:{&a,&b}) {
        const auto& other=(p==&a)?b:a;
        int sign=det(p->p[1]-p->p[0],p->p[2]-p->p[0])>0?1:-1;
        for (int i=0;i<p->size;++i) {
            Point u=p->p[i],d=p->p[(i+1)%p->size]-u;
            bool separated=true;
            for (int j=0;j<other.size;++j) if (sign*det(d,other.p[j]-u)>0) separated=false;
            if (separated) return true;
        }
    }
    return false;
}
struct Arc {I lo,hi; int left,right,object;};
template<class Vertices,class Tag>
std::vector<std::pair<I,int>> hits(const Vertices& points,int n,Line line,Tag tag) {
    std::vector<std::pair<I,int>> out;
    for (int j=0;j<n;++j) {
        Point p=rotate(points[j],line.axis),q=rotate(points[(j+1)%n],line.axis);
        if ((2*p.x<line.pos)==(2*q.x<line.pos)) continue;
        I num=denominator*(q.y-p.y),div=2*(q.x-p.x);
        assert(num%div==0);
        out.emplace_back(denominator*p.y+(num/div)*(line.pos-2*p.x),tag(j));
    }
    std::sort(out.begin(),out.end());
    return out;
}

struct Reach {
    std::set<std::pair<I,int>> points;
    bool open;
    int sign;
    I first=infinity;
    void add(I y,int marker) {
        if (open && marker==1) first=std::min(first,sign*y);
        else points.insert({y,marker});
    }
    bool has(I y,int marker) const {
        return open && marker==1 ? sign*y>=first : points.count({y,marker});
    }
};

class SectionTest {
    const Polygon& polygon;
    const std::vector<int>& boundary;
    bool open;
    int root_limit;
    Shapes shapes;
    std::vector<bool> forced;
    int root_used=0;
public:
    SectionTest(const Polygon& p,const std::vector<int>& tags,bool wildcard,int cap,Shapes pool)
        :polygon(p),boundary(tags),open(wildcard),root_limit(cap),
         shapes(std::move(pool)),forced(shapes.size(),false) {}
    size_t size() const {return shapes.size();}
    int step(Line line,bool enforce_population=true) {
        auto ends=hits(polygon,polygon.size(),line,[&](int j){return boundary[j];});
        assert(ends.size()%2==0);
        std::vector<bool> keep(shapes.size(),true);
        std::vector<Arc> arcs;
        for (int i=0;i<(int)shapes.size();++i) {
            auto& o=shapes[i];
            auto e=hits(o.p,o.size,line,[&](int j){return o.size==3 && j==2 ? o.long_cell : o.cell;});
            if (e.empty()) continue;
            assert(e.size()==2 && e[0].first<e[1].first);
            arcs.push_back({e[0].first,e[1].first,e[0].second,e[1].second,i});
            keep[i]=false;
        }
        std::sort(arcs.begin(),arcs.end(),[](Arc a,Arc b){return a.lo<b.lo;});
        auto rev=arcs;
        std::sort(rev.begin(),rev.end(),[](Arc a,Arc b){return a.hi>b.hi;});
        std::vector<int> newly_forced;
        for (unsigned j=0;j<ends.size();j+=2) {
            auto [lo,in]=ends[j]; auto [hi,out]=ends[j+1];
            Reach left{{},open,1},right{{},open,-1};
            left.add(lo,in); right.add(hi,out);
            for (Arc s:arcs) if (s.lo>=lo && s.hi<=hi && left.has(s.lo,s.left))
                left.add(s.hi,s.right);
            if (!left.has(hi,out)) return 1;
            for (Arc s:rev) if (s.lo>=lo && s.hi<=hi && right.has(s.hi,s.right))
                right.add(s.lo,s.left);
            // Between event coordinates maintain the number and XOR of possible
            // covering intervals. Index -1 denotes unconstrained nonroot material.
            std::map<I,std::pair<int,int>> events;
            auto span=[&](I x,I y,int id) {
                ++events[x].first; --events[y].first;
                events[x].second^=id; events[y].second^=id;
            };
            if (open && left.first < -right.first) span(left.first,-right.first,-1);
            for (Arc s:arcs) if (s.lo>=lo && s.hi<=hi && left.has(s.lo,s.left) && right.has(s.hi,s.right)) {
                keep[s.object]=true;
                if (open) span(s.lo,s.hi,s.object);
            }
            int count=0,id=0;
            for (auto [y,event]:events) {
                count+=event.first; id^=event.second;
                if (count==1 && id>=0 && !forced[id]) {
                    newly_forced.push_back(id);
                    forced[id]=true;
                }
            }
        }
        for (int i:newly_forced) {
            if (shapes[i].cell==0) root_used+=shapes[i].size-2;
            if (root_used>root_limit) return 2;
            for (int j=0;j<(int)shapes.size();++j)
                if (j!=i && keep[j] && !disjoint(shapes[i],shapes[j])) keep[j]=false;
        }
        size_t kept=0;
        int cap[3]{};
        for (size_t i=0;i<shapes.size();++i) {
            if (!keep[i]) {
                if (forced[i]) return 3;
                continue;
            }
            if (enforce_population) cap[shapes[i].cell]+=shapes[i].size-2;
            shapes[kept]=shapes[i]; forced[kept]=forced[i]; ++kept;
        }
        shapes.resize(kept); forced.resize(kept);
        if (!open && enforce_population && (cap[1]<2*c || cap[2]<2*c)) return 4;
        return 0;
    }
};

Point multiplier(int h) {return h==1?Point{a,b}:Point{a+b,-b};}
int hand(int gate) {return gate<c?-1:1;}
void append(Shapes& to,const Shapes& from) {to.insert(to.end(),from.begin(),from.end());}
int trial(const Polygon& p,const std::vector<int>& tags,const std::vector<Line>& lines,
          Shapes shapes,bool wildcard,int root_cap) {
    SectionTest test(p,tags,wildcard,root_cap,std::move(shapes));
    for (int pass=0;pass<3;++pass) {
        size_t start=test.size();
        for (Line line:lines) {
            int result=test.step(line);
            if (result) return result;
        }
        if (test.size()==start) break;
    }
    return 0;
}
void set_denominator(const std::vector<Mesh>& nodes) {
    denominator=2;
    for (Mesh m:nodes) {
        I x=m.basis.x,y=m.basis.y,div=std::gcd(x,y);
        for (I k:{x,y,x+y}) if (k) denominator=std::lcm(denominator,2*std::abs(k/div));
    }
}
