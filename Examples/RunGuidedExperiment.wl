(* ::Package:: *)

(* ::Title:: *)
(* BARYCENTRIC DYNAMIC SYMMETRIES - FULL GUIDED EXECUTION EXPERIMENT                                                                        *)
(*                                                                             *)
(* Terms used below:                                                          *)
(*  - MICROSTATE: a four-vertex graph or 3-uniform hypergraph, with 0/1        *)
(*    edges and 0/1 vertex attributes.                                        *)
(*  - ORBIT: equivalence class under all 24 permutations of vertex labels.    *)
(*  - OBSERVER: vector of induced colored-subgraph motif counts.              *)
(*  - EXACT MACRODYNAMICS: q(F(x)) depends only on q(x), not on x itself.           *)


(* ------------------------------------------------------------------------- *)
(* STEP 0 - Locate project     *)
(* ------------------------------------------------------------------------- *)
ClearAll[bdProjectRoot, bdResults, bdCheck, bdGraphPicture,
  bdGraphReps, bdHyperReps, bdObserver, bdInitial,
  bdTrajectory, bdCandidates, bdKernelFile, bdReportPath,
  bdPassed, bdSelectedGroups, bdMergedGroups, bdActiveMerged];

bdCandidates = DeleteDuplicates @ Select[
  {
    If[StringQ[$InputFileName] && $InputFileName =!= "",
      DirectoryName[DirectoryName[$InputFileName]], ""],
    Directory[],
    Quiet[Check[NotebookDirectory[], ""]]
  },
  StringQ[#] && DirectoryQ[#] &
];

bdProjectRoot = SelectFirst[
  bdCandidates,
  FileExistsQ[FileNameJoin[{#, "Kernel", "DynamicBarycentric.wl"}]] &,
  Missing["NoProjectFound"]
];
If[MissingQ[bdProjectRoot],
  Print["Choose the extracted PROJECT directory (the folder containing Kernel/ and Examples/)."];
  bdProjectRoot = SystemDialogInput["Directory"];
];

Catch[
 If[!StringQ[bdProjectRoot] ||
    !FileExistsQ[FileNameJoin[{bdProjectRoot, "Kernel", "DynamicBarycentric.wl"}]],
   Print["ERROR: Project source not found. Select the folder containing Kernel/DynamicBarycentric.wl."];
   Throw[$Failed, "BarycentricGuide"]
 ];
 Print[Style["BARYCENTRIC DYNAMIC SYMMETRIES - NATIVE STUDY RUN", 16, Bold]];
 Print["Project directory: ", bdProjectRoot];
 Print["Wolfram version: ", $Version];

 (* ---------------------------------------------------------------------- *)
 (* STEP 1 - Import the implementation and inspect available public functions. *)
 (* ---------------------------------------------------------------------- *)
 bdKernelFile = FileNameJoin[{bdProjectRoot, "Kernel", "DynamicBarycentric.wl"}];
 Get[bdKernelFile];
 If[!MemberQ[Names["DynamicBarycentric`*"], "DynamicBarycentric`DBAllStates"],
   Print["ERROR: Kernel file did not define expected public symbols."];
   Throw[$Failed, "BarycentricGuide"]
 ];
 Print[Style["STEP 1 - Package loaded", 13, Bold]];
 Print["Public functions: ", Names["DynamicBarycentric`*"]];

 bdResults = {};
 bdCheck[label_String, observed_, expected_] := Module[{ok},
   ok = SameQ[observed, expected];
   AppendTo[bdResults, <|
     "Check" -> label, "Passed" -> ok,
     "Observed" -> ToString[InputForm[observed]],
     "Expected" -> ToString[InputForm[expected]]
   |>];
   Print[If[ok, "PASS | ", "FAIL | "], label,
     " | observed = ", ToString[InputForm[observed]]];
   ok
 ];

 (* ---------------------------------------------------------------------- *)
 (* STEP 2 - Enumerate every binary-decorated 4-vertex microstate.           *)
 (* Graph: 6 potential edges, 4 binary colors => 2^(6+4) = 1024.          *)
 (* Ternary hypergraph: 4 potential triples, 4 colors => 2^8 = 256.       *)
 (* ---------------------------------------------------------------------- *)
 Print[Style["STEP 2 - Exhaustive microscopic states", 13, Bold]];
 bdCheck["Graph microstate count", Length[DynamicBarycentric`DBAllStates[2]], 1024];
 bdCheck["3-uniform hypergraph microstate count",
   Length[DynamicBarycentric`DBAllStates[3]], 256];

 (* ---------------------------------------------------------------------- *)
 (* STEP 3 - Quotient by permutation symmetry of the four vertices.          *)
 (* Each orbit is represented by its lexicographically canonical state.       *)
 (* ---------------------------------------------------------------------- *)
 Print[Style["STEP 3 - Decorated isomorphism classes", 13, Bold]];
 bdGraphReps = DynamicBarycentric`DBOrbitRepresentatives[2];
 bdHyperReps = DynamicBarycentric`DBOrbitRepresentatives[3];
 bdCheck["Graph orbit count", Length[bdGraphReps], 90];
 bdCheck["Ternary hypergraph orbit count", Length[bdHyperReps], 35];

 (* ---------------------------------------------------------------------- *)
 (* STEP 4 - Observable signatures.                                           *)
 (* A motif count records how many induced colored substructures of the      *)
 (* indicated size occur in a microscopic state. Every count is invariant    *)
 (* under permutation of the four vertex labels.                              *)
 (* ---------------------------------------------------------------------- *)
 Print[Style["STEP 4 - Motif observers and compression", 13, Bold]];
 bdCheck["All motif types through two vertices",
   Length[DynamicBarycentric`DBMotifCatalog[2, 2]], 8];
 bdCheck["All motif types through three vertices",
   Length[DynamicBarycentric`DBMotifCatalog[2, 3]], 28];

 bdObserver = DynamicBarycentric`DBSelectedObserver;
 bdCheck["Distinct selected 13-component observer values",
   Length[DeleteDuplicates[bdObserver /@ bdGraphReps]], 86];
 bdCheck["Selected observer produces a 13-component vector",
   Length[bdObserver[First[bdGraphReps]]], 13];
 bdCheck["Complete 3-vertex motif census separates 90 orbits",
   Length[DeleteDuplicates[
     (DynamicBarycentric`DBMotifCensus[#, 3] &) /@ bdGraphReps]], 90];

 (* ---------------------------------------------------------------------- *)
 (* STEP 5 - Exact dynamics test.                                             *)
 (* An observer q descends exactly iff                                        *)
 (*       q(x)=q(y)  =>  q(F(x))=q(F(y)) for all x,y.                         *)
 (* We implement this via DBMacroMap and DBMacroExactQ.              *)
 (* ---------------------------------------------------------------------- *)
 Print[Style["STEP 5 - Does the observer determine its own future?", 13, Bold]];
 bdCheck["Two-vertex motif observer is NOT exact",
   DynamicBarycentric`DBMacroExactQ[
     Function[st, DynamicBarycentric`DBMotifCensus[st, 2]], 2], False];
 bdCheck["Full three-vertex motif observer IS exact",
   DynamicBarycentric`DBMacroExactQ[
     Function[st, DynamicBarycentric`DBMotifCensus[st, 3]], 2], True];
 bdCheck["Selected 13-component observer IS exact",
   DynamicBarycentric`DBMacroExactQ[bdObserver, 2], True];
 bdCheck["Observer also exact for complement-composed dynamics",
   DynamicBarycentric`DBMacroExactQ[
     bdObserver, 2, DynamicBarycentric`DBStepComplement], True];
 bdCheck["Full three-vertex hypergraph observer IS exact",
   DynamicBarycentric`DBMacroExactQ[
     Function[st, DynamicBarycentric`DBMotifCensus[st, 3]], 3], True];

 (* ---------------------------------------------------------------------- *)
 (* STEP 6 - Positional encoding, connecting back to the number-designs      *)
 (* manuscript. Every selected count is in 0..6, thus an allowed base-7 digit. *)
 (* Base 7 is an exact packaging of observations and it does not restore lost    *)
 (* microscopic information.                                                   *)
 (* ---------------------------------------------------------------------- *)
 Print[Style["STEP 6 - Faithful base-seven encoding", 13, Bold]];
 bdCheck["Number of distinct base-seven observer codes",
   Length[DeleteDuplicates[
     (DynamicBarycentric`DBSignatureCode /@ bdGraphReps)]], 86];
 bdCheck["Codes are exact integers",
   AllTrue[(DynamicBarycentric`DBSignatureCode /@ bdGraphReps), IntegerQ], True];

 (* ---------------------------------------------------------------------- *)
 (* STEP 7 - One real trajectory and its changing graph symmetries.           *)
 (* IMPORTANT!: graph automorphisms may shrink or grow and decorated-state        *)
 (* stabilizers are nondecreasing under deterministic equivariant evolution.  *)
 (* ---------------------------------------------------------------------- *)
 Print[Style["STEP 7 - Changing automorphism groups", 13, Bold]];
 bdInitial = <|"Arity" -> 2, "Edges" -> {1, 1, 1, 0, 0, 0},
               "Colors" -> {0, 1, 0, 0}|>;
 bdTrajectory = DynamicBarycentric`DBOrbitTrajectory[bdInitial, 5];
 bdCheck["Uncolored graph automorphism orders, steps 0..3",
   Take[(DynamicBarycentric`DBAutomorphismOrder[#, False] &) /@ bdTrajectory, 4],
   {6, 8, 24, 8}];
 bdCheck["Decorated automorphism orders never decrease",
   And @@ Thread[Differences[
     (DynamicBarycentric`DBAutomorphismOrder[#, True] &) /@ bdTrajectory] >= 0], True];

 (* Graph drawing: vertex attributes are rendered as colors.                *)
 bdGraphPicture[st_Association] := Module[{edges, colors},
   edges = Pick[Subsets[Range[4], {2}], st["Edges"], 1];
   colors = Thread[Range[4] -> (
     If[# == 1, RGBColor[0.94, 0.61, 0.24], RGBColor[0.12, 0.53, 0.54]] & /@
       st["Colors"])];
   Graph[Range[4], (Apply[UndirectedEdge, #] & /@ edges),
     VertexStyle -> colors, VertexLabels -> "Name",
     GraphLayout -> "CircularEmbedding", VertexSize -> .32,
     ImageSize -> 270, EdgeStyle -> Directive[GrayLevel[.35], Thick]]
 ];

 (* ---------------------------------------------------------------------- *)
 (* STEP 8 - Find a pair of genuinely different microscopic orbit states      *)
 (* sharing an observer value. For Fsharp=Complement[ F(x) ], test if this    *)
 (* merged macrostate still moves => this is more than merging fixed states.    *)
 (* ---------------------------------------------------------------------- *)
 Print[Style["STEP 8 - Active, merged macrostate witness", 13, Bold]];
 bdSelectedGroups = GatherBy[bdGraphReps, bdObserver];
 bdMergedGroups = Select[bdSelectedGroups, Length[#] > 1 &];
 bdCheck["At least one nontrivial observer fiber exists",
   Length[bdMergedGroups] > 0, True];
 bdActiveMerged = SelectFirst[
   bdMergedGroups,
   Function[group,
     bdObserver[DynamicBarycentric`DBStepComplement[First[group]]] =!=
       bdObserver[First[group]]
   ], Missing["None"]
 ];
 If[!MissingQ[bdActiveMerged],
   bdCheck["Two merged microstates share an observation",
     SameQ @@ (bdObserver /@ bdActiveMerged), True];
   bdCheck["Their next observations agree under complement evolution",
     Length[DeleteDuplicates[bdObserver /@
       (DynamicBarycentric`DBStepComplement /@ bdActiveMerged)]], 1];
   bdCheck["The merged observable state moves",
     bdObserver[DynamicBarycentric`DBStepComplement[First[bdActiveMerged]]] =!=
       bdObserver[First[bdActiveMerged]], True];
   Print["A nontrivial merged block contains ", Length[bdActiveMerged], " orbit states."];
   Print["Its observed signature: ", bdObserver[First[bdActiveMerged]]];
   Print["Its successor signature: ",
     bdObserver[DynamicBarycentric`DBStepComplement[First[bdActiveMerged]]]],
   Print["No active merged block found; inspect the Python reference classification."];
   bdCheck["Active merged block found", False, True]
 ];

 (* ---------------------------------------------------------------------- *)
 (* STEP 9 - Export a genuine native Wolfram trajectory and a machine-readable *)
 (* summary of these checks. This does not overwrite the original Python oracle!   *)
 (* ---------------------------------------------------------------------- *)
 Print[Style["STEP 9 - Figures and verification record", 13, Bold]];
 Quiet[CreateDirectory[FileNameJoin[{bdProjectRoot, "Results"}],
    CreateIntermediateDirectories -> True]];
 bdReportPath = FileNameJoin[{bdProjectRoot, "Results", "guided_native_run.json"}];

 If[$Notebooks,
   Print["A native graph-trajectory visualization follows:"];
   Print[GraphicsGrid[Partition[bdGraphPicture /@ bdTrajectory, 3],
     ImageSize -> 980]];
 ];
 Check[
   Export[FileNameJoin[{bdProjectRoot, "Results", "guided_wolfram_trajectory.png"}],
     GraphicsGrid[Partition[bdGraphPicture /@ bdTrajectory, 3],
       ImageSize -> 1000], "PNG"];
   Print["Saved graph illustration to Results/guided_wolfram_trajectory.png"],
   Print["WARNING: Figure export failed; the mathematical checks remain separately recorded."]
 ];

 bdPassed = AllTrue[bdResults, TrueQ[# ["Passed"]] &];
 Check[
   Export[bdReportPath,
     <|"RunDate" -> DateString[{"Year", "-", "Month", "-", "Day", " ", "Hour", ":", "Minute"}],
       "WolframVersion" -> $Version, "ProjectDirectory" -> bdProjectRoot,
       "NativeKernelExecuted" -> True,
       "AllGuidedChecksPassed" -> bdPassed,
       "CheckCount" -> Length[bdResults],
       "Checks" -> bdResults,
       "Scope" -> "Guided verification only; run Examples/RunNative.wls separately for full native suite."|>,
     "RawJSON"],
   Print["WARNING: Could not export the JSON summary."]
 ];

 Print[Style["FINAL SUMMARY", 14, Bold]];
 Print["Passed: ", Count[bdResults, a_ /; TrueQ[a["Passed"]]],
       " / ", Length[bdResults]];
 Print["Native guided run record: ", bdReportPath];
 If[bdPassed,
   Print[Style["All guided checks passed. Now run the independent native suite externally.",
     Darker[Green], Bold]],
   Print[Style["One or more checks failed. Inspect the output and JSON record before proceeding.",
     Red, Bold]]
 ];
 Print["For interactive exploration, evaluate this IN A SEPARATE NOTEBOOK CELL:"];
 Print["Get[FileNameJoin[{bdProjectRoot, \"Examples\", \"InteractiveSimulator.wl\"}]]"];
 Print["For the complete strict native suite in a separate WolframScript process:"];
 Print["wolframscript -file Examples/RunNative.wls"];

 , "BarycentricGuide"
];
