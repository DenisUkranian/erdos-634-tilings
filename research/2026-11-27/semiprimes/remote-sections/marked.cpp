#include "marked_geometry.hpp"

int main(int argc,char** argv) {
    if (argc!=2) return 1;
    std::string mode=argv[1];
    a=33;b=7;c=37;
    if (mode=="controls") {
        I den; int n,m,wild;
        while (std::cin>>den>>n>>m>>wild) {
            denominator=den; Polygon p(n); std::vector<int> tags(n);
            for (int i=0;i<n;++i) std::cin>>p[i].x>>p[i].y>>tags[i];
            Shapes pool(m);
            for (auto& sh:pool) {
                std::cin>>sh.size>>sh.cell>>sh.long_cell;
                for (int i=0;i<sh.size;++i) std::cin>>sh.p[i].x>>sh.p[i].y;
            }
            int checkpoints; std::cin>>checkpoints;
            SectionTest test(p,tags,wild,143,std::move(pool));
            for (int i=0;i<checkpoints;++i) {
                Line line;std::cin>>line.axis>>line.pos;
                assert(!test.step(line,false) && test.size()==size_t(m));
            }
            std::cout<<checkpoints<<"\n";
        }
        return 0;
    }
    bool wildcard=mode=="open";
    if (!wildcard && mode!="exact") return 1;
    resolution=wildcard?c:c*c;
    int n,root_cap;std::cin>>n>>root_cap;
    Polygon polygon(n);std::vector<int> tags(n,0);
    for (Point& p:polygon) {std::cin>>p.x>>p.y; p=resolution*p;}
    auto lines=probes(polygon,true,resolution);
    Mesh root{{resolution,0},{0,0},0};
    Shapes root_pairs;std::vector<Shapes> banks(2*c);
    if (wildcard) {
        set_denominator({root,{multiplier(1),{0,0},1}});
        root_pairs=catalog(polygon,root,0,{},true);
        for (int g=0;g<2*c;++g) {
            Mesh child{multiplier(hand(g)),{c*(g%c),0},hand(g)};
            banks[g]=catalog(polygon,root,0,{{1,child}},false);
            append(banks[g],catalog(polygon,child,1,{{0,root}},false));
        }
    }
    int chain,g,k;
    while (std::cin>>chain>>g>>k) {
        Shapes pool;
        if (wildcard) {
            pool=root_pairs;append(pool,banks[g]);
            if (!chain) append(pool,banks[k]);
        } else {
            int h=hand(g),s=hand(k);
            Mesh A{c*multiplier(h),{resolution*(g%c),0},h};
            Mesh B=chain ? Mesh{product(multiplier(h),multiplier(s)),A.origin+(k%c)*A.basis,h+s}
                         : Mesh{c*multiplier(s),{resolution*(k%c),0},s};
            if (chain && B.height==0 && belongs(B.origin,root)) {
                std::cout<<chain<<" "<<g<<" "<<k<<" 5\n";continue;
            }
            set_denominator({root,A,B});
            std::vector<std::pair<int,Mesh>> rn{{1,A}},an{{0,root}};
            if (chain) an.push_back({2,B}); else rn.push_back({2,B});
            pool=catalog(polygon,root,0,rn,true);
            append(pool,catalog(polygon,A,1,an,true));
            append(pool,catalog(polygon,B,2,{{chain?1:0,chain?A:root}},true));
        }
        int outcome=trial(polygon,tags,lines,std::move(pool),wildcard,root_cap);
        std::cout<<chain<<" "<<g<<" "<<k<<" "<<outcome<<"\n";
    }
}
