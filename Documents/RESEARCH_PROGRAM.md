# Research program: symmetry-dependent reconstruction in graph and hypergraph rewriting

*Barycentric Observers under Changing Symmetries: Exact Motif Reconstruction, Rewriting Groupoids and Effective Dynamics.*



## A. Why this is a natural continuation of the attached manuscript

The manuscript *Barycentric Number Designs — From Grid Symmetries to Averaging Identities* isolates the linearity of affine labels and positional encodings, extends midpoint identities to finite affine-group orbit barycenters, uses Reynolds projections, and proves a representation-theoretic odd/even integrality distinction on cubes. Those are results about finite *static* geometric configurations. The present extension tests the **dynamic sufficiency** of symmetry-invariant information after graph topology itself evolves.

For a fixed group H, the Reynolds operator projects onto its fixed-point representation. For a changing graph G\_t, however, the automorphism groups H\_{G\_t} are not canonically identified. Worse, the Reynolds barycenter of binary vertex states loses nonlinear correlations with edges. Therefore, we replace any fixed group's particular average with induced colored-motif census functions, which are universally invariant under all vertex relabelings. They may be regarded as polynomial orbit sums => indicator monomials for patterns are averaged/reindexed under the finite permutation action.



## B. Exact experiment and its finite certification

The binary 4-vertex colored-graph state consists of 6 edge bits and 4 vertex-color bits. The rule is

* a'*{ij} = a*{ij} XOR s\_i XOR s\_j;
* s'*i = s\_i XOR (XOR over j of (a*{ij} AND s\_j)).

Both interactions and topology change simultaneously. This rule is equivariant under S4 vertex relabeling. Hence a functor on the isomorphism groupoid exists, even when the underlying uncolored automorphism group changes.

**Finite results:** 1,024 labeled states; 90 colored-graph isomorphism classes. The complete 1- and 2-vertex colored induced-motif census has 8 entries, creates 66 observed classes, and is dynamically incompatible in 15 classes. Adding 5 selected colored 3-vertex motif counts makes the observer exact, with just 86 observed classes. There are 20 candidate 3-vertex motifs. Exhaustive search shows zero exact subsets at sizes 0 through 4 and 98 exact subsets at size 5. All these successful 5-subset observers yield 86 classes. Complete 3-vertex motif census separates all 90 orbit classes. Importantly, these are finite machine-checkable classification facts, not general theorems for arbitrary n.

The 86-observation map is a genuine **coarser-than-isomorphism** dynamically exact model - its three nontrivial fibers have sizes 2, 3, 2, collapsing seven colored-graph orbits to three observer classes (a reduction by four). Under the original F these fibers consist of zero-color states that are individually fixed, a limitation that should not be concealed. Under the complement-composed update C∘F, the same observer remains exactly sufficient and the merged two-edge and four-edge classes undergo a genuine nontrivial two-cycle. The original F macro has 13 fixed points, three 2-cycles and one 3-cycle, and C∘F has two fixed points and eight 2-cycles.

**Ternary hypergraph:** On four vertices, there are four possible 3-edges. The color update includes products of neighboring colors within each 3-edge. The exact enumerator finds 256 labeled states, 35 colored-hypergraph orbit classes, and exact reconstruction by induced motifs of size at most 3. This is a local higher-arity interaction model. It is important to state that its four-vertex finite scope does not justify a continuum or field-theory interpretation.



## C. Three levels of symmetry

1. **Underlying geometry:** Aut(G\_t), the uncolored graph automorphism group. Orders may fluctuate freely as the graph changes => in the present exact example they are 6 → 8 → 24 → 8 → 24 → 8.
2. **Decorated symmetry:** Aut(G\_t,s\_t). For deterministic S\_n-equivariant rewriting on a fixed labeled vertex set, Aut(x\_t) ≤ Aut(x\_{t+1}). This is a simple but essential stabilizer theorem. Here orders are 2 → 4 → 4 → 4 → 4 → 4.
3. **Multiway event symmetry:** For a relation R(x) of possible successor events, a symmetry of x need only *permute* events, not stabilize an individual event. For the four-cycle single-edge deletion example, D4 (order 8) acts transitively on four matches and every branch produces P4 (automorphism order 2). The appropriate structure is a span of event groupoids, not a single group homomorphism between Aut(C4) and Aut(P4).

This separation prevents the common mistake of asserting monotone automorphism groups for the geometry alone or using a deterministic functor for a nondeterministic rewrite relation.



## D. Categorical formulation

Let X be the groupoid of labeled colored finite graphs and their vertex relabelings. A permutation-equivariant deterministic rewrite F defines F:X→X. Each motif observer Q\_m is invariant under all groupoid isomorphisms, hence factors through the set of isomorphism classes. A coarser observer Q descends dynamically iff its induced equivalence relation is an F-congruence:

Q(x)=Q(x') implies Q(F(x))=Q(F(x')).

The present 13-component observer meets this condition without being injective on isomorphism classes. Accordingly an exact finite macro endomorphism F\_bar exists on its 86 observable states.

For a multiway relation, let us define the event groupoid E whose objects are (x,m), where m is an enabled match, with morphisms the relabelings respecting both x and m. Source and target functors create a span X ← E → X. The event stabilizer is the subgroup fixing the chosen match, and the orbit-stabilizer formula counts symmetry-related branches. In categorical extensions, such spans naturally compose by weak pullback (taking event matching and intermediate isomorphisms into account). Proving coherence, exactness of a chosen observational quotient, and appropriate finite-to-infinite limits remain future work.



## E. Proposed higher-level investigations



### E1. Minimal dynamically closed invariant algebra

Given a finite space of colored graphs and a menu of orbit-sum polynomial invariants, find a minimum-cardinality subset yielding exact deterministic quotient dynamics. This resembles finite feature-selection and congruence computation, but the candidate features are symmetry-invariant motif polynomials. Investigate parameterized complexity, canonical minimal witnesses, and symbolic certificates using integer linear algebra, SAT/SMT, and modular invariant theory. In particular, the finite 5-feature result is an experimental benchmark, not an optimality statement beyond the specified feature menu.



### E2. Higher-arity motif observers and changing hypergraph groups

Extend the experiment to 3-uniform and mixed-arity hyperedges, hypergraphs with changing vertex count, and event-dependent rewrite schedules. Build induced hypergraph motif inventories and test which low-order motifs close exact dynamics. For vertex-changing rewrites, replace the fixed S\_n action by a family of groupoids indexed by n, while event spans or double-pushout-style rewriting approaches are natural candidates. Importantly, no categorical equivalence to the Institute's particular hypergraph implementation is assumed in advance.



### E3. Approximate reconstruction and scaling

For larger n and bounded motif size k, exact closure is expected to become uncommon. Replace exact congruence by a stochastic/approximate observer with explicit TV or KL predictive errors. Study whether the required motif order grows slowly with n in constrained families, and whether a continuum geometric observable can be predicted from finite local motifs. This is a concrete entry toward multiscale observer theory.



### E4. From barycentric arithmetic labels to causal graph observables

The manuscript's affine integer labels can be attached to graph/hypergraph vertex coordinates or selected orbit invariants. Test which labelings commute with event-orbit averaging and whether group averaging remains integral after a change of graph symmetry. When a symmetry group changes, the relevant arithmetic obstruction may also change. This route directly connects the original number-design theme to discrete causal experiments. Notice that careful attention is needed because an invariant polynomial observer and a Reynolds barycenter are different objects.



## F. Wolfram Institute connection and scope

The Institute's Hypergraph Rewriting and Causality/Observers/Computation research emphasizes higher-arity rewrites, equivariance/composition, causal and observer structures. Our source provides a compact, exact, independently verifiable mathematical experiment exhibiting: (i) nontrivial interacting rules, (ii) changing graph symmetries, (iii) exact motif-based effective dynamics, (iv) a computer-assisted minimality classification, and (v) a precise reason to organize multiway matches as groupoid spans.

The repository does **not** claim that these custom synchronous rules are native Wolfram Physics Project rules; the `HypergraphRewritingEngine` has distinct event semantics. The next scientific integration would feed an actual set of engine-generated state/event records into the motif observer pipeline, preserving event multiplicities and the model's precise canonicalization policy. It also does **not** claim an unqualified new general theorem: classical invariant theory, lumpability and groupoids are established. Novelty is in the chosen synthesis, finite mathematical examples, exhaustive exact classification, and potential subsequent structural theorems.



## G. Faithful positional encoding of symmetry-invariant data

Each of the thirteen selected induced motif counts is an integer between 0 and 6. The positional map `N\_7(x) = sum(q\_i \* 7^(13-i))` is therefore an injective representation of the **observable** 13-vector as one base-seven number, without carries. The exact observed transition map induces a map on precisely 86 such integers. This connects the project directly to the original manuscript’s central mechanism of linear positional encoding, but it does not make the number code injective on microscopic graph states. Averaging identities hold algebraically by linearity of the encoding. A digitwise barycentric interpretation additionally requires admissible integral coordinatewise means.

