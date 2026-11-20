(* Run from project root: wolframscript -file Examples/RunNative.wls *)
project=DirectoryName[DirectoryName[$InputFileName]];
Get[FileNameJoin[{project,"Kernel","DynamicBarycentric.wl"}]];
G=DynamicBarycentric`DBOrbitRepresentatives[2];
H=DynamicBarycentric`DBOrbitRepresentatives[3];
If[Length[G]=!=90 || Length[H]=!=35,Print["FAIL orbit enumeration"];Exit[1]];
If[Length[DynamicBarycentric`DBMotifCatalog[2,2]]=!=8 ||
 Length[DynamicBarycentric`DBMotifCatalog[2,3]]=!=28,
 Print["FAIL motif catalog"];Exit[1]];
results=<||>;
Do[
 fun=Function[st,DynamicBarycentric`DBMotifCensus[st,k]];
 observations=DeleteDuplicates[fun/@G];
 exact=DynamicBarycentric`DBMacroExactQ[fun,2];
 AssociateTo[results,ToString[k]-><|"Classes"->Length[observations],"Exact"->exact|>],
 {k,{1,2,3}}];
obs=DynamicBarycentric`DBSelectedObserver;
AssociateTo[results,"Selected"-><|"Classes"->Length[DeleteDuplicates[obs/@G]],
 "Exact"->DynamicBarycentric`DBMacroExactQ[obs,2]|>];
If[results["Selected"]=!=<|"Classes"->86,"Exact"->True|> ||
 results["3"]=!=<|"Classes"->90,"Exact"->True|>,
 Print["FAIL graph macro model: ",results];Exit[2]];
Do[
 fun=Function[st,DynamicBarycentric`DBMotifCensus[st,k]];
 If[Not[DynamicBarycentric`DBMacroExactQ[fun,3]] && k==3,
 Print["FAIL ternary hypergraph macro"];Exit[3]],{k,{1,2,3}}];
init=<|"Arity"->2,"Edges"->{1,1,1,0,0,0},"Colors"->{0,1,0,0}|>;
traj=DynamicBarycentric`DBOrbitTrajectory[init,5];
aut=DynamicBarycentric`DBAutomorphismOrder[#,False]& /@ traj;
If[Take[aut,4]=!={6,8,24,8},Print["FAIL group changes: ",aut];Exit[4]];
(* Equivariance and observer invariance independently checked on 90 orbit reps. *)
perms=Permutations[Range[4]];
Do[
 If[Not[And@@Table[
    DynamicBarycentric`DBStep[DynamicBarycentric`DBPermute[st,p]]===
       DynamicBarycentric`DBPermute[DynamicBarycentric`DBStep[st],p] &&
    DynamicBarycentric`DBSelectedObserver[DynamicBarycentric`DBPermute[st,p]]===
       DynamicBarycentric`DBSelectedObserver[st],{p,perms}]],
    Print["FAIL equivariance or observer invariance"];Exit[5]],{st,G}];
(* Independent built-in automorphism calculation on the sample trajectory. *)
Do[
 edges=Pick[Subsets[Range[4],{2}],st["Edges"],1];
 graph=Graph[Range[4],Apply[UndirectedEdge,#]& /@ edges];
 If[GroupOrder[GraphAutomorphismGroup[graph]]=!=
    DynamicBarycentric`DBAutomorphismOrder[st,False],
    Print["FAIL built-in GraphAutomorphismGroup cross-check"];Exit[6]],
 {st,traj}];
If[Not[DynamicBarycentric`DBMacroExactQ[
   DynamicBarycentric`DBSelectedObserver,2,DynamicBarycentric`DBStepComplement]],
 Print["FAIL complement-composed exact macro model"];Exit[7]];
codes=DeleteDuplicates[DynamicBarycentric`DBSignatureCode/@G];
If[Length[codes]=!=86 || Not[AllTrue[codes,IntegerQ]],
 Print["FAIL base-7 positional encoding"];Exit[8]];
results["BaseSevenDistinctCodes"]=Length[codes];
results["ComplementVariantExact"]=True;
results["GraphAutomorphismOrders"]=aut;
results["GraphOrbitCount"]=Length[G];
results["HypergraphOrbitCount"]=Length[H];
results["NativeWolframExecuted"]=True;
Export[FileNameJoin[{project,"Results","native_wolfram_results.json"}],results,"RawJSON"];
Print["PASS Mathematica native experiment: ",results];
