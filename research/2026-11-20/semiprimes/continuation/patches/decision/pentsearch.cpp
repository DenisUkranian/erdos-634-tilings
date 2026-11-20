#include <gmpxx.h>
#include <algorithm>
#include <array>
#include <iostream>
#include <map>
#include <set>
#include <vector>
#include <numeric>
#include <string>
using namespace std;
using Q=mpq_class;
struct Point {Q x,y; bool operator<(Point const& p)const{if(x!=p.x)return x<p.x;return y<p.y;}bool operator==(Point const&p)const{return x==p.x&&y==p.y;}bool operator!=(Point const&p)const{return !(*this==p);} };
Point operator+(Point a,Point b){return {a.x+b.x,a.y+b.y};}
Point operator-(Point a,Point b){return {a.x-b.x,a.y-b.y};}
Point operator*(Q n,Point p){return {n*p.x,n*p.y};}
Point mul(Point a,Point b){return {a.x*b.x-a.y*b.y,a.x*b.y+a.y*b.x+a.y*b.y};}
Point conjugate(Point a){return {a.x+a.y,-a.y};}
Q det(Point a,Point b){return a.x*b.y-a.y*b.x;}
Q rat(long p,long q){Q x(p,q);x.canonicalize();return x;}
Q norm(Point a){return a.x*a.x+a.x*a.y+a.y*a.y;}
Q length(Point a){Q z=norm(a);mpz_class num,den; mpz_sqrt(num.get_mpz_t(),z.get_num().get_mpz_t()); mpz_sqrt(den.get_mpz_t(),z.get_den().get_mpz_t());if(num*num!=z.get_num()||den*den!=z.get_den())abort();return Q(num,den);}
using Tri=array<Point,3>;using E=pair<Point,Point>;
int a,b,c,t,k,target;long long nodes=0,maxnodes; bool unknown=false;
vector<Point> outer;vector<Tri> chosen;vector<int> coin;
bool isCoin(Q x){return x>=0&&x.get_den()==1&& x<((int)coin.size()) &&coin[x.get_num().get_si()];}
bool separates(Tri const& t,Tri const& u){ for(int i=0;i<3;i++){Point d=t[(i+1)%3]-t[i];if(all_of(u.begin(),u.end(),[&](Point q){return det(d,q-t[i])<=0;}))return true;}return false;}
struct Border{Point p,d; Q len;};vector<Border> bd;
bool phaseOK(Tri const &v,Tri const&t){
 for(int i=0;i<3;i++){Point p=v[i],q=v[(i+1)%3],vec=q-p;for(auto x:t){
    if(min(p,q)<x&&x<max(p,q)&&det(vec,x-p)==0&&length(x-p).get_den()!=1)return false;
 }}return true;
}
bool good(Tri const&t){
 for(auto &wall:bd)for(auto p:t){auto off=p-wall.p;auto area=det(wall.d,off);if(area<0)return false;if(area==0){Q s=wall.len*(wall.d.x!=0?off.x/wall.d.x:off.y/wall.d.y);if(!isCoin(s)||!isCoin(wall.len-s))return false;}}
 for(const auto&u:chosen){if(!separates(t,u)&&!separates(u,t))return false;if(!phaseOK(t,u)||!phaseOK(u,t))return false;}return true;
}
vector<E> update(vector<E> old,Tri const&t){
 for(int j=0;j<3;j++){
  Point start=t[(j+1)%3],end=t[j],d=end-start;
  map<Point,int> events;vector<E> keep;
  auto add=[&](Point p,Point q){events[p]++;events[q]--;};add(start,end);
  for(auto [p,q]:old){if(det(q-p,d)!=0||det(p-start,d)!=0)keep.push_back({p,q});else add(p,q);}
  int n=0;Point prev;
  for(auto [p,v]:events)if(v){if(n==1)keep.push_back({prev,p});if(n==-1)keep.push_back({p,prev});n+=v;if(abs(n)>1)abort();prev=p;}
  old=move(keep);
 }
 return old;
}
set<Point> feasibleAngles;
map<Point,Point> unitMap;
Point unit(Point d){auto hit=unitMap.find(d);if(hit!=unitMap.end())return hit->second;return unitMap.emplace(d,(1/length(d))*d).first->second;}
bool legalAngle(Point x,Point y){return feasibleAngles.count(mul(unit(y),conjugate(unit(x))));}
map<Point,vector<Tri>> templateMap[2];
vector<Tri> const& templates(Point d,int side){
 Q len=length(d);Point u=(1/len)*d;
 auto& cache=templateMap[side];auto it=cache.find(u);if(it!=cache.end())return it->second;
 vector<Tri> out;array<int,3> sizes{a,b,c};sort(sizes.begin(),sizes.end());
 do {long r=sizes[0],s=sizes[1],v=sizes[2];Point apex={rat(r*r+s*s-v*v-a*b,2*r),rat(a*b,r)};if(side)apex=conjugate(apex);Tri q={Point{0,0},r*u,mul(u,apex)};if(side)swap(q[1],q[2]);out.push_back(q);}while(next_permutation(sizes.begin(),sizes.end()));
 return cache.emplace(u,out).first->second;
}
bool dfs(vector<E> const& edges){
 if(nodes && nodes%1000==0)cerr<<nodes<<" nodes, depth "<<chosen.size()<<"\n";if(++nodes>maxnodes){cerr<<"budget "<<nodes<<" depth "<<chosen.size()<<"\n";exit(2);}
 if(chosen.size()==target){if(edges.size())abort();cout<<"YES "<<nodes<<"\n";for(auto tr:chosen){for(auto p:tr)cout<<p.x<<','<<p.y<<' ';cout<<'\n';}return true;}
 map<Point,vector<Point>> in,out;for(auto [p,q]:edges){in[q].push_back(q-p);out[p].push_back(q-p);}
 set<Point> clamps;
 for(auto const&[p,r]:out){if(r.size()!=1||in[p].size()!=1||det(in[p][0],r[0])<=0)continue;
 bool through=false;for(auto [x,y]:edges)if(min(x,y)<p&&p<max(x,y)&&!det(y-x,p-x)){through=true;break;}if(!through)clamps.insert(p);}
 for(auto p:clamps)if(!legalAngle(out[p][0],(-1)*in[p][0]))return false;
 for(auto [p,q]:edges)if(clamps.count(p)&&clamps.count(q)&&!isCoin(length(q-p)))return false;
 vector<Border> localLower,localUpper;
 for(auto [p,q]:edges){
  if(clamps.count(p))localLower.push_back({p,q-p,length(q-p)});
  if(clamps.count(q))localLower.push_back({q,p-q,length(p-q)});
 }
 vector<Tri> best;bool ok=false;
 for(auto p:clamps)for(int side:{0,1}){
   Point aim=side?(-1)*in[p][0]:out[p][0];vector<Tri> cand;
   for(auto tr:templates(aim,side)){
    for(auto& x:tr)x=x+p;
    bool local=true;for(auto const&w:localLower)for(auto v:tr){
      Point off=v-w.p;if(det(w.d,off)!=0||!(min(w.p,w.p+w.d)<v&&v<max(w.p,w.p+w.d)))continue;
      Q s=w.len*(w.d.x!=0?off.x/w.d.x:off.y/w.d.y);if(!isCoin(s))local=false;
    }if(!local)continue;
    if(!legalAngle(side?out[p][0]:tr[2]-p,side?tr[1]-p:(-1)*in[p][0]))continue;
    if(all_of(tr.begin(),tr.end(),[&](Point x){return det(out[p][0],x-p)>=0&&det(in[p][0],x-p)>=0;})&&good(tr))cand.push_back(tr);
   }
   if(cand.empty())return false;if(!ok||cand.size()<best.size()){best=move(cand);ok=true;}
 }
 if(!ok){unknown=true;return false;}
 for(auto tr:best){chosen.push_back(tr);if(dfs(update(edges,tr)))return true;chosen.pop_back();}
 return false;
}
int main(int argc,char**argv){
 if(argc!=6&&argc!=9&&argc!=10&&argc!=11)return 2;
 a=atoi(argv[1]);b=atoi(argv[2]);c=atoi(argv[3]);string mode=argv[4];maxnodes=atoll(argv[5]);
 int s=(c-a)/2;t=(a-b)/2;k=(c-3*b)/2;
 int j=argc>=10?atoi(argv[9]):1;
 if(argc>=9){s=atoi(argv[6]);t=atoi(argv[7]);k=atoi(argv[8]);}
 Point X={0,s*c},Y={0,s*c+t*b},W={t*a-k*c,s*c+t*b};
 Point D=X+Point{t*a,t*b}-Point{rat(k*a*a,c),rat(k*a*b,c)};
 Point V={rat(a*b,c),rat(b*b-c*c,c)};
 outer={Point{0,(s-j)*c},Y,W,D,D+j*V};
 target=t*t-k*k+2*j*(a-s)+j*j;
 if(mode=="hex"){
   if(argc!=11 || j!=s)return 3;
   int l=atoi(argv[10]);Point P={0,0},T=P+Point{rat(a*a*b,c),rat(a*b*b,c)},U={rat(b*(a+b),c),rat(-a*b,c)};
   outer={P,Y,W,D+l*U,T+l*U,P+Point{l*c,0}};target+=l*(2*b-l+2*s);
 }
 if(mode=="quad"){outer={Point{t*a,0},Point{t*a,t*b},Point{rat(k*a*a,c),rat(k*a*b,c)},Point{k*c,0}};target=t*t-k*k;}
 if(mode=="tri"){outer={Point{0,0},Point{2*a,0},Point{-2*b,2*b}};target=4;}
 Q ar=0;int n=outer.size();for(int i=0;i<n;i++)ar+=det(outer[i],outer[(i+1)%n]);if(ar<0){reverse(outer.begin(),outer.end());ar=-ar;}
 if(ar!=target*a*b){cerr<<"target from area: "<<ar/(a*b)<<"\n";return 5;}
 vector<E> edges;for(int i=0;i<n;i++){
  Point p=outer[i],q=outer[(i+1)%n];for(auto x:outer)if(det(q-p,x-p)<0){cerr<<"nonconvex\n";return 6;}
  edges.push_back({p,q});bd.push_back({p,q-p,length(q-p)});
 }
 int limit=8*(c*c+a*b);coin.resize(limit);coin[0]=1;for(int i=1;i<limit;i++)for(int s:{a,b,c})if(i>=s&&coin[i-s])coin[i]=1;
 Point beta={rat(a,c),rat(b,c)},alpha=mul(Point{0,1},conjugate(beta));
 for(Point n={1,0};n.y>=0;n=mul(n,alpha))
   for(Point m=n;m.y>=0;m=mul(m,beta))feasibleAngles.insert(m);
 if(!dfs(edges))cout<<(unknown?"INCONCLUSIVE":"NO")<<" "<<nodes<<'\n';
}
