// Physical two-lift sections at the first charged equality on the full board.
#include "marked_geometry.hpp"

#include <unordered_set>
struct Pool {
    Shapes shapes;
    std::vector<bool> live;
    std::array<std::vector<std::pair<I,int>>,3> centers;
    I radii[3]{};
    int count;
    explicit Pool(Shapes objects):shapes(std::move(objects)),live(shapes.size(),true),count(shapes.size()) {
        for (int axis=0;axis<3;++axis) {
            auto& list=centers[axis];
            list.reserve(shapes.size());
            for (int i=0;i<(int)shapes.size();++i) {
                I center=2*rotate(shapes[i].p[1],axis).x;
                list.emplace_back(center,i);
                for(int j=0;j<shapes[i].size;++j)
                    radii[axis]=std::max(radii[axis],std::abs(2*rotate(shapes[i].p[j],axis).x-center));
            }
            std::sort(list.begin(),list.end());
        }
    }
    bool apply(const Polygon& polygon,const std::vector<int>& boundary,Line line) {
        auto ends=hits(polygon,polygon.size(),line,[&](int j){return boundary[j];});
        assert(ends.size()%2==0);
        // The precomputed maximum includes the fourth corner of every pair.
        I radius=radii[line.axis];
        auto& list=centers[line.axis];
        auto first=std::lower_bound(list.begin(),list.end(),std::make_pair(line.pos-radius,-1));
        struct Edge {I low,high;int id;};
        std::vector<Edge> arcs;
        for (auto it=first; it!=list.end() && it->first<=line.pos+radius; ++it) {
            int id=it->second;
            if (!live[id]) continue;
            auto& obj=shapes[id];
            I endpoints[4]; int n=0;
            for (int j=0;j<obj.size;++j) {
                Point u=rotate(obj.p[j],line.axis),v=rotate(obj.p[(j+1)%obj.size],line.axis);
                if ((2*u.x<line.pos)==(2*v.x<line.pos)) continue;
                I numer=denominator*(v.y-u.y),div=2*(v.x-u.x);
                assert(numer%div==0);
                I y=denominator*u.y+(numer/div)*(line.pos-2*u.x);
                int lift=obj.size==3 && j==2 ? obj.long_cell : obj.cell;
                endpoints[n++]=2*y+lift;
            }
            if (!n) continue;
            assert(n==2 && std::abs(endpoints[0]-endpoints[1])>0);
            arcs.push_back({std::min(endpoints[0],endpoints[1]),std::max(endpoints[0],endpoints[1]),id});
            live[id]=false; --count;
        }
        std::sort(arcs.begin(),arcs.end(),[](Edge s,Edge t){return s.low<t.low;});
        for (unsigned j=0;j<ends.size();j+=2) {
            I lo=2*ends[j].first,hi=2*ends[j+1].first;
            std::unordered_set<I> left{lo+ends[j].second},right{hi+ends[j+1].second};
            for (auto e:arcs)
                if (e.low>=lo && e.high<=hi+1 && left.count(e.low)) left.insert(e.high);
            if (!left.count(hi+ends[j+1].second)) return false;
            for (auto it=arcs.rbegin();it!=arcs.rend();++it)
                if (it->low>=lo && it->high<=hi+1 && right.count(it->high)) {
                    right.insert(it->low);
                    if (left.count(it->low) && !live[it->id]) {live[it->id]=true; ++count;}
                }
        }
        return true;
    }
};
int main(int argc,char** argv) {
    if(argc==2 && std::string(argv[1])=="controls") {
        int n,m,wild;
        while(std::cin>>denominator>>n>>m>>wild) {
            Polygon p(n);std::vector<int> tags(n);
            for(int i=0;i<n;i++){std::cin>>p[i].x>>p[i].y>>tags[i];tags[i]=tags[i]!=0;}
            Shapes shapes(m);
            for(auto &sh:shapes) {
                std::cin>>sh.size>>sh.cell>>sh.long_cell;
                sh.cell=sh.cell!=0; sh.long_cell=sh.long_cell!=0;
                for(int i=0;i<sh.size;i++)std::cin>>sh.p[i].x>>sh.p[i].y;
            }
            int probes;std::cin>>probes;Pool pool(std::move(shapes));
            assert(!wild);
            for(int i=0;i<probes;i++){Line line;std::cin>>line.axis>>line.pos;
                assert(pool.apply(p,tags,line) && pool.count==m);}
            std::cout<<probes<<"\n";
        }
        return 0;
    }
    int n;
    std::cin>>a>>b>>c>>n; resolution=c;
    Polygon polygon(n);
    for (Point& p:polygon) {std::cin>>p.x>>p.y;p=c*p;}
    std::vector<int> tags(n,0);
    auto lines=probes(polygon,true);
    Mesh root{{c,0},{0,0},0};
    Shapes root_pairs=catalog(polygon,root,0,{},true);
    int s,t;
    while (std::cin>>s>>t) {
        Mesh terminal{multiplier(s),{c*t,0},s};
        set_denominator({root,terminal});
        Shapes candidates=root_pairs;
        for (int owner:{0,1}) {
            Mesh here=owner?terminal:root,other=owner?root:terminal;
            auto bank=catalog(polygon,here,owner,{{1-owner,other}},owner==1);
            std::set<std::pair<I,I>> negative;
            for (int j=0;j<6;++j) if ((other.height-here.height)*(j%2?-1:1)==-1) {
                Point v=a*product(here.basis,unit[j]);
                negative.insert({v.x,v.y});
            }
            for (auto shape:bank) {
                Point v=shape.p[1]-shape.p[0];
                if (shape.size==4 || negative.count({v.x,v.y})) candidates.push_back(shape);
            }
        }
        Pool pool(std::move(candidates));
        int step=0,fail=0;
        while (!fail) {
            int before=pool.count;
            for (Line line:lines) {
                ++step;
                if (!pool.apply(polygon,tags,line)) {fail=step;break;}
            }
            if (before==pool.count) break;
        }
        std::cout<<s<<" "<<t<<" "<<fail<<std::endl;
    }
}
