# fsmbin

Python script with tools for working with binary alphabet [FSMs](https://en.wikipedia.org/wiki/Finite-state_machine).  
This is fitted to the purposes of data compression ([read more](https://encode.su/threads/3681-GDCC-21-T5-FSM-Counter-Optimization)).

Graph editor online: [yEd Live](https://www.yworks.com/yed-live/)

## Structure of a state machine

![Example state machine](https://github.com/Mitiko/fsmbin/blob/main/example.svg?raw=true)

Unlike most uses for deterministic finite automata, in compression there are no acceptor states.
Instead, each state holds a probability between 0 and 1 (scaled by 2^16 to fit in `u16`).
A compressor may use a state machine as a more general case of a counter, to collect statistics,
and to recognize complex patterns.

Furthermore states can be mapped to probabilities in runtime, thus adapting the FSM to better suite the current data stream.

## File format

This tool recognizes the T5 format from GDCC and a 16-bit version of it.
The state machine is encoded plainly in text, such that:  
Each line `i` is a tuple of 3 values which represent state `i`:
- `s0` - next state if bit = 0
- `s1` - next state if bit = 1
- `p` - probability of bit = 1 scaled by 2^16 (aka 0 <= prob <= 65535)

The GDCC T5 version instead uses 15-bit probabilities (0 <= prob <= 32767) and encodes the inverse probability (bit = 0).
The script autodetects the T5 file format (if all probabilities are in the 15-bit range) and converts them to the 16-bit version.

### Example 1

Pro tip: Use comments to show the regular language a state "accepts".

```
1, 2, 32768
3, 4, 21845, only the first 3 values are considered
5, 6, 43691, anything after the third comma is a comment
3, 4, 16384, -> .*00
5, 6, 32768, -> .*01
3, 4, 32768, -> .*10
5, 6, 49152, -> .*11
1, 2, 0, this state is unreachable

42, 69, 1337, a blank line is ignored
```

The reachable states from this FSM are shown in the diagram above.

### Example 2

Furthermore, this format is extended by an optional initial state on the first line, otherwise assumed to be 0.
This is helpful for machines where the 0th state is reserved with a different meaning or a particular ordering
is employed for easier bit math.

No comments are allowed on first line that defines initial state.

```
1
0, 0, 0, zero-th state is unreachable, do not use
2, 3, 32768
1, 1, 16384
1, 1, 49152
```

## Usage

```bash
# Convert FSM to a digraph file
./fsmbin.py print fsm.txt graphname.gv
# Use dot to print to svg:
dot graphname.gv -Tsvg > graphname.svg
# TODO: Other commands
```

## paq8

The cannonical example is [paq8px](https://github.com/hxim/paq8px) which uses an 8-bit
non-deterministic [machine](https://github.com/hxim/paq8px/blob/master/StateTable.hpp).
Most states in the beginning have deterministic transitions but states 205-252 use incremental counting.
States are then mapped to a probability which may be static or adaptive.

paq8's state machine is often criticized for being too small, human readable, and slow with non-deterministic updates.
