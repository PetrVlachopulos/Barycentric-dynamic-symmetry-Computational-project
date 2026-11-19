(* ::Package:: *)

(* Interactive Simulator. Requires Kernel/DynamicBarycentric.wl loaded. *)
Get[FileNameJoin[{DirectoryName[DirectoryName[$InputFileName]],"Kernel","DynamicBarycentric.wl"}]];
DynamicModule[{initial=<|"Arity"->2,"Edges"->{1,1,1,0,0,0},"Colors"->{0,1,0,0}|>},
 Manipulate[
  Module[{st=Nest[DynamicBarycentric`DBStep,initial,t],obs},
   obs=DynamicBarycentric`DBSelectedObserver[st];
   Column[{
    Style["Changing graph symmetries and exact motif reconstruction",17,Bold],
    Row[{"Step ",t,"    graph automorphisms: ",
       DynamicBarycentric`DBAutomorphismOrder[st,False],
       "    decorated automorphisms: ",DynamicBarycentric`DBAutomorphismOrder[st,True]}],
    Graph[Range[4],Apply[UndirectedEdge,#]& /@
      Pick[Subsets[Range[4],{2}],st["Edges"],1],
      VertexStyle->Thread[Range[4]->(If[#==1,Orange,Darker[Green]]&/@st["Colors"])],
      VertexLabels->"Name",VertexSize->.3,GraphLayout->"CircularEmbedding",ImageSize->420],
    Row[{"Exact 13-component observed signature: ",obs}]
   }]
  ],
  {{t,0,"Rewrite step"},0,12,1,Appearance->"Labeled"},
  SaveDefinitions->True,TrackedSymbols:>{t}
 ]
]
