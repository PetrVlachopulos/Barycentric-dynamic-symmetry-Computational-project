# Barycentric Dynamic Symmetry

**Exact observable dynamics from changing graph symmetries**

&#x20;
*A Wolfram Language computational project in invariant theory, interacting graph/hypergraph systems, and computational observers*



**Research question:** How much of a discrete computational system must be retained by an observer to precisely describe its evolution? Can symmetry-based measurements forget microscopic differences while still determining the observable future?



## From Numerical Symmetries to Computational Observers



An unexpected place to begin is the familiar 3\\times 3 grid labeled with the numbers 1 through 9. For example, consider the averaging operation \\frac{159+357}{2}=258. This is not merely a numerical coincidence. The labels come from an **affine function of lattice coordinates**, and positional numeral encoding is **linear in its digit entries**. Therefore, them midpoints of grid points become averaging identities of the corresponding numbers. More generally, averaging over a finite group of geometric symmetries is governed by a **Reynolds operator**: a projection onto the subspace fixed by that group.



My manuscript, *Barycentric Number Designs — From Grid Symmetries to Averaging Identities*, develops this mechanism from rectangular grids to higher-dimensional lattice boxes and finite affine symmetry groups. It relates orbit barycenters, representation-theoretic projections, and the arithmetic conditions under which averaged points remain integral. Its central insight is that apparently elementary number patterns reflect a systematic relationship between **geometry, symmetry, and information-preserving encoding**.



**This computational project asks what happens when the underlying configuration starts to evolve.** Rather than averaging static arrays, we study **interacting graphs and ternary hypergraphs** whose vertex states and connectivity change together. Their symmetry groups can change along a computational trajectory. The key question is: can an observer made from invariant measurements — such as counts of small colored subgraphs, still determine the next observable state, even though it cannot reconstruct every microscopic configuration?

The project answers that question exactly for a bounded four-vertex laboratory. Using exhaustive enumeration, it constructs a **13-component motif observer** whose measurements admit an autonomous **86-state effective dynamics**, while the underlying system has **90 colored-graph isomorphism classes**. It also exhibits genuinely moving, non-isomorphic states that the observer identifies without losing predictive consistency.



This computational experiment was highly motivated by the Wolfram Institute's research interests in **observer theory, graph/hypergraph rewriting, discrete symmetries, and computational foundations**.



## Key Mathematical and Computational Results



|Experiment|Labeled configurations|Colored isomorphism classes|Observable result|
|-|-:|-:|-|
|Interacting four-vertex binary **graph**|**1,024**|**90**|Exact **86-state** quotient from 13 selected motif counts|
|Interacting four-vertex binary **ternary hypergraph**|**256**|**35**|Full induced-motif census distinguishes all 35 classes|

### 

### 1\. Exact dynamics from incomplete observations

Let F be the finite deterministic update and Q the invariant observer. The objective is to construct \\overline F satisfying



&#x09;								Q\\\\circ F=\\\\overline F\\\\circ Q.





This holds precisely when any two states with the same observation have **identical next observations**. It does *not* require (Q) to reconstruct the microscopic state.

For the graph system, the eight induced colored-motif counts of size at most two yield **66** observable classes but fail this exactness condition (**15 defective classes**). Adding five carefully chosen three-vertex motif counts gives **86** observed classes and an exact effective evolution. This demonstrates **dynamical sufficiency without full microscopic identification**.

!\[Observer refinement and exactness](Results/figures/02\_observer\_ladder.png)



### 2\. A finite, certified feature-selection result

An exhaustive search over a specified menu of **20 candidate three-vertex motif counts** establishes that, relative to the eight basic motif counts:

* **No** selection of four or fewer candidates makes this particular graph update exactly observable.
* **98** distinct five-feature selections do.
* The included 13-component observer is one such minimal selection **within this candidate menu**.

This is a finite optimality statement for **one defined model and feature family**, not a universal claim that five motifs are needed for every graph dynamic.

!\[Selected graph motifs](Results/figures/03\_selected\_motifs.png)



### 3\. Nontrivial exact dynamics after information is discarded

A stronger demonstration composes the update with graph complementation, (F^\\sharp=C\\circ F). The **same observer remains exact**, yet pairs of non-isomorphic graph states that it merges now participate in genuine **two-cycles**. Thus the reduction is not merely hiding stationary or frozen states.

!\[A nontrivial merged-state macrocycle](Results/figures/07\_nontrivial\_merged\_macrocycle.png)

[View the macrocycle animation](Results/animations/02_exact_macro_merged_cycle.gif) · [Inspect the exact 86-state transition table](Data/exact_macro_complement_86.csv)



### 4\. Changing symmetry groups: geometry versus decorated dynamics

One computed trajectory has automorphism-group orders of the **uncolored underlying graphs**

\[
6\\rightarrow8\\rightarrow24\\rightarrow8\\rightarrow24\\rightarrow8.
]

The stabilizers of the **fully decorated vertex-and-edge states** are different: for a deterministic update equivariant under relabeling, a symmetry of a state remains a symmetry of its image. Their stabilizers therefore cannot decrease along a trajectory. The fluctuating geometry-level group and the monotone decorated-state stabilizer must not be confused.

!\[Changing automorphism groups](Results/figures/01\_changing\_automorphisms.png)

[View the graph-evolution animation](Results/animations/01_group_changes.gif)



### 5\. Hypergraph extension and numerical encoding

A separate **three-uniform hypergraph** experiment uses ternary interactions between vertex states and hyperedges. Its induced motifs of size at most three distinguish all **35** decorated-isomorphism classes; this is an exact orbit description, not yet a nontrivial compression analogous to the graph's 90-to-86 reduction.

The 13 graph-observer counts also admit a **faithful base-seven positional encoding** into a single integer. This reconnects the project to the numeral-encoding viewpoint of the motivating manuscript. Encoding the observable vector into one number **does not recover information already discarded by the observer**.

!\[Ternary hypergraph trajectory](Results/figures/08\_ternary\_hypergraph\_trajectory.png)

## 

## Explore the Project

**Start with the results, then inspect the implementation:**

|Resource|What it contains|
|-|-|
|One-page brief summary|Fast scientific overview for a first-time reader|
|Technical report|Definitions, exact update rules, propositions, proofs, finite classifications and limitations|
|Main Wolfram Language source|Graph/hypergraph states, group actions, motif observers and exactness checks|
|Guided Mathematica notebook|Step-by-step interactive execution, with explanations|
|Commented Wolfram execution script|Guided automated checks and output exports|
|Mathematica interactive viewer|Interactive graph evolution and symmetry measurements|
|Interative simulation|Standalone demonstration (open locally in a browser)|
|Reference data|Independently calculated enumeration and classification results|
|Research prorgram|Further directions in changing observers and event-groupoid formulations|

For a broader view, the 86-state transition network visualizes the effective dynamics, and the event-grupoid diagram motivates how to extend from deterministic updates to multiway rewriting.



## Run in Mathematica

**Requirements:** Mathematica / Wolfram Language for the native package and notebook. Keep the repository's folder structure intact.

**Recommended route:**

1. Download or clone this repository; open Mathematica and create a notebook.
2. Evaluate the following cell and select the directory containing "Kernel", "Examples", and "Data":

```wolfram
   project = SystemDialogInput\\\\\\\["Directory"];
   ```

3. Open "Guides/Barycentric\\Execution\\Guide.nb" and evaluate its cells in order, **or** run the guided script:

```wolfram
   Get\\\\\\\[FileNameJoin\\\\\\\[{project, "Examples", "RunGuidedExperiment.wl"}]]
   ```

4. Launch the interactive viewer in a separate notebook cell:

```wolfram
   Get\\\\\\\[FileNameJoin\\\\\\\[{project, "Examples", "InteractiveSimulator.wl"}]]
   ```

**Verification** (run in a separate WolframScript process because the validator uses `Exit\\\\\\\[...]` on failure):

```bash
wolframscript -file Examples/RunNative.wls
python validation/verify\\\\\\\_native.py
```

On Windows, the repository also includes "run\\\_native\\\_verification.ps1", which manages the run and reference comparison. See the guided-execution instructions and dependency notes.

## 

## Reproduce the Independent Reference Experiments

The complete independent verification uses Python and the dependencies documented in Dependencies.md, including "networkx", "pytest", "matplotlib", and "Pillow" for the complete analysis and figure pipeline.



From the repository root:

bash
python validation/reference.py --out Data
pytest -q Tests/test\\\_reference.py
python validation/make\\\_figures.py
python validation/build\\\_simulator.py



The reference pipeline enumerates the finite state spaces and exhaustively checks the candidate motif selections. The repository provides the resulting CSV files, computed graphics, animations, and a GitHub Actions workflow for independent Python tests at ".github/workflows/reference-tests.yml".



## Verification Status and Scope

|Check|Status|
|-|-|
|Independent Python reference calculations|**Executed**|
|Automated reference tests|**23/23 passed** in the prior recorded environment|
|Exact graph quotient and bounded five-feature classification|**Verified by exhaustive reference enumeration**|
|Hypergraph orbit enumeration and motif analysis|**Verified by independent reference checks**|





## Mathematical Perspective and Research Outlook



The conceptual starting point is the Reynolds operator. Averaging over finite symmetries produces canonical invariant quantities. The computational question is **which invariants are dynamically sufficient**, and how to reconstruct missing information if a coarser observer fails to determine the next observation. Motif counts provide a finite, explicit laboratory for that question.

The results above are **finite-model computational findings**. Reynolds projection, graph invariants, and exact quotient criteria are established objects/constructions. The distinct contribution of this prototype is their explicit combination in interacting update systems, together with a bounded optimality search and a nontrivial exact reduced dynamics.

A longer-term direction is to replace the single global relabeling group by **state-dependent automorphism groups**, with spans of rewrite-event groupoids organizing possible transitions between different symmetry structures. Importantly, the research program discusses this as a prospective extension rather than an already validated model.



## Related Work and References



* *Barycentric Number Designs — From Grid Symmetries to Averaging Identities* — motivating research manuscript
* [Wolfram Institute: Causality, Observers \& Computation](https://wolframinstitute.org/research/causality-observers-computation)
* [Wolfram Institute: Hypergraph Rewriting](https://wolframinstitute.org/research/hypergraph-rewriting)
* [Wolfram Institute: HypergraphRewritingEngine](https://github.com/WolframInstitute/HypergraphRewritingEngine)

