#include <gmpxx.h>
#include <algorithm>
#include <array>
#include <chrono>
#include <cmath>
#include <fstream>
#include <iostream>
#include <map>
#include <set>
#include <sstream>
#include <string>
#include <tuple>
#include <vector>
using namespace std;using Q=mpq_class; Q frac(long n,long d){Q x(n,d);x.canonicalize();return x;}
struct P{Q x,y; bool operator<(const P&p)const {return x<p.x||(x==p.x&&y<p.y);} bool operator==(const P&p)const{return x==p.x&&y==p.y;}bool operator!=(const P&p)const{return !(*this==p);}};
P operator+(P a,P b){return {a.x+b.x,a.y+b.y};} P operator-(P a,P b){return {a.x-b.x,a.y-b.y};} P operator*(P a,Q s){return {a.x*s,a.y*s};}
Q cr(P a,P b){return a.x*b.y-a.y*b.x;}Q ori(P a,P b,P c){return cr(b-a,c-a);} Q norm(P a,int D){return a.x*a.x+D*a.y*a.y;} Q dot(P a,P b,int D){return a.x*b.x+D*a.y*b.y;} P cm(P a,P b,int D){return {a.x*b.x-D*a.y*b.y,a.x*b.y+a.y*b.x};}P con(P a){return {a.x,-a.y};}
Q sqr(Q x){mpz_class a,b;mpz_sqrt(a.get_mpz_t(),x.get_num().get_mpz_t());mpz_sqrt(b.get_mpz_t(),x.get_den().get_mpz_t());if(a*a!=x.get_num()||b*b!=x.get_den())throw runtime_error("irrational sqrt");Q ans(a,b);ans.canonicalize();return ans;}
using T=array<P,3>;using E=pair<P,P>;using B=vector<E>;
T ccw(T t){Q o=ori(t[0],t[1],t[2]);if(o==0)throw runtime_error("degenerate");if(o<0)swap(t[1],t[2]);int k=min_element(t.begin(),t.end())-t.begin();return {t[k],t[(k+1)%3],t[(k+2)%3]};}
bool inside(T t,P p){for(int i=0;i<3;i++)if(ori(t[i],t[(i+1)%3],p)<0)return false;return true;}
struct Box{Q x0,x1,y0,y1;};Box box(T t){Box b{t[0].x,t[0].x,t[0].y,t[0].y};for(auto p:t){b.x0=min(b.x0,p.x);b.x1=max(b.x1,p.x);b.y0=min(b.y0,p.y);b.y1=max(b.y1,p.y);}return b;}
bool bbinter(Box b,Box c){return b.x1>c.x0&&c.x1>b.x0&&b.y1>c.y0&&c.y1>b.y0;}
bool overlaps(T t,T u){for(int k=0;k<2;k++){for(int i=0;i<3;i++){bool sep=true;for(auto p:u)if(ori(t[i],t[(i+1)%3],p)>0){sep=false;break;}if(sep)return false;}swap(t,u);}return true;}
struct Line{bool vert;Q slope,inter;bool operator<(const Line& l)const{return tie(vert,slope,inter)<tie(l.vert,l.slope,l.inter);}};
Line line(P a,P b){P d=b-a;if(d.x==0)return {true,0,a.x};Q r=d.y/d.x;return {false,r,a.y-r*a.x};}
bool onseg(P a,P b,P p){return !(p<min(a,b))&&!(max(a,b)<p)&&ori(a,b,p)==0;}
B subtract_tile(B bd,T t){map<Line,map<P,int>> events;auto add=[&](P a,P b){auto &ev=events[line(a,b)];int s=a<b?1:-1;ev[min(a,b)]+=s;ev[max(a,b)]-=s;};for(auto [a,b]:bd)add(a,b);for(int i=0;i<3;i++)add(t[(i+1)%3],t[i]);B out;set<P> pts;for(auto &[l,ev]:events){int at=0;P prev;bool ini=false;for(auto &[p,ch]:ev){if(ch==0)continue;if(ini&&at){if(abs(at)!=1)throw runtime_error("mult");out.push_back(at==1?E(prev,p):E(p,prev));pts.insert(prev);pts.insert(p);}at+=ch;prev=p;ini=true;}if(at)throw runtime_error("event");}B ret;for(auto [a,b]:out){vector<P> pp;for(P p:pts)if(onseg(a,b,p))pp.push_back(p);if(b<a)reverse(pp.begin(),pp.end());for(size_t i=1;i<pp.size();i++)ret.emplace_back(pp[i-1],pp[i]);}sort(ret.begin(),ret.end());ret.erase(unique(ret.begin(),ret.end()),ret.end());return ret;}
struct Ray{P d,end;bool out;};int half(P p){return (p.y>0||(p.y==0&&p.x>=0))?0:1;}bool rayless(Ray a,Ray b){int ha=half(a.d),hb=half(b.d);return ha!=hb?ha<hb:cr(a.d,b.d)>0;}
struct Sector{P x,d,e;Q cosine;};
vector<Sector> sectors(const B& bd,int D,map<E,E>& nx){map<P,vector<Ray>> rays;for(auto [a,b]:bd){rays[a].push_back({b-a,b,true});rays[b].push_back({a-b,a,false});}vector<Sector> s;for(auto &[x,rr]:rays){sort(rr.begin(),rr.end(),rayless);for(size_t j=0;j<rr.size();j++)if(rr[j].out){auto r=rr[j],t=rr[(j+1)%rr.size()];if(t.out)throw runtime_error("nonalternating");nx[{t.end,x}]={x,r.end};if(cr(r.d,t.d)>0){s.push_back({x,r.d,t.d,dot(r.d,t.d,D)/(sqr(norm(r.d,D))*sqr(norm(t.d,D)))});}}}sort(s.begin(),s.end(),[](Sector a,Sector b){return a.cosine>b.cosine||(a.cosine==b.cosine&&b.x<a.x);});return s;}
string ptjson(P p){return "[\""+p.x.get_str()+"\",\""+p.y.get_str()+"\"]";}string trjson(T t){return "["+ptjson(t[0])+","+ptjson(t[1])+","+ptjson(t[2])+"]";}
struct BC{T t;Box bx;int side,pos,len,sg,eg;};
struct ProofNode{Sector s;vector<pair<T,int>> kids;string reason;};
struct Stop{};
struct Search{int u,v,m,D,N,ta,tb,tc;string fam,out;T target,tile;vector<pair<Q,P>> shapes;vector<T> placed,best,found;vector<Box> boxes;map<B,int> dead;vector<ProofNode> proof;vector<BC> bcs;array<vector<vector<int>>,3> steps;array<int,3> side_lengths;vector<int> ban;vector<vector<int>> undo;map<T,vector<int>> conflicts;bool bcheck=false;long prune_boundary=0;size_t nodes=0;long checks=0,pruned_chain=0,pruned_area=0;int maxdepth=0;double seconds;bool prune;chrono::steady_clock::time_point start,last;
 Search(int u,int v,int m,string fam,double seconds,bool prune,string out):u(u),v(v),m(m),fam(fam),seconds(seconds),prune(prune),out(out){int a=u*v,b=v*v-u*u,c=v*v,Qw=b+c,Pb=b+2*c;D=4*v*v-u*u;int root=1;for(int p=2;p*p<=D;p++)while(D%(p*p)==0){D/=p*p;root*=p;}tile=ccw(T{P{0,0},P{a,0},P{-frac(b*u,2*v),frac(b*root,2*v)}});
 if(fam=="W"){target=ccw(T{P{0,0},P{-frac(v*Qw*m,2),-frac(u*v*m*root,2)},P{-frac(b*Qw*m,2*v),frac(u*b*m*root,2*v)}});N=Qw*m*m;}else{target=ccw(T{P{0,0},P{u*Pb*m,0},P{frac(u*Pb*m,2),frac(b*m*root,2)}});N=Pb*m*m;}
 if(fam=="E120"){a=u;b=v;c=(int)llround(sqrt(a*a+a*b+b*b));if(c*c!=a*a+a*b+b*b)throw runtime_error("norm triple");D=3;tile=ccw(T{P{0,0},P{a,0},P{-frac(b,2),frac(b,2)}});int L=a*b*m;target=ccw(T{P{0,0},P{L,0},P{frac(L,2),frac(L,2)}});N=a*b*m*m;}ta=a;tb=b;tc=c;
 for(int i=0;i<3;i++)for(int j=0;j<3;j++)if(i!=j){int k=3-i-j;P d=tile[j]-tile[i],e=tile[k]-tile[i];Q le=sqr(norm(d,D));for(int fl=0;fl<2;fl++){P dd=fl?con(d):d,ee=fl?con(e):e;P ra=cm(ee,con(dd),D)*(Q(1)/le);if(ra.y>0)shapes.emplace_back(le,ra);}}sort(shapes.begin(),shapes.end(),[](auto x,auto y){return x.first<y.first||(x.first==y.first&&x.second<y.second);});shapes.erase(unique(shapes.begin(),shapes.end(),[](auto x,auto y){return x.first==y.first&&x.second==y.second;}),shapes.end());start=last=chrono::steady_clock::now();bcheck=getenv("BOUNDARY")!=nullptr;if(bcheck)init_boundary();}

 int angtype(Q opposite){if(opposite==ta)return 0;if(opposite==tb)return 1;if(opposite==tc)return 2;throw runtime_error("angle");}
 bool angleok(int vertex,int angle){if(fam=="E120")return angle<2;Q op=sqr(norm(target[(vertex+1)%3]-target[(vertex+2)%3],D));int b=v*v-u*u,Qw=b+v*v,Pb=Qw+v*v;if(fam=="W"){if(op==m*v*b)return angle==1;if(op==m*u*Qw)return angle==0;return angle<2;}else{if(op==m*u*Pb)return angle==0;return angle==1;}}
 void init_boundary(){for(int e=0;e<3;e++){P base=target[e],dd=target[(e+1)%3]-base;Q le=sqr(norm(dd,D));if(le.get_den()!=1)throw runtime_error("side len");int L=le.get_num().get_si();side_lengths[e]=L;steps[e].resize(L+1);P unit=dd*(1/le);for(int x=0;x<L;x++)for(auto [si,ra]:shapes){int l=si.get_num().get_si();if(x+l>L)continue;P z=cm(unit,ra,D);int sg=angtype(sqr(norm(z-unit*si,D))),eg=angtype(sqr(norm(z,D)));if(x==0&&!angleok(e,sg))continue;if(x+l==L&&!angleok((e+1)%3,eg))continue;P at=base+unit*x;T t=ccw(T{at,at+unit*si,at+z});bool ok=true;for(P p:t)if(!inside(target,p))ok=false;if(!ok)continue;int k=bcs.size();bcs.push_back({t,box(t),e,x,l,sg==2,eg==2});steps[e][x].push_back(k);}}ban.assign(bcs.size(),0);cerr<<"boundary dictionary "<<bcs.size()<<endl;}
 void boundary_push(T t){auto it=conflicts.find(t);if(it==conflicts.end()){Box bx=box(t);vector<int> bad;for(size_t k=0;k<bcs.size();k++){BC bc=bcs[k];if(t==bc.t)continue;if(bbinter(bx,bc.bx)&&overlaps(t,bc.t))bad.push_back(k);}it=conflicts.emplace(t,std::move(bad)).first;}undo.push_back(it->second);for(int k:undo.back())ban[k]++;}
 void boundary_pop(){for(int k:undo.back())ban[k]--;undo.pop_back();}
 bool boundary_ok(){for(int e=0;e<3;e++){int L=side_lengths[e];vector<unsigned int> reachable(L+1,0);reachable[0]=1;for(int p=0;p<L;p++)if(reachable[p]){for(int k:steps[e][p])if(!ban[k]){BC bc=bcs[k];for(int st=0;st<12;st++)if(reachable[p]&(1u<<st)){int cc=st/6,pg=st%6/3,pc=st%3; if(pg&&bc.sg)continue;if(pc==2&&bc.sg)continue;bool isc=bc.len==tc;int nc=isc?(p==0||pg?2:1):0,ncc=cc||(pc&&isc);int ns=ncc*6+bc.eg*3+nc;reachable[p+bc.len]|=1u<<ns;}}}if(!(reachable[L]&((1u<<6)|(1u<<7)|(1u<<9)|(1u<<10))))return false;}return true;}
 double elapsed(){return chrono::duration<double>(chrono::steady_clock::now()-start).count();}
 vector<T> placements(Sector s){Q le=sqr(norm(s.d,D));P unit=s.d*(1/le);vector<T> res;for(auto[si,ra]:shapes){P q=cm(unit,ra,D);if(cr(q,s.e)<0)continue;T cand=ccw(T{s.x,s.x+unit*si,s.x+q});bool ok=true;for(P p:cand)if(!inside(target,p)){ok=false;break;}if(!ok)continue;Box bx=box(cand);for(size_t j=0;j<placed.size();j++)if(bbinter(bx,boxes[j])&&overlaps(cand,placed[j])){ok=false;break;}if(ok)res.push_back(cand);}sort(res.begin(),res.end());res.erase(unique(res.begin(),res.end()),res.end());return res;}
 bool rayblocked(P x,P d){for(int i=0;i<3;i++){P a=target[i],b=target[(i+1)%3];if(ori(a,b,x)==0&&cr(b-a,d)<0)return true;}for(T t:placed){bool ok=true,zero=true;for(int i=0;i<3;i++){Q sg=ori(t[i],t[(i+1)%3],x);if(sg<0||(sg==0&&cr(t[(i+1)%3]-t[i],d)<=0)){ok=false;break;}}if(ok)return true;}return false;}
 bool coins(int L){int a=ta,b=tb,c=tc;for(int k=0;k*c<=L;k++)for(int j=0;j*b<=L-k*c;j++)if((L-k*c-j*b)%a==0)return true;return false;}
 bool lengthok(B bd){map<Line,vector<tuple<P,P,int>>> groups;for(auto[a,b]:bd)groups[line(a,b)].emplace_back(min(a,b),max(a,b),a<b?1:-1);for(auto &[l,es]:groups){sort(es.begin(),es.end());vector<tuple<P,P,int>> vv;for(auto e:es){if(!vv.empty()&&get<1>(vv.back())==get<0>(e)&&get<2>(vv.back())==get<2>(e))get<1>(vv.back())=get<1>(e);else vv.push_back(e);}for(auto[a,b,s]:vv){P d=b-a;if(rayblocked(a,d*(-1))&&rayblocked(b,d)){Q le=sqr(norm(d,D));if(le.get_den()!=1||!coins(le.get_num().get_si()))return false;}}}return true;}
 bool areaok(B bd,map<E,E>&nx){set<E> un(bd.begin(),bd.end());vector<Q> ar;while(!un.empty()){E e=*un.begin(),cur=e;Q a=0;while(true){auto it=un.find(cur);if(it==un.end()){if(cur!=e)throw runtime_error("cycle");break;}un.erase(it);a+=cr(cur.first,cur.second);cur=nx.at(cur);}if(a<0)return true;if(a>0)ar.push_back(a);}for(Q a:ar)if(Q(a/ori(tile[0],tile[1],tile[2])).get_den()!=1)return false;return true;}
 pair<bool,int> dfs(const B& bd){if((++nodes%128)==0){auto now=chrono::steady_clock::now();if(elapsed()>seconds)throw Stop();if(chrono::duration<double>(now-last).count()>10){cerr<<"nodes="<<nodes<<" depth="<<maxdepth<<" seconds="<<elapsed()<<" boundary="<<prune_boundary<<" cached="<<dead.size()<<endl;last=now;}}if((int)placed.size()>maxdepth){maxdepth=placed.size();best=placed;}
 if((int)placed.size()==N){if(!bd.empty())throw runtime_error("bad coverage");found=placed;return {true,-1};}
 // no memoization in proof-producing replay

 ProofNode pn;bool bad=false;if(bcheck&&!boundary_ok()){bad=true;pn.reason="boundary";prune_boundary++;}if(!bad&&prune&&!lengthok(bd)){bad=true;pn.reason="chain";pruned_chain++;}
 map<E,E> nx;vector<Sector> ss;if(!bad){ss=sectors(bd,D,nx);if(prune&&!areaok(bd,nx)){bad=true;pn.reason="area";pruned_area++;}}
 vector<T> ps;bool ini=false;if(!bad){for(auto s:ss){auto cur=placements(s);if(!ini||cur.size()<ps.size()){ini=true;ps=cur;pn.s=s;}if(ps.size()<=1)break;}if(!ini)throw runtime_error("no convex");pn.reason=ps.empty()?"no_corner_tile":"branch";}
 int node=proof.size();proof.push_back(pn);
 for(auto t:ps){B nb=subtract_tile(bd,t);placed.push_back(t);boxes.push_back(box(t));if(bcheck)boundary_push(t);auto [yes,k]=dfs(nb);if(bcheck)boundary_pop();boxes.pop_back();placed.pop_back();if(yes)return {true,-1};proof[node].kids.emplace_back(t,k);}return {false,node};}
 void save(string status,int root){ofstream f(out);f<<"{\"status\":\""<<status<<"\",\"u\":"<<u<<",\"v\":"<<v<<",\"m\":"<<m<<",\"branch\":\""<<fam<<"\",\"D\":"<<D<<",\"N\":"<<N<<",\"nodes\":"<<nodes<<",\"maximum_placed\":"<<maxdepth<<",\"seconds\":"<<elapsed()<<",\"target\":"<<trjson(target)<<",\"template\":"<<trjson(tile)<<",\"prunes_chain\":"<<pruned_chain<<",\"prunes_area\":"<<pruned_area<<",\"triangles\":[";auto &ts=found.empty()?best:found;for(size_t j=0;j<ts.size();j++){if(j)f<<",";f<<trjson(ts[j]);}f<<"],\"proof_root\":"<<root<<",\"proof\":[";
 if(status=="EXHAUSTED"){for(size_t j=0;j<proof.size();j++){if(j)f<<",";auto p=proof[j];f<<"{\"reason\":\""<<p.reason<<"\",\"x\":"<<ptjson(p.s.x)<<",\"d\":"<<ptjson(p.s.d)<<",\"e\":"<<ptjson(p.s.e)<<",\"children\":[";for(size_t k=0;k<p.kids.size();k++){if(k)f<<",";f<<"["<<trjson(p.kids[k].first)<<","<<p.kids[k].second<<"]";}f<<"]}";}}f<<"]}\n";cerr<<status<<" nodes="<<nodes<<" depth="<<maxdepth<<" secs="<<elapsed()<<" saved="<<out<<endl;}
 void run(){B bd;for(int i=0;i<3;i++)bd.emplace_back(target[i],target[(i+1)%3]);sort(bd.begin(),bd.end());

 const char*rt=getenv("W_ADJ_ROOT");if(rt){
 if(u!=v-1 || v<3 || m!=2 || fam!="W")throw runtime_error("general adjacent root domain");
 int k=atoi(rt);if(k<0||k>1)throw runtime_error("root choice");
 P C,A,third;bool fc=false,fa=false; int b=v*v-u*u,c=v*v,a=u*v;
 for(int j=0;j<3;j++){Q op=sqr(norm(target[(j+1)%3]-target[(j+2)%3],D));
 if(op==m*u*(2*v*v-u*u)){C=target[j];fc=true;}
 if(op==m*v*v*v){A=target[j];fa=true;}}
 if(!fc||!fa)throw runtime_error("root corners");
 for(P p:target)if(p!=C&&p!=A)third=p;
 P axis=(A-C)*(Q(1)/sqr(norm(A-C,D)));bool left=cr(A-C,third-C)>0;
 vector<array<int,3>> choices={{c,b,a},k==0?array<int,3>{c,b,a}:array<int,3>{c,a,b},{a,b,c},{a,b,c}};
 int pos=0;for(auto sr:choices){int ss=sr[0],rr=sr[1],op=sr[2];
 Q proj=frac(ss*ss+rr*rr-op*op,2*ss);Q h=sqr(Q(rr*rr-proj*proj)/D);
 P vv=cm(axis,P{proj,left?h:-h},D),at=C+axis*pos;
 T t=ccw(T{at,at+axis*ss,at+vv});
 for(P p:t)if(!inside(target,p))throw runtime_error("root containment");
 for(T old:placed)if(overlaps(old,t))throw runtime_error("root overlap");
 placed.push_back(t);boxes.push_back(box(t));if(bcheck)boundary_push(t);bd=subtract_tile(bd,t);pos+=ss;}
 if(pos!=m*v*b)throw runtime_error("root side length");
 }
 const char*bf=getenv("BETAFAN");if(bf){if(fam!="beta")throw runtime_error("fan target");int mask=atoi(bf);if(mask<0||mask>7)throw runtime_error("fan mask");int apex=0;for(int j=0;j<3;j++)if(sqr(norm(target[(j+1)%3]-target[(j+2)%3],D))==m*u*(3*v*v-u*u))apex=j;P origin=target[apex],ray=target[(apex+1)%3]-origin;P axis=ray*(1/sqr(norm(ray,D)));for(int j=0;j<3;j++){int a=u*v,b=v*v-u*u,c=v*v;int side=(mask>>j)&1?c:b;bool found=false;P next;T chosen;for(auto[si,ra]:shapes)if(si==side&&angtype(sqr(norm(ra-P{si,0},D)))==0){P vv=cm(axis,ra,D);chosen=ccw(T{origin,origin+axis*si,origin+vv});next=vv*(1/sqr(norm(vv,D)));found=true;break;}if(!found)throw runtime_error("no alpha template");for(P p:chosen)if(!inside(target,p))throw runtime_error("fan outside");for(T t:placed)if(overlaps(t,chosen))throw runtime_error("fan overlap");placed.push_back(chosen);boxes.push_back(box(chosen));if(bcheck)boundary_push(chosen);bd=subtract_tile(bd,chosen);axis=next;}}
 try{auto [y,r]=dfs(bd);save(y?"TILING_FOUND":"EXHAUSTED",r);}catch(Stop&){save("INCOMPLETE",-1);}}
};
int main(int argc,char**argv){if(argc<8){cerr<<"u v m W seconds prune output\n";return 1;}try{int u=stoi(argv[1]),v=stoi(argv[2]),m=stoi(argv[3]);string fam=argv[4];if(u!=3||v!=4||m!=2||fam!="W"||stoi(argv[6])!=0)throw runtime_error("This exploratory branch is restricted to W92 with no chain/area pruning");Search s(u,v,m,fam,stod(argv[5]),false,argv[7]);s.run();}catch(exception&e){cerr<<"ERROR "<<e.what()<<endl;return 2;}}
