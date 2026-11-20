(* ::Package:: *)

(* DynamicBarycentric - exact, finite attributed-graph and ternary hypergraph
   experiments. All group actions, motif counts and transition rules use
   exact integers. *)
BeginPackage["DynamicBarycentric`"];
DBAllStates::usage="DBAllStates[arity] lists all binary-decorated 4-vertex arity-2 or arity-3 hypergraphs.";
DBGraphComplement::usage="DBGraphComplement[state] toggles all six graph edges while preserving colors.";
DBStepComplement::usage="DBStepComplement[state] applies the interacting graph step followed by edge complementation.";
DBStep::usage="DBStep[state] applies simultaneous pair (or ternary) interactions and topology rewriting.";
DBPermute::usage="DBPermute[state,p] relabels old vertex i as p[[i]].";
DBCanonical::usage="DBCanonical[state] is the lexicographically least state in its S4 orbit.";
DBOrbitRepresentatives::usage="DBOrbitRepresentatives[arity] lists unlabeled decorated orbits.";
DBAutomorphismOrder::usage="DBAutomorphismOrder[state,decorated] counts structure automorphisms or decorated-state automorphisms.";
DBMotifKey::usage="DBMotifKey[state,subset] is the canonical induced colored motif on a specified vertex subset.";
DBMotifCatalog::usage="DBMotifCatalog[arity,k] lists all colored motif types through k vertices.";
DBMotifCensus::usage="DBMotifCensus[state,k] returns exact induced motif counts through k vertices.";
DBSelectedObserver::usage="DBSelectedObserver[state] uses all <=2 vertex motifs plus five selected 3-vertex motifs (graph case).";
DBSignatureCode::usage="DBSignatureCode[state] faithfully encodes the thirteen selected motif counts as a base-seven integer.";
DBMacroExactQ::usage="DBMacroExactQ[observer,arity,evolution] tests exact descent for a chosen update.";
DBMacroMap::usage="DBMacroMap[observer,arity,evolution] produces observed transitions (default DBStep), or $Failed.";
DBOrbitTrajectory::usage="DBOrbitTrajectory[state,steps] returns labeled graph/hypergraph states along a deterministic evolution.";
Begin["`Private`"];
DBFaces[a_] := Subsets[Range[4],{a}];
DBBits[m_Integer,len_Integer] := Reverse[IntegerDigits[m,2,len]];
DBAllStates[a_Integer:2] /; MemberQ[{2,3},a] := DBAllStates[a] = Module[{edges=DBFaces[a]},
 Flatten[Table[<|"Arity"->a,"Edges"->DBBits[e,Length[edges]],"Colors"->DBBits[s,4]|>,
    {e,0,2^Length[edges]-1},{s,0,15}],1]];

DBStep[st_Association] := Module[{a=st["Arity"],e=st["Edges"],s=st["Colors"],faces,adj,newColors,newEdges},
 faces=DBFaces[a];
 If[a==2,
  adj=ConstantArray[0,{4,4}];
  Do[adj[[faces[[k,1]],faces[[k,2]]]]=e[[k]];
     adj[[faces[[k,2]],faces[[k,1]]]]=e[[k]],{k,Length[faces]}];
  newColors=Table[Mod[s[[i]]+Sum[adj[[i,j]]s[[j]],{j,4}],2],{i,4}];
  newEdges=Table[Mod[e[[k]]+Abs[s[[faces[[k,1]]]]-s[[faces[[k,2]]]]],2],{k,Length[faces]}],
  newColors=Table[Mod[s[[i]]+Sum[e[[k]] Times@@(s[[Complement[faces[[k]],{i}]]]),
                          {k,Select[Range[Length[faces]],MemberQ[faces[[#]],i]&]}],2],{i,4}];
  newEdges=Table[Mod[e[[k]]+Total[s[[faces[[k]]]]],2],{k,Length[faces]}]
 ];
 <|"Arity"->a,"Edges"->newEdges,"Colors"->newColors|>
];
DBGraphComplement[st_Association] /; st["Arity"]==2 :=
 Join[st,<|"Edges" -> (1-#& /@ st["Edges"])|>];
DBStepComplement[st_Association] /; st["Arity"]==2 := DBGraphComplement[DBStep[st]];
DBPermute[st_Association,p_List] := Module[{inv=Ordering[p],faces=DBFaces[st["Arity"]],e=st["Edges"],newEdges},
 newEdges=Table[With[{idx=First@FirstPosition[faces,Sort[inv[[f]]]]},e[[idx]]],{f,faces}];
 <|"Arity"->st["Arity"],"Edges"->newEdges,"Colors"->st["Colors"][[inv]]|>
];
DBCode[st_] := Join[st["Edges"],st["Colors"]];
DBCanonical[st_Association] := First[SortBy[(DBPermute[st,#]&) /@ Permutations[Range[4]],DBCode]];
DBOrbitRepresentatives[a_Integer:2] := DBOrbitRepresentatives[a] =
 SortBy[DeleteDuplicates[DBCanonical /@ DBAllStates[a]],DBCode];
DBAutomorphismOrder[st_Association,decorated_:False] := Module[{base},
 base=If[TrueQ[decorated],st,Join[st,<|"Colors"->ConstantArray[0,4]|>]];
 Count[(DBPermute[base,#]===base&) /@ Permutations[Range[4]],True]
];

DBMotifKey[st_Association,subset_List] := Module[
 {a=st["Arity"], faces=DBFaces[st["Arity"]],s=st["Colors"],ord,k=Length[subset],versions},
 versions=Table[
   ord=subset[[p]];
   {s[[ord]],If[k<a,{},(With[{pos=First@FirstPosition[faces,Sort[#]]},st["Edges"][[pos]]]& /@ Subsets[ord,{a}])]},
   {p,Permutations[Range[k]]}];
 {k,First[Sort[versions]]}
];
DBMotifCatalog[a_Integer,k_Integer] := DBMotifCatalog[a,k] = Module[{slist={},m,localfaces,allfaces,idx,st,base},
 allfaces=DBFaces[a];
 Do[
  localfaces=Subsets[Range[j],{a}];
  Do[
   st=<|"Arity"->a,
       "Edges"->Table[With[{pos=FirstPosition[localfaces,f,Missing["Absent"]]},
          If[MissingQ[pos],0,DBBits[edgeCode,Length[localfaces]][[pos[[1]]]]]],{f,allfaces}],
       "Colors"->Join[DBBits[colorCode,j],ConstantArray[0,4-j]]|>;
   AppendTo[slist,DBMotifKey[st,Range[j]]],
   {edgeCode,0,2^Length[localfaces]-1},{colorCode,0,2^j-1}],
 {j,1,k}];
 Sort[DeleteDuplicates[slist]]
];
DBMotifCensus[st_Association,k_Integer] := Module[{counts,features},
 features=Flatten[Table[DBMotifKey[st,#]& /@ Subsets[Range[4],{j}],{j,1,k}],1];
 counts=Counts[(ToString[InputForm[#]]& /@ features)];
 Lookup[counts,(ToString[InputForm[#]]& /@ DBMotifCatalog[st["Arity"],k]),0]
];
(* Explicit motif patterns avoid depending on language-specific ordering of
   canonical keys. Each is {size,{vertexColors,edges12/13/23}}. *)
DBSelectedMotifs={
 {3,{{0,0,1},{0,0,0}}},
 {3,{{0,0,1},{1,0,1}}},
 {3,{{0,1,1},{0,0,0}}},
 {3,{{0,1,1},{0,1,1}}},
 {3,{{1,1,1},{0,0,1}}}
};
DBSelectedObserver[st_Association] /; st["Arity"]==2 := Module[{c2,c3,cat,pos},
 c2=DBMotifCensus[st,2];c3=DBMotifCensus[st,3];cat=DBMotifCatalog[2,3];
 pos=(First@FirstPosition[cat,#,Missing["NotFound"]]& /@ DBSelectedMotifs);
 If[AnyTrue[pos,MissingQ],Return[$Failed]];
 Join[c2,c3[[pos]]]
];
DBSignatureCode[st_Association] /; st["Arity"]==2 := Module[{q=DBSelectedObserver[st]},
 If[Length[q]=!=13 || Not[AllTrue[q,0<=#<7&]],Return[$Failed]];
 FromDigits[q,7]
];
DBMacroMap[observer_,arity_Integer:2,evolution_:DBStep] := Module[{reps=DBOrbitRepresentatives[arity],map=<||>,key,val},
 Do[
  key=ToString[InputForm[observer[st]]];val=observer[evolution[st]];
  If[KeyExistsQ[map,key] && map[key]=!=val,Return[$Failed]];
  AssociateTo[map,key->val],
 {st,reps}];map
];
DBMacroExactQ[observer_,arity_Integer:2,evolution_:DBStep] := DBMacroMap[observer,arity,evolution]=!=$Failed;
DBOrbitTrajectory[st_Association,steps_Integer?NonNegative] := NestList[DBStep,st,steps];
End[];
EndPackage[];
