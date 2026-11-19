#!/usr/bin/env python3
"""Compare an actual Wolfram kernel run against independent Python certificates.
This DOES NOT run Wolfram; it strictly requires a native-created JSON file.
"""
import json,sys
from pathlib import Path
root=Path(__file__).resolve().parents[1]
native_file=root/'Results'/'native_wolfram_results.json'
if not native_file.exists():
    raise SystemExit('No native Wolfram result file: run Examples/RunNative.wls with wolframscript first.')
native=json.loads(native_file.read_text(encoding='utf-8'))
py=json.loads((root/'Data'/'verified_results.json').read_text(encoding='utf-8'))
assert native['NativeWolframExecuted'] is True
assert native['GraphOrbitCount']==py['graph_orbits']==90
assert native['HypergraphOrbitCount']==py['hyper_orbits']==35
assert native['GraphAutomorphismOrders']==[z['graph_aut_order'] for z in py['trajectory']]
assert native['Selected']=={'Classes':86,'Exact':True}
assert native['3']=={'Classes':90,'Exact':True}
assert native['ComplementVariantExact'] is True
assert native['BaseSevenDistinctCodes']==86
print('PASS: Actual Wolfram kernel export matches independent Python reference.')
