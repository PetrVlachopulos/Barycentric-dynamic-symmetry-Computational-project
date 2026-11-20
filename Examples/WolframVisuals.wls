(* Native Wolfram visualization helper. Execute from project root. *)
root=DirectoryName[DirectoryName[$InputFileName]];
Get[FileNameJoin[{root,"Kernel","DynamicBarycentric.wl"}]];
pairs=Subsets[Range[4],{2}];
showState[st_] := Module[{g,colors,faces=Subsets[Range[4],{st["Arity"]}],ef,gg},
 colors=Thread[Range[4]->(If[#==1,RGBColor[.88,.65,.23],RGBColor[.05,.47,.43]]& /@ st["Colors"])];
 If[st["Arity"]==2,
   ef=Pick[faces,st["Edges"],1];
   g=Graph[Range[4],(Apply[UndirectedEdge,#]& /@ ef),VertexStyle->colors,
      VertexLabels->"Name",VertexSize->.24,GraphLayout->"CircularEmbedding",
      ImageSize->340,EdgeStyle->Directive[RGBColor[.16,.26,.35],Thick]],
   (* Incidence representation of ternary hypergraph. *)
   ef=Pick[faces,st["Edges"],1];
   gg=Flatten[Table[UndirectedEdge["h"<>ToString[k],i],{k,Length[ef]},{i,ef[[k]]}],1];
   g=Graph[Join[Range[4],("h"<>ToString[#]& /@ Range[Length[ef]])],gg,
      VertexLabels->"Name",VertexStyle->Join[colors,Thread[("h"<>ToString[#]& /@ Range[Length[ef]])->LightGray]],
      VertexSize->.22,GraphLayout->"SpringElectricalEmbedding",ImageSize->340]
 ];
 Labeled[g,Style["Aut (structure) = "<>
  ToString[DynamicBarycentric`DBAutomorphismOrder[st,False]],12],Bottom]
];
init=<|"Arity"->2,"Edges"->{1,1,1,0,0,0},"Colors"->{0,1,0,0}|>;
trajectory=DynamicBarycentric`DBOrbitTrajectory[init,5];
graphs=showState/@trajectory;
Export[FileNameJoin[{root,"Results","wolfram_trajectory.png"}],
 GraphicsGrid[Partition[graphs,3],ImageSize->1050]];
Print["Wolfram figure exported."];
