#include <bits/stdc++.h>
using namespace std;
using I=long long;
using P=pair<int,int>;using Poly=vector<P>;
I cross(P a,P b,P c){return I(b.first-a.first)*(c.second-a.second)-I(b.second-a.second)*(c.first-a.first);}
I area(Poly const&p){I a=0;for(int i=0,j=p.size()-1;i<(int)p.size();j=i++)a+=I(p[j].first)*p[i].second-I(p[j].second)*p[i].first;return a;}
Poly hull(Poly p){sort(p.begin(),p.end());p.erase(unique(p.begin(),p.end()),p.end());Poly q;size_t k=0;for(int d=0;d<2;d++){for(P a:p){while(q.size()>=k+2&&cross(q[q.size()-2],q.back(),a)<=0)q.pop_back();q.push_back(a);}q.pop_back();k=q.size();reverse(p.begin(),p.end());}return q;}
struct B{int x=INT_MAX,y=INT_MAX,X=INT_MIN,Y=INT_MIN;};B box(Poly const&p){B b;for(auto[x,y]:p){b.x=min(b.x,x);b.y=min(b.y,y);b.X=max(b.X,x);b.Y=max(b.Y,y);}return b;}
bool meet(B a,B b){return a.x<b.X&&b.x<a.X&&a.y<b.Y&&b.y<a.Y;}
bool separate(Poly const&p,Poly const&q){for(int i=0,j=p.size()-1;i<(int)p.size();j=i++){bool all=true;for(auto z:q)if(cross(p[j],p[i],z)>0){all=false;break;}if(all)return true;}return false;}
bool contained(Poly const&t,Poly const&p){for(int i=0,j=p.size()-1;i<(int)p.size();j=i++)for(P z:t)if(cross(p[j],p[i],z)<0)return false;return true;}
vector<Poly> tiles;vector<B> boxes;map<pair<int,int>,vector<int>> bins;
constexpr int unit=2000;int flop(int x){return x>=0?x/unit:-((-x+unit-1)/unit);}vector<int> stamp;int id=0;
vector<int> near(B b){id++;vector<int> ids;for(int x=flop(b.x);x<=flop(b.X);x++)for(int y=flop(b.y);y<=flop(b.Y);y++){auto k=bins.find({x,y});if(k==bins.end())continue;for(int j:k->second)if(stamp[j]!=id){stamp[j]=id;ids.push_back(j);}}return ids;}
int A=2135*43,Bb=1079*43,M=455*43*43,limit,cap;P T={-11180,13545};P add(P a,P b){return {a.first+b.first,a.second+b.second};}
map<Poly,Poly> closed;
Poly closep(Poly p){auto found=closed.find(p);if(found!=closed.end())return found->second;Poly orig=p;for(;;){bool good=area(p)<=I(limit)*M;Poly t;for(auto z:p){auto v=add(z,T);t.push_back(v);for(auto q:{z,v})if(q.first<0||q.second<0||I(A)*q.first+I(Bb)*q.second>I(A)*Bb)good=false;}if(!good||(!separate(p,t)&&!separate(t,p)))return closed[orig]={};auto bb=box(p);auto g=p;for(int i:near(bb)){auto &t=tiles[i];if(!meet(bb,boxes[i])||contained(t,p)||separate(t,p)||separate(p,t))continue;g.insert(g.end(),t.begin(),t.end());}if(g==p)return closed[orig]=p;p=hull(g);}}
set<int> touching(Poly const&p){set<int> nbr;for(int i=0,j=p.size()-1;i<(int)p.size();j=i++){P a=p[j],b=p[i];auto aa=min(a,b),bb=max(a,b);for(int k:near(box({a,b}))){auto &t=tiles[k];P lo=bb,hi=aa;bool plus=false;for(auto z:t){auto s=cross(a,b,z);if(s>0){plus=true;break;}if(!s){lo=min(lo,z);hi=max(hi,z);}}if(!plus&&max(aa,lo)<min(bb,hi))nbr.insert(k);}}return nbr;}
map<P,pair<int,int>> dirs;set<int> coins={0};
bool good(Poly const &p, int n){vector<tuple<int,int,int>> E;I x=0,y=0;
 for(int i=0,j=p.size()-1;i<(int)p.size();j=i++){int dx=p[i].first-p[j].first,dy=p[i].second-p[j].second;int g=gcd(dx,dy);auto it=dirs.find({dx/g,dy/g});if(it==dirs.end())return false;I sq=I(dx)*dx+I(dy)*dy+I(dx)*dy;I r=llround(sqrt(double(sq)));if(r*r!=sq||r%43||!coins.count(r/43))return false;int l=r/43,h=it->second.first,t=it->second.second;x+=(t%2?-l:l);y+=((t+h+12)%2?-l:l);E.push_back({l,h,t});}
 if(x%(-21)||y%65||abs(x/(-21))>n||abs(y/65)>n||(x/(-21)-n)%2||(y/65-n)%2)return false;
 for(int i=0,j=E.size()-1;i<(int)E.size();j=i++){auto [li,h,t]=E[i];auto [lj,k,s]=E[j];int r=(t-s+6)%6;bool legal=false;for(int m=0;m<=6;m++)for(int n=0;n<=6;n++)if((3-m+6)%6==r && (m-n)==h-k)legal=true;if(!legal)return false;}
 return true;}
int main(int ac,char**av){limit=atoi(av[1]);cap=atoi(av[2]);int n;cin>>n;for(int i=0;i<n;i++){Poly p(3);for(auto &[x,y]:p)cin>>x>>y;tiles.push_back(p);B b=box(p);boxes.push_back(b);for(int x=flop(b.x);x<=flop(b.X);x++)for(int y=flop(b.y);y<=flop(b.Y);y++)bins[{x,y}].push_back(i);}stamp.resize(n);int m;cin>>m;Poly starting(m);for(auto &[x,y]:starting)cin>>x>>y;
 for(int x=1;x<=4500;x++)if(coins.count(x-13)||coins.count(x-35)||coins.count(x-43))coins.insert(x);
 for(int h=-2;h<=3;h++){I x=1,y=0;for(int k=0;k<abs(h);k++){int a=h>0?35:48,b=h>0?13:-13;I X=x*a-y*b,Y=x*b+y*a+y*b;x=X;y=Y;}for(int j=0;j<6;j++){int g=gcd(x,y);dirs[{int(x/g),int(y/g)}]={h,j};I X=-y,Y=x+y;x=X;y=Y;}}
 set<Poly>seen;set<pair<I,Poly>>q;starting=closep(hull(starting));if(starting.empty())return 2;seen.insert(starting);q.insert({area(starting),starting});int exp=0,pass=0;
 while(!q.empty()&&exp<cap){auto entry=*q.begin();q.erase(q.begin());auto &[m,p]=entry;exp++;if(m%M){cerr<<"nonintegral\n";return 1;}if(good(p,m/M)){cout<<m/M<<" "<<p.size();for(auto[x,y]:p)cout<<" "<<x<<" "<<y;cout<<"\n";pass++;}
  if(exp%1000==0){cerr<<exp<<" seen "<<seen.size()<<" area "<<m/M<<" pass "<<pass<<" cache "<<closed.size()<<"\n";cout.flush();}
  for(int k:touching(p)){Poly trial=p;trial.insert(trial.end(),tiles[k].begin(),tiles[k].end());auto t=closep(hull(trial));if(!t.empty()&&seen.insert(t).second)q.insert({area(t),t});}
 }
 cerr<<"finish expanded "<<exp<<" remaining "<<q.size()<<" pass "<<pass<<"\n";}
