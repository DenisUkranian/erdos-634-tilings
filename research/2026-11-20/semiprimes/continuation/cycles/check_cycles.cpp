// g++ -std=c++20 -O3 check_cycles.cpp -o check_cycles
// Restricted to the three boards in main. All placement comparisons are exact.
#include <algorithm>
#include <array>
#include <compare>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <numeric>
#include <stdexcept>
#include <string>
#include <vector>

using Int = std::int64_t;
using Wide = __int128_t;
struct Point {
    Int x, y; // x + y*rho, rho = exp(i*pi/3)
    auto operator<=>(const Point&) const = default;
};
Point operator+(Point u, Point v) { return {u.x + v.x, u.y + v.y}; }
Point operator-(Point u, Point v) { return {u.x - v.x, u.y - v.y}; }
Point operator*(Int t, Point v) { return {t * v.x, t * v.y}; }
Point conjugate(Point u) { return {u.x + u.y, -u.y}; }
Point product(Point u, Point v) {
    return {u.x*v.x - u.y*v.y, u.x*v.y + u.y*v.x + u.y*v.y};
}
Int norm(Point v) { return v.x*v.x + v.x*v.y + v.y*v.y; }
Int cross(Point u, Point v) { return u.x*v.y - u.y*v.x; }
const std::array<Point,6> directions{{{1,0}, {0,1}, {-1,1}, {-1,0}, {0,-1}, {1,-1}}};
using Polygon = std::vector<Point>;
using Runs = std::array<Int,9>;
void require(bool condition, const char* message) {
    if (!condition) throw std::logic_error(message);
}

Polygon convex_hull(Polygon points) {
    std::sort(points.begin(), points.end());
    points.erase(std::unique(points.begin(), points.end()), points.end());
    if (points.size() <= 2) return points;
    Polygon hull;
    auto append = [&](Point p, std::size_t start) {
        while (hull.size() >= start + 2 &&
               cross(hull.back() - hull[hull.size()-2], p - hull.back()) <= 0)
            hull.pop_back();
        hull.push_back(p);
    };
    for (Point p : points) append(p, 0);
    auto start = hull.size() - 1;
    for (int i = static_cast<int>(points.size())-2; i >= 0; --i)
        append(points[i], start);
    hull.pop_back();
    return hull;
}

struct Board {
    Int a, b, c;
    Int p() const { return a+2*b; }
    Int q() const { return 2*a+b; }
    Int run_limit() const { return a*p()/c; }
    Int area_bound() const { return p()*q()*a*b/(2*c*c); }
    Point third_direction() const { return {a*a-b*b, b*q()}; }

    bool within_diameter(const Polygon& polygon) const {
        for (std::size_t i=0; i<polygon.size(); ++i)
            for (std::size_t j=0; j<i; ++j)
                if (norm(polygon[i]-polygon[j])*c*c > a*a*p()*p()) return false;
        return true;
    }
    bool fits_at(const Polygon& vertices, Point rotation) const {
        // The rotation is the nonzero complex integer divided by its modulus.
        const auto [X, Y] = a*p()*third_direction();
        const Int F = c*c*c*c, D = c*Y;
        Int min_i=0, min_j=0, max_sum=0;
        bool first = true;
        for (Point v : vertices) {
            Point w = product(rotation, v);
            Int i = Y*w.x - X*w.y, j = F*w.y;
            if (first) { min_i=i; min_j=j; max_sum=i+j; first=false; }
            else {
                min_i=std::min(min_i,i); min_j=std::min(min_j,j);
                max_sum=std::max(max_sum,i+j);
            }
        }
        Int cost = max_sum-min_i-min_j;
        require(cost>=0 && norm(rotation)>0, "invalid support cost or rotation");
        return Wide(cost)*cost <= Wide(D)*D*norm(rotation);
    }
    bool fits(const Polygon& hull, Point& witness_rotation) const {
        const Point side = third_direction();
        const std::array<Point,3> sides{{{1,0}, side, product({0,1},side)}};
        for (std::size_t i=0; i<hull.size(); ++i) {
            Point edge = hull[(i+1)%hull.size()]-hull[i];
            for (Point s : sides) {
                Point r = product(s, conjugate(edge));
                for (Point rotation : {r, -1*r}) {
                    if (fits_at(hull,rotation)) { witness_rotation=rotation; return true; }
                }
            }
        }
        return false;
    }
};

struct Counts { Int tried=0, diameter=0, fit=0; };
struct Scan {
    Board board;
    Int lo, hi; // K = number of upward grid cells, also number of downward cells
    std::array<Counts,3> counts{};
    Int best=0;
    Runs witness{};
    Point rotation{};

    void consider(int turn, const Runs& lengths, Int area) {
        ++counts[turn].tried;
        Polygon polygon;
        Point end{0,0};
        Int double_area=0;
        for (int j=0; j<=6+turn; ++j) {
            if (lengths[j]==0) continue;
            polygon.push_back(end);
            Point next=end+lengths[j]*directions[j%6];
            double_area+=cross(end,next);
            end=next;
        }
        require(end==Point{0,0} && double_area==2*area, "area identity or closure failed");
        if (!board.within_diameter(polygon)) return;
        ++counts[turn].diameter;
        Point r;
        if (!board.fits(convex_hull(polygon),r)) return;
        ++counts[turn].fit;
        if (area>best) { best=area; witness=lengths; rotation=r; }
    }
    void run() {
        const Int L=board.run_limit();
        for (Int A=1; A<=L; ++A) for (Int B=0; B<=L; ++B) for (Int C=0; C<=L; ++C) {
            const Int hex=A*B+A*C+B*C;
            for (Int x=1; x<=A; ++x) for (Int y=0; y<=B; ++y) {
                const Int first=hex-x*(B-y);
                if (first<lo) continue;
                if (first<=hi && y<B) consider(1,{x,y,C,A,B,C,A-x,B-y},first);
                // At a -120 degree turn the last run has length t=C-z>0.
                const Int last_min = first>hi ? (first-hi+x+y-1)/(x+y) : 1;
                const Int last_max = std::min(C,(first-lo)/(x+y));
                for (Int t=last_min; t<=last_max; ++t)
                    consider(2,{x,y,C-t,A,B,C,A-x,B-y,t},first-(x+y)*t);
            }
        }
    }
};

void print_witness(const Scan& scan) {
    std::cout<<"K="<<scan.best<<" runs";
    for (Int length : scan.witness) std::cout<<' '<<length;
    std::cout<<" rotation "<<scan.rotation.x<<' '<<scan.rotation.y<<'\n';
}

int main(int argc, char** argv) {
    bool capacity=argc==2 && std::string(argv[1])=="--capacity";
    if (argc!=1 && !capacity) { std::cerr<<"usage: check_cycles [--capacity]\n"; return 2; }
    const std::array<Board,3> boards{{{5,3,7},{33,7,37},{35,13,43}}};
    for (Board board : boards) {
        const Int tiles=board.p()*board.q(), needed=board.a*board.b;
        Scan test{board,needed,needed};
        test.run();
        for(int t : {1,2}) {
            auto result=test.counts[t];
            std::cout<<tiles<<" turn "<<-60*t<<" generated "<<result.tried
                     <<" diameter "<<result.diameter<<" fit "<<result.fit<<'\n';
        }
        require(test.counts[1].fit==0, "unexpected -60 degree placement");
        require(test.counts[2].fit==(tiles==143 ? 3 : 0), "unexpected -120 degree count");
        if(test.best) print_witness(test);
        if(capacity && tiles!=143) {
            const Int low=tiles==3431 ? 193 : 432;
            Scan range{board,low,board.area_bound()};
            range.run();
            require(range.best==low, "unexpected exact capacity");
            std::cout<<tiles<<" capacity scan "; print_witness(range);
        }
    }
}
