#pragma once
// Triangular lattice geometry and integral intersections with half-integral probes.
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

struct Line {int axis; I pos;};
std::vector<Line> probes(const Polygon& polygon,bool dense,I spacing=0) {
    if (!spacing) spacing=c;
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
        for (I left=lo,right=hi;left<right;left+=6*spacing,right-=6*spacing) {
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
