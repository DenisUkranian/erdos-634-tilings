// Evaluate the bounded grammar in the max-plus semiring on actual gate sites.
// Input and output consist of little-endian signed int32 values.
#include <algorithm>
#include <cassert>
#include <cstdint>
#include <iostream>
#include <limits>
#include <map>
#include <vector>

using namespace std;
static_assert(sizeof(int32_t)==4);

int read_int() {
    unsigned char b[4];
    cin.read(reinterpret_cast<char*>(b),4);
    if (!cin) throw runtime_error("truncated input");
    uint32_t v=0;
    for (int i=0;i<4;++i) v |= uint32_t(b[i]) << (8*i);
    return static_cast<int32_t>(v);
}
void write_int(int value) {
    for (int k=0;k<4;++k) cout.put(static_cast<char>((uint32_t(value)>>(8*k)) & 255));
}

struct State {
    vector<int> values, support;
};

int main() {
    ios::sync_with_stdio(false);
    int n=read_int(), count=read_int();
    assert(n>0 && count>=7);
    vector<int> slots(n);
    for (int &x:slots) x=read_int();
    assert(is_sorted(slots.begin(),slots.end()));
    vector<int> index(slots.back()+1,-1);
    for (int p=0;p<n;++p) index[slots[p]]=p;

    constexpr int absent=-100000000;
    vector<State> states(count);
    vector<int> offset(count);
    map<int,vector<int>> transports;
    auto transport = [&](int shift) -> const vector<int>& {
        auto [it,fresh]=transports.try_emplace(shift);
        if (fresh) {
            auto &to=it->second;
            to.assign(n,-1);
            for(int p=0;p<n;++p) {
                int q=slots[p]+shift;
                if(q>=0 && q<int(index.size())) to[p]=index[q];
            }
        }
        return it->second;
    };
    for(int id=0;id<count;++id) {
        State &dst=states[id];
        offset[id]=read_int();
        if(id<7) {
            int size=read_int();
            dst.values.assign(n,absent);
            while(size--) {
                int p=read_int();
                assert(p>=0 && p<n);
                dst.support.push_back(p);
                dst.values[p]=0;
            }
            continue;
        }
        int terms=read_int();
        while(terms--) {
            int i=read_int(), j=read_int(), cross=read_int();
            assert(i>=0 && j>=0 && i<id && j<id && offset[i]+offset[j]==offset[id]);
            const State &left=states[i], &right=states[j];
            if(left.support.empty() || right.support.empty()) continue;
            if(dst.values.empty()) dst.values.assign(n,absent);
            if(left.support.size()<=right.support.size()) {
                const auto &next=transport(offset[i]);
                for(int p:left.support) {
                    int q=next[p];
                    if(q>=0 && right.values[q]!=absent)
                        dst.values[p]=max(dst.values[p],left.values[p]+right.values[q]+cross);
                }
            } else {
                const auto &prev=transport(-offset[i]);
                for(int q:right.support) {
                    int p=prev[q];
                    if(p>=0 && left.values[p]!=absent)
                        dst.values[p]=max(dst.values[p],left.values[p]+right.values[q]+cross);
                }
            }
        }
        for(int p=0;p<int(dst.values.size());++p)
            if(dst.values[p]!=absent) dst.support.push_back(p);
    }
    assert(cin.peek()==char_traits<char>::eof());
    const auto &last=states.back();
    for(int p=0;p<n;++p) write_int(last.values.empty()?absent:last.values[p]);
}
