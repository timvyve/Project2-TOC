# Results for the 3 required program traces

## aplus with 'aaa'
```text
uv run main.py ./input/aplus.csv "aaa"    
Tracing NTM: a plus on input 'aaa'
Machine name: a plus
Initial String: aaa
Tree Depth: 4
Total transitions simulated: 10
Degree of nondeterminism: 1.43
String accepted in 4 transitions.
, q1, a, aa
a, q1, a, a
aa, q1, a, 
aaa, q2, _, 
aa, q3, a, _
```

## composite with input '111111'
```text
uv run main.py ./input/composite.csv "111111"
Tracing NTM: Composite_tester on input '111111'
Machine name: Composite_tester
Initial String: 111111
Tree Depth: 27
Total transitions simulated: 101
Degree of nondeterminism: 1.04
String accepted in 27 transitions.
, q1, 1, 11111
$, q2, 1, 1111
$x, q3, 1, 111
$xx, q3, 1, 11
$xxx, q3, 1, 1
$xx, q4, x, 11
$x, q4, x, x11
$, q4, x, xx11
, q4, $, xxx11
_, q5s, x, xx11
_x, q5s, x, x11
_xx, q5s, x, 11
_xxx, q5s, 1, 1
_xx, q6, x, $1
_x, q6, x, x$1
_, q6, x, xx$1
, q6, _, xxx$1
_, q7, x, xx$1
__, q5x, x, x$1
___, q5x, x, $1
____, q5x, $, 1
____$, q5x, 1, 
____, q6, $, x
___, q6, _, $x
____, q7, $, x
_____, q5s, x, 
_____x, q5s, _, 
_____, qacc, x, _
```


## ntm_n1 with '0011'
```text
uv run main.py ./input/ntm_n1n.csv "0011"   
Tracing NTM: ZeroNOneN on input '0011'
Machine name: ZeroNOneN
Initial String: 0011
Tree Depth: 6
Total transitions simulated: 10
Degree of nondeterminism: 1.25
String rejected in 6 transitions.
```