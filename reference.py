#!/usr/bin/env python3
"""Executable finite certificate for dynamically sufficient symmetry observers.
4-vertex binary attributed graphs + 3-uniform binary attributed hypergraphs.
"""
from __future__ import annotations
import itertools, collections, math, csv, json, hashlib, argparse
from pathlib import Path

N=4
PERMS=tuple(itertools.permutations(range(N)))
PAIRS=tuple(itertools.combinations(range(N),2))
TRIPLES=tuple(itertools.combinations(range(N),3))


def bits(k,m):return tuple((k>>i)&1 for i in range(m))
def mask(b):return sum(int(v)<<i for i,v in enumerate(b))

def all_states(arity=2):
    a=PAIRS if arity==2 else TRIPLES
    return [(bits(e,len(a)), bits(s,N)) for e in range(1<<len(a)) for s in range(1<<N)]

def permute(state,p,arity=2):
    edges=PAIRS if arity==2 else TRIPLES
    d=dict(zip(edges,state[0]));inv=[0]*N
    for i,v in enumerate(p):inv[v]=i
    return (tuple(d[tuple(sorted(inv[v] for v in h))] for h in edges),
            tuple(state[1][inv[i]] for i in range(N)))

def canonical(state,arity=2):return min(permute(state,p,arity) for p in PERMS)

def step_graph(state):
    e,s=state
    # pairwise, simultaneous equivariant topology rewrite
    ne=tuple(e[k] ^ s[i] ^ s[j] for k,(i,j) in enumerate(PAIRS))
    ns=tuple((s[i]+sum(e[k]*s[j] for k,(u,j) in enumerate(PAIRS) if u==i)
                   +sum(e[k]*s[u] for k,(u,j) in enumerate(PAIRS) if j==i))%2
             for i in range(N))
    return ne,ns

def complement_graph(state):
    return tuple(1-z for z in state[0]),state[1]

def step_graph_complement(state):
    return complement_graph(step_graph(state))

def step_hypergraph(state):
    e,s=state
    ne=tuple(e[k]^(sum(s[v] for v in h)%2) for k,h in enumerate(TRIPLES))
    ns=tuple(s[i] ^ (sum(e[k] * math.prod(s[v] for v in h if v!=i)
                for k,h in enumerate(TRIPLES) if i in h)%2) for i in range(N))
    return ne,ns

def automorphisms(state,arity=2,decorated=False):
    base=state if decorated else (state[0],(0,)*N)
    return [p for p in PERMS if permute(base,p,arity)==base]


def motif_key(state,subset,arity=2):
    e,s=state; EDGES=PAIRS if arity==2 else TRIPLES; d=dict(zip(EDGES,e)); k=len(subset)
    variants=[]
    for p in itertools.permutations(range(k)):
        order=tuple(subset[i] for i in p)
        col=tuple(s[i] for i in order)
        ee=tuple(d[tuple(sorted(h))] for h in itertools.combinations(order,arity)) if k>=arity else ()
        variants.append((col,ee))
    return k,min(variants)

def motif_types(k,arity=2):
    pat=[]
    for j in range(1,k+1):
        # use first j vertices with every possible edge and color pattern
        hcount=math.comb(j,arity) if j>=arity else 0
        for eh in range(1<<hcount):
            for sh in range(1<<j):
                edge_mask=[0]*len(PAIRS if arity==2 else TRIPLES)
                edge_positions=(PAIRS if arity==2 else TRIPLES)
                for idx,comb in enumerate(itertools.combinations(range(j),arity)):
                    edge_mask[edge_positions.index(comb)]=(eh>>idx)&1
                state=(tuple(edge_mask),bits(sh,j)+(0,)*(N-j))
                pat.append(motif_key(state,tuple(range(j)),arity))
    return tuple(sorted(set(pat)))

TYPES={2:{k:motif_types(k,2) for k in range(1,5)},3:{k:motif_types(k,3) for k in range(1,5)}}
THREE_TYPES=tuple(t for t in TYPES[2][3] if t[0]==3)
# Exact 0-indexed indices obtained by exhaustive search among 20 colored 3-vertex motifs
SELECTED=(4,8,10,13,17)

def all_motif_counts(state,k,arity=2):
    tally=collections.Counter(motif_key(state,subset,arity)
                  for j in range(1,k+1) for subset in itertools.combinations(range(N),j))
    return tuple(tally.get(t,0) for t in TYPES[arity][k])

def graph_motif_observer(state,level='selected'):
    if level in (1,2,3,4):return all_motif_counts(state,level)
    if level=='selected':
        base=all_motif_counts(state,2)
        tally=collections.Counter(motif_key(state,subset,2) for subset in itertools.combinations(range(N),3))
        return base+tuple(tally.get(THREE_TYPES[j],0) for j in SELECTED)
    raise ValueError(level)


def encode_base7(signature):
    """Faithful base-7 positional encoding of the 13 selected motif counts."""
    assert len(signature)==13 and all(0<=int(v)<7 for v in signature)
    result=0
    for v in signature:result=7*result+int(v)
    return result

def hyper_motif_observer(state,level):return all_motif_counts(state,level,3)

def exactness(states,observer,step):
    relation={};witness=None; classes=collections.defaultdict(list)
    for st in states:
        v=observer(st);nxt=observer(step(st));classes[v].append(st)
        if v in relation and relation[v]!=nxt and witness is None:witness=(st,classes[v][0],v,relation[v],nxt)
        if v not in relation:relation[v]=nxt
    bad=sum(len({observer(step(s)) for s in block})>1 for block in classes.values())
    return {'exact':bad==0,'classes':len(classes),'bad_classes':bad,'witness':witness,'macro':relation}

def cert():
    states=all_states(2); reps=sorted(set(canonical(x,2) for x in states));
    C={s:canonical(s,2) for s in states}
    B=[graph_motif_observer(s,2) for s in reps]
    V=[all_motif_counts(s,3)[len(TYPES[2][2]):] for s in reps]
    ridx={s:i for i,s in enumerate(reps)}
    nextindices=[ridx[C[step_graph(s)]] for s in reps]
    def check(sel):
        mapping={}
        for i in range(len(reps)):
            x=B[i]+tuple(V[i][j] for j in sel)
            j=nextindices[i]
            y=B[j]+tuple(V[j][k] for k in sel)
            if x in mapping:
                if mapping[x]!=y:return False
            else:mapping[x]=y
        return True
    counts={};five=[]
    for r in range(6):
        good=[]
        for subset in itertools.combinations(range(len(THREE_TYPES)),r):
            if check(subset):good.append(subset)
        counts[r]=len(good)
        if r==5:five=good
    assert counts=={0:0,1:0,2:0,3:0,4:0,5:98},counts
    assert SELECTED in five
    return counts

def extract_representatives(states,arity):return sorted(set(canonical(st,arity) for st in states))

def validate():
    G=all_states(2);H=all_states(3)
    for x in G:
        assert canonical(step_graph(x),2)==canonical(step_graph(canonical(x,2)),2)
    for x in H:
        assert canonical(step_hypergraph(x),3)==canonical(step_hypergraph(canonical(x,3)),3)
    for obs in [1,2,3,'selected']:
        for x in G:
            assert graph_motif_observer(x,obs)==graph_motif_observer(canonical(x,2),obs)
    results={'graph_microstates':len(G),'graph_orbits':len(extract_representatives(G,2)),
        'hyper_microstates':len(H),'hyper_orbits':len(extract_representatives(H,3)),
        'graph_levels':{},'hyper_levels':{}}
    for k in [1,2,3,'selected']:
        a=exactness(G,lambda x:graph_motif_observer(x,k),step_graph)
        results['graph_levels'][str(k)]={z:a[z] for z in ['classes','bad_classes','exact']}
    for k in [1,2,3]:
        a=exactness(H,lambda x:hyper_motif_observer(x,k),step_hypergraph)
        results['hyper_levels'][str(k)]={z:a[z] for z in ['classes','bad_classes','exact']}
    bc=exactness(G,lambda s:graph_motif_observer(s,'selected'),step_graph_complement)
    cc=exactness(G,lambda s:graph_motif_observer(s,'selected'),complement_graph)
    assert bc['exact'] and bc['classes']==86 and cc['exact']
    results['complement_variant']={'classes':86,'exact':True,'complement_alone_exact':True}
    results['motif_types']={'size_1' :len(TYPES[2][1]),'through_2':len(TYPES[2][2]),'three_only':len(THREE_TYPES),'through_3':len(TYPES[2][3])}
    results['minimal_extension_counts']=cert()
    initial=(bits(7,6),bits(2,4))
    cur=initial; traj=[]
    for i in range(6):
        traj.append({'step':i,'edge_mask':mask(cur[0]),'spin_mask':mask(cur[1]),
                     'edges':sum(cur[0]),'ones':sum(cur[1]),
                     'graph_aut_order':len(automorphisms(cur,2,False)),
                     'decorated_aut_order':len(automorphisms(cur,2,True)),
                     'observer_key':repr(graph_motif_observer(cur,'selected'))})
        cur=step_graph(cur)
    results['trajectory']=traj
    cur=(bits(1,4),bits(11,4)); ht=[]
    for i in range(5):
        ht.append({'step':i,'hyperedge_mask':mask(cur[0]),'spin_mask':mask(cur[1]),'hyperedges':sum(cur[0]),
                   'hypergraph_aut_order':len(automorphisms(cur,3,False)),
                   'decorated_aut_order':len(automorphisms(cur,3,True))});cur=step_hypergraph(cur)
    results['hyper_trajectory']=ht
    results['chosen_three_vertex_motifs']=[{'index_zero_based':j,'colors':list(THREE_TYPES[j][1][0]),
                                            'edges':list(THREE_TYPES[j][1][1])} for j in SELECTED]
    assert results['graph_orbits']==90 and results['hyper_orbits']==35
    assert results['graph_levels']['selected']=={'classes':86,'bad_classes':0,'exact':True}
    assert results['graph_levels']['3']=={'classes':90,'bad_classes':0,'exact':True}
    assert results['hyper_levels']['3']=={'classes':35,'bad_classes':0,'exact':True}
    assert [z['graph_aut_order'] for z in traj[:4]]==[6,8,24,8]
    assert all(traj[i]['decorated_aut_order'] <= traj[i+1]['decorated_aut_order'] for i in range(len(traj)-1))
    return results

def output(path):
    path=Path(path);path.mkdir(parents=True,exist_ok=True)
    r=validate()
    (path/'verified_results.json').write_text(json.dumps(r,indent=2),encoding='utf-8')
    G=all_states(2); reps=extract_representatives(G,2); ridx={st:i for i,st in enumerate(reps)}
    byobs={graph_motif_observer(s,'selected'):j for j,s in enumerate(reps)}
    # export exact induced 86-state observer transition table, stable sorted lexically
    objs=sorted(set(graph_motif_observer(s,'selected') for s in reps)); obsindex={ob:i for i,ob in enumerate(objs)}
    rows=[]
    for i,ob in enumerate(objs):
        represented=[s for s in reps if graph_motif_observer(s,'selected')==ob]
        nxt={obsindex[graph_motif_observer(step_graph(s),'selected')] for s in represented}
        assert len(nxt)==1
        rows.append({'observer_id':i,'successor_id':next(iter(nxt)),'number_colored_graph_orbits':len(represented),
                     'signature':','.join(map(str,ob)),
                     'base7_number':str(encode_base7(ob))})
    # A second exact macro system: compose F with whole-graph complement C.
    crow=[]
    for i,ob in enumerate(objs):
        represented=[s for s in reps if graph_motif_observer(s,'selected')==ob]
        succ={obsindex[graph_motif_observer(step_graph_complement(s),'selected')] for s in represented}
        assert len(succ)==1
        crow.append({'observer_id':i,'successor_id':next(iter(succ)),
                     'number_colored_graph_orbits':len(represented), 'signature':','.join(map(str,ob)),
                     'base7_number':str(encode_base7(ob))})
    with (path/'exact_macro_complement_86.csv').open('w',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=list(crow[0]));writer.writeheader();writer.writerows(crow)
    with (path/'exact_macro_dynamics_86.csv').open('w',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
    orows=[]
    for i,st in enumerate(reps):
        orows.append({'orbit_id':i,'edge_mask':mask(st[0]),'spin_mask':mask(st[1]),
                      'edge_count':sum(st[0]),'colored_automorphism_order':len(automorphisms(st,2,True)),
                      'graph_automorphism_order':len(automorphisms(st,2,False)),
                      'observer_id':obsindex[graph_motif_observer(st,'selected')],
                      'successor_orbit_id':ridx[canonical(step_graph(st),2)],
                     'base7_number':str(encode_base7(graph_motif_observer(st,'selected')))})
    with (path/'colored_graph_orbits_90.csv').open('w',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=list(orows[0]));writer.writeheader();writer.writerows(orows)
    return r
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--out',default='Data');a=p.parse_args()
    r=output(a.out)
    print(json.dumps({k:v for k,v in r.items() if k!='trajectory' and k!='hyper_trajectory'},indent=2))
    print('Group orders:',[x['graph_aut_order'] for x in r['trajectory']])
