#include <algorithm>
#include <array>
#include <cstdlib>
#include <iostream>
#include <vector>
using namespace std;
struct V {int x=0,y=0;V operator+(V o)const{return{x+o.x,y+o.y};} V operator*(int a)const{return{x*a,y*a};}int det(V o)const{return x*o.y-y*o.x;}};
const V U[]={{1,0},{0,1},{-1,1},{-1,0},{0,-1},{1,-1}};
struct Half {array<int,10> key{};array<int,3> moment{};int word=0;int inside=0;};
int a,b,c,half,ab,n;
vector<Half> paths;
long long hits=0,valid=0;
void generate(int len,bool back,V p,array<int,6> net,int area,array<int,3> moment,int word,int inside){
 if(len==half){
   Half h;h.moment=moment;h.word=word;h.inside=inside;
   copy(net.begin(),net.end(),h.key.begin());
   for(int i=0;i<3;i++)h.key[6+i]=(moment[i]%ab+ab)%ab;
   h.key[9]=area;
   if(!back){paths.push_back(h);return;}
   h.key[9]+=ab*n/c;
   auto it=lower_bound(paths.begin(),paths.end(),h,[](const Half& u,const Half& v){return u.key<v.key;});
   for(;it!=paths.end() && it->key==h.key;++it){
    hits++;
    int Npair=(n-inside-it->inside)/2;
    bool ok=(n-inside-it->inside)%2==0;
    int sum=0;
    for(int i=0;i<3;i++){
     int J=it->moment[i]-moment[i];sum+=J;
     if(J<0||J>ab*Npair)ok=false;
    }
    if(sum!=2*ab*Npair){cerr<<"area mismatch "<<sum<<" "<<2*ab*Npair<<"\n";exit(2);}
    if(ok){++valid;cout<<it->word<<" "<<word<<"\n";}
   }
   return;
 }
 for(int t=0;t<((len==0 && !back)?1:12);t++){
  int j=t%6, bank=t/6;
  auto g=net;g[3*bank+j%3]+=j<3?1:-1;
  auto J=moment;V step;
  if(bank){step=U[j]*c;J[j%3]+=p.det(step);}
  else{
   int k=(j+5)%6;
   V s=U[j]*a, w=U[k]*b;step=s+w;
   if(back){J[k%3]+=p.det(w);J[j%3]+=(p+w).det(s);}
   else{J[j%3]+=p.det(s);J[k%3]+=(p+s).det(w);}
  }
  int det=p.det(step);
  if(det%c)abort();
  generate(len+1,back,p+step,g,area+det/c,J,word*12+t,inside+!bank);
 }
}
int main(int argc,char**argv){
 a=atoi(argv[1]);b=atoi(argv[2]);c=atoi(argv[3]);half=atoi(argv[4]);n=c*atoi(argv[5]);ab=a*b;
 generate(0,false,{},{},0,{},0,0);
 sort(paths.begin(),paths.end(),[](const Half& u,const Half& v){return u.key<v.key;});
 generate(0,true,{},{},0,{},0,0);
 cerr<<c<<" length "<<2*half<<" n "<<n<<" modular "<<hits<<" pass "<<valid<<"\n";
}
