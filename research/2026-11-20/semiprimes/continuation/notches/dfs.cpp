#include <array>
#include <vector>
#include <map>
#include <set>
#include <algorithm>
#include <numeric>
#include <iostream>
#include <cstdlib>
#include <tuple>
#include <limits>
using namespace std;
using Z=long long; using W=__int128_t;
struct P { Z x,y; auto operator<=>(const P&)const=default;};
P operator+(P a,P b){return {a.x+b.x,a.y+b.y};}
P operator-(P a,P b){return {a.x-b.x,a.y-b.y};}
P operator*(Z t,P a){return {t*a.x,t*a.y};}
P rot(P a){return {-a.y,a.x+a.y};}
P mul(P a,P b){return {a.x*b.x-a.y*b.y,a.x*b.y+a.y*b.x+a.y*b.y};}
W cross(P a,P b){return W(a.x)*b.y-W(a.y)*b.x;}
P dir(P a){Z d=gcd(abs(a.x),abs(a.y));return {a.x/d,a.y/d};}
// A direction is an oriented primitive integer vector in the Eisenstein basis.
// All metric computations below compare integer squared norms.
W norm(P d){return W(d.x)*d.x+W(d.x)*d.y+W(d.y)*d.y;}
int exact_length(P d,Z den,int upper){
 W square=norm(d);
 int lo=0,hi=upper+1;
 while(lo<hi){int mid=(lo+hi)/2;if(W(mid)*mid*den*den<square)lo=mid+1;else hi=mid;}
 return lo<=upper&&W(lo)*lo*den*den==square?lo:-1;
}
using Tri=array<P,3>;using Edge=pair<P,P>;
struct Shape {Tri t;int h,sign,long_offset;};
int a,b,c,t,k,extra=0,extension=0,target,hlo,hhi;
Z nodes=0,limit,gridDen;
vector<array<int,7>> inventories; array<int,7> used{};
vector<array<int,14>> signed_inventories;array<int,14> signed_used{};
int sign_index(const Shape &s){return 2*(s.h+2)+(s.sign<0);}
struct DirectionalPopulation{array<int,7> total{},up{},down{};};
vector<DirectionalPopulation> directional;
array<int,7> usedup{},useddown{};
void count_chirality(const Shape &s,int delta){
 auto &v=s.long_offset==1?usedup:useddown;
 v[s.h+2]+=delta*s.sign;
}

map<P,vector<bool>> coins;
vector<P> outer;vector<Shape> chosen;
map<P,vector<Shape>> byout;
// Cache the fan routings on an open half-plane. An orientation is used
// at each ray and the sweep angle strictly increases.
map<pair<P,P>,bool> routing;
bool canfan(P source,P end){
 if(source==end)return true;
 if(cross(source,end)<=0)return false;
 auto key=make_pair(source,end);
 auto it=routing.find(key); if(it!=routing.end())return it->second;
 for(const auto &s:byout[source]){
  P mid=dir(s.t[2]);
  if(mid==end||(cross(mid,end)>0 && canfan(mid,end)))return routing[key]=true;
 }
 return routing[key]=false;
}
struct Step{int length;P left,right;auto operator<=>(const Step&)const=default;};
map<P,vector<Step>> along;
map<tuple<P,P,int>,vector<bool>> words;
// A clamped exposed edge is tiled end-to-end. Two tiles meeting on the edge
// leave a sector between their off-edge rays which must itself have a fan.
const vector<bool>& ends(P ray,P cap,int length){
 auto key=make_tuple(ray,cap,length);
 if(auto it=words.find(key);it!=words.end())return it->second;
 const auto &options=along[ray];
 vector<bool> valid(options.size());
 for(int i=0;i<(int)options.size();i++){
  const auto &v=options[i];
  if(v.length>length)continue;
  if(v.length==length){valid[i]=cap==P{0,0}||canfan(v.left,cap);continue;}
  const auto &prev=ends(ray,cap,length-v.length);
  for(int j=0;j<(int)options.size();j++)if(prev[j]&&canfan(v.left,options[j].right)){valid[i]=true;break;}
 }
 return words.emplace(key,move(valid)).first->second;
}
bool sideword(P ray,P cap,P next,int length){
 const auto& valid=ends(ray,cap,length);
 for(int j=0;j<(int)valid.size();j++)
  if(valid[j]&&(next==P{0,0}||canfan(next,along[ray][j].right)))return true;
 return false;
}

bool sep(const Tri &t,const Tri &v){
 for(int i=0;i<3;i++){P d=t[(i+1)%3]-t[i];bool ok=true;for(P q:v)if(cross(d,q-t[i])>0){ok=false;break;}if(ok)return true;}return false;
}
bool integral_contacts(P p,P q,const Tri &vertices,bool board_wall){
 P d=q-p;
 for(P v:vertices){
  if(v==p||v==q||cross(d,v-p)||v<min(p,q)||v>max(p,q))continue;
  int from=exact_length(v-p,gridDen,10000);
  if(from<0)return false;
  if(board_wall){
   P ray=dir(d);
   int to=exact_length(q-v,gridDen,10000);
   if(to<0||!coins.count(ray)||!coins.at(ray)[from]||!coins.at(ray)[to])return false;
  }
 }
 return true;
}
bool good(const Shape &s){for(int i=0;i<(int)outer.size();i++)for(auto q:s.t)if(cross(outer[(i+1)%outer.size()]-outer[i],q-outer[i])<0)return false;
#ifndef IGNORE_CONTACTS
 for(int i=0;i<(int)outer.size();i++)if(!integral_contacts(outer[i],outer[(i+1)%outer.size()],s.t,true))return false;
#endif
 for(const auto &v:chosen){
  if(!sep(s.t,v.t)&&!sep(v.t,s.t))return false;
#ifndef IGNORE_CONTACTS
  for(int i=0;i<3;i++)
   if(!integral_contacts(v.t[i],v.t[(i+1)%3],s.t,false)
    ||!integral_contacts(s.t[i],s.t[(i+1)%3],v.t,false))return false;
#endif
 }
 return true;}
vector<Edge> update(const vector<Edge> &old,const Tri &t){
 vector<Edge> z=old;
 for(int j=0;j<3;j++){
  P a=t[(j+1)%3],b=t[j],u=dir(b-a);if(u<P{0,0})u=-1*u;
  map<P,int> event;vector<Edge> keep;
  auto add=[&](P p,P q){event[p]++;event[q]--;};
  add(a,b);
  for(auto [p,q]:z){if(cross(q-p,u)||cross(p-a,u))keep.push_back({p,q});else add(p,q);}
  P prev{};int n=0;
  for(auto [cur,val]:event)if(val){
    if(n==1)keep.push_back({prev,cur});if(n==-1)keep.push_back({cur,prev});
    n+=val;if(abs(n)>1){cerr<<"invalid boundary";exit(3);}prev=cur;
  }
  z=move(keep);
 }
 return z;
}
bool dfs(const vector<Edge>&edges){
 nodes++;if(nodes%50000==0)cerr<<"nodes "<<nodes<<" depth "<<chosen.size()<<"\n";if(nodes>limit){cerr<<"budget "<<nodes<<"\n";exit(2);}
 if(chosen.size()>target)abort();
 if(chosen.size()==target){if(!edges.empty())abort();cout<<"YES "<<nodes<<"\n";for(auto &tile:chosen){for(P p:tile.t)cout<<p.x<<" "<<p.y<<" ";cout<<tile.h<<"\n";}return true;}
 map<P,vector<P>> in,out;
 for(auto [p,q]:edges){out[p].push_back(q-p);in[q].push_back(q-p);}
 bool populationOK=false;for(const auto &row:inventories){bool ok=true;for(int j=0;j<7;j++)if(used[j]>row[j])ok=false;if(ok){populationOK=true;break;}}if(!populationOK)return false;
#ifndef IGNORE_SIGNS
 bool signsOK=false;
 for(const auto &row:signed_inventories){
  bool ok=true;
  for(int j=0;j<14;j++)if(signed_used[j]>row[j]){ok=false;break;}
  if(ok){signsOK=true;break;}
 }
 if(!signsOK)return false;
#endif
#ifndef IGNORE_CHIRALITY
 bool directionOK=false;
 for(const auto &row:directional){
  bool ok=true;
  for(int j=0;j<7;j++)
   if(used[j]+abs(row.up[j]-usedup[j])+abs(row.down[j]-useddown[j])>row.total[j]){ok=false;break;}
  if(ok){directionOK=true;break;}
 }
 if(!directionOK)return false;
#endif
 set<P> convex;
 for(auto &[p,r]:out){if(r.size()!=1||in[p].size()!=1||cross(in[p][0],r[0])<=0)continue;
  bool transit=false;for(auto [x,y]:edges)if(p!=x&&p!=y&&!cross(y-x,p-x)&&min(x,y)<p&&p<max(x,y)){transit=true;break;}if(!transit)convex.insert(p);
 }
 for(auto [p,q]:edges){bool clamped=convex.count(p)&&convex.count(q);for(int i=0;i<(int)outer.size()&&!clamped;i++){P d=outer[(i+1)%outer.size()]-outer[i];if(!cross(q-p,d)&&!cross(p-outer[i],d))clamped=true;}
  if(clamped){P d=q-p;int L=exact_length(d,gridDen,10000);P ray=dir(d);
   if(norm(d)>W(10000)*10000*gridDen*gridDen){cerr<<"length table exceeded"<<endl;exit(5);}
   if(L<0||!coins.count(ray)||!coins[ray][L])return false;
#ifndef IGNORE_SIDE_FANS
   P cap=convex.count(p)?dir(-1*in[p][0]):P{0,0};
   P next=convex.count(q)?dir(out[q][0]):P{0,0};
   if(!sideword(ray,cap,next,L))return false;
#endif
  }
 }
 vector<vector<Shape>> best;bool init=false;
 vector<P> pivots(convex.begin(),convex.end());
#ifdef REVERSE_TIES
 reverse(pivots.begin(),pivots.end());
#endif
#ifdef WALL_FIRST
 P wall_dir=outer[2]-outer[1];
 stable_sort(pivots.begin(),pivots.end(),[&](P x,P y){
  return cross(wall_dir,x-outer[1])<cross(wall_dir,y-outer[1]);
 });
#endif
#ifdef FORCE_WALL
 W nearest=0;
 bool selected=false;
#endif
 for(P p:pivots){
#ifdef FORCE_WALL
  W distance=cross(outer[2]-outer[1],p-outer[1]);
  if(selected && distance!=nearest)break;
  nearest=distance;selected=true;
#endif
  P begin=dir(out[p][0]),end=dir(-1*in[p][0]);
  vector<vector<Shape>> cand;vector<Shape> fan;
  auto addfan=[&](auto &&self,P source)->void{
   if(init && cand.size()>=best.size())return;
   if(source==end){cand.push_back(fan);return;}
   for(auto s:byout[source]){
    P next=dir(s.t[2]);if(cross(next,end)<0 || (cross(next,end)==0 && next!=end) || cross(begin,next)<=0)continue;
    for(auto &q:s.t)q=q+p;if(!good(s))continue;
    fan.push_back(s);self(self,next);fan.pop_back();
   }
  };
  addfan(addfan,begin);if(cand.empty())return false;if(!init||cand.size()<best.size()){init=true;best=move(cand);}
 }
 if(!init){cerr<<"singular state; no decision\n";exit(4);}
 for(const auto &fan:best){auto child=edges;for(const auto &s:fan){chosen.push_back(s);used[s.h+2]++;signed_used[sign_index(s)]++;count_chirality(s,1);child=update(child,s.t);}if(dfs(child))return true;for(auto &s:fan){chosen.pop_back();used[s.h+2]--;signed_used[sign_index(s)]--;count_chirality(s,-1);}}
 return false;
}
int main(int ac,char**av){
 if(ac!=9&&ac!=10)return 1;a=atoi(av[1]);b=atoi(av[2]);c=atoi(av[3]);t=atoi(av[4]);k=atoi(av[5]);hlo=atoi(av[6]);hhi=atoi(av[7]);limit=atoll(av[8]);target=t*t-k*k;
 // This replay is deliberately scoped to the small audited fixtures.
 if(a<=b||b<=0||c>100||W(a)*a+W(a)*b+W(b)*b!=W(c)*c||
    gcd(a,b)!=1||a%2==0||b%2==0||t<=0||t>100||k<0||
    k*c>=t*a||hlo< -2||hlo>0||hhi<1||hhi>3||limit<=0)return 1;
 int pow=max({1,-hlo,hhi});Z den=1;for(int i=0;i<pow;i++)den*=c;
 gridDen=den;
 outer={{t*a*den,0},{t*a*den,t*b*den},{k*a*a*(den/c),k*a*b*(den/c)},{k*c*den,0}};
 if(ac==10){
  int j=atoi(av[9]); extension=j;
  if(j<=0||j>100||(t*c-k*a)%b)return 1;
  extra=j*(2*((t*c-k*a)/b)+j); target+=extra;
  outer[1].y+=j*c*den;
  P extended=outer[2]+P{-j*a*b*(den/c),j*(c*c-b*b)*(den/c)};
  outer.insert(outer.begin()+2,extended);
 }
 if(k==0)outer.pop_back();
 W area=0;
 for(int i=0;i<(int)outer.size();i++){
  P prev=outer[(i+outer.size()-1)%outer.size()],here=outer[i],next=outer[(i+1)%outer.size()];
  if(cross(here-prev,next-here)<=0)abort();
  area+=cross(here,next);
 }
 if(area!=W(target)*a*b*den*den)abort();

 for(int h=hlo;h<=hhi;h++){
  P d={1,0};Z n=1;for(int i=0;i<abs(h);i++){d=mul(d,h>0?P{a,b}:P{a+b,-b});n*=c;}d=(den/n)*d;
  for(int j=0;j<6;j++,d=rot(d))for(int sign:{-1,1}){
   P f=rot(rot(d));if(sign<0)f=rot(rot(f));
   Tri s={P{0,0},a*d,b*f};if(cross(s[1],s[2])<0)swap(s[1],s[2]);
   for(int i=0;i<3;i++){Tri row{P{0,0},s[(i+1)%3]-s[i],s[(i+2)%3]-s[i]};byout[dir(row[1])].push_back({row,h,(j%2?-sign:sign),-sign});}
  }
 }
 for(auto &[ray,vec]:byout){
  vector<bool> dp(10001);dp[0]=true;for(auto &s:vec){P d=s.t[1];int l=exact_length(d,den,c);if(l!=a&&l!=b&&l!=c)abort();
   for(int j=l;j<(int)dp.size();j++)if(dp[j-l])dp[j]=true;
   along[ray].push_back({l,dir(s.t[2]),dir(s.t[2]-s.t[1])});
  }coins[ray]=move(dp);
  auto &opts=along[ray];sort(opts.begin(),opts.end());opts.erase(unique(opts.begin(),opts.end()),opts.end());
 }
 array<int,7> rr{};
 auto inv=[&](auto &&self,int h,int remaining)->void{if(h>hhi){if(!remaining)inventories.push_back(rr);return;}
   int res=h==0?t*t%c:h==1?((extra-k*k)%c+c)%c:0;
   for(int n=res;n<=remaining;n+=c){if(h!=0&&h!=1&&n==c)continue;rr[h+2]=n;self(self,h+1,remaining-n);}
 };inv(inv,hlo,target);
 for(const auto &pop:inventories){
  array<int,14> row{};
  auto signs=[&](auto &&self,int h,int even,int odd)->void{
   if(h>hhi){if(even!=t||odd!=k+extension)return;
#ifndef IGNORE_BOUNDARY_COUNT
    if(extension==1 && (a+c)%b==0 && (t*c-k*a)%b==0){
     int H=(t*c-k*a)/b,u=(a+c)/b;
     if(H+1<a && k<a){
      int n1=pop[3],g1=row[6]-row[7];
      // The middle wall of length a is pure a (gcd(a,b)=1, b>1).
      if(b>1 && (u+1)*n1-(u-1)*g1<2*(H+k))return;
     }
    }
#endif
    signed_inventories.push_back(row);
    DirectionalPopulation item;item.total=pop;int offsets[11]{}; // index h+4
    auto signed_at=[&](int i){return i<hlo||i>hhi?0:row[2*(i+2)]-row[2*(i+2)+1];};
    for(int i=hlo-1;i<=hhi+1;i++){
     int d=a-b;
     int exterior=i==0?d*t-c*(k+extension):i==1?d*(k+extension)-c*t:0;
     int numerator=d*signed_at(i)-exterior;
     if(numerator%c)return;
     int down_next=numerator/c-offsets[i+3];
     int next=i+1;
     if(next>hhi){if(down_next)return;continue;}
     int up=signed_at(next)-down_next;
     if(abs(up)+abs(down_next)>pop[next+2])return;
     offsets[next+4]=up;item.up[next+2]=up;item.down[next+2]=down_next;
    }
    directional.push_back(item);return;}
   int n=pop[h+2],wanted=h==0?t:h==1?k+extension:0;
   for(int signed_count=-n;signed_count<=n;signed_count+=2){
    if((signed_count-wanted)%c)continue;
    row[2*(h+2)]=(n+signed_count)/2;
    row[2*(h+2)+1]=(n-signed_count)/2;
    self(self,h+1,even+(h%2?0:signed_count),odd+(h%2?signed_count:0));
   }
  };signs(signs,hlo,0,0);
 }
 vector<Edge> edges;for(int i=0;i<(int)outer.size();i++)edges.push_back({outer[i],outer[(i+1)%outer.size()]});
 if(!dfs(edges))cout<<"NO(in palette) "<<nodes<<"\n";
}
