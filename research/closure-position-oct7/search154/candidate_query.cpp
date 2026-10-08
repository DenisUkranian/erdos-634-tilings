// Machine-readable interface used by check_fixed_search.py.
#define main search_main
#include "fixed_search.cpp"
#undef main
int main() {
    setup();
    L x,y,dx,dy;
    while(cin>>x>>y>>dx>>dy) {
        auto alternatives=candidates(point({x,y}),normal({dx,dy}));
        cout<<alternatives.size();
        for(auto alternative:alternatives) {
            auto t=tri[alternative.t];
            cout<<' '<<t.h<<' '<<t.group;
            for(int p:t.v)cout<<' '<<pts[p].x<<' '<<pts[p].y;
        }
        cout<<'\n';
    }
}
