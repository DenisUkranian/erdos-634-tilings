// Independent exact geometric columns and disjoint residual search branches.
// Input: a b c total orbit_count, then one 12-entry inventory per orbit.
// This searches first-return kernels. The Python wrapper checks the separate
// component-size induction before interpreting an absent full population.
#include <algorithm>
#include <array>
#include <chrono>
#include <cstdint>
#include <iostream>
#include <limits>
#include <vector>

struct P { int x,y; };
P operator-(P a,P b){return {a.x-b.x,a.y-b.y};}
int cross(P a,P b){return a.x*b.y-a.y*b.x;}
int norm(P a){return a.x*a.x+a.x*a.y+a.y*a.y;}
const std::array<P,6> U={P{1,0},P{0,1},P{-1,1},P{-1,0},P{0,-1},P{1,-1}};
struct Col { int x,y,j,s,ori; std::array<int,4> row,val; };
class Search {
 public:
 int a,b,c,total,nrows; std::vector<Col> col;
 std::vector<std::vector<int>> inc;
 std::vector<int> residual,active,position,blocked,selected,answer;
 std::array<int,12> left{};
 int l1=0,remaining=0; std::uint64_t states=0; bool found=false;
 Search(int aa,int bb,int cc,int nn):a(aa),b(bb),c(cc),total(nn),nrows(3*c*c),inc(2*nrows),residual(nrows,0),position(nrows,-1) {
  for(int x=0;x<c;x++)for(int y=0;y<c;y++)for(int j=0;j<6;j++)for(int s:{-1,1}) {
   std::array<P,3> v={P{x,y},P{x-a*U[j].x,y-a*U[j].y},P{x+b*U[(j+s+6)%6].x,y+b*U[(j+s+6)%6].y}};
   if(cross(v[1]-v[0],v[2]-v[0])<0)std::swap(v[1],v[2]);
   Col C{x,y,j,s,2*j+(s==1),{}, {}};int z=0;
   for(int e=0;e<3;e++){
    P p=v[e],q=v[(e+1)%3],d=q-p;int n=norm(d);
    if(n==c*c)continue;
    if(n!=a*a && n!=b*b)throw "bad metric";
    int axis=-1;for(int i=0;i<3;i++)if(cross(d,U[i])==0)axis=i;
    if(axis<0)throw "missing short axis";
    auto row=[&](P p){int xx=((p.x%c)+c)%c,yy=((p.y%c)+c)%c;return axis*c*c+xx*c+yy;};
    C.row[z]=row(p);C.val[z++]=-1;C.row[z]=row(q);C.val[z++]=1;
   }
   if(z!=4)throw "wrong endpoint count";
   int id=col.size();col.push_back(C);
   for(int k=0;k<4;k++)inc[2*C.row[k]+(C.val[k]>0)].push_back(id);
  }
  blocked.assign(col.size(),0);
 }
 void addrow(int r,int delta){
  int old=residual[r],now=old+delta;l1+=std::abs(now)-std::abs(old);residual[r]=now;
  if(old==0 && now!=0){position[r]=active.size();active.push_back(r);}
  if(old!=0 && now==0){int p=position[r],last=active.back();active[p]=last;position[last]=p;active.pop_back();position[r]=-1;}
 }
 void addcol(int k,int sg){for(int z=0;z<4;z++)addrow(col[k].row[z],sg*col[k].val[z]);}
 void dfs(){
  ++states;
  if(active.empty()){
   if(remaining==0){found=true;answer=selected;}
   return;
  }
  if(remaining==0 || l1>4*remaining)return;
  std::vector<int> opts;std::size_t best=std::numeric_limits<std::size_t>::max();
  for(int r:active){
   if(std::abs(residual[r])>remaining)return;
   std::vector<int> here;
   for(int k:inc[2*r+(residual[r]<0)])if(left[col[k].ori]>0 && blocked[k]==0)here.push_back(k);
   if(here.empty())return;
   if(here.size()<best){best=here.size();opts=std::move(here);}
  }
  std::vector<int> forbidden;
  for(int k:opts){
   // Partition completions by their smallest eligible column at this row.
   --left[col[k].ori];--remaining;selected.push_back(k);addcol(k,1);
   dfs();addcol(k,-1);selected.pop_back();++remaining;++left[col[k].ori];
   ++blocked[k];forbidden.push_back(k);
   if(found)break;
  }
  for(int k:forbidden)--blocked[k];
 }
 void run(std::array<int,12> counts){
  left=counts;remaining=total;states=0;found=false;answer.clear();selected.clear();
  if(!active.empty() || l1!=0)throw "dirty replay";
  int ori=-1;for(int i=0;i<12;i++)if(counts[i]>0 && (ori<0 || counts[i]<counts[ori]))ori=i;
  int k=ori; // At anchor (0,0), generated orientation order is the first 12.
  --left[ori];--remaining;selected.push_back(k);addcol(k,1);dfs();addcol(k,-1);selected.pop_back();++remaining;++left[ori];
 }
};
int main(){
 int a,b,c,n,m;if(!(std::cin>>a>>b>>c>>n>>m))return 2;
 Search S(a,b,c,n);std::uint64_t total_states=0;bool all_absent=true;
 auto start=std::chrono::steady_clock::now();
 for(int i=0;i<m;i++){
  std::array<int,12> counts{};int sum=0,charge=0;
  for(int o=0;o<12;o++){std::cin>>counts[o];sum+=counts[o];int j=o/2,s=(o%2)?1:-1;charge+=counts[o]*s*((j%2)?-1:1);}
  if(sum!=n || charge!=0)return 3;
  S.run(counts);total_states+=S.states;
  std::cout<<"{\"index\":"<<i<<",\"states\":"<<S.states<<",\"found\":"<<(S.found?"true":"false");
  if(S.found){all_absent=false;std::cout<<",\"support\":[";bool first=true;for(int k:S.answer){auto C=S.col[k];if(!first)std::cout<<',';first=false;std::cout<<'['<<C.x<<','<<C.y<<','<<C.j<<','<<C.s<<']';}std::cout<<']';}
  std::cout<<"}\n"<<std::flush;
  if(S.found)break;
 }
 double sec=std::chrono::duration<double>(std::chrono::steady_clock::now()-start).count();
 std::cout<<"{\"all_inventories_absent\":"<<(all_absent?"true":"false")<<",\"states\":"<<total_states<<",\"seconds\":"<<sec<<"}\n";
}
