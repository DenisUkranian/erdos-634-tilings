// Exact single-offset gate-profile filter. This is a necessary projection,
// not a geometric tiling solver. Input is the existing serialized cut format.
// A special upward gate has offset c; the other 2c-1 gates have offset 0.
#include <algorithm>
#include <chrono>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <limits>
#include <vector>
using I=std::int64_t;
struct Cut { I D; std::vector<I> up,down; };
struct Current { int r; I q; };
int c,d,cap,maxP,maxM,ncuts,limit;
I visited=0,reserves=0,survivors=0;
std::vector<int> positives;
std::vector<Cut> cuts;
std::vector<I> rejected;
bool stopped=false;
std::ofstream pool;
I maxcorr(const std::vector<I>& w,const std::vector<Current>& q){
 I best=std::numeric_limits<I>::min();
 for(int shift=0;shift<c;shift++){
  I x=0;for(auto a:q)x+=a.q*w[(a.r+shift)%c];best=std::max(best,x);
 }
 return best;
}
void examine(int neg){
 if(stopped)return;
 int p=positives.size(),m=neg>=0,u=m-p,q0=c+d*u;
 if(q0 < -c || q0 > cap)return;
 visited++;
 if(std::max(q0,0)+d*p>2*c || std::max(-q0,0)+d*m>c)return;
 reserves++;
 std::vector<Current> up{{0,q0}},down;
 auto add=[&](int index,int charge){
  auto &q=index<c-1?up:down;
  int r=index<c-1?index+1:index-(c-1);
  for(auto &x:q)if(x.r==r){x.q+=d*charge;return;}
  q.push_back({r,d*charge});
 };
 for(int i:positives)add(i,1);
 if(neg>=0)add(neg,-1);
 for(int k=0;k<ncuts;k++){
  I score=maxcorr(cuts[k].up,up)+maxcorr(cuts[k].down,down);
  if(score>3*c*cuts[k].D){rejected[k]++;return;}
 }
 survivors++;
 if(pool){pool<<u;for(int i=0;i<maxP;i++)pool<<' '<<(i<p?positives[i]:-1);pool<<' '<<neg<<'\n';}
 if(limit>0){
  std::cout<<"{\"special_up_charge\":"<<u<<",\"positive_indices\":[";
  for(int i=0;i<p;i++){if(i)std::cout<<',';std::cout<<positives[i];}
  std::cout<<"],\"negative_index\":"<<neg<<"}"<<std::endl;
  if(survivors>=limit)stopped=true;
 }
}
void generate(int count,int first){
 if(stopped)return;
 if(count==0){
  examine(-1);
  if(maxM)for(int neg=0;neg<2*c-1&&!stopped;neg++)
   if(std::find(positives.begin(),positives.end(),neg)==positives.end())examine(neg);
  return;
 }
 for(int k=first;k<2*c-1&&!stopped;k++){
  int copies=std::count(positives.begin(),positives.end(),k);
  if((copies+1)*d>cap)continue;
  positives.push_back(k);generate(count-1,k);positives.pop_back();
 }
}
int main(int argc,char **argv){
 if(!(std::cin>>c>>d>>cap>>maxP>>maxM>>ncuts>>limit))return 2;
 if(c<=0||d<=0||cap<=0||maxP!=2*c/d||maxM!=1||c/d!=1)return 3;
 cuts.resize(ncuts);rejected.assign(ncuts,0);
 for(auto &x:cuts){std::cin>>x.D;x.up.resize(c);x.down.resize(c);for(auto &v:x.up)std::cin>>v;for(auto &v:x.down)std::cin>>v;}
 if(!std::cin)return 4;
 if(argc>1)limit=std::stoi(argv[1]);
 if(argc>2){pool.open(argv[2]);if(!pool)return 5;}
 auto start=std::chrono::steady_clock::now();
 for(int p=0;p<=maxP&&!stopped;p++)generate(p,0);
 double seconds=std::chrono::duration<double>(std::chrono::steady_clock::now()-start).count();
 std::cout<<"{\"summary\":true,\"exhaustive\":"<<(stopped?"false":"true")
 <<",\"visited\":"<<visited<<",\"reserve_passed\":"<<reserves<<",\"cut_passed\":"<<survivors<<",\"seconds\":"<<seconds<<",\"rejected\":[";
 for(int k=0;k<ncuts;k++){if(k)std::cout<<',';std::cout<<rejected[k];}
 std::cout<<"]}"<<std::endl;
}
