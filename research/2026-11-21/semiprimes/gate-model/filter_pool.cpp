// Apply additional exact translated gate cuts to a previously exhaustive pool.
#include <algorithm>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <limits>
#include <sstream>
#include <vector>
using I=std::int64_t;
struct Cut{I D;std::vector<I> up,down;};
struct Current{int r;I q;};
I correlation(const std::vector<I>&w,const std::vector<Current>&q,int c){
 I ans=std::numeric_limits<I>::min();
 for(int s=0;s<c;s++){I v=0;for(auto e:q)v+=e.q*w[(e.r+s)%c];ans=std::max(ans,v);}return ans;
}
int main(int argc,char**argv){
 if(argc!=3)return 2;
 int c,d,cap,maxP,maxM,K,unused;
 if(!(std::cin>>c>>d>>cap>>maxP>>maxM>>K>>unused))return 3;
 std::vector<Cut> cuts(K);
 for(auto&cut:cuts){std::cin>>cut.D;cut.up.resize(c);cut.down.resize(c);for(auto&x:cut.up)std::cin>>x;for(auto&x:cut.down)std::cin>>x;}
 if(!std::cin)return 4;
 std::ifstream in(argv[1]);std::ofstream out(argv[2]);if(!in||!out)return 5;
 I seen=0,kept=0,bestN=std::numeric_limits<I>::max(),bestD=1;
 std::vector<I> best;std::string line;
 std::vector<I> rejected(K,0);
 while(std::getline(in,line)){
  std::istringstream is(line);std::vector<I> row;I x;while(is>>x)row.push_back(x);
  if(row.size()!=static_cast<std::size_t>(maxP+3) && row.size()!=static_cast<std::size_t>(maxP+5))return 6;
  seen++;
  I u=row[0],v=row[1],q0=2*c+d*u,q1=-c+d*v;
  std::vector<Current> up{{0,q0}},down{{0,q1}};
  auto add=[&](int index,int sign){auto&z=index<c-1?up:down;int r=index%(c-1)+1;for(auto&e:z)if(e.r==r){e.q+=d*sign;return;}z.push_back({r,d*sign});};
  for(int i=0;i<maxP;i++)if(row[2+i]>=0)add(row[2+i],1);
  if(row[2+maxP]>=0)add(row[2+maxP],-1);
  I n=std::numeric_limits<I>::min()/2,den=1;
  if(row.size()==static_cast<std::size_t>(maxP+5)){n=row[maxP+3];den=row[maxP+4];}
  bool pass=true;
  for(int k=0;k<K;k++){
   I score=correlation(cuts[k].up,up,c)+correlation(cuts[k].down,down,c);
   if(score>cuts[k].D*3*c){rejected[k]++;pass=false;break;}
   if((__int128)score*den>(__int128)n*cuts[k].D){n=score;den=cuts[k].D;}
  }
  if(!pass)continue;
  kept++;
  for(int i=0;i<maxP+3;i++)out<<row[i]<<' ';out<<n<<' '<<den<<'\n';
  if((__int128)n*bestD<(__int128)bestN*den){best=row;bestN=n;bestD=den;}
 }
 if(kept){
  std::cout<<"{\"native_up\":"<<best[0]<<",\"native_down\":"<<best[1]<<",\"remote_positive_indices\":[";
  bool first=true;for(int i=0;i<maxP;i++)if(best[2+i]>=0){if(!first)std::cout<<',';first=false;std::cout<<best[2+i];}
  std::cout<<"],\"remote_negative_index\":"<<best[2+maxP]<<",\"current_lower_numerator\":"<<bestN<<",\"current_lower_denominator\":"<<bestD<<"}\n";
 }
 std::cout<<"{\"summary\":true,\"pool_input\":"<<seen<<",\"pool_survivors\":"<<kept<<",\"rejected\":[";
 for(int i=0;i<K;i++){if(i)std::cout<<',';std::cout<<rejected[i];}std::cout<<"]}\n";
}
