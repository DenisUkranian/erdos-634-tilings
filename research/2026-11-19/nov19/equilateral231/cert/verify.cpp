// Independently replay packed endpoint deductions, in reverse order on disk.
// Usage: ./verify L U proof.backtrace.bin root_vertex root_axis_x root_axis_y root_sign
// root_sign = 0 for the start or 1 for the end of a CCW target edge.
// Build with c++ -O3 -std=c++17 verify.cpp -o verify
#include <algorithm>
#include <array>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <iostream>
#include <fstream>
#include <cstring>
#include <map>
#include <memory>
#include <numeric>
#include <stdexcept>
#include <string>
#include <utility>
#include <vector>
using namespace std;
using LL = long long;
using Word = uint64_t;
using V = pair<int,int>;
using Triangle = array<V,3>;

V add(V a,V b) {return {a.first+b.first,a.second+b.second};}
V minusv(V a,V b) {return {a.first-b.first,a.second-b.second};}
V scale(V v,int n) {return {n*v.first,n*v.second};}
V product(V a,V b) {
    return {a.first*b.first-a.second*b.second,
            a.first*b.second+a.second*b.first+a.second*b.second};
}
V power(V v,int n) {V result{1,0};while(n-->0) result=product(result,v);return result;}
LL cross(V a,V b) {return LL(a.first)*b.second-LL(a.second)*b.first;}
V axis(V direction) {
    int g=gcd(direction.first,direction.second);
    if(direction<V{0,0}) g=-g;
    return {direction.first/g,direction.second/g};
}
void require(bool condition,const string& why) {if(!condition) throw runtime_error(why);}

struct Endpoint {int orientation;V vertex;};
struct Constraint {array<vector<Endpoint>,2> ends;map<V,int> external;};
struct Edge {Constraint* rule;V offset;int sign;};
struct Shape {array<Edge,6> incidences;array<LL,3> boundary;};

// One bit per forbidden translation. Initial geometric containment is checked
// separately by translating the three target half-planes inward.
class Forbidden {
    int rows,words;
    vector<Word> data;
public:
    Forbidden(int ny,int nw):rows(ny),words(nw), data(size_t(36)*ny*nw,0){}
    Word get(int o,int y,int w) const{
        if(y<0||y>=rows||w<0||w>=words)return 0;
        return data[(size_t(o)*rows+y)*words+w];
    }
    void mark(int o,int y,int w,Word mask){
        if(y<0||y>=rows||w<0||w>=words)return;
        data[(size_t(o)*rows+y)*words+w]|=mask;
    }
};
struct Packed {uint32_t di,y,w;uint64_t starts,ends;} __attribute__((packed));
static_assert(sizeof(Packed)==28);
struct Range{int lo,hi;};
LL floor_div(LL a,LL b){if(b<=0)throw runtime_error("denominator");return a>=0?a/b:-((-a+b-1)/b);}
struct Shift {int o,dy,blocks,bits;};
int main(int argc,char**argv){
    size_t processed=0;
    try {
        require(argc==8,"arguments: L U certificate root_vertex root_axis_x root_axis_y root_sign");
        int lo=stoi(argv[1]),hi=stoi(argv[2]),corner=stoi(argv[4]),ux=stoi(argv[5]),uy=stoi(argv[6]),rootEnd=stoi(argv[7]);
        require((lo==0&&hi==2)||(lo==-1&&hi==1),"unknown band");
        require(corner>=0&&corner<3&&(rootEnd==0||rootEnd==1),"invalid root");
        const V p{7,-3},q{4,3},rho{0,1};
        V factor=product(power(p,-lo),power(q,hi));
        Triangle target{{{0,0},scale(factor,231),scale(product(rho,factor),231)}};
        array<V,3> wall;
        map<V,Constraint> rules;
        for(int k=0;k<3;++k){
            V from=target[k],to=target[(k+1)%3];wall[k]=minusv(to,from);
            auto& rhs=rules[axis(wall[k])].external;
            rhs[from]++;rhs[to]--;
        }
        vector<Shape> shapes;vector<V> axes;
        for(int h=lo;h<=hi;h++){
            V basis=product(power(p,h-lo),power(q,hi-h));
            for(int first: {33,7}){
                for(int j=0;j<6;j++){
                    V u=product(basis,power(rho,j));
                    Triangle t{{{0,0},scale(u,first),scale(product(u,power(rho,2)),40-first)}};
                    require(cross(t[1],t[2])>0,"internal orientation");
                    Shape shape;int o=shapes.size();
                    for(int k=0;k<3;k++){
                        shape.boundary[k]=cross(wall[k],target[k])-min({LL(0),cross(wall[k],t[1]),cross(wall[k],t[2])});
                        V start=t[k],end=t[(k+1)%3];V ax=axis(minusv(end,start));
                        if(find(axes.begin(),axes.end(),ax)==axes.end())axes.push_back(ax);
                        auto& row=rules[ax];
                        row.ends[0].push_back({o,start});row.ends[1].push_back({o,end});
                        shape.incidences[2*k]={&row,start,0};shape.incidences[2*k+1]={&row,end,1};
                    }
                    shapes.push_back(shape);
                }
            }
        }

        int xmin=0,xmax=0,ymin=0,ymax=0;
        for(V v:target){xmin=min(xmin,v.first);xmax=max(xmax,v.first);ymin=min(ymin,v.second);ymax=max(ymax,v.second);}
        int height=ymax-ymin+1,width=(xmax-xmin+64)/64;
        vector<vector<Range>> admissible(36,vector<Range>(height));
        for(int o=0;o<36;++o)for(int iy=0;iy<height;++iy){
            LL low=xmin,high=xmax;int y=iy+ymin;
            for(int k=0;k<3;++k){
                auto [dx,dy]=wall[k];LL val=LL(dx)*y-shapes[o].boundary[k];
                if(dy>0)high=min(high,floor_div(val,dy));
                else if(dy<0)low=max(low,-floor_div(val,-dy));
                else if(val<0){low=1;high=0;break;}
            }
            admissible[o][iy]={int(low)-xmin,int(high)-xmin};
        }
        Forbidden rejected(height,width);
        vector<array<vector<Shift>,2>> tests(axes.size());
        struct Boundary {int iy,w,sign;Word mask;};
        vector<vector<Boundary>> outer(axes.size());
        for(size_t i=0;i<axes.size();++i){
            auto& row=rules[axes[i]];
            for(auto [p,amt]:row.external){
                int x=p.first-xmin;outer[i].push_back({p.second-ymin,x/64,amt,Word(1)<<(x%64)});
            }
            for(int sign=0;sign<2;++sign)for(auto e:row.ends[sign]){
                int dx=-e.vertex.first;int blocks=floor_div(dx,64);
                tests[i][sign].push_back({e.orientation,-e.vertex.second,blocks,dx-64*blocks});
            }
        }
        auto available=[&](int o,int y,int w)->Word{
            if(y<0||y>=height||w<0||w>=width)return 0;
            auto [a,b]=admissible[o][y];int x=64*w;
            if(a>b||x>b||x+63<a)return 0;
            Word mask=~Word(0);
            if(a>x)mask<<=a-x;
            if(b<x+63)mask&=(~Word(0)>>(x+63-b));
            return mask&~rejected.get(o,y,w);
        };
        auto possible=[&](const Shift& s,int y,int w){
            int yy=y+s.dy,ww=w+s.blocks;
            Word bits=available(s.o,yy,ww)>>s.bits;
            if(s.bits)bits|=available(s.o,yy,ww+1)<<(64-s.bits);
            return bits;
        };
        auto insert=[&](const Shift& s,int y,int w,Word mask){
            rejected.mark(s.o,y+s.dy,w+s.blocks,mask<<s.bits);
            if(s.bits)rejected.mark(s.o,y+s.dy,w+s.blocks+1,mask>>(64-s.bits));
        };
        auto rootIt=find(axes.begin(),axes.end(),V{ux,uy});
        require(rootIt!=axes.end(),"unknown root direction");
        auto& root=rules[*rootIt];V rp=target[corner];
        auto rhs=root.external.find(rp);
        require(rhs!=root.external.end()&&rhs->second==(rootEnd?-1:1),"root lacks required exterior sign");
        ifstream f(argv[3],ios::binary|ios::ate);require(bool(f),"cannot read proof");
        auto bytes=static_cast<size_t>(f.tellg());require(bytes%sizeof(Packed)==0,"truncated proof record");
        size_t remaining=bytes/sizeof(Packed),bit_count=0;
        vector<Packed> buf(65536);
        while(remaining){
            size_t n=min(remaining,buf.size());remaining-=n;f.seekg(remaining*sizeof(Packed));
            require(bool(f.read(reinterpret_cast<char*>(buf.data()),n*sizeof(Packed))),"read failure");
            while(n-->0){
                const auto& r=buf[n];++processed;
                require(r.di<axes.size()&&r.y<unsigned(height)&&r.w<unsigned(width),"row out of range");
                require((r.starts||r.ends)&&!(r.starts&r.ends),"empty or contradictory mask");
                for(const auto& b:outer[r.di])if(b.iy==int(r.y)&&b.w==int(r.w))
                    require(!((r.starts|r.ends)&b.mask),"zero boundary rule used on exterior term");
                for(int j=0;j<2;++j){
                    Word mask=j?r.ends:r.starts;if(!mask)continue;
                    for(const auto& t:tests[r.di][1-j])
                        if(possible(t,r.y,r.w)&mask)throw runtime_error("an opposite endpoint placement is still possible");
                }
                for(int j=0;j<2;++j){
                    Word mask=j?r.ends:r.starts;if(!mask)continue;
                    bit_count+=__builtin_popcountll(mask);
                    for(const auto& t:tests[r.di][j])insert(t,r.y,r.w,mask);
                }
            }
        }
        int x=rp.first-xmin;
        for(const auto& t:tests[rootIt-axes.begin()][rootEnd])
            require(!(possible(t,rp.second-ymin,x/64)&(Word(1)<<(x%64))),"root still has a placement");
        cout<<"PASS band "<<lo<<" "<<hi<<" verified_packed_rows "<<processed<<" endpoint_deductions "<<bit_count
            <<" root "<<rp.first<<" "<<rp.second<<" axis "<<ux<<" "<<uy<<" sign "<<(rootEnd?-1:1)<<"\n";
    }catch(const exception& e){cerr<<"REJECT after "<<processed<<" packed deductions: "<<e.what()<<"\n";return 1;}
}
