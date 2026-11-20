"""Independent checks for finite exactness certificates."""
import sys,itertools,collections,math
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'validation'))
import reference as r
import networkx as nx

def nx_state(st,arity=2):
    G=nx.Graph();G.add_nodes_from((i,{'spin':st[1][i]}) for i in range(4))
    if arity==2:G.add_edges_from(h for h,v in zip(r.PAIRS,st[0]) if v)
    else:
      # incidence graph with vertex colors/type labels and hyperedge nodes
      G=nx.Graph()
      G.add_nodes_from((i,{'kind':'v','spin':st[1][i]}) for i in range(4))
      for k,(h,v) in enumerate(zip(r.TRIPLES,st[0])):
        if v:
          G.add_node(('h',k),kind='h',spin=-1)
          G.add_edges_from((('h',k),i) for i in h)
    return G

def test_graph_cardinality():
    assert len(r.all_states(2))==1024
    assert len(r.extract_representatives(r.all_states(2),2))==90

def test_hypergraph_cardinality():
    assert len(r.all_states(3))==256
    assert len(r.extract_representatives(r.all_states(3),3))==35

def test_graph_explicit_equivariance():
    for st in r.all_states(2):
        for p in r.PERMS:
            assert r.step_graph(r.permute(st,p,2))==r.permute(r.step_graph(st),p,2)

def test_hyper_explicit_equivariance():
    for st in r.all_states(3):
        for p in r.PERMS:
            assert r.step_hypergraph(r.permute(st,p,3))==r.permute(r.step_hypergraph(st),p,3)

def test_catalog_sizes():
    assert [len(r.TYPES[2][k]) for k in range(1,4)]==[2,8,28]
    assert len(r.THREE_TYPES)==20

def test_selected_exactness():
    o=r.graph_motif_observer
    ans=r.exactness(r.all_states(2),lambda s:o(s,'selected'),r.step_graph)
    assert ans['exact'] and ans['classes']==86 and ans['bad_classes']==0

def test_baseline_failure():
    a=r.exactness(r.all_states(2),lambda s:r.graph_motif_observer(s,2),r.step_graph)
    assert a['classes']==66 and a['bad_classes']==15

def test_complete_motifs_exact():
    a=r.exactness(r.all_states(2),lambda s:r.graph_motif_observer(s,3),r.step_graph)
    assert a['classes']==90 and a['exact']

def test_minimality_5():
    assert r.cert()=={0:0,1:0,2:0,3:0,4:0,5:98}

def test_graph_group_changes():
    s=(r.bits(7,6),r.bits(2,4));gs=[];hs=[]
    for _ in range(6):
      gs.append(len(r.automorphisms(s,2,False)))
      hs.append(len(r.automorphisms(s,2,True)))
      s=r.step_graph(s)
    assert gs==[6,8,24,8,24,8]
    assert hs==[2,4,4,4,4,4]

def test_hypergraph_exactness():
    a=r.exactness(r.all_states(3),lambda s:r.hyper_motif_observer(s,3),r.step_hypergraph)
    assert a['exact'] and a['classes']==35

def test_hypergraph_group_changes():
    st=(r.bits(1,4),r.bits(11,4));groups=[]
    for _ in range(5):
        groups.append(len(r.automorphisms(st,3,False)))
        st=r.step_hypergraph(st)
    assert groups==[6,4,4,24,4]

def test_independent_networkx_graph_isomorphism():
    reps=r.extract_representatives(r.all_states(2),2)
    graphs=[nx_state(s) for s in reps]
    nm=nx.algorithms.isomorphism.categorical_node_match('spin',None)
    for i, G in enumerate(graphs):
        for j in range(i+1,len(reps)):
            assert not nx.is_isomorphic(G, graphs[j],node_match=nm)

def test_independent_networkx_automorphism_counts():
    seeds=[(r.bits(7,6),r.bits(2,4)),(r.bits(0,6),r.bits(15,4)),(r.bits(15,6),r.bits(0,4))]
    for st in seeds:
        G=nx_state(st)
        nm=nx.algorithms.isomorphism.categorical_node_match('spin',None)
        nxfull=sum(1 for _ in nx.algorithms.isomorphism.GraphMatcher(G,G,node_match=nm).isomorphisms_iter())
        nxgraph=sum(1 for _ in nx.algorithms.isomorphism.GraphMatcher(G,G).isomorphisms_iter())
        assert nxfull==len(r.automorphisms(st,2,True))
        assert nxgraph==len(r.automorphisms(st,2,False))

def test_multiway_edge_deletion():
    cycle={(0,1),(1,2),(2,3),(0,3)}
    s=(tuple(int(h in cycle) for h in r.PAIRS),(0,0,0,0))
    out=[]
    for e in cycle:
        out.append((tuple(int(h in cycle and h !=e) for h in r.PAIRS),s[1]))
    assert len({r.canonical(x,2) for x in out})==1
    assert len(r.automorphisms(s,2,False))==8
    assert all(len(r.automorphisms(x,2,False))==2 for x in out)
    # all four matches form one orbit under automorphisms
    E=[p for p in r.PERMS if r.permute(s,p,2)==s]
    e=(0,1)
    orbit={tuple(sorted((p[e[0]],p[e[1]]))) for p in E}
    assert orbit==cycle and len(orbit)==4

def test_sum_of_canonical_orbit_sizes():
    reps=r.extract_representatives(r.all_states(2),2)
    assert sum(24//len(r.automorphisms(s,2,True)) for s in reps)==1024

def test_macro_cycles():
    import csv
    rows=list(csv.DictReader(open(Path(__file__).resolve().parents[1]/'Data'/'exact_macro_dynamics_86.csv')))
    G=nx.DiGraph((int(v['observer_id']),int(v['successor_id'])) for v in rows)
    lens=collections.Counter(len(c) for c in nx.simple_cycles(G))
    assert lens=={1:13,2:3,3:1}

def test_complement_variant_exact():
    o=lambda st:r.graph_motif_observer(st,'selected')
    for f in [r.complement_graph,r.step_graph_complement]:
        ans=r.exactness(r.all_states(2),o,f)
        assert ans['exact'] and ans['classes']==86

def test_complement_changes_merged_states():
    a=(r.bits(48,6),(0,0,0,0))
    b=(r.bits(12,6),(0,0,0,0))
    assert r.canonical(a,2)!=r.canonical(b,2)
    q=lambda x:r.graph_motif_observer(x,'selected')
    assert q(a)==q(b)
    for start in [a,b]:
        assert q(r.step_graph_complement(start))!=q(start)
        assert q(r.step_graph_complement(r.step_graph_complement(start)))==q(start)

def test_complement_macro_cycle_count():
    import csv
    rows=list(csv.DictReader(open(Path(__file__).resolve().parents[1]/'Data'/'exact_macro_complement_86.csv')))
    G=nx.DiGraph((int(x['observer_id']),int(x['successor_id'])) for x in rows)
    assert collections.Counter(len(c) for c in nx.simple_cycles(G))=={1:2,2:8}

def test_all_decorated_group_stabilizers_nondecrease():
    for st in r.all_states(2):
        before=set(r.automorphisms(st,2,True))
        after=set(r.automorphisms(r.step_graph(st),2,True))
        assert before<=after

def test_positional_encoding_unique_and_lossless():
    reps=r.extract_representatives(r.all_states(2),2)
    sigs={r.graph_motif_observer(s,'selected') for s in reps}
    vals={r.encode_base7(q) for q in sigs}
    assert len(sigs)==len(vals)==86
    for q in sigs:
        value=r.encode_base7(q)
        digits=[]
        for _ in range(13):
            digits.append(value%7);value//=7
        assert tuple(reversed(digits))==q and value==0

def test_positional_encoding_preserves_barycentric_linearity():
    reps=r.extract_representatives(r.all_states(2),2)
    q=[r.graph_motif_observer(s,'selected') for s in reps]
    for p0,p1 in zip(q[:40],q[40:80]):
        left=r.encode_base7(p0)+r.encode_base7(p1)
        # General linear identity, without assuming digitwise mean integrality.
        rhs=sum((a+b)*7**(12-i) for i,(a,b) in enumerate(zip(p0,p1)))
        assert left==rhs
