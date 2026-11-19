// An actual terminal population of absolute height >=2 contains at least six
// tiles (HEIGHT.md). Each incenter has a physical open disk of radius sqrt(2).
// A 2-by-1 axial box has diameter sqrt(6), so it can hold at most one incenter.
bool has_height(int h) {
    for (int k=4*(h+B); k<4*(h+B+1); ++k) {
        for (const Z& row : poses[k]) if (row != 0) return true;
    }
    return false;
}

bool enough_incenter_boxes(int h, int xoffset, int yoffset) {
    // Offsets are expressed in half-units of the axial coordinate axes.
    set<pair<int,int>> boxes;
    for (int k=4*(h+B); k<4*(h+B+1); ++k) {
        const auto& f=shapes[k];
        auto center= f.len[1]*f.v[0] + f.len[2]*f.v[1] + f.len[0]*f.v[2];
        // The axial incenter relative to the anchor is center/(20*S).
        I unit=20*S, step=2*unit;
        I cx=Q*(2*center.x + xoffset*unit), cy=Q*(2*center.y + yoffset*unit);
        for (int y=0; y<H; ++y) {
            const Z& row=poses[k][y];
            if (row==0) continue;
            int low_y=floor_div(step*y+cy,step*Q);
            int high_y=floor_div(step*(y+1)+cy,step*Q);
            for (auto bit=mpz_scan1(row.get_mpz_t(),0); bit<(unsigned)W; bit=mpz_scan1(row.get_mpz_t(),bit+1)){
                auto x=static_cast<int>(bit);
                int low_x=floor_div(step*x+cx,2*step*Q);
                int high_x=floor_div(step*(x+1)+cx,2*step*Q);
                for (int a=low_x;a<=high_x;++a) for(int b=low_y;b<=high_y;++b) boxes.emplace(a,b);
                if(boxes.size()>=6) return true;
            }
        }
    }
    return false;
}

void prune_unoccupied_terminal() {
    if(freeze_h<B) return;
    for(int sign:{-1,1}) {
        for(int i=B;i>=2;--i) {
            int h=sign*i;
            if(!has_height(h)) continue;
            bool enough=true;
            for(int xoff:{0,1,2,3}) for(int yoff:{0,1}) {
                if(enough && !enough_incenter_boxes(h,xoff,yoff)) enough=false;
            }
            if(enough) break;
            for(int k=4*(h+B);k<4*(h+B+1);++k) for(Z& row:poses[k]) row=0;
        }
    }
}
