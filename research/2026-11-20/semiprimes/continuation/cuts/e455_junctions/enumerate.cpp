// Enumerate straight three-arm junctions in the side-455 equilateral triangle.
// Adapted from the project archive, cuts/three_regions/enumerate_stars.cpp.
#include <algorithm>
#include <array>
#include <cassert>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <tuple>
#include <vector>

using I = std::int64_t;
using Wide = __int128_t;
struct Point { I x, y; };
Point operator+(Point u, Point v) { return {u.x + v.x, u.y + v.y}; }
Point operator-(Point u, Point v) { return {u.x - v.x, u.y - v.y}; }
Point operator*(Point u, I n) { return {u.x*n, u.y*n}; }
Point multiply(Point u, Point v) {
    return {u.x*v.x - u.y*v.y, u.x*v.y + u.y*v.x + u.y*v.y};
}
Point rotate(Point u) { return {-u.y, u.x + u.y}; }
I det(Point u, Point v) { return u.x*v.y - u.y*v.x; }
Wide wide_det(Point u, Point v) { return Wide(u.x)*v.y - Wide(u.y)*v.x; }
int sign(int j) { return j % 2 == 0 ? 1 : -1; }
struct Ray { int height, phase; Point step; };
struct Site { Point point; I area, first, second; };
struct Arm { I x, y; std::uint16_t site, length; std::uint8_t direction; };

int main() {
    constexpr int a=35,b=13,c=43;
    constexpr int width=455,height=455;
    std::array<Point,3> board{{{0,0},{width,0},{0,height}}};
    std::array<int,3> lengths{width,width,height};
    I scale = I(c)*c*c*c*c;
    std::vector<Ray> directions;
    for (int h = -5; h <= 5; ++h) {
        Point d{1,0};
        I den = 1;
        for (int n = 0; n < std::abs(h); ++n) {
            d = multiply(d,h < 0 ? Point{a+b,-b} : Point{a,b});
            den *= c;
        }
        d = d*(scale/den);
        for (int j = 0; j < 6; ++j, d=rotate(d)) directions.push_back({h,j,d});
    }
    const int diameter = *std::max_element(lengths.begin(),lengths.end());
    std::vector<bool> coin(diameter+1);
    coin[0] = true;
    for (int i = 1; i <= diameter; ++i)
        for (int s : {a,b,c}) if (i >= s && coin[i-s]) coin[i] = true;

    std::vector<Site> sites;
    std::vector<Arm> arms;
    I area = 0, first = 0, second = 0;
    for (int k = 0; k < 3; ++k) {
        Point u = board[k], v = board[(k+1)%3], edge = v-u;
        int len = lengths[k];
        auto wall = std::find_if(directions.begin(),directions.end(),[&](Ray r) {
            return r.step.x*len == edge.x*scale && r.step.y*len == edge.y*scale;
        });
        assert(wall != directions.end());
        for (int offset = 0; offset < len; ++offset) {
            if (!coin[offset] || !coin[len-offset]) continue;
            Point p = u*scale + wall->step*offset;
            auto site = sites.size();
            assert(site < 65536);
            sites.push_back({p,area+det(u,p),first+sign(wall->phase)*offset,
                             second+sign(wall->phase+wall->height)*offset});
            for (std::size_t ri = 0; ri < directions.size(); ++ri) {
                Ray r = directions[ri];
                int m = (r.phase-wall->phase+6)%6, n = m+r.height-wall->height;
                if (m>3 || n<0 || n>3 || m+n==0 || m+n==6) continue;
                I limit = diameter;
                for (int side = 0; side < 3; ++side) {
                    Point e = board[(side+1)%3]-board[side];
                    I start = det(e,p-board[side]*scale), slope = det(e,r.step);
                    assert(start >= 0);
                    if (slope <= 0 && start == 0) limit = 0;
                    else if (slope < 0) limit = std::min(limit,(start-1)/(-slope));
                }
                for (int l = 1; l <= limit; ++l) if (coin[l]) {
                    Point center = p+r.step*l;
                    arms.push_back({center.x,center.y,std::uint16_t(site),
                                    std::uint16_t(l),std::uint8_t(ri)});
                }
            }
        }
        area += det(u,v)*scale;
        first += sign(wall->phase)*len;
        second += sign(wall->phase+wall->height)*len;
    }
    std::sort(arms.begin(),arms.end(),[](Arm p, Arm q) {
        return std::tie(p.x,p.y,p.site,p.direction)<std::tie(q.x,q.y,q.site,q.direction);
    });
    auto sector = [&](Arm p, Arm q) {
        if (p.site == q.site) return false;
        Point center{p.x,p.y};
        Site s=sites[p.site], t=sites[q.site];
        Ray r=directions[p.direction], f=directions[q.direction];
        if (wide_det(f.step,r.step)>=0) return false;
        bool wraps=q.site<p.site;
        Wide total = Wide(t.area-s.area+(wraps?area:0))*scale+wide_det(t.point-s.point,center);
        Wide unit = Wide(a)*b*scale*scale;
        if (total<=0 || total%unit) return false;
        I mass=I(total/unit);
        I x=t.first-s.first+(wraps?first:0)+sign(f.phase)*q.length-sign(r.phase)*p.length;
        I y=t.second-s.second+(wraps?second:0)
            +sign(f.phase+f.height)*q.length-sign(r.phase+r.height)*p.length;
        for (auto [sum,divisor] : {std::pair<I,I>{x,a-b-c},{y,a-b+c}}) {
            if (sum%divisor || std::abs(sum/divisor)>mass || (sum/divisor-mass)%2)
                return false;
        }
        return true;
    };
    for (std::size_t begin=0; begin<arms.size();) {
        std::size_t end=begin+1;
        while (end<arms.size() && arms[end].x==arms[begin].x && arms[end].y==arms[begin].y)
            ++end;
        for (auto i=begin; i<end; ++i) for (auto j=i+1; j<end; ++j) {
            if (!sector(arms[i],arms[j])) continue;
            for (auto k=j+1; k<end; ++k) {
                if (!sector(arms[j],arms[k]) || !sector(arms[k],arms[i])) continue;
                std::cout<<arms[i].x<<" "<<arms[i].y<<" "<<scale;
                for (auto index : {i,j,k}) {
                    auto s=sites[arms[index].site];
                    std::cout<<" "<<s.point.x<<" "<<s.point.y;
                }
                std::cout<<"\n";
            }
        }
        begin=end;
    }
}
