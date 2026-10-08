// Independent replay of endpoint-current propagation: scatter each geometric
// triangle's incidences into row bounds. No inverse-template row generator or
// propagation queue is used. A source assignment must have a currently tight
// incident equation, then all six row bounds are updated exactly.
#include <algorithm>
#include <array>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <map>
#include <numeric>
#include <stdexcept>
#include <string>
#include <vector>
using namespace std;
struct Point {int x,y;};
Point minusp(Point a,Point b){return {a.x-b.x,a.y-b.y};}
Point plusp(Point a,Point b){return {a.x+b.x,a.y+b.y};}
Point product(Point a,Point b){return {a.x*b.x-a.y*b.y,a.x*b.y+a.y*b.x+a.y*b.y};}
Point times(Point a,int n){return {n*a.x,n*a.y};}
int64_t det(Point a,Point b){return int64_t(a.x)*b.y-int64_t(a.y)*b.x;}
int64_t length2(Point a){return int64_t(a.x)*a.x+int64_t(a.x)*a.y+int64_t(a.y)*a.y;}
pair<int,int> line_direction(Point v){int g=gcd(abs(v.x),abs(v.y));if(!g)throw runtime_error("zero edge");v.x/=g;v.y/=g;if(v.x<0||(v.x==0&&v.y<0)){v.x=-v.x;v.y=-v.y;}return {v.x,v.y};}
void require(bool yes,const string& what){if(!yes)throw runtime_error(what);}
struct Shape {array<Point,3> vertex;array<int,3> direction;};
int main(int argc,char**argv){try{
 require(argc==4,"usage: replay_three_level CENTER ASSIGNMENTS.bin REPORT.json");
 int center=stoi(argv[1]);require(center==0||center==1,"center");
 array<Point,3> target=center==0?array<Point,3>{{{0,0},{2002,0},{637,728}}}:array<Point,3>{{{0,0},{2310,-1078},{1127,105}}};
 int left=target[0].x,right=left,bottom=target[0].y,top=bottom;
 for(Point p:target){left=min(left,p.x);right=max(right,p.x);bottom=min(bottom,p.y);top=max(top,p.y);}
 int width=right-left+1,height=top-bottom+1,points=width*height;
 auto pointid=[&](Point p){require(p.x>=left&&p.x<=right&&p.y>=bottom&&p.y<=top,"endpoint out of box");return(p.y-bottom)*width+p.x-left;};
 auto contains=[&](Point p){for(int e=0;e<3;e++)if(det(minusp(target[(e+1)%3],target[e]),minusp(p,target[e]))<0)return false;return true;};
 array<Point,6> sixth_roots={Point{1,0},Point{0,1},Point{-1,1},Point{-1,0},Point{0,-1},Point{1,-1}};
 vector<Shape> shape;map<pair<int,int>,int> direction_ids;
 for(Point unit:array<Point,3>{Point{15,-7},Point{13,0},Point{8,7}}){
  require(length2(unit)==169,"unit norm");
  for(int flip=0;flip<2;flip++)for(int r=0;r<6;r++){
   Shape s; s.vertex={Point{0,0},times(product(unit,sixth_roots[r]),flip?7:8),times(product(unit,sixth_roots[(r+2)%6]),flip?8:7)};
   require(det(s.vertex[1],s.vertex[2])==9464,"tile orientation or area");
   array<int64_t,3> lengths;for(int e=0;e<3;e++){Point d=minusp(s.vertex[(e+1)%3],s.vertex[e]);lengths[e]=length2(d);direction_ids[line_direction(d)]=0;}
   sort(lengths.begin(),lengths.end());require(lengths==array<int64_t,3>{49*169,64*169,169*169},"wrong tile sides");shape.push_back(s);
  }
 }
 require(shape.size()==36,"template number");int nd=0;vector<pair<int,int>> direction;
 for(auto& kv:direction_ids){kv.second=nd++;direction.push_back(kv.first);}require(nd==15,"direction number");
 for(auto& s:shape)for(int e=0;e<3;e++)s.direction[e]=direction_ids.at(line_direction(minusp(s.vertex[(e+1)%3],s.vertex[e])));
 vector<int16_t> lower(size_t(points)*nd,0),upper(size_t(points)*nd,0);
 vector<int8_t> rhs(size_t(points)*nd,0);vector<uint8_t> state(size_t(points)*36,0);
 auto incidences=[&](int variable,auto operation){int anchor=variable/36,o=variable%36;Point p{anchor%width+left,anchor/width+bottom};auto& s=shape[o];for(int e=0;e<3;e++){
  operation(pointid(plusp(p,s.vertex[e]))*nd+s.direction[e],1);
  operation(pointid(plusp(p,s.vertex[(e+1)%3]))*nd+s.direction[e],-1);
 }};
 for(int e=0;e<3;e++){auto key=line_direction(minusp(target[(e+1)%3],target[e]));require(direction_ids.count(key),"target direction");int d=direction_ids.at(key);rhs[pointid(target[e])*nd+d]++;rhs[pointid(target[(e+1)%3])*nd+d]--;}
 int valid=0;
 for(int y=bottom;y<=top;y++)for(int x=left;x<=right;x++){Point p{x,y};if(!contains(p))continue;int anchor=pointid(p);for(int o=0;o<36;o++){
  if(!contains(plusp(p,shape[o].vertex[1]))||!contains(plusp(p,shape[o].vertex[2])))continue;
  int variable=36*anchor+o;state[variable]=1;valid++;
  incidences(variable,[&](int row,int sign){if(sign==1)upper[row]++;else lower[row]--;});
 }}
 cerr<<"Independent valid placements="<<valid<<"\n";
 for(size_t row=0;row<rhs.size();row++)require(lower[row]<=rhs[row]&&rhs[row]<=upper[row],"initial contradiction: handle separately");
 ifstream in(argv[2],ios::binary);require(bool(in),"cannot read trace");int32_t encoded;uint64_t checked=0;int ones=0,bad=-1;
 while(in.read(reinterpret_cast<char*>(&encoded),4)){
  require(encoded!=0&&encoded!=INT32_MIN,"bad trace integer");int value=encoded>0?1:0,variable=abs(encoded)-1;
  require(variable>=0&&size_t(variable)<state.size()&&state[variable]==1,"trace repeats or invalid placement");
  bool justified=false;
  incidences(variable,[&](int row,int sign){if(value==0&&(sign==1?rhs[row]==lower[row]:rhs[row]==upper[row]))justified=true;if(value==1&&(sign==1?rhs[row]==upper[row]:rhs[row]==lower[row]))justified=true;});
  require(justified,"unjustified forced assignment at step "+to_string(checked));
  state[variable]=value?3:2;checked++;ones+=value;
  incidences(variable,[&](int row,int sign){lower[row]+=sign*value-min(0,sign);upper[row]+=sign*value-max(0,sign);if(rhs[row]<lower[row]||rhs[row]>upper[row])bad=row;});
  if(bad>=0)break;
 }
 require(bad>=0,"trace has no reproduced contradiction");int anchor=bad/nd;auto dir=direction[bad%nd];
 ofstream report(argv[3]);require(bool(report),"cannot write report");
 report<<"{\"status\":\"PASS\",\"scope\":\"independent complete three-height placement enumeration and forced-assignment replay\",\"center\":"<<center<<",\"placements\":"<<valid<<",\"assignments_checked\":"<<checked<<",\"forced_ones\":"<<ones<<",\"terminal_point\":["<<anchor%width+left<<","<<anchor/width+bottom<<"],\"terminal_direction\":["<<dir.first<<","<<dir.second<<"],\"lower\":"<<lower[bad]<<",\"upper\":"<<upper[bad]<<",\"rhs\":"<<int(rhs[bad])<<",\"full_154_decided\":false}\n";
 cerr<<"PASS after "<<checked<<" assignments: "<<lower[bad]<<" <= "<<int(rhs[bad])<<" <= "<<upper[bad]<<" is false\n";
 return 0;
 }catch(const exception& ex){cerr<<"FAIL: "<<ex.what()<<"\n";return 1;}}
