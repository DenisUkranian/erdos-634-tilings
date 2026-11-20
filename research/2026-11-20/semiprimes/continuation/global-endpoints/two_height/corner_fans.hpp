#include <unordered_map>
#include <deque>
using Stars=array<U,3>;
struct StarKey {Stars a;int lo,hi;auto operator<=>(const StarKey &)const=default;};
struct KeyHash{size_t operator()(StarKey const&k) const noexcept {uint64_t v=(uint64_t(k.a[0])<<32)^k.a[1];v^=uint64_t(k.a[2])*0x9e3779b185ebca87ull;v^=uint64_t((k.lo+2)*64+k.hi+2)*0x85ebca6bull;v^=v>>30;v*=0xbf58476d1ce4e5b9ull;return v^(v>>27);}};
struct StarArc {int t,k,lo,hi;};
struct StarFilter{
 int nx,ny,T,N,nr;vector<array<P,3>>&tri;vector<P>&poly;vector<U>&mask;vector<bool>&inside;map<P,int> rays;vector<int> low,high;vector<StarArc> arcs;unordered_map<StarKey,Stars,KeyHash> kept;
 static P dir(P p){int g=gcd(abs(p.x),abs(p.y));return {p.x/g,p.y/g};}
 StarFilter(int sx,int sy,vector<array<P,3>>&sh, vector<P>&wall,vector<U>&alive,vector<bool>&ins):nx(sx),ny(sy),T(sh.size()),N(wall.size()),tri(sh),poly(wall),mask(alive),inside(ins){
  vector<P> ds;for(auto tr:tri)for(int k=0;k<3;k++){ds.push_back(dir(tr[(k+1)%3]-tr[k]));ds.push_back(dir(tr[(k+2)%3]-tr[k]));}
  sort(ds.begin(),ds.end(),[](P p,P q){bool a=p.y>0||(p.y==0&&p.x>0),b=q.y>0||(q.y==0&&q.x>0);if(a!=b)return a>b;return cross(p,q)>0;});ds.erase(unique(ds.begin(),ds.end()),ds.end());nr=ds.size();for(int z=0;z<nr;z++)rays[ds[z]]=z;
  for(int t=0;t<T;t++)for(int k=0;k<3;k++)arcs.push_back({t,k,rays.at(dir(tri[t][(k+1)%3]-tri[t][k])),rays.at(dir(tri[t][(k+2)%3]-tri[t][k]))});
  for(int i=0;i<N;i++){low.push_back(rays.at(dir(poly[(i+1)%N]-poly[i])));high.push_back(rays.at(dir(poly[(i+N-1)%N]-poly[i])));}
 }
 Stars solve(StarKey const &key){auto hit=kept.find(key);if(hit!=kept.end())return hit->second;Stars keep{};array<unsigned,32> jumps{};for(auto a:arcs)if(key.a[a.k]&(U(1)<<a.t))jumps[a.lo]|=1u<<((a.hi-a.lo+nr)%nr);
  const int H=nr/2,M=2*nr+H;array<K,64> reach{},pred{};if(M>=64)abort();for(int x=0;x<=M;x++){reach[x]=pred[x]=K(1)<<x;}
  for(int x=M-1;x>=0;x--)for(U d=jumps[x%nr];d;d&=d-1){int j=x+countr_zero(d);if(j<=M)reach[x]|=reach[j];}
  if(key.lo<0)for(int x=0;x<M;x++)for(U d=jumps[x%nr];d;d&=d-1){int j=x+countr_zero(d);if(j<=M)pred[j]|=pred[x];}
  for(auto a:arcs)if(key.a[a.k]&(U(1)<<a.t)){int step=(a.hi-a.lo+nr)%nr;bool ok;if(key.lo<0){int x=a.lo<H?a.lo+nr:a.lo,j=x+step;ok=(reach[j]&(K(1)<<(x+nr)))||(pred[x]&(reach[j]>>H));}
   else{int x=a.lo<key.lo?a.lo+nr:a.lo,j=x+step,hi=key.hi<=key.lo?key.hi+nr:key.hi;ok=j<=hi&&(reach[key.lo]&(K(1)<<x))&&(reach[j]&(K(1)<<hi));}if(ok)keep[a.k]|=U(1)<<a.t;}
  if(kept.size()>70000)kept.clear();kept.emplace(key,keep);return keep;
 }
 bool sweep(long long &avail){
  int padding=0;array<int,24> offsets[3];for(int t=0;t<T;t++)for(int k=0;k<3;k++){P p=tri[t][k];offsets[k][t]=p.x+p.y*nx;padding=max({padding,abs(p.x),abs(p.y)});}Stars all{(1u<<T)-1,(1u<<T)-1,(1u<<T)-1};
  vector<bool> queued(nx*ny);deque<int> queue;int pass=0;
  uint64_t work=0;while(pass<nx*ny||!queue.empty()){int id;if(pass<nx*ny){id=pass++;if(!inside[id])continue;}else{id=queue.front();queue.pop_front();queued[id]=0;}if(!(++work%10000000))cerr<<"visits "<<work<<" queue "<<queue.size()<<" live "<<avail<<"\n";int x=id%nx,y=id/nx;P p{x,y};bool interior=x>=padding&&x+padding<nx&&y>=padding&&y+padding<ny;Stars m{};m[0]=mask[id];for(int k=1;k<3;k++)for(int t=0;t<T;t++){if(!interior){P q=p-tri[t][k];if(q.x<0||q.y<0||q.x>=nx||q.y>=ny)continue;}m[k]|=mask[id-offsets[k][t]]&(1u<<t);}if(m==all||!(m[0]|m[1]|m[2]))continue;
   StarKey state{m,-1,-1};bool corner=false;for(int i=0;i<N;i++){if(p==poly[i]){state.lo=low[i];state.hi=high[i];corner=true;break;}if(!cross(poly[(i+1)%N]-poly[i],p-poly[i])){state.lo=low[i];state.hi=(low[i]+nr/2)%nr;}}
   auto keep=solve(state);if(corner&&!(keep[0]|keep[1]|keep[2]))return false;
   for(int k=0;k<3;k++)for(U lost=m[k]&~keep[k];lost;lost&=lost-1){int t=countr_zero(lost);U bit=1u<<t;auto &q=mask[id-offsets[k][t]];if(q&bit){q^=bit;avail--;int anch=id-offsets[k][t];for(int s=0;s<3;s++)if(s!=k){int idx=anch+offsets[s][t];if(idx<pass&&!queued[idx]){queued[idx]=1;queue.push_back(idx);}}}}
  }
  for(auto v:poly){bool any=false;for(int t=0;t<T&&!any;t++)for(auto q:tri[t]){P p=v-q;if(p.x>=0&&p.y>=0&&p.x<nx&&p.y<ny&&(mask[p.y*nx+p.x]&(U(1)<<t)))any=true;}if(!any)return false;}return true;
 }
};
