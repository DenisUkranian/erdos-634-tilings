#define main reduction_main
#include "rle_equilateral135.cpp"
#undef main
int main(){int n,m,shift,p;while(cin>>n>>m>>shift>>p){Runs a(n),b(m),work,c;for(auto&s:a)cin>>s.lo>>s.hi;for(auto&s:b)cin>>s.lo>>s.hi;c=a;unite(c,b,shift,work);cout<<c.size();for(auto s:c)cout<<' '<<s.lo<<' '<<s.hi;cout<<'\n';UI deleted=difference(a,b,shift,c);cout<<deleted<<' '<<c.size();for(auto s:c)cout<<' '<<s.lo<<' '<<s.hi;cout<<'\n';cout<<contains(a,p)<<'\n';c=a;removePoint(c,p);cout<<c.size();for(auto s:c)cout<<' '<<s.lo<<' '<<s.hi;cout<<'\n';}}
