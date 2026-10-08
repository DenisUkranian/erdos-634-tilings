// Independent verifier for complete E45 placement deletions, no search/queue.
// Geometry uses rational intersections of horizontal lines with polygon edges.
// Each trace range is checked term by term, without the producer's unions.
#include <algorithm>
#include <array>
#include <chrono>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <map>
#include <numeric>
#include <stdexcept>
#include <vector>
using namespace std; using I=int64_t; using U=uint64_t;
void need(bool ok,const char*message){if(!ok)throw runtime_error(message);}
struct P{I x,y;};
P operator+(P a,P b){return {a.x+b.x,a.y+b.y};}
P operator-(P a,P b){return {a.x-b.x,a.y-b.y};}
P cmul(P a,P b){return {a.x*b.x-a.y*b.y,a.x*b.y+a.y*b.x+a.y*b.y};}
P times(P a,I b){return {a.x*b,a.y*b};}
P power(P a,int n){need(n>=0,"negative exponent");P r{1,0};while(n--){r=cmul(r,a);}return r;}
I cross(P a,P b){return a.x*b.y-a.y*b.x;}
I norm(P a){return a.x*a.x+a.x*a.y+a.y*a.y;}
I down(I n,I d){need(d>0,"denominator");I q=n/d,r=n%d;return q-(r<0);}
I up(I n,I d){return -down(-n,d);}
struct Rat{I n,d;};
bool lessrat(Rat a,Rat b){return (__int128)a.n*b.d<(__int128)b.n*a.d;}
struct Run{int lo,hi;}; using Runs=vector<Run>;
struct Event{int tile;int dx,dy;int sign;};
int32_t read32(const unsigned char*p){uint32_t n=uint32_t(p[0])|(uint32_t(p[1])<<8)|(uint32_t(p[2])<<16)|(uint32_t(p[3])<<24);return int32_t(n);}
int main(int argc,char**argv){try{
 need(argc==11,"usage L U rotation trace remaining report expectedCount expectedRemaining expectedRecords label");
 int L=stoi(argv[1]),H=stoi(argv[2]),rotation=stoi(argv[3]);
 need(L<=0&&H>=0&&H-L<=8&&rotation>=0&&rotation<6,"band range");
 U expected=stoull(argv[7]),expectedRemaining=stoull(argv[8]),expectedRecords=stoull(argv[9]);
 const array<P,6> roots{{{1,0},{0,1},{-1,1},{-1,0},{0,-1},{1,-1}}};
 P frame=cmul(cmul(power({2,1},-L),power({3,-1},H)),roots[rotation]);
 I scaleNorm=1;for(int k=L;k<H;k++)scaleNorm*=7;
 need(norm(frame)==scaleNorm,"frame norm");
 array<P,3> target{{{0,0},times(frame,45),times(cmul(frame,{0,1}),45)}};
 int ymin=0,ymax=0,xmin=0,xmax=0;for(P p:target){ymin=min<I>(ymin,p.y);ymax=max<I>(ymax,p.y);xmin=min<I>(xmin,p.x);xmax=max<I>(xmax,p.x);}
 int height=ymax-ymin+1;vector<int> left(height),right(height);U points=0;
 for(int iy=0;iy<height;iy++){
  I y=ymin+iy;vector<Rat> intersections;
  for(int k=0;k<3;k++){
   P a=target[k],b=target[(k+1)%3];
   if(a.y==b.y){if(y==a.y){intersections.push_back({a.x,1});intersections.push_back({b.x,1});}continue;}
   if(y<min(a.y,b.y)||y>max(a.y,b.y))continue;
   I d=b.y-a.y,n=a.x*d+(b.x-a.x)*(y-a.y);if(d<0){n=-n;d=-d;}intersections.push_back({n,d});
  }
  need(!intersections.empty(),"horizontal target slice missing");
  auto mm=minmax_element(intersections.begin(),intersections.end(),lessrat);
  left[iy]=up(mm.first->n,mm.first->d);right[iy]=down(mm.second->n,mm.second->d);
  if(right[iy]>=left[iy])points+=U(right[iy]-left[iy]+1);
 }
 vector<array<P,3>> templates;vector<array<int,3>> tileDirections;map<pair<I,I>,int> lookup;vector<vector<Event>> events;
 auto direction=[&](P e){I g=gcd(e.x,e.y);need(g!=0,"zero edge");e.x/=g;e.y/=g;if(e.x<0||(e.x==0&&e.y<0)){e.x=-e.x;e.y=-e.y;}auto key=make_pair(e.x,e.y);auto it=lookup.find(key);if(it!=lookup.end())return it->second;int id=lookup.size();lookup[key]=id;events.emplace_back();return id;};
 for(int h=L;h<=H;h++){
  P unit=cmul(cmul(power({2,1},h-L),power({3,-1},H-h)),roots[rotation]);
  for(int mirror=0;mirror<2;mirror++)for(int r=0;r<6;r++){
   P u=cmul(unit,roots[r]);array<P,3> tri{{{0,0},times(u,mirror?5:3),times(cmul(u,{-1,1}),mirror?3:5)}};
   need(cross(tri[1],tri[2])==15*scaleNorm,"template area");
   array<I,3> n{{norm(tri[1]),norm(tri[2]-tri[1]),norm(tri[2])}};sort(n.begin(),n.end());need(n==array<I,3>{{9*scaleNorm,25*scaleNorm,49*scaleNorm}},"template congruence");
   array<int,3>d;int ti=templates.size();for(int k=0;k<3;k++)d[k]=direction(tri[(k+1)%3]-tri[k]);
   templates.push_back(tri);tileDirections.push_back(d);
   for(int k=0;k<3;k++){P a=tri[k],b=tri[(k+1)%3];events[d[k]].push_back({ti,int(a.x),int(a.y),1});events[d[k]].push_back({ti,int(b.x),int(b.y),-1});}
  }
 }
 int nt=templates.size(),nd=events.size();vector<vector<pair<P,int>>> specials(nd);
 for(int k=0;k<3;k++){int d=direction(target[(k+1)%3]-target[k]);need(d<nd,"new target direction");specials[d].push_back({target[k],1});specials[d].push_back({target[(k+1)%3],-1});}
 vector<Runs> placements(size_t(nt)*height);U count=0;
 for(int t=0;t<nt;t++)for(int y=0;y<height;y++){
  int lo=left[y],hi=right[y];
  for(P v:templates[t]){I yy=I(y)+v.y;if(yy<0||yy>=height){hi=lo-1;break;}lo=max<I>(lo,I(left[yy])-v.x);hi=min<I>(hi,I(right[yy])-v.x);}
  if(lo<=hi){placements[size_t(t)*height+y].push_back({lo,hi});count+=U(hi-lo+1);}
 }
 need(count==expected,"independent placement count differs");cerr<<"initialized "<<count<<" placements in "<<height<<" rows\n";
 ifstream trace(argv[4],ios::binary);need(bool(trace),"trace unavailable");unsigned char raw[20];U records=0,removed=0;Runs replacement;
 while(trace.read((char*)raw,20)){
  int d=read32(raw),y=read32(raw+4),lo=read32(raw+8),hi=read32(raw+12),sign=read32(raw+16);
  need(d>=0&&d<nd&&y>=0&&y<height&&lo<=hi&&(sign==1||sign==-1),"invalid trace record");
  for(auto special:specials[d])need(!(special.first.y==y+ymin&&lo<=special.first.x&&special.first.x<=hi),"nonzero target row removed");
  for(Event e:events[d])if(e.sign!=sign){
   I yy=I(y)-e.dy;if(yy<0||yy>=height)continue;const Runs& runs=placements[size_t(e.tile)*height+yy];I a=I(lo)-e.dx,b=I(hi)-e.dx;
   auto it=lower_bound(runs.begin(),runs.end(),a,[](Run r,I x){return r.hi<x;});need(it==runs.end()||it->lo>b,"opposite-sign support survives in claimed cut");
  }
  for(Event e:events[d])if(e.sign==sign){
   I yy=I(y)-e.dy;if(yy<0||yy>=height)continue;Runs&runs=placements[size_t(e.tile)*height+yy];I a=I(lo)-e.dx,b=I(hi)-e.dx;
   auto first=lower_bound(runs.begin(),runs.end(),a,[](Run r,I x){return r.hi<x;});
   if(first==runs.end()||first->lo>b)continue;
   replacement.clear();replacement.reserve(runs.size()+1);
   for(Run r:runs){
    if(r.hi<a||r.lo>b){replacement.push_back(r);continue;}
    I dl=max<I>(r.lo,a),dh=min<I>(r.hi,b);need(dl<=dh,"intersection invariant");removed+=U(dh-dl+1);
    if(r.lo<dl)replacement.push_back({r.lo,int(dl-1)});
    if(dh<r.hi)replacement.push_back({int(dh+1),r.hi});
   }
   runs.swap(replacement);
  }
  records++;if(records%10000000==0)cerr<<"verified "<<records<<" trace ranges, removed "<<removed<<"\n";
 }
 need(trace.eof()&&trace.gcount()==0,"truncated trace");need(records==expectedRecords,"trace record count differs");
 ifstream expectedPool(argv[5]);need(bool(expectedPool),"remaining pool unavailable");int poolL,poolH;U poolN;expectedPool>>poolL>>poolH>>poolN;need(bool(expectedPool)&&poolL==L&&poolH==H&&poolN==expectedRemaining,"remaining pool header");
 U surviving=0;for(int t=0;t<nt;t++)for(int y=0;y<height;y++)for(Run r:placements[size_t(t)*height+y])for(int x=r.lo;x<=r.hi;x++){
  int tt,xx,yy;expectedPool>>tt>>xx>>yy;need(bool(expectedPool)&&tt==t&&xx==x&&yy==y+ymin,"remaining placement differs");surviving++;
 }
 string extra;need(!(expectedPool>>extra),"extra remaining placement");need(surviving==expectedRemaining&&count-removed==surviving,"remaining cardinality differs");
 ofstream out(argv[6]);need(bool(out),"output unavailable");out<<"{\"status\":\"PASS\",\"L\":"<<L<<",\"U\":"<<H<<",\"basis_rotation\":"<<rotation<<",\"independent_candidate_count\":"<<count<<",\"target_lattice_points\":"<<points<<",\"verified_range_records\":"<<records<<",\"verified_removed\":"<<removed<<",\"remaining\":"<<surviving<<",\"every_remaining_placement_matches\":true,\"opposite_support_checked_term_by_term\":true,\"all_arithmetic_exact\":true,\"result_is_reduction_not_infeasibility\":true}\n";cerr<<"PASS complete replay; remaining="<<surviving<<"\n";
 }catch(const exception&e){cerr<<"FAIL: "<<e.what()<<"\n";return 1;}}
