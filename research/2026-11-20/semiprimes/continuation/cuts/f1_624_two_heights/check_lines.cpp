// Repeatedly discard a placement whose edge cannot occur in any pair
// of interval partitions on its supporting line.
#include <algorithm>
#include <array>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <map>
#include <numeric>
#include <set>
#include <stdexcept>
#include <string>
#include <tuple>
#include <vector>
using namespace std;
struct Point { int x, y; };
Point add(Point p, Point q) { return {p.x+q.x,p.y+q.y}; }
Point scale(Point p,int k) { return {k*p.x,k*p.y}; }
Point product(Point p,Point q) { return {p.x*q.x-p.y*q.y,p.x*q.y+p.y*q.x+p.y*q.y}; }
struct Edge { long long line; int left,right,id,side; };
struct Arc { int left,right,available,supported; };
using Paths=array<uint64_t,4>;

void support(vector<Arc>& arcs,int vertices,bool scalar) {
    vector<int> signs(vertices,0), origins;
    for(auto a:arcs) signs[a.left]|=a.available;
    for(int j=0;j<vertices;j++) if(signs[j]==3) origins.push_back(j);
    if(scalar) {
        // For each source and each common reachable sink, following edges
        // backwards recovers exactly the edges on some path between them.
        for(int source:origins) {
            vector<unsigned char> from(vertices), to(vertices);
            from[source]=3;
            for(auto a:arcs) from[a.right]|=from[a.left]&a.available;
            for(int i=0;i<vertices;i++) if(from[i]==3) to[i]=3;
            for(auto it=arcs.rbegin();it!=arcs.rend();++it) {
                auto& a=*it;
                a.supported|=from[a.left]&to[a.right]&a.available;
                to[a.left]|=to[a.right]&a.available;
            }
        }
    } else {
        for(size_t base=0;base<origins.size();base+=64) {
            vector<Paths> path(vertices);
            for(int i=0;i<64 && base+i<origins.size();i++) {
                uint64_t bit=uint64_t(1)<<i;
                path[origins[base+i]]={bit,bit,0,0};
            }
            for(auto a:arcs) for(int side=0;side<2;side++)
                if(a.available&(1<<side)) path[a.right][side]|=path[a.left][side];
            for(auto& p:path) p[2]=p[3]=p[0]&p[1];
            for(auto it=arcs.rbegin();it!=arcs.rend();++it) {
                auto& a=*it;
                for(int side=0;side<2;side++) if(a.available&(1<<side)) {
                    if(path[a.left][side]&path[a.right][side+2]) a.supported|=1<<side;
                    path[a.left][side+2]|=path[a.right][side+2];
                }
            }
        }
    }
}

int run(const char* path,bool control,bool scalar) {
    ifstream input(path);int lower,upper,total;
    if(!(input>>lower>>upper>>total)||upper!=lower+1||lower>0||upper<0||total<1) throw runtime_error("invalid input");
    using Triangle=array<Point,3>;
    Point eta{6,1},bar{7,-1},rho{0,1};
    Point normalization=lower<0?eta:bar;
    vector<Triangle> templates;
    for(Point u0:{bar,eta}) for(bool swap:{false,true}) {
        Point u=u0;
        for(int rot=0;rot<6;rot++) {
            templates.push_back({Point{0,0},scale(u,swap?13:35),scale(product(rho,product(rho,u)),swap?35:13)});
            u=product(rho,u);
        }
    }
    map<pair<int,int>,vector<Edge>> groups;
    auto insert=[&](Triangle tri,int id) {
        for(int k=0;k<3;k++) {
            Point p=tri[k],q=tri[(k+1)%3];int x=q.x-p.x,y=q.y-p.y;
            int g=gcd(x,y);if(x<0||(!x&&y<0))g=-g;x/=g;y/=g;
            int a=x?p.x:p.y, b=x?q.x:q.y;
            int side=(a<b)^(id==total);
            groups[{x,y}].push_back({int64_t(x)*p.y-int64_t(y)*p.x,min(a,b),max(a,b),id,side});
        }
    };
    Point A=scale(normalization,35),B=scale(product(rho,product(rho,normalization)),13),S=add(A,B);
    int first=-12*lower;
    set<tuple<int,int,int>> known{{first,0,0},{first,A.x,A.y},{first,B.x,B.y},{first+3,S.x,S.y}};
    vector<int> controls;
    for(int i=0;i<total;i++) {
        int t,x,y;if(!(input>>t>>x>>y))throw runtime_error("truncated list");
        Triangle tr=templates.at(t);for(auto& p:tr)p=add(p,{x,y});insert(tr,i);
        if(control&&known.count({t,x,y}))controls.push_back(i);
    }
    int extra;if(input>>extra)throw runtime_error("extra records");
    if(control&&controls.size()!=4)throw runtime_error("missing known grid placements");
    Triangle target=control?Triangle{Point{0,0},scale(A,2),scale(B,2)}:
        Triangle{Point{0,0},scale(normalization,455),product({0,624},normalization)};
    insert(target,total);
    for(auto& [axis,group]:groups)
        sort(group.begin(),group.end(),[](Edge a,Edge b){return tie(a.line,a.left,a.right)<tie(b.line,b.left,b.right);});
    vector<bool> active(total+1,true);int live=total;
    for(int sweep=1;;sweep++) {
        int previous=live;
        for(auto& [axis,group]:groups) for(size_t i=0,j;i<group.size();i=j) {
            j=i+1;while(j<group.size()&&group[j].line==group[i].line)j++;
            vector<Arc> arcs;vector<int> vertices;
            for(size_t k=i;k<j;k++) {
                auto e=group[k];if(!active[e.id])continue;
                if(arcs.empty()||arcs.back().left!=e.left||arcs.back().right!=e.right) {
                    arcs.push_back({e.left,e.right,0,0});vertices.push_back(e.left);vertices.push_back(e.right);
                }
                arcs.back().available|=1<<e.side;
            }
            sort(vertices.begin(),vertices.end());vertices.erase(unique(vertices.begin(),vertices.end()),vertices.end());
            for(auto& a:arcs){
                a.left=lower_bound(vertices.begin(),vertices.end(),a.left)-vertices.begin();
                a.right=lower_bound(vertices.begin(),vertices.end(),a.right)-vertices.begin();
            }
            support(arcs,vertices.size(),scalar);
            size_t ai=0;
            for(size_t k=i;k<j;k++) {
                auto e=group[k];if(!active[e.id])continue;
                while(vertices[arcs.at(ai).left]!=e.left||vertices[arcs.at(ai).right]!=e.right)ai++;
                if(arcs[ai].supported&(1<<e.side))continue;
                if(e.id==total) {
                    if(control)throw runtime_error("known grid contradicted");
                    cout<<"contradiction on sweep "<<sweep<<" axis "<<axis.first<<','<<axis.second
                        <<" line "<<e.line<<" interval "<<e.left<<','<<e.right<<" surviving "<<live<<'\n';return 0;
                }
                active[e.id]=false;live--;
            }
        }
        cout<<"sweep "<<sweep<<" surviving "<<live<<'\n';
        if(control)for(int id:controls)if(!active[id])throw runtime_error("known grid tile removed");
        if(live==previous)break;
    }
    if(!control)throw runtime_error("no contradiction");
    cout<<"all four control placements survive\n";return 0;
}
int main(int argc,char** argv) {
    if(argc!=4)return 2;
    try{return run(argv[1],string(argv[2])=="control",string(argv[3])=="scalar");}
    catch(const exception& e){cerr<<e.what()<<'\n';return 1;}
}
