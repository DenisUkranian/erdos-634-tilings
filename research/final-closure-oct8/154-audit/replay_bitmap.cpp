// Independent complete-lattice geometry and zero-current support certificate
// verifier. Reads claimed zero masks; proves them from current geometric
// endpoint supports. The producer's scan order and status are not trusted.
#include <algorithm>
#include <array>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <map>
#include <numeric>
#include <stdexcept>
#include <string>
#include <vector>
using namespace std;using I=int64_t;using U=uint64_t;
struct P{int x,y;};P add(P a,P b){return{a.x+b.x,a.y+b.y};}P sub(P a,P b){return{a.x-b.x,a.y-b.y};}P mul(P a,P b){return{a.x*b.x-a.y*b.y,a.x*b.y+a.y*b.x+a.y*b.y};}P scale(P a,int n){return{a.x*n,a.y*n};}P powr(P a,int n){P r{1,0};while(n-->0)r=mul(r,a);return r;}I cross(P a,P b){return I(a.x)*b.y-I(a.y)*b.x;}I norm(P a){return I(a.x)*a.x+I(a.x)*a.y+I(a.y)*a.y;}
void require(bool a,const string&b){if(!a)throw runtime_error(b);}
I floorq(I a,I b){require(b>0,"denominator");return a>=0?a/b:-((-a+b-1)/b);}I ceilq(I a,I b){return-floorq(-a,b);}
pair<int,int> direction(P a){int d=gcd(abs(a.x),abs(a.y));require(d!=0,"zero direction");a.x/=d;a.y/=d;if(a.x<0||(a.x==0&&a.y<0)){a.x=-a.x;a.y=-a.y;}return{a.x,a.y};}
struct Fraction{I n,d;};bool lessf(Fraction a,Fraction b){return a.n*b.d<b.n*a.d;}
struct Shape{array<P,3> p;array<int,3>d;};struct Incidence{int tile;P endpoint;int sign;};struct Boundary{int d,y,x,sign;};
U decode(const unsigned char*p,int n){U x=0;for(int j=n-1;j>=0;j--)x=(x<<8)|p[j];return x;}
int main(int argc,char**argv){try{
 require(argc==12,"usage: L U rotation trace output expectedPlacements badD badY badW badMask sourceLabel");int L=stoi(argv[1]),H=stoi(argv[2]),rotation=stoi(argv[3]);require(L<=0&&H>=0&&H-L<=4&&rotation>=0&&rotation<6,"parameter range");
 U expected=stoull(argv[6]),badMask=stoull(argv[10]);int badD=stoi(argv[7]),badY=stoi(argv[8]),badW=stoi(argv[9]);
 array<P,6> roots{P{1,0},P{0,1},P{-1,1},P{-1,0},P{0,-1},P{1,-1}};
 P invg=mul(mul(powr({3,1},-L),powr({4,-1},H)),roots[rotation]);I normscale=norm(invg);
 array<P,3> target{P{0,0},scale(invg,154),mul(invg,{49,56})};int xmin=0,xmax=0,ymin=0,ymax=0;
 for(P p:target){xmin=min(xmin,p.x);xmax=max(xmax,p.x);ymin=min(ymin,p.y);ymax=max(ymax,p.y);}
 const int rows=ymax-ymin+1,words=(xmax-xmin+64)/64;const U size=U(rows)*words;
 vector<int> left(rows),right(rows);
 // Independent initialization: intersect horizontal lines with the three
 // boundary segments using rational interpolation, then round endpoints.
 U points=0;
 for(int y=ymin;y<=ymax;y++){
  vector<Fraction> xs;
  for(int e=0;e<3;e++){P a=target[e],b=target[(e+1)%3];if(y<min(a.y,b.y)||y>max(a.y,b.y))continue;
   if(a.y==b.y){xs.push_back({a.x,1});xs.push_back({b.x,1});}
   else{I den=I(b.y)-a.y,num=I(a.x)*den+I(y-a.y)*(b.x-a.x);if(den<0){den=-den;num=-num;}xs.push_back({num,den});}
  }
  require(xs.size()>=2,"missing polygon slice");auto lo=*min_element(xs.begin(),xs.end(),lessf),hi=*max_element(xs.begin(),xs.end(),lessf);
  left[y-ymin]=int(ceilq(lo.n,lo.d));right[y-ymin]=int(floorq(hi.n,hi.d));points+=max(0,right[y-ymin]-left[y-ymin]+1);
 }
 map<pair<int,int>,int> did;vector<pair<int,int>> dirs;vector<Shape> shapes;
 for(int h=L;h<=H;h++){P unit=mul(mul(powr({3,1},h-L),powr({4,-1},H-h)),roots[rotation]);require(norm(unit)==normscale,"unit length");for(int ch=0;ch<2;ch++)for(int r=0;r<6;r++){
  Shape s;s.p={P{0,0},scale(mul(unit,roots[r]),ch?7:8),scale(mul(unit,roots[(r+2)%6]),ch?8:7)};require(cross(s.p[1],s.p[2])==56*normscale,"tile oriented area");array<I,3> ns;
  for(int e=0;e<3;e++){P d=sub(s.p[(e+1)%3],s.p[e]);ns[e]=norm(d);auto key=direction(d);if(!did.count(key)){did[key]=dirs.size();dirs.push_back(key);}s.d[e]=did.at(key);}
  sort(ns.begin(),ns.end());require(ns==array<I,3>{49*normscale,64*normscale,169*normscale},"tile norms");shapes.push_back(s);
 }}
 vector<vector<Incidence>> incidences(dirs.size());for(int s=0;s<int(shapes.size());s++)for(int e=0;e<3;e++){incidences[shapes[s].d[e]].push_back({s,shapes[s].p[e],1});incidences[shapes[s].d[e]].push_back({s,shapes[s].p[(e+1)%3],-1});}
 vector<Boundary> boundary;for(int e=0;e<3;e++){int d=did.at(direction(sub(target[(e+1)%3],target[e])));for(int end=0;end<2;end++){P p=target[(e+end)%3];boundary.push_back({d,p.y-ymin,p.x-xmin,end?-1:1});}}
 vector<vector<U>> allowed(shapes.size(),vector<U>(size));U count=0;
 for(int s=0;s<int(shapes.size());s++)for(int yy=0;yy<rows;yy++){
  int a=left[yy],b=right[yy];for(int k=1;k<3;k++){P p=shapes[s].p[k];int y=yy+p.y;if(y<0||y>=rows){b=a-1;break;}a=max(a,left[y]-p.x);b=min(b,right[y]-p.x);}
  if(a>b)continue;count+=b-a+1;int from=a-xmin,to=b-xmin;
  for(int w=from/64;w<=to/64;w++){int first=max(from-64*w,0),last=min(to-64*w,63);U mask=(~U(0)<<first)&(~U(0)>>(63-last));allowed[s][U(yy)*words+w]=mask;}
 }
 require(count==expected,"independent complete-placement count mismatch");cerr<<"Independent bitmap initialization: "<<count<<" placements, "<<points<<" points\n";
 auto word=[&](int s,int y,I w)->U{if(y<0||y>=rows||w<0||w>=words)return 0;return allowed[s][U(y)*words+U(w)];};
 auto fetch=[&](int s,int y,I x)->U{I q=floorq(x,64);int k=int(x-64*q);U a=word(s,y,q);return k?((a>>k)|(word(s,y,q+1)<<(64-k))):a;};
 auto erase=[&](int s,int y,I x,U mask)->U{if(!mask||y<0||y>=rows)return 0;I q=floorq(x,64);int k=int(x-64*q);U removed=0;for(int part=0;part<(k?2:1);part++){I w=q+part;if(w<0||w>=words)continue;U cut=part?(mask>>(64-k)):(mask<<k);U& current=allowed[s][U(y)*words+U(w)];removed+=__builtin_popcountll(current&cut);current&=~cut;}return removed;};
 auto banks=[&](int d,int y,int w){array<U,2> result{0,0};for(auto e:incidences[d])result[e.sign<0]|=fetch(e.tile,y-e.endpoint.y,I(64)*w-e.endpoint.x);return result;};
 ifstream in(argv[4],ios::binary);require(bool(in),"trace unavailable");unsigned char raw[28];U records=0,removed=0;
 while(in.read(reinterpret_cast<char*>(raw),28)){
  int d=int(decode(raw,4)),y=int(decode(raw+4,4)),w=int(decode(raw+8,4));U p=decode(raw+12,8),n=decode(raw+20,8);
  require(d>=0&&d<int(dirs.size())&&y>=0&&y<rows&&w>=0&&w<words,"trace record outside geometry");require((p|n)!=0&&(p&n)==0,"malformed zero masks");auto available=banks(d,y,w);
  require((p&~(available[0]&~available[1]))==0,"positive deletion lacks zero opposite bank");require((n&~(available[1]&~available[0]))==0,"negative deletion lacks zero opposite bank");
  for(auto b:boundary)if(b.d==d&&b.y==y&&b.x/64==w)require(((p|n)&(U(1)<<(b.x%64)))==0,"deleting at a nonzero target row");
  for(auto e:incidences[d])removed+=erase(e.tile,y-e.endpoint.y,I(64)*w-e.endpoint.x,e.sign>0?p:n);
  records++;if(records%1000000==0)cerr<<"verified mask records="<<records<<" deleted="<<removed<<"\n";
 }
 require(in.gcount()==0,"truncated record");require(badD>=0&&badD<int(dirs.size())&&badY>=0&&badY<rows&&badW>=0&&badW<words,"bad terminal index");require(__builtin_popcountll(badMask)==1,"terminal not one row");
 int terminalSign=0;for(auto b:boundary)if(b.d==badD&&b.y==badY&&b.x/64==badW&&(U(1)<<(b.x%64))==badMask)terminalSign=b.sign;
 require(terminalSign!=0,"terminal is not a nonzero target-current row");auto available=banks(badD,badY,badW);require((available[terminalSign<0]&badMask)==0,"terminal required-sign support survives");
 ofstream out(argv[5]);require(bool(out),"report unavailable");
 out<<"{\"status\":\"PASS\",\"L\":"<<L<<",\"U\":"<<H<<",\"basis_rotation\":"<<rotation<<",\"placements\":"<<count<<",\"points\":"<<points<<",\"verified_zero_mask_records\":"<<records<<",\"verified_removed\":"<<removed<<",\"remaining\":"<<count-removed<<",\"terminal_direction\":"<<badD<<",\"terminal_y\":"<<badY<<",\"terminal_word\":"<<badW<<",\"terminal_mask\":"<<badMask<<",\"required_sign\":"<<terminalSign<<",\"required_sign_support_empty\":true,\"proof_uses_only_nonnegative_variables\":true,\"producer_label\":\""<<argv[11]<<"\"}\n";
 cerr<<"PASS: target row requires sign "<<terminalSign<<" with no surviving placement of that sign\n";return 0;
 }catch(const exception&e){cerr<<"FAIL: "<<e.what()<<"\n";return 1;}}
