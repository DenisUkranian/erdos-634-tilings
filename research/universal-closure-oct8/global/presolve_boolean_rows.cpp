// Exact row-driven Boolean presolve. Every unit/identification cites its source row.
#include <algorithm>
#include <fstream>
#include <iostream>
#include <map>
#include <numeric>
#include <set>
#include <stdexcept>
#include <string>
#include <vector>
using namespace std;
void need(bool x,const char*s){if(!x)throw runtime_error(s);}
struct Row{int rhs;vector<int>lits;};
struct UF{vector<int>p,s,parity,value;UF(int n):p(n),s(n,1),parity(n),value(n,-1){iota(p.begin(),p.end(),0);}pair<int,int>find(int x){if(p[x]==x)return{x,0};auto[r,q]=find(p[x]);parity[x]^=q;p[x]=r;return{r,parity[x]};}bool fix(int x,int v){auto[r,q]=find(x);v^=q;if(value[r]>=0){need(value[r]==v,"inconsistent unit");return false;}value[r]=v;return true;}bool join(int x,int y,int q){auto[a,u]=find(x);auto[b,v]=find(y);q^=u^v;if(a==b){need(q==0,"inconsistent equality");return false;}if(s[a]<s[b])swap(a,b);p[b]=a;parity[b]=q;s[a]+=s[b];if(value[b]>=0){int va=value[b]^q;need(value[a]<0||value[a]==va,"fixed values disagree");value[a]=va;}return true;}};
pair<map<int,int>,int> reduce(const Row&r,UF&uf){map<int,int>c;int b=r.rhs;for(int lit:r.lits){int sign=lit>0?1:-1;auto[t,p]=uf.find(abs(lit)-1);if(uf.value[t]>=0)b-=sign*(uf.value[t]^p);else{if(p){b-=sign;sign=-sign;}c[t]+=sign;}}for(auto i=c.begin();i!=c.end();)if(i->second==0)i=c.erase(i);else++i;return{c,b};}
int main(int argc,char**argv){try{need(argc==3,"usage original-model prefix");ifstream src(argv[1]);need(bool(src),"source unavailable");int nv,nsel;src>>nv>>nsel;need(nsel==0,"selected metadata unsupported");string line;getline(src,line);for(int i=0;i<nv+nsel;i++)getline(src,line);vector<Row>rows;int b,n;while(src>>b>>n){need(n>=0,"negative row size");Row r{b,{}};for(int i=0;i<n;i++){int lit;src>>lit;need(bool(src)&&abs(lit)>=1&&abs(lit)<=nv,"invalid literal");r.lits.push_back(lit);}rows.push_back(move(r));}need(src.eof(),"model parse failed");
 string prefix=argv[2];ofstream trace(prefix+".trace.txt");UF uf(nv);int merges=0,units=0,passes=0;bool changed,conflict=false;int badrow=-1;
 do{changed=false;passes++;for(int ri=0;ri<(int)rows.size();ri++){
  auto[c,rhs]=reduce(rows[ri],uf);int lo=0,hi=0,g=0;for(auto[x,a]:c){lo+=min(a,0);hi+=max(a,0);g=gcd(g,abs(a));}
  if(rhs<lo||rhs>hi||(g&&rhs%g)||(c.empty()&&rhs!=0)){trace<<"c "<<ri<<'\n';conflict=true;badrow=ri;break;}
  auto setunit=[&](int x,int v){if(uf.fix(x,v)){trace<<"u "<<ri<<' '<<x+1<<' '<<v<<'\n';units++;changed=true;}};
  if(c.empty())continue;
  if(rhs==lo||rhs==hi){bool upper=rhs==hi;for(auto[x,a]:c)setunit(x,upper?(a>0):(a<0));continue;}
  if(c.size()==2){auto it=c.begin();int x=it->first,a=it->second;++it;int y=it->first,d=it->second;vector<pair<int,int>>sol;for(int vx=0;vx<2;vx++)for(int vy=0;vy<2;vy++)if(a*vx+d*vy==rhs)sol.push_back({vx,vy});if(sol.empty()){trace<<"c "<<ri<<'\n';conflict=true;badrow=ri;break;}if(sol.size()==1){setunit(x,sol[0].first);setunit(y,sol[0].second);}else if(sol.size()==2){if(sol[0].first==sol[1].first)setunit(x,sol[0].first);else if(sol[0].second==sol[1].second)setunit(y,sol[0].second);else{int q=sol[0].first^sol[0].second;need((sol[1].first^sol[1].second)==q,"two-solution relation");if(uf.join(x,y,q)){trace<<"m "<<ri<<' '<<x+1<<' '<<y+1<<' '<<q<<'\n';merges++;changed=true;}}}}
 }
 cerr<<"pass "<<passes<<" units "<<units<<" merges "<<merges<<" conflict "<<conflict<<'\n';
 }while(changed&&!conflict);
 trace.close();set<int>rootset;for(int i=0;i<nv;i++){auto[r,q]=uf.find(i);if(uf.value[r]<0)rootset.insert(r);}vector<int>roots(rootset.begin(),rootset.end());map<int,int>index;for(int j=0;j<(int)roots.size();j++)index[roots[j]]=j+1;
 ofstream mapping(prefix+".map.txt");mapping<<nv<<'\n';for(int i=0;i<nv;i++){auto[r,q]=uf.find(i);mapping<<i+1<<' '<<r+1<<' '<<q<<' '<<(uf.value[r]<0?-1:(uf.value[r]^q))<<'\n';}
 ofstream out(prefix+".model.txt");out<<roots.size()<<" 0\n";for(int i=0;i<(int)roots.size();i++)out<<i<<' '<<roots[i]+1<<" 0 0\n";
 set<pair<int,vector<int>>>unique;for(auto&r:rows){auto[c,rhs]=reduce(r,uf);if(c.empty()&&rhs==0)continue;int g=0;for(auto[x,a]:c)g=gcd(g,abs(a));if(g>1&&rhs%g==0){rhs/=g;for(auto&kv:c)kv.second/=g;}vector<int>lits;for(auto[x,a]:c)for(int j=0;j<abs(a);j++)lits.push_back(a>0?index.at(x):-index.at(x));if(!lits.empty()&&lits[0]<0){rhs=-rhs;for(int&v:lits)v=-v;}unique.insert({rhs,lits});}
 if(conflict)unique.insert({1,{}});for(auto&row:unique){out<<row.first<<' '<<row.second.size();for(int lit:row.second)out<<' '<<lit;out<<'\n';}
 ofstream report(prefix+".json");report<<"{\"original_variables\":"<<nv<<",\"original_rows\":"<<rows.size()<<",\"variables\":"<<roots.size()<<",\"rows\":"<<unique.size()<<",\"units\":"<<units<<",\"merges\":"<<merges<<",\"passes\":"<<passes<<",\"conflict\":"<<(conflict?"true":"false")<<",\"bad_row\":"<<badrow<<",\"independently_checked\":false}\n";
 }catch(const exception&e){cerr<<"ERROR "<<e.what()<<'\n';return 1;}}
