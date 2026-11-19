// Vertical reflection of an unrestricted isosceles target. The mask stores
// cells which may occur in any solution; its mirror need only belong to the
// mask of the reflected solution. No one tiling is assumed symmetric.
// Requires W-1=Q times the full target width, and min target x=0.
struct MeshMirror {int peer=-1,dx=0,y0=0,y1=0;};
std::vector<MeshMirror> mesh_mirrors;
void prepare_mirrors(){
  mesh_mirrors.resize(shapes.size());
  std::map<std::array<P,3>,int> identities;
  for(int k=0;k<(int)shapes.size();++k){
    auto& v=shapes[k].v;
    assert(v[0].x==0&&v[0].y==0);
    std::array<P,3> points={v[0],v[1],v[2]};
    std::sort(points.begin(),points.end());
    identities[points]=k;
  }
  for(int k=0;k<(int)shapes.size();++k){
    auto& v=shapes[k].v;
    std::array<P,3> image={P{-v[0].x,v[0].y},P{-v[1].x,v[1].y},P{-v[2].x,v[2].y}};
    for(P a:image){
      std::array<P,3> translated={image[0]-a,image[1]-a,image[2]-a};
      std::sort(translated.begin(),translated.end());
      auto it=identities.find(translated);if(it==identities.end())continue;
      assert(mesh_mirrors[k].peer==-1);
      mesh_mirrors[k]={it->second,floor_div(Q*a.x,S),floor_div(Q*a.y,S),ceil_div(Q*a.y,S)};
    }
  }
}
void prune_mirrors(){
  std::array<unsigned char,256> table{};
  for(int n=0;n<256;++n){unsigned char x=n,v=0;for(int i=0;i<8;++i){v=(v<<1)|(x&1);x>>=1;}table[n]=v;}
  std::size_t nbytes=(W+7)/8;
  std::vector<unsigned char> in(nbytes),out(nbytes);
  Z a,b,ok;
  std::vector<Z> flipped(H);
  for(int k=0;k<(int)shapes.size();++k){
    if(std::abs(k/4-B)>freeze_h)continue;
    auto m=mesh_mirrors[k];if(m.peer<0)continue;
    for(int y=0;y<H;++y){
      const auto& row=poses[m.peer][y];
      if(row==0){flipped[y]=0;continue;}
      std::fill(in.begin(),in.end(),0);std::size_t used=0;
      mpz_export(in.data(),&used,-1,1,0,0,row.get_mpz_t());assert(used<=nbytes);
      for(std::size_t j=0;j<nbytes;++j)out[nbytes-1-j]=table[in[j]];
      mpz_import(flipped[y].get_mpz_t(),nbytes,-1,1,0,0,out.data());
      mpz_fdiv_q_2exp(flipped[y].get_mpz_t(),flipped[y].get_mpz_t(),8*nbytes-W);
    }
    for(int y=0;y<H;++y){
      if(poses[k][y]==0)continue;ok=0;
      for(int dy=m.y0;dy<=m.y1;++dy){
        int yy=y+dy;if(yy<0||yy>=H)continue;
        // Mirror x for an anchor-coordinate cell at x is in
        // W-1-x+dx or its left neighbor, including exact endpoints.
        shift(a,flipped[yy],m.dx);shift(b,flipped[yy],m.dx-1);
        add_or(ok,a);add_or(ok,b);
      }
      poses[k][y]&=ok;
    }
  }
}
