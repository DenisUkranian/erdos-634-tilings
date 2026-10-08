// Test-only interface to exact search primitives; no search conclusions.
#define main search_main
#include "fixed_search.cpp"
#undef main

int query_triangle(array<int,3> v) {
    if (orient(v[0],v[1],v[2])<0) swap(v[1],v[2]);
    T t{}; t.v=v;
    t.box={pts[v[0]].x,pts[v[0]].x,pts[v[0]].y,pts[v[0]].y};
    for (int p:v) {
        t.box[0]=min(t.box[0],pts[p].x);t.box[1]=max(t.box[1],pts[p].x);
        t.box[2]=min(t.box[2],pts[p].y);t.box[3]=max(t.box[3],pts[p].y);
    }
    tri.push_back(t);return tri.size()-1;
}

void write_fans(const vector<Fan>& fs) {
    cout << fs.size();
    for (const Fan& f : fs) {
        cout << ' ' << f.size();
        for (int t : f) {
            for (int v : tri[t].v) cout << ' ' << pts[v].x << ' ' << pts[v].y;
        }
    }
    cout << '\n';
}

int main() {
    setup();
    char command;
    while (cin >> command) {
        if (command == 'F') {
            L x,y,sx,sy,ex,ey;
            cin >> x >> y >> sx >> sy >> ex >> ey;
            write_fans(rawfans(point({x,y}), normal({sx,sy}), normal({ex,ey}), {}));
        } else if (command == 'I') {
            array<int,3> a,b;
            for (int& v : a) { L x,y; cin >> x >> y; v=point({x,y}); }
            for (int& v : b) { L x,y; cin >> x >> y; v=point({x,y}); }
            cout << incompatible(query_triangle(a),query_triangle(b)) << '\n';
        } else if (command == 'B') {
            int count;
            cin >> count;
            Boundary boundary;
            for (int j=0;j<3;++j) {
                L x,y; cin >> x >> y;
                boundary.push_back({point({x,y}),0});
            }
            for (int j=0;j<3;++j) boundary[j].second=boundary[(j+1)%3].first;
            Fan added;
            for (int j=0;j<count;++j) {
                array<int,3> vertices;
                for (int& v : vertices) { L x,y; cin >> x >> y; v=point({x,y}); }
                added.push_back(query_triangle(vertices));
            }
            cout << addtiles(boundary,added).size() << '\n';
        } else throw runtime_error("unknown primitive command");
    }
}
