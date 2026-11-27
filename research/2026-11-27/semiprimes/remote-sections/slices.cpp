// Exact line sections of candidate physical pairs and single triangles.
#include <algorithm>
#include <array>
#include <cassert>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <map>
#include <numeric>
#include <set>
#include <string>
#include <vector>

using I = std::int64_t;
struct Point { I x,y; };
Point operator+(Point p, Point q) {return {p.x+q.x,p.y+q.y};}
Point operator-(Point p, Point q) {return {p.x-q.x,p.y-q.y};}
Point operator*(I k, Point p) {return {k*p.x,k*p.y};}
Point product(Point p, Point q) {
    return {p.x*q.x-p.y*q.y,p.x*q.y+p.y*q.x+p.y*q.y};
}
I det(Point p, Point q) {return p.x*q.y-p.y*q.x;}
Point rotate(Point p,int axis) {
    for (int i=0;i<axis;++i) p={-p.y,p.x+p.y};
    return p;
}
constexpr Point unit[]={{1,0},{0,1},{-1,1},{-1,0},{0,-1},{1,-1}};
using Polygon=std::vector<Point>;
struct Object {
    std::array<Point,4> p;
    int size;
    bool child;
};
using Objects=std::vector<Object>;
I mod(I x,I m) {return (x%m+m)%m;}
int a,b,c;
I denominator;

bool inside(Point p,const Polygon& polygon) {
    int winding=0;
    for (unsigned i=0;i<polygon.size();++i) {
        Point u=polygon[i],v=polygon[(i+1)%polygon.size()];
        I d=det(v-u,p-u);
        if (!d && std::min(u.x,v.x)<=p.x && p.x<=std::max(u.x,v.x)
               && std::min(u.y,v.y)<=p.y && p.y<=std::max(u.y,v.y)) return true;
        if (u.y<=p.y && p.y<v.y && d>0) ++winding;
        if (v.y<=p.y && p.y<u.y && d<0) --winding;
    }
    return winding!=0;
}

struct Catalog {
    Objects pairs;
    std::map<std::pair<int,int>,Objects> singles;
};
Catalog catalog(const Polygon& polygon,int hand,int t) {
    Point mesh=hand==0 ? Point{c,0} : (hand==1 ? Point{a,b} : Point{a+b,-b});
    Point shift{c*t,0}, conjugate{mesh.x+mesh.y,-mesh.y};
    I lx=1000000,ly=lx,hx=-lx,hy=-lx;
    for (Point p:polygon) {
        Point v=product(p-shift,conjugate);
        lx=std::min(lx,v.x/(c*c)-1); hx=std::max(hx,v.x/(c*c)+1);
        ly=std::min(ly,v.y/(c*c)-1); hy=std::max(hy,v.y/(c*c)+1);
    }
    // Precompute containment on the possibly padded bounding box in mesh coordinates.
    const I pad=a+b+1, stride=hy-ly+1+2*pad;
    std::vector<bool> legal((hx-lx+1+2*pad)*stride);
    auto index=[&](I x,I y){return (x-lx+pad)*stride+(y-ly+pad);};
    for (I x=lx;x<=hx;++x) for (I y=ly;y<=hy;++y)
        legal[index(x,y)]=inside(shift+product(mesh,{x,y}),polygon);
    int weights[2]{};
    for (int w=0;w<c;++w) {
        if (mod(b+a*w,c)==0) weights[0]=w;
        if (mod(a+b*w,c)==0) weights[1]=w;
    }
    Catalog out;
    for (I x=lx;x<=hx;++x) for (I y=ly;y<=hy;++y) {
        if (!legal[index(x,y)]) continue;
        Point q=shift+product(mesh,{x,y});
        for (int j=0;j<6;++j) for (int h:{-1,1}) {
            Point du=(-a)*unit[j], dv=b*unit[(j+h+6)%6];
            if (!legal[index(x+du.x,y+du.y)] || !legal[index(x+dv.x,y+dv.y)]) continue;
            Point u=q+product(mesh,du), v=q+product(mesh,dv);
            if (j<3 && legal[index(x+du.x+dv.x,y+du.y+dv.y)])
                out.pairs.push_back({{u,q,v,u+v-q},4,hand!=0});
            if (!hand) {
                int label=mod(u.x/c+weights[h==1]*(u.y/c),c);
                assert(label==mod(v.x/c+weights[h==1]*(v.y/c),c));
                out.singles[{h,label}].push_back({{u,q,v,u},3,false});
            } else if (h==-hand && u.x%c==0 && u.y%c==0) {
                assert(v.x%c==0 && v.y%c==0);
                out.singles[{hand,t}].push_back({{u,q,v,u},3,true});
            }
        }
    }
    return out;
}

struct Line {int axis; I pos;};
std::vector<Line> probes(const Polygon& polygon,bool dense) {
    std::array<std::vector<I>,3> by_axis;
    std::vector<Line> lines;
    for (int axis=0;axis<3;++axis) {
        std::set<I> coords;
        for (Point p:polygon) coords.insert(rotate(p,axis).x);
        for (I x:coords) if (x<*coords.rbegin()) by_axis[axis].push_back(2*x+1);
        for (auto it=coords.rbegin(); *it>*coords.begin(); ++it)
            by_axis[axis].push_back(2*(*it)-1);
    }
    for (size_t i=0;i<std::max({by_axis[0].size(),by_axis[1].size(),by_axis[2].size()});++i)
        for (int axis=0;axis<3;++axis) if (i<by_axis[axis].size())
            lines.push_back({axis,by_axis[axis][i]});
    if (dense) for (int axis=0;axis<3;++axis) {
        I lo=by_axis[axis].front(), hi=*std::max_element(by_axis[axis].begin(),by_axis[axis].end());
        for (I left=lo,right=hi;left<right;left+=6*c,right-=6*c) {
            lines.push_back({axis,left});
            lines.push_back({axis,right});
        }
    }
    return lines;
}
template<class Vertices>
int crossings(const Vertices& vertices,int n,Line line,I* out) {
    int count=0;
    for (int i=0;i<n;++i) {
        Point p=rotate(vertices[i],line.axis),q=rotate(vertices[(i+1)%n],line.axis);
        if ((2*p.x<line.pos)==(2*q.x<line.pos)) continue;
        I top=denominator*(q.y-p.y),bottom=2*(q.x-p.x);
        assert(top%bottom==0);
        out[count++]=denominator*p.y+(top/bottom)*(line.pos-2*p.x);
    }
    return count;
}
struct Span {I lower,upper; int shape;};
bool prune(const Polygon& polygon,Objects& objects,Line line) {
    std::vector<I> ends(polygon.size());
    ends.resize(crossings(polygon,polygon.size(),line,ends.data()));
    std::sort(ends.begin(),ends.end());
    assert(ends.size()%2==0);
    std::vector<Span> spans;
    std::vector<bool> keep(objects.size(),true);
    for (int i=0;i<(int)objects.size();++i) {
        I e[4];
        int n=crossings(objects[i].p,objects[i].size,line,e);
        if (!n) continue;
        assert(n==2 && e[0]!=e[1]);
        spans.push_back({std::min(e[0],e[1]),std::max(e[0],e[1]),i});
        keep[i]=false;
    }
    std::sort(spans.begin(),spans.end(),[](Span s,Span t){return s.lower<t.lower;});
    for (unsigned i=0;i<ends.size();i+=2) {
        I lo=ends[i],hi=ends[i+1];
        std::set<I> left{lo},right{hi};
        for (Span s:spans) if (s.upper<=hi && left.count(s.lower)) left.insert(s.upper);
        if (!left.count(hi)) return false;
        for (auto it=spans.rbegin();it!=spans.rend();++it) {
            if (it->lower>=lo && right.count(it->upper)) {
                right.insert(it->lower);
                if (left.count(it->lower)) keep[it->shape]=true;
            }
        }
    }
    size_t kept=0;
    for (size_t i=0;i<objects.size();++i) if (keep[i]) objects[kept++]=objects[i];
    objects.resize(kept);
    return true;
}

// Read fixed physical shapes for a complete control and test every projected gap.
int control() {
    I scale;
    int n,count;
    while (std::cin>>scale>>n>>count) {
        denominator=scale;
        Polygon polygon(n);
        for (Point& p:polygon) std::cin>>p.x>>p.y;
        Objects objects(count);
        for (Object& obj:objects) {
            std::cin>>obj.size;
            obj.child=false;
            for (int i=0;i<obj.size;++i) std::cin>>obj.p[i].x>>obj.p[i].y;
        }
        for (int axis=0;axis<3;++axis) {
            std::set<I> coords;
            for (const Object& obj:objects) for (int i=0;i<obj.size;++i)
                coords.insert(rotate(obj.p[i],axis).x);
            for (I x:coords) if (x<*coords.rbegin()) {
                assert(prune(polygon,objects,{axis,2*x+1}));
                assert((int)objects.size()==count);
            }
            std::cout<<coords.size()-1<<" ";
        }
        std::cout<<"\n";
    }
    return 0;
}

int main(int argc,char** argv) {
    if (argc==2 && std::string(argv[1])=="--control") return control();
    if (argc!=4) return 1;
    a=std::atoi(argv[1]); b=std::atoi(argv[2]); c=std::atoi(argv[3]);
    denominator=2*std::lcm(std::lcm(a,b),a+b);
    int n, dense;
    while (std::cin>>n>>dense) {
        Polygon polygon(n);
        for (Point& p:polygon) {std::cin>>p.x>>p.y; p=c*p;}
        auto root=catalog(polygon,0,0);
        auto lines=probes(polygon,dense);
        for (int hand:{-1,1}) for (int t=0;t<c;++t) {
            auto child=catalog(polygon,hand,t);
            Objects objects=root.pairs;
            for (auto* list:{&root.singles[{hand,t}],&child.pairs,&child.singles[{hand,t}]})
                objects.insert(objects.end(),list->begin(),list->end());
            int outcome=0, step=0;
            for (int pass=0;pass<3 && !outcome;++pass) {
                size_t previous=objects.size();
                for (Line line:lines) {
                    ++step;
                    if (!prune(polygon,objects,line)) {outcome=1; break;}
                    int capacity=0;
                    for (const Object& obj:objects) if (obj.child) {
                        capacity+=obj.size==4 ? 2 : 1;
                        if (capacity>=2*c) break;
                    }
                    if (capacity<2*c) {outcome=2; break;}
                }
                if (objects.size()==previous) break;
            }
            std::cout<<hand<<" "<<t<<" "<<outcome<<" "<<step<<"\n";
        }
    }
}
