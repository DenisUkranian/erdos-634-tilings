// Necessary whole-edge support for the outward-rounded triangular mesh.
// Include after P, Off, Cover/shift/add_or/clip, shapes, walls and poses exist.
// Ray r means a CCW tile side, with the interior on its left. All unit ray
// vectors and shape offsets are stored in units of the common denominator S.
// prepare_half_edges() follows init(); prune_half_edges() follows a star pass.
struct HalfRequest {
  int shape;
  std::vector<std::vector<Off>> probes;
};
std::vector<std::vector<HalfRequest>> half_requests;
std::vector<std::vector<Off>> half_sources;
std::vector<std::map<int,Z>> half_outside;

std::vector<Off> half_cells(int shape, P twice_point) {
  std::vector<Off> out;
  for(int x=floor_div(Q*twice_point.x,2*S);x<=ceil_div(Q*twice_point.x,2*S);++x)
    for(int y=floor_div(Q*twice_point.y,2*S);y<=ceil_div(Q*twice_point.y,2*S);++y)
      out.push_back({shape,x,y});
  return out;
}
void prepare_half_edges() {
  half_requests.resize(R);
  half_sources.resize(R);
  half_outside.resize(R);
  std::vector<std::set<Off>> all(R);
  for(int k=0;k<(int)shapes.size();++k) {
    auto& f=shapes[k];
    for(int side=0;side<3;++side) {
      int r=f.ray[side],length=f.len[side];
      HalfRequest need{k,{}};
      for(int m=0;m<length;++m) {
        auto offsets=half_cells(k,2*f.v[side]+(2*m+1)*rays[r]);
        all[r].insert(offsets.begin(),offsets.end());
        need.probes.push_back(std::move(offsets));
      }
      half_requests[r].push_back(std::move(need));
    }
  }
  for(int r=0;r<R;++r) half_sources[r].assign(all[r].begin(),all[r].end());
  for(const auto& wall:walls) {
    for(int m=0;m<wall.len;++m) {
      auto twice=2*S*wall.a+(2*m+1)*rays[wall.ray];
      int x=floor_div(Q*twice.x,2*S), y=floor_div(Q*twice.y,2*S);
      if(0<=x&&x<W&&0<=y&&y<H)
        mpz_setbit(half_outside[wall.ray][y].get_mpz_t(),x);
    }
  }
}
void prune_half_edges() {
  Z shifted,allowed;
  for(int r=0;r<R;++r) {
    std::vector<Z> facing(H);
    for(auto& [y,mask]:half_outside[r]) facing[y]=mask;
    for(auto off:half_sources[(r+R/2)%R]) {
      for(int y=std::max(0,-off.y);y<std::min(H,H-off.y);++y) {
        if(poses[off.k][y]==0)continue;
        shift(shifted,poses[off.k][y],off.x);
        add_or(facing[y+off.y],shifted);
      }
    }
    for(auto& row:facing)clip(row);
    for(auto& need:half_requests[r]) {
      if(std::abs(need.shape/4-B)>freeze_h)continue;
      auto& candidates=poses[need.shape];
      for(int y=0;y<H;++y) {
        for(const auto& offsets:need.probes) {
          if(candidates[y]==0)break;
          allowed=0;
          for(auto off:offsets) {
            int yy=y+off.y;
            if(yy<0||yy>=H||facing[yy]==0)continue;
            shift(shifted,facing[yy],-off.x);
            add_or(allowed,shifted);
          }
          candidates[y]&=allowed;
        }
      }
    }
  }
}
