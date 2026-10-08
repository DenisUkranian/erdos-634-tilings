// Independent proof replay for the restricted (8,7,13), N=154 problem.
// This program does not solve an LP and does not trust a solver status.
// Every asserted assignment is derived again from one complete signed row.
#include <algorithm>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <limits>
#include <sstream>
#include <stdexcept>
#include <string>
#include <vector>
using namespace std;

template<class T> vector<T> read_array(const string& name, size_t expected) {
    ifstream file(name, ios::binary | ios::ate);
    if (!file) throw runtime_error("Cannot read " + name);
    const auto bytes = file.tellg();
    if (bytes < 0 || static_cast<uint64_t>(bytes) != expected * sizeof(T))
        throw runtime_error("Incorrect binary size: " + name);
    vector<T> values(expected);
    file.seekg(0);
    if (!file.read(reinterpret_cast<char*>(values.data()), bytes))
        throw runtime_error("Truncated binary file: " + name);
    return values;
}

int main() {
    try {
        uint16_t endian = 1;
        if (*reinterpret_cast<unsigned char*>(&endian) != 1)
            throw runtime_error("This binary interchange uses little-endian integers.");
        int nr = 0, nc = 0; int64_t nz = 0;
        ifstream dims("dimensions.txt");
        if (!(dims >> nr >> nc >> nz) || nr != 550333 || nc != 873496 || nz != 19222288)
            throw runtime_error("Unexpected instance dimensions");
        auto ptr = read_array<int64_t>("row_ptr.bin", size_t(nr)+1);
        auto ind = read_array<int32_t>("row_idx.bin", size_t(nz));
        auto sg = read_array<int8_t>("row_dat.bin", size_t(nz));
        auto q = read_array<int32_t>("rhs.bin", size_t(nr));
        if (ptr.front() != 0 || ptr.back() != nz)
            throw runtime_error("Invalid row pointers");
        for (int r=0; r<nr; ++r) {
            if (ptr[r] > ptr[r+1]) throw runtime_error("Nonmonotone pointers");
            int last=-1;
            for (auto k=ptr[r]; k<ptr[r+1]; ++k) {
                if (ind[k] <= last || ind[k] >= nc || (sg[k] != -1 && sg[k] != 1))
                    throw runtime_error("Invalid or duplicated signed row entry");
                last=ind[k];
            }
        }
        vector<int8_t> value(nc, -1);
        ifstream proof("twolevel154_steps.txt");
        if (!proof) throw runtime_error("Missing propagation transcript");
        int64_t checked=0;
        string line;
        while (getline(proof,line)) {
            istringstream in(line);
            int col, v, row; string extra;
            if (!(in >> col >> v >> row) || (in >> extra))
                throw runtime_error("Malformed proof step");
            if (col<0 || col>=nc || row<0 || row>=nr || value[col]!=-1 || (v!=0 && v!=1))
                throw runtime_error("Invalid assignment");
            int64_t residual=q[row], lo=0, hi=0;
            int sign=0;
            // An unassigned variable is any real number in [0,1].
            for (auto k=ptr[row]; k<ptr[row+1]; ++k) {
                const int c=ind[k], a=sg[k];
                if (c==col) sign=a;
                if (value[c]>=0) residual-=a*value[c];
                else if (a>0) ++hi;
                else --lo;
            }
            if (sign==0) throw runtime_error("Variable not present in cited row");
            const bool forced =
                (residual==lo && v==int(sign<0)) ||
                (residual==hi && v==int(sign>0));
            if (!forced) throw runtime_error("Assignment is not forced by its row");
            value[col]=static_cast<int8_t>(v);
            ++checked;
        }
        if (!proof.eof()) throw runtime_error("Proof read failure");
        int conflict=-1;
        int64_t lo=0, hi=0, residual=0;
        for (int row=0; row<nr; ++row) {
            int64_t rr=q[row], mn=0, mx=0;
            for (auto k=ptr[row]; k<ptr[row+1]; ++k) {
                const int col=ind[k], a=sg[k];
                if (value[col]>=0) rr-=a*value[col];
                else if (a>0) ++mx;
                else --mn;
            }
            if (rr<mn || rr>mx) {
                conflict=row; lo=mn; hi=mx; residual=rr; break;
            }
        }
        if (conflict<0) throw runtime_error("Transcript does not establish a contradiction");
        ofstream report("twolevel154_replay.json");
        report << "{\"status\":\"EXACT_PASS\",\"arithmetic\":\"integers only\","
               << "\"steps_checked\":" << checked << ",\"conflict_row\":" << conflict
               << ",\"rhs\":" << residual << ",\"min\":" << lo << ",\"max\":" << hi << "}\n";
        cout << "PASS " << checked << " steps; row " << conflict << " residual " << residual
             << " outside [" << lo << "," << hi << "]\n";
        return 0;
    } catch (const exception& error) {
        cerr << "REJECT: " << error.what() << '\n';
        return 1;
    }
}
