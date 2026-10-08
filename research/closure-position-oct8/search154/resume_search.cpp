// Continue a trusted local run, retaining only fully rejected search states.
// This is an operational checkpoint, not an independent negative certificate.
#define main search_main
#include "fixed_search.cpp"
#undef main

size_t load_checkpoint(const string& prefix,Search& search) {
    ifstream geometry(prefix+"-geometry.txt");
    L scale;size_t np,nt;
    if (!(geometry>>scale>>np>>nt) || scale!=D) throw runtime_error("bad checkpoint geometry");
    for (size_t i=0;i<np;++i) {
        P p;
        if (!(geometry>>p.x>>p.y) || size_t(point(p))!=i) throw runtime_error("checkpoint point mismatch");
    }
    for (size_t i=0;i<nt;++i) {
        array<int,3> v;int h,g;
        if (!(geometry>>v[0]>>v[1]>>v[2]>>h>>g)) throw runtime_error("truncated checkpoint");
        for (int p:v) if(p<0 || size_t(p)>=np) throw runtime_error("bad checkpoint point index");
        if(h< -11 || h>11 || g<0 || g>3) throw runtime_error("bad checkpoint classification");
        array<I,3> norms;
        for(int j=0;j<3;++j)norms[j]=norm(pts[v[j]]-pts[v[(j+1)%3]]);
        sort(norms.begin(),norms.end());
        if(norms!=array<I,3>{I(49)*D*D,I(64)*D*D,I(169)*D*D})throw runtime_error("bad checkpoint triangle");
        if(size_t(triangle(v,h,g))!=i)throw runtime_error("checkpoint triangle mismatch");
    }
    ifstream trace(prefix+"-trace.txt");
    if(!trace)throw runtime_error("missing checkpoint trace");
    string line;
    while(getline(trace,line)) {
        istringstream row(line);int rule,t;Fan state;
        if(!(row>>rule) || rule<1 || rule>14)throw runtime_error("bad checkpoint rule");
        while(row>>t){if(t<0 || size_t(t)>=nt)throw runtime_error("bad trace triangle");state.push_back(t);}
        if(!row.eof() || !is_sorted(state.begin(),state.end()) || adjacent_find(state.begin(),state.end())!=state.end())throw runtime_error("bad checkpoint state");
        search.dead.insert(statekey(state));
        search.trace<<line<<'\n';
    }
    search.start=chrono::steady_clock::now();
    return search.dead.size();
}

int main(int argc,char**argv) {
    try {
        if(argc<4)throw runtime_error("usage: resume_search PRIOR_PREFIX SECONDS OUTPUT_PREFIX [NODE_CAP]");
        string prior=argv[1],prefix=argv[3];
        if(prior==prefix)throw runtime_error("output prefix must differ from input");
        double seconds=stod(argv[2]);uint64_t cap=argc>4?stoull(argv[4]):100000000;
        setup();Search search(seconds,cap,prefix+"-trace.txt");
        size_t previous=load_checkpoint(prior,search);
        cerr<<"Loaded "<<previous<<" completed dead states and "<<tri.size()<<" triangles\n";
        Boundary boundary{{OUT[0],OUT[1]},{OUT[1],OUT[2]},{OUT[2],OUT[0]}};
        string status;
        try {status=search.run({},boundary)?"TILING_CANDIDATE":"EXHAUSTED_REQUIRES_INDEPENDENT_REPLAY";}
        catch(const runtime_error&e){if(string(e.what())=="RESOURCE_LIMIT")status="INCOMPLETE";else throw;}
        ofstream report(prefix+"-report.json");
        report<<"{\n\"status\":\""<<status<<"\",\n\"nodes_this_run\":"<<search.nodes
              <<",\n\"seconds\":"<<search.elapsed()<<",\n\"maximum_depth_this_run\":"<<search.maxdepth
              <<",\n\"prior_dead_states\":"<<previous<<",\n\"dead_states\":"<<search.dead.size()
              <<",\n\"generated_triangles\":"<<tri.size()<<",\n\"allowed_support_lengths\":[3,5],"
              <<"\n\"checkpoint_independently_replayed\":false,\n\"N154_decided\":false,\n\"full_Erdos634_solved\":false,\n\"solution\":[";
        for(size_t i=0;i<search.solution.size();++i){
            if(i)report<<',';
            report<<'[';
            for(int j=0;j<3;++j){if(j)report<<',';P p=pts[tri[search.solution[i]].v[j]];report<<"[\""<<p.x<<'/'<<D<<"\",\""<<p.y<<'/'<<D<<"\"]";}
            report<<']';
        }
        report<<"]\n}\n";
        ofstream geometry(prefix+"-geometry.txt");
        geometry<<D<<' '<<pts.size()<<' '<<tri.size()<<'\n';
        for(P p:pts)geometry<<p.x<<' '<<p.y<<'\n';
        for(auto&t:tri)geometry<<t.v[0]<<' '<<t.v[1]<<' '<<t.v[2]<<' '<<t.h<<' '<<t.group<<'\n';
        cerr<<status<<" nodes="<<search.nodes<<" seconds="<<search.elapsed()<<'\n';
        return 0;
    } catch(const exception&e){cerr<<"ERROR "<<e.what()<<'\n';return 1;}
}
