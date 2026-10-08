// Enumerate every (8,7,13) tile whose 120-degree vertex lies in either
// adjacent-band lattice: h=1 uses x-3y=0 mod13, h=-1 uses x+4y=0 mod13;
// h=0 uses their union. Coordinates have denominator13. This is restricted.
#include <array>
#include <fstream>
#include <iostream>
#include <map>
#include <vector>
using namespace std;struct P{int x,y;};P add(P a,P b){return {a.x+b.x,a.y+b.y};}P mul(P p,int n){return {p.x*n,p.y*n};}P rot(P p){return {-p.y,p.x+p.y};}bool inside(P p){return p.y>=0&&8*p.x>=7*p.y&&8*p.x+15*p.y<=1232*13;}struct T{array<int,3>v;int h;};
int main(int argc,char**argv){map<pair<int,int>,int> ids;vector<P>points;vector<T>ts;auto point=[&](P p){auto k=make_pair(p.x,p.y);auto it=ids.find(k);if(it!=ids.end())return it->second;int i=points.size();ids[k]=i;points.push_back(p);return i;};point({0,0});point({154*13,0});point({49*13,56*13});
for(int h=-1;h<=1;h++){P u=h==0?P{13,0}:h==1?P{8,7}:P{15,-7};vector<array<P,2>> shapes;for(int order=0;order<2;order++){P a=mul(u,order?7:8),b=mul(rot(rot(u)),order?8:7);for(int r=0;r<6;r++){shapes.push_back({a,b});a=rot(a);b=rot(b);}}
for(int y=0;y<=56*13;y++)for(int x=0;x<=154*13;x++){P p{x,y};if(!inside(p))continue;bool plus=(x-3*y)%13==0,minus=(x+4*y)%13==0;if(!(h==1?plus:h==-1?minus:plus||minus))continue;for(auto s:shapes){P a=add(p,s[0]),b=add(p,s[1]);if(inside(a)&&inside(b))ts.push_back({{point(p),point(a),point(b)},h});}}
}
ofstream f(argv[1]);f<<13<<' '<<points.size()<<' '<<ts.size()<<'\n';for(P p:points)f<<p.x<<' '<<p.y<<'\n';for(auto t:ts)f<<t.v[0]<<' '<<t.v[1]<<' '<<t.v[2]<<' '<<t.h<<" 0\n";cerr<<points.size()<<" points "<<ts.size()<<" tiles\n";}
