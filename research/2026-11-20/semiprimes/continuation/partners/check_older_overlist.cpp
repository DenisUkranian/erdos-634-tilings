// Count all prime rows resolved without the two additional moving-bank exclusions.
// Run beside the documented unit-staircase CSV. All primality tests use division.
#include <algorithm>
#include <array>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <set>
#include <sstream>
#include <stdexcept>
#include <string>
#include <vector>

using integer = std::int64_t;

int main(int argc, char** argv) {
    constexpr int limit = 1000000;
    std::vector<bool> composite(limit+1, false);
    std::vector<int> primes;
    for (int d=2; d<=limit; ++d) {
        if (composite[d]) continue;
        primes.push_back(d);
        for (integer n=integer(d)*d; n<=limit; n+=d)
            composite[n]=true;
    }
    const auto prime = [&](integer n) {
        if (n <= limit) return n>=2 && !composite[static_cast<size_t>(n)];
        for (int d : primes) {
            if (integer(d)*d > n) return true;
            if (n % d == 0) return false;
        }
        throw std::runtime_error("trial-prime list exhausted");
    };
    std::set<int> mixed, distant, endpoints;
    std::ifstream in(argc>1 ? argv[1] : "residuals.csv");
    if (!in) throw std::runtime_error("missing residuals CSV");
    std::string line;
    std::getline(in,line);
    int rows=0;
    while (std::getline(in,line)) {
        std::replace(line.begin(),line.end(),',',' ');
        std::istringstream row(line);
        integer n,p,q;
        if (!(row>>n>>p>>q) || p*q!=n || p>=q || p<5 || p>limit)
            throw std::runtime_error("bad input row");
        ++rows;
        mixed.insert(static_cast<int>(p));
        if(q<=limit) mixed.insert(static_cast<int>(q));
    }
    if(rows!=312 || mixed.size()!=511) throw std::runtime_error("unexpected mixed census");
    int far_pairs=0, total=0;
    for (int endpoint : primes) {
        if (endpoint<=3) continue;
        ++total;
        if (endpoint % 4 != 3) continue;
        integer p=endpoint;
        std::array<integer,3> values={p*p+6*p+1,3*p*p+6*p-1,p*p+6*p-3};
        for (integer value : values) {
            if (value%4) continue;
            integer q=value/4;
            if (q<=2*p || q%4!=3 || !prime(q)) continue;
            ++far_pairs;
            distant.insert(endpoint);
            if (q<=limit) distant.insert(static_cast<int>(q));
        }
    }
    endpoints=mixed;
    endpoints.insert(distant.begin(),distant.end());
    std::cout << "prime endpoints: " << total << "\nmixed residual endpoints: " << mixed.size()
              << "\ndistant candidate pairs: " << far_pairs << "\ndistant candidate endpoints: "
              << distant.size() << "\nendpoints on both lists: "
              << mixed.size()+distant.size()-endpoints.size() << "\nfully decided rows using the older overlist alone: "
              << total-endpoints.size() << '\n';
}
