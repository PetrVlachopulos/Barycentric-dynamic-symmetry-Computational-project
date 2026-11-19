#!/usr/bin/env python3
import sys,json, math, collections
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from reference import *
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.animation import FuncAnimation, PillowWriter
root=Path(__file__).resolve().parents[1]
figdir=root/'Results'/'figures'; anidir=root/'Results'/'animations'
figdir.mkdir(parents=True,exist_ok=True);anidir.mkdir(parents=True,exist_ok=True)
r=json.loads((root/'Data'/'verified_results.json').read_text())
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,'axes.spines.right':False,'figure.facecolor':'white','savefig.facecolor':'white'})
C0='#0C766E';C1='#E0A43D';NAV='#22364C';GREY='#DDE3E8';RED='#CC5D57'
POS={0:(0.0,1.05),1:(1.0,0.0),2:(0.0,-1.05),3:(-1.0,0.0)}

def draw_state(ax,st,arity=2,title='',small=False):
    e,s=st;hfaces=PAIRS if arity==2 else TRIPLES
    ax.set(xlim=(-1.38,1.38),ylim=(-1.33,1.33));ax.set_aspect('equal');ax.axis('off')
    if arity==2:
        for bit,(i,j) in zip(e,hfaces):
            if bit:
                x,y=POS[i],POS[j]
                ax.plot([x[0],y[0]],[x[1],y[1]],lw=3.5 if not small else 2.8,color=NAV,zorder=1,alpha=.85)
    else:
        import matplotlib.patches as patches
        for bit,h in zip(e,hfaces):
            if bit:
                polygon=patches.Polygon([POS[i] for i in h],closed=True,facecolor=C0,edgecolor=C0,alpha=.18,lw=2,zorder=0)
                ax.add_patch(polygon)
    for i,p in POS.items():
        ax.scatter([p[0]],[p[1]],s=580 if not small else 460,c=[C1 if s[i] else C0],edgecolor='white',linewidth=2,zorder=3)
        ax.text(p[0],p[1],f'{i+1}',va='center',ha='center',color='white',weight='bold',fontsize=10 if not small else 9,zorder=4)
    ax.set_title(title,fontsize=11,weight='bold',color=NAV,pad=4)

init=(bits(7,6),bits(2,4));trajectory=[init]
for i in range(5):trajectory.append(step_graph(trajectory[-1]))
fig,axs=plt.subplots(2,3,figsize=(12.5,7.5));fig.suptitle('Changing symmetries in an interacting four-vertex graph rewrite',fontsize=16,weight='bold',color=NAV,y=.99)
for t,ax in enumerate(axs.flatten()):
 st=trajectory[t];draw_state(ax,st,2,f't = {t} | Aut(G) = {len(automorphisms(st,2))}',True)
 ax.text(0,-1.37,f'edges {sum(st[0])}  •  active spins {sum(st[1])}',ha='center',fontsize=9,color='#526174')
fig.subplots_adjust(top=.90,bottom=.06,hspace=.42,wspace=.05)
fig.savefig(figdir/'01_changing_automorphisms.png',dpi=180);plt.close(fig)

# observer ladder with failure counts
labs=['1-vertex','≤2-vertex','≤2 + five selected 3-motifs','≤3-vertex']
items=[r['graph_levels']['1'],r['graph_levels']['2'],r['graph_levels']['selected'],r['graph_levels']['3']]
fig,ax=plt.subplots(figsize=(11,4.6))
y=list(range(4));v=[u['classes'] for u in items]
ax.barh(y,v,color=[GREY,GREY,C0,'#647C8D'],height=.63)
for i,(val,item) in enumerate(zip(v,items)):
 ax.text(val+1.1,i,f'{val} observable states  |  {item["bad_classes"]} defective blocks',va='center',fontsize=9)
ax.set(yticks=y,yticklabels=labs,xlim=(0,128),xlabel='Number of distinct observable signatures');ax.invert_yaxis()
ax.set_title('A smaller exact observer than the full orbit quotient',fontsize=15,weight='bold',color=NAV)
fig.tight_layout();fig.savefig(figdir/'02_observer_ladder.png',dpi=190);plt.close(fig)

# motif drawings
fig,axs=plt.subplots(1,5,figsize=(13.5,3.5)); fig.suptitle('Five selected three-vertex invariants (all counts of induced motifs)',fontsize=14,color=NAV,weight='bold')
p3={0:(0,.9),1:(-.83,-.5),2:(.83,-.5)}
for ii,(j,ax) in enumerate(zip(SELECTED,axs)):
 (size,(colors,edges))=THREE_TYPES[j];ax.set_aspect('equal');ax.axis('off');ax.set_xlim(-1.25,1.25);ax.set_ylim(-1.2,1.25)
 for b,(a,c) in zip(edges,((0,1),(0,2),(1,2))):
  if b: ax.plot([p3[a][0],p3[c][0]],[p3[a][1],p3[c][1]],lw=3,color=NAV)
 for q,c in enumerate(colors):
  ax.scatter([p3[q][0]],[p3[q][1]],s=430,color=C1 if c else C0,zorder=4,edgecolor='white',linewidth=1.5)
  ax.text(*p3[q],str(c),color='white',ha='center',va='center',weight='bold',zorder=5)
 ax.set_title(f'Motif {ii+1}\n3-pattern index {j+1}',fontsize=10,color=NAV)
fig.tight_layout(rect=(0,0,1,.87));fig.savefig(figdir/'03_selected_motifs.png',dpi=180);plt.close(fig)

# C4 branching diagram
fig,axs=plt.subplots(1,5,figsize=(14.5,3.2));
cyc_edges=((0,1),(1,2),(2,3),(0,3));
edict={p:1 if p in cyc_edges else 0 for p in PAIRS}
cyc=(tuple(edict[p] for p in PAIRS),(0,0,0,0))
draw_state(axs[0],cyc,title='C4 | |Aut|=8',small=True)
for i,p in enumerate(cyc_edges):
 e2=tuple(0 if pair==p else edict[pair] for pair in PAIRS)
 st=(e2,(0,0,0,0));draw_state(axs[i+1],st,title=f'delete edge {p[0]+1}-{p[1]+1}',small=True)
 axs[i+1].text(0,-1.28,'P4 | |Aut|=2',ha='center',fontsize=9,color='#526174')
fig.suptitle('Multiway rewriting: four labeled branches, one unlabeled successor class',fontsize=14,color=NAV,weight='bold')
fig.tight_layout(rect=(0,0,1,.86));fig.savefig(figdir/'04_multiway_event_groupoid.png',dpi=180);plt.close(fig)

# graph quotient functional graph of 86 obs states
import csv
mac=list(csv.DictReader(open(root/'Data'/'exact_macro_dynamics_86.csv')))
G=nx.DiGraph([(int(x['observer_id']),int(x['successor_id'])) for x in mac]);
cycs=list(nx.simple_cycles(G)); cycc=collections.Counter(map(len,cycs))
fig,ax=plt.subplots(figsize=(10.5,7.2));pos=nx.spring_layout(G,seed=9,k=.22,iterations=240)
nx.draw_networkx_edges(G,pos,ax=ax,arrows=True,arrowsize=8,edge_color='#B4BCC5',width=.65,alpha=.7,connectionstyle='arc3,rad=.07')
oncyc={v for c in cycs for v in c}
nx.draw_networkx_nodes(G,pos,nodelist=sorted(set(G)-oncyc),node_color='#7B909F',node_size=45,ax=ax)
nx.draw_networkx_nodes(G,pos,nodelist=sorted(oncyc),node_color=C1,node_size=82,ax=ax)
ax.set_title('Exact 86-state macrodynamics\n13 fixed points, 3 two-cycles and 1 three-cycle',fontsize=14,color=NAV,weight='bold')
ax.axis('off');fig.tight_layout();fig.savefig(figdir/'05_exact_macro_dynamics.png',dpi=180);plt.close(fig)

# gif changing graph and symmetry groups
from PIL import Image
frames=[]
for t,st in enumerate(trajectory):
 fig,ax=plt.subplots(figsize=(5.4,5.0))
 draw_state(ax,st,title=f'Step {t}  |  graph symmetry order {len(automorphisms(st,2))}')
 ax.text(0,-1.42,f'{sum(st[0])} edges   |   {sum(st[1])} active vertices',ha='center',fontsize=11)
 fig.tight_layout()
 fig.canvas.draw()
 frames.append(Image.frombytes('RGB',fig.canvas.get_width_height(),fig.canvas.tostring_rgb()) if hasattr(fig.canvas,'tostring_rgb') else Image.frombuffer('RGBA',fig.canvas.get_width_height(),fig.canvas.buffer_rgba()).convert('RGB'))
 plt.close(fig)
frames[0].save(anidir/'01_group_changes.gif',save_all=True,append_images=frames[1:],duration=1100,loop=0,optimize=True)
# diagram showing finite sigma group inclusion versus graph-aut variance
fig,ax=plt.subplots(figsize=(9.5,3.8))
y1=[len(automorphisms(st,2,False)) for st in trajectory]
y2=[len(automorphisms(st,2,True)) for st in trajectory]
ax.plot(range(len(y1)),y1,'o-',lw=2.6,color=C0,label='Graph automorphisms (uncolored)')
ax.plot(range(len(y2)),y2,'s--',lw=2.4,color=C1,label='Full decorated-state stabilizer')
ax.set_xticks(range(len(y1)));ax.set_xlabel('Discrete time step');ax.set_ylabel('Symmetry-group order');ax.set_title('Geometric symmetries may fluctuate; decorated symmetries cannot decrease',fontsize=13.5,color=NAV,weight='bold')
ax.legend(frameon=False,loc='upper left');ax.grid(alpha=.15)
fig.tight_layout();fig.savefig(figdir/'06_symmetry_group_orders.png',dpi=180);plt.close(fig)
print('Saved figures to',figdir)

# Two microscopic orbit classes merged by Q* yet evolving through an exact two-cycle.
zero=(0,0,0,0)
gA=(bits(48,6),zero);gB=(bits(12,6),zero)
C=lambda st:complement_graph(st)
fig,axs=plt.subplots(2,2,figsize=(8.8,7.0))
for row,g in enumerate([gA,gB]):
 draw_state(axs[row,0],g,title=f'microstate {row+1}: {sum(g[0])} edges')
 draw_state(axs[row,1],C(g),title='complement after one step')
fig.suptitle('Distinct microscopic orbits, one exact dynamical observer',weight='bold',fontsize=15,color=NAV)
fig.text(.23,.035,'Same Q*: two-edge observer block',ha='center',fontsize=10,color=C0)
fig.text(.76,.035,'Same Q*: four-edge observer block',ha='center',fontsize=10,color=C0)
fig.subplots_adjust(top=.88,bottom=.09,hspace=.28)
fig.savefig(figdir/'07_nontrivial_merged_macrocycle.png',dpi=180);plt.close(fig)

frames=[]
for t in range(6):
 fig,axs=plt.subplots(1,2,figsize=(8.3,4.25))
 aa=gA if t%2==0 else C(gA); bb=gB if t%2==0 else C(gB)
 draw_state(axs[0],aa,title='Microscopic A')
 draw_state(axs[1],bb,title='Microscopic B')
 fig.suptitle(f'Same observed Q* at time {t}  |  {sum(aa[0])} edges',fontsize=14,color=NAV,weight='bold')
 fig.tight_layout(rect=(0,0,1,.92));fig.canvas.draw()
 frames.append(Image.frombuffer('RGBA',fig.canvas.get_width_height(),fig.canvas.buffer_rgba()).convert('RGB'))
 plt.close(fig)
frames[0].save(anidir/'02_exact_macro_merged_cycle.gif',save_all=True,append_images=frames[1:],duration=750,loop=0,optimize=True)

# genuinely 3-ary interactions and changing symmetries
st=(bits(1,4),bits(11,4));htraj=[]
for t in range(5):htraj.append(st);st=step_hypergraph(st)
fig,axs=plt.subplots(1,5,figsize=(15,3.6));
for t,(st,ax) in enumerate(zip(htraj,axs)):
 draw_state(ax,st,3,title=f't={t} | Aut={len(automorphisms(st,3))}',small=True)
fig.suptitle('Ternary interactions and changing hypergraph automorphisms',fontsize=14,color=NAV,weight='bold')
fig.tight_layout(rect=(0,0,1,.84));fig.savefig(figdir/'08_ternary_hypergraph_trajectory.png',dpi=180);plt.close(fig)
print('Added complement-composed and ternary figures')
