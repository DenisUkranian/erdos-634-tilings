// Independent geometric enumeration and scatter-bound replay of packed-band
// forcing-row traces. No propagation queue, no copied producer scanline formula.
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
using U64=uint64_t;using I64=int64_t;
struct P {int x,y;};
P sub(P a,P b){return{a.x-b.x,a.y-b.y};}P add(P a,P b){return{a.x+b.x,a.y+b.y};}P scale(P a,int k){return{k*a.x,k*a.y};}
P cmul(P a,P b){return{a.x*b.x-a.y*b.y,a.x*b.y+a.y*b.x+a.y*b.y};}
P cpow(P a,int n){P b{1,0};for(int i=0;i<n;i++)b=cmul(b,a);return b;}
I64 det(P a,P b){return I64(a.x)*b.y-I64(a.y)*b.x;}I64 norm(P a){return I64(a.x)*a.x+I64(a.x)*a.y+I64(a.y)*a.y;}
void need(bool c,const string&s){if(!c)throw runtime_error(s);}
pair<int,int> direction(P d){int q=gcd(abs(d.x),abs(d.y));need(q>0,"zero direction");d.x/=q;d.y/=q;if(d.x<0||(d.x==0&&d.y<0)){d.x=-d.x;d.y=-d.y;}return{d.x,d.y};}
struct Shape{array<P,3>p;array<int,3>d;};
struct End {int shape,vertex,coefficient;};
int main(int argc,char**argv){try{
 need(argc==6,"usage: L U trace.rows.bin report.json expected_placements");int L=stoi(argv[1]),U=stoi(argv[2]);need(L<=0&&U>=0&&U>=L&&U-L<=3,"auditor currently up to four heights");U64 expected=stoull(argv[5]);
 P factor=cmul(cpow({2,1},-L),cpow({3,-1},U));I64 normfactor=norm(factor);
 array<P,3> target{P{0,0},scale(factor,30),cmul(factor,{0,30})};int xmin=0,xmax=0,ymin=0,ymax=0;
 for(P p:target){xmin=min(xmin,p.x);xmax=max(xmax,p.x);ymin=min(ymin,p.y);ymax=max(ymax,p.y);}
 auto inside=[&](P p){for(int e=0;e<3;e++)if(det(sub(target[(e+1)%3],target[e]),sub(p,target[e]))<0)return false;return true;};
 // Brute exact half-plane containment over the bounding box independently
 // constructs dense scanline indices, avoiding producer ceil/floor formulas.
 vector<P> point;vector<int> left(ymax-ymin+1,1),right(ymax-ymin+1,0);vector<U64> offset(ymax-ymin+2,0);
 for(int y=ymin;y<=ymax;y++){int yy=y-ymin;offset[yy]=point.size();bool begun=false,ended=false;for(int x=xmin;x<=xmax;x++){
  if(inside({x,y})){need(!ended,"nonconvex scanline");if(!begun){left[yy]=x;begun=true;}right[yy]=x;point.push_back({x,y});}
  else if(begun)ended=true;
 }offset[yy+1]=point.size();}
 auto index=[&](P p)->I64{int yy=p.y-ymin;if(yy<0||yy>=int(left.size())||p.x<left[yy]||p.x>right[yy])return -1;return offset[yy]+p.x-left[yy];};
 array<P,6> roots{P{1,0},P{0,1},P{-1,1},P{-1,0},P{0,-1},P{1,-1}};
 map<pair<int,int>,int> directions;vector<pair<int,int>> direction_values;vector<Shape> shapes;
 for(int h=L;h<=U;h++){P unit=cmul(cpow({2,1},h-L),cpow({3,-1},U-h));need(norm(unit)==normfactor,"wrong unit norm");for(int flip=0;flip<2;flip++)for(int r=0;r<6;r++){
  Shape s;s.p={P{0,0},scale(cmul(unit,roots[r]),flip?5:3),scale(cmul(unit,roots[(r+2)%6]),flip?3:5)};need(det(s.p[1],s.p[2])==15*normfactor,"wrong area");array<I64,3> q;
  for(int e=0;e<3;e++){P d=sub(s.p[(e+1)%3],s.p[e]);q[e]=norm(d);auto key=direction(d);if(!directions.count(key)){int k=directions.size();directions[key]=k;direction_values.push_back(key);}s.d[e]=directions.at(key);}
  sort(q.begin(),q.end());need(q==array<I64,3>{9*normfactor,25*normfactor,49*normfactor},"wrong side norm");shapes.push_back(s);
 }}
 int ns=shapes.size(),nd=directions.size();U64 np=point.size(),nv=np*ns,nr=np*nd;
 need(nr<=UINT32_MAX,"trace row width exceeded");vector<vector<End>> ends(nd);
 for(int s=0;s<ns;s++)for(int e=0;e<3;e++){ends[shapes[s].d[e]].push_back({s,e,1});ends[shapes[s].d[e]].push_back({s,(e+1)%3,-1});}
 array<U64,3> corners;array<int,3> targetdir;for(int e=0;e<3;e++){I64 k=index(target[e]);need(k>=0,"missing target corner");corners[e]=k;targetdir[e]=directions.at(direction(sub(target[(e+1)%3],target[e])));}
 auto rhs=[&](U64 row){U64 p=row/nd;int d=row%nd,v=0;for(int e=0;e<3;e++){if(p==corners[e]&&d==targetdir[e])v++;if(p==corners[(e+1)%3]&&d==targetdir[e])v--;}return v;};
 vector<uint8_t> state(nv,0);vector<int16_t> lower(nr,0),upper(nr,0);
 auto each_row=[&](U64 variable,auto work){P p=point[variable/ns];auto&s=shapes[variable%ns];for(int e=0;e<3;e++){I64 a=index(add(p,s.p[e])),b=index(add(p,s.p[(e+1)%3]));if(a<0||b<0)throw runtime_error("invalid selected edge endpoint");work(U64(a)*nd+s.d[e],1);work(U64(b)*nd+s.d[e],-1);}};
 U64 valid=0;
 for(U64 p=0;p<np;p++){for(int s=0;s<ns;s++){if(index(add(point[p],shapes[s].p[1]))<0||index(add(point[p],shapes[s].p[2]))<0)continue;U64 variable=p*ns+s;state[variable]=1;valid++;each_row(variable,[&](U64 row,int sign){if(sign>0)upper[row]++;else lower[row]--;});}if(p%2000000==0)cerr<<"enumerated points "<<p<<"/"<<np<<"\n";}
 need(valid==expected,"independent placement count differs");cerr<<"Independent placements="<<valid<<" rows="<<nr<<"\n";
 for(U64 row=0;row<nr;row++){int b=rhs(row);need(lower[row]<=b&&b<=upper[row],"initial contradiction");}
 ifstream trace(argv[3],ios::binary);need(bool(trace),"no trace");uint32_t encoded;U64 checkedrows=0,assigned=0,ones=0,bad=UINT64_MAX;
 while(trace.read(reinterpret_cast<char*>(&encoded),4)){
  U64 row=encoded;need(row<nr,"trace row outside range");int b=rhs(row),lo=lower[row],hi=upper[row];need(lo<=b&&b<=hi,"preceding contradiction escaped detection");need(b==lo||b==hi,"forcing row not tight");
  P endpoint=point[row/nd];bool changed=false;checkedrows++;
  for(End end:ends[row%nd]){I64 anchor=index(sub(endpoint,shapes[end.shape].p[end.vertex]));if(anchor<0)continue;U64 variable=U64(anchor)*ns+end.shape;if(state[variable]!=1)continue;changed=true;int value=b==lo?(end.coefficient<0):(end.coefficient>0);state[variable]=value?3:2;assigned++;ones+=value;
   each_row(variable,[&](U64 incident,int sign){lower[incident]+=sign*value-min(0,sign);upper[incident]+=sign*value-max(0,sign);int rr=rhs(incident);if(rr<lower[incident]||rr>upper[incident])bad=incident;});
   if(bad!=UINT64_MAX)break;
  }
  need(changed,"trace row forced no variable");if(bad!=UINT64_MAX)break;
  if(checkedrows%10000000==0)cerr<<"replayed forcing rows "<<checkedrows<<" assigned "<<assigned<<"\n";
 }
 need(bad!=UINT64_MAX,"no independently reproduced contradiction");P p=point[bad/nd];auto d=direction_values[bad%nd];ofstream out(argv[4]);need(bool(out),"report write");
 out<<"{\"status\":\"PASS\",\"L\":"<<L<<",\"U\":"<<U<<",\"placements\":"<<valid<<",\"points\":"<<np<<",\"rows_checked\":"<<checkedrows<<",\"assignments_checked\":"<<assigned<<",\"ones\":"<<ones<<",\"terminal_point\":["<<p.x<<","<<p.y<<"],\"terminal_direction\":["<<d.first<<","<<d.second<<"],\"lower\":"<<lower[bad]<<",\"upper\":"<<upper[bad]<<",\"rhs\":"<<rhs(bad)<<",\"full_60_decided\":false}\n";
 cerr<<"PASS: "<<lower[bad]<<" <= "<<rhs(bad)<<" <= "<<upper[bad]<<" is false after "<<assigned<<" assignments\n";
 return 0;
 }catch(const exception&e){cerr<<"FAIL: "<<e.what()<<"\n";return 1;}}
