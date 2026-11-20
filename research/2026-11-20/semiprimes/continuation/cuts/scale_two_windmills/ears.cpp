#include <algorithm>
#include <array>
#include <cassert>
#include <cmath>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <map>
#include <tuple>
#include <vector>
using ll = int64_t;
using W = __int128_t;
struct P {ll x,y;};
P operator+(P a,P b){return {a.x+b.x,a.y+b.y};}
P operator-(P a,P b){return {a.x-b.x,a.y-b.y};}
P operator*(P a,ll n){return {a.x*n,a.y*n};}
P mul(P a,P b){return {a.x*b.x-a.y*b.y,a.x*b.y+a.y*b.x+a.y*b.y};}
W det(P a,P b){return W(a.x)*b.y-W(a.y)*b.x;}
int sgn(int j){return (j%2)?-1:1;}
struct Edge{int l,h,j;};
struct Ray{int h,j;P d;};
struct Site{P p;W area;int f,g,k,t;};
struct Arm{ll x,y;uint16_t q,l;uint8_t r;};
struct Fan{int m,n;};
Fan angle(int h,int j){for(int m=(j%6+6)%6;m<=6;m+=6){int n=m+h;if(n>=0&&n<=6&&m+n>0&&m+n<12)return{m,n};}return{-1,-1};}
int main(int argc,char **argv){
  int shards=argc>1?std::atoi(argv[1]):1,id=argc>2?std::atoi(argv[2]):0;assert(shards>=1&&id>=0&&id<shards);
  int a,b,c,n,stars; if(!(std::cin>>a>>b>>c>>n>>stars))return 1;
  std::vector<Edge> e(n);int perimeter=0;
  for(auto &[l,h,j]:e){std::cin>>l>>h>>j;perimeter+=l;}
  std::vector<Fan> corners;
  int low=100,high=-100;
  for(int k=0;k<n;k++){
    Edge ahead=e[k],behind=e[(k+n-1)%n];
    Fan f=angle(behind.h-ahead.h,behind.j+3-ahead.j);
    if(f.m<0)return 0;
    corners.push_back(f);
    low=std::min(low,ahead.h-std::max(3,f.m)); high=std::max(high,ahead.h+std::max(3,f.n));
  }
  int mid=(high+low)/2;
  for(auto &ed:e)ed.h-=mid;
  low-=mid;high-=mid;
  ll D=1; for(int t=0;t<std::max(-low,high);t++){if(D>100000000000000LL/c) return 3;D*=c;}
  std::vector<Ray> rays;std::map<std::pair<int,int>,int> ind;
  for(int h=low;h<=high;h++){
    ll denom=1;P u={1,0};
    for(int t=0;t<std::abs(h);t++){denom*=c;u=mul(u,h<0?P{a+b,-b}:P{a,b});}
    u=u*(D/denom);
    for(int j=0;j<6;j++){ind[{h,j}]=rays.size();rays.push_back({h,j,u});u=mul(u,{0,1});}
  }
  std::vector<P> v;P pos{0,0};
  int diameter=perimeter/2;
  for(auto ed:e){v.push_back(pos);pos=pos+rays[ind.at({ed.h,ed.j})].d*ed.l;}
  assert(pos.x==0&&pos.y==0);

  std::vector<bool> coin(perimeter+1);coin[0]=true;
  for(int i=1;i<=perimeter;i++)for(int l:{a,b,c})if(i>=l&&coin[i-l])coin[i]=true;
  std::vector<Site> sites;
  std::map<std::pair<ll,ll>,int> lookup;
  W area=0,unit=W(a)*b*D*D;
  int f=0,g=0;
  for(int k=0;k<n;k++){
    auto [l,h,j]=e[k];auto raw=rays[ind.at({h,j})].d;
    for(int t=0;t<l;t++)if(coin[t]&&coin[l-t]){
      auto p=v[k]+raw*t;
      lookup[{p.x,p.y}]=sites.size();
      sites.push_back({p,area+det(v[k],p),f+sgn(j)*t,g+sgn(j+h)*t,k,t});
    }
    area+=det(v[k],v[(k+1)%n]);f+=sgn(j)*l;g+=sgn(j+h)*l;
  }
  int mass=area/unit;
  auto accept=[&](W raw,int x,int y){
    if(raw<=0||raw%unit)return false;
    int m=raw/unit;
    // The ordinary weight scales by a global sign on rotating the board.
    int u=a-b-c,w=a-b+c;
    if(x%u||y%w)return false;
    return std::abs(x/u)<=m&&std::abs(y/w)<=m&&(x/u-m)%2==0&&(y/w-m)%2==0;
  };
  auto arc=[&](const Site &s,const Site &t){return (t.k<s.k||(t.k==s.k&&t.t<s.t));};
  ll minx=v.front().x,maxx=minx; for(P vtx:v){minx=std::min(minx,vtx.x);maxx=std::max(maxx,vtx.x);}
  auto band=[&](P p){return int((W(p.x)-minx)*shards/(maxx-minx+1));};
  std::vector<Arm> arms;
  for(int qi=0;qi<(int)sites.size();qi++){
    auto s=sites[qi];auto ed=e[s.k];Fan local=s.t?Fan{3,3}:corners[s.k];
    for(int m=0;m<=local.m;m++)for(int nn=0;nn<=local.n;nn++){
      if((!m&&!nn)||(m==local.m&&nn==local.n))continue;
      int r=ind.at({ed.h+nn-m,(ed.j+m)%6}); auto ray=rays[r];
      int limit=diameter;
      for(int k=0;k<n;k++){
        P side=rays[ind.at({e[k].h,e[k].j})].d;
        W start=det(side,s.p-v[k]),slope=det(side,ray.d);assert(start>=0);
        if(start==0&&slope<=0){limit=0;break;}
        if(slope<0){W t=start/-slope;if(t<limit)limit=int(t);}
      }
      if(limit<=0)continue;
      P last=s.p+ray.d*limit;
      auto end=lookup.find({last.x,last.y});
      bool boundary=false;
      if(end!=lookup.end()){
        boundary=true;
        if(!id&&end->second>qi&&coin[limit]){
          Site t=sites[end->second];
          W sub=t.area-s.area+det(t.p,s.p);
          int x=t.f-s.f-sgn(ray.j)*limit,y=t.g-s.g-sgn(ray.j+ray.h)*limit;
          if(accept(sub,x,y)&&accept(area-sub,f-x,g-y))
            std::cout<<"C "<<s.k<<' '<<s.t<<' '<<t.k<<' '<<t.t<<' '<<limit<<' '<<ray.h+mid<<' '<<ray.j<<'\n';
        }
      }
      if(!stars)continue;
      if(!boundary)for(int k=0;k<n;k++)if(det(rays[ind.at({e[k].h,e[k].j})].d,last-v[k])==0)boundary=true;
      for(int l=1;l<=limit-boundary;l++)if(coin[l]){
        P p=s.p+ray.d*l;if(band(p)!=id)continue;arms.push_back({p.x,p.y,uint16_t(qi),uint16_t(l),uint8_t(r)});
      }
    }
  }
  std::sort(arms.begin(),arms.end(),[](const Arm &a,const Arm &b){return std::tie(a.x,a.y,a.q,a.r)<std::tie(b.x,b.y,b.q,b.r);});
  auto sector=[&](Arm a,Arm b){
    if(a.q==b.q)return false;Site s=sites[a.q],t=sites[b.q];Ray r=rays[a.r],z=rays[b.r];
    if(det(r.d,z.d)<=0||angle(z.h-r.h,z.j-r.j).m<0)return false;
    bool wrap=arc(s,t);
    return accept(t.area-s.area+(wrap?area:0)+det(t.p-s.p,{a.x,a.y}),
      t.f-s.f+(wrap?f:0)+sgn(z.j)*b.l-sgn(r.j)*a.l,
      t.g-s.g+(wrap?g:0)+sgn(z.j+z.h)*b.l-sgn(r.j+r.h)*a.l);
  };
  for(size_t i=0;i<arms.size();){
    size_t end=i+1;while(end<arms.size()&&arms[i].x==arms[end].x&&arms[i].y==arms[end].y)end++;
    if(stars==4){
      for(size_t u=i;u<end;u++)for(size_t vv=i;vv<end;vv++)if(sector(arms[u],arms[vv])){
        const auto arm1=arms[u],arm2=arms[vv];const auto q=sites[arm1.q],t=sites[arm2.q];
        const auto r=rays[arm1.r],z=rays[arm2.r];
        std::cout<<arm1.x<<" "<<arm1.y<<" "<<D<<" "<<q.k<<" "<<q.t<<" "<<arm1.l<<" "<<r.h+mid<<" "<<r.j<<" "<<t.k<<" "<<t.t<<" "<<arm2.l<<" "<<z.h+mid<<" "<<z.j<<"\n";
      }
      i=end;continue;
    }
    for(size_t j=i;j+2<end;j++)for(size_t k=j+1;k+1<end;k++)if(sector(arms[j],arms[k]))
      for(size_t l=k+1;l<end;l++)if(sector(arms[k],arms[l])&&sector(arms[l],arms[j])){
        std::cout<<"S";
        for(size_t idx:{j,k,l}){
          Arm arm=arms[idx];auto s=sites[arm.q];auto r=rays[arm.r];
          std::cout<<' '<<s.k<<' '<<s.t<<' '<<arm.l<<' '<<r.h+mid<<' '<<r.j;
        }
        std::cout<<'\n';
      }
    i=end;
  }
}
