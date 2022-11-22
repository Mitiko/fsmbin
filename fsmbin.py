#!/usr/bin/python3

import sys
from typing import List, Tuple

class FSM:
    def __init__(self, state_transitions: List[Tuple[int, int]], probabilities: List[int], initial_state: int):
        self.state_transitions = state_transitions
        self.probabilities = probabilities
        self.initial_state = initial_state

        # for emulating the machine
        self.curr = self.initial_state
        self.steps = 0

    def len(self) -> int:
        return len(self.state_transitions)

    def next(self, bit: int):
        assert(bit == 0 or bit == 1)
        self.curr = self.state_transitions[self.curr][bit]
        self.steps += 1

    # TODO: __str__ vs __repr__
    def __str__(self) -> str:
        if self.steps > 0:
            return f"[step={self.steps}] state={self.curr}"
        return f"""FSM with {self.len()}) states
        initial_state = {self.initial_state}
        """

def write_to_file(fsm: FSM, filename: str):
    with open(filename, "w") as f:
        if fsm.initial_state != 0:
            f.write(f"{fsm.initial_state}\n")
        for ((s0, s1), p) in fsm.state_transitions.zip(fsm.probabilities):
            f.write(f"{s0},{s1},{p}\n")

def read_from_file(filename: str) -> FSM:
    # TODO: autodetect T5 format
    state_id, initial_state = 0, 0
    states, probs = [], []

    def error(msg: str):
        print(f"Error parsing FSM for {filename}")
        print(msg)
        sys.exit(1)

    file = open(filename)
    for line in file:
        if line == "\n":
            continue

        vals = line.split(",")
        if len(vals) == 1 and state_id == 0:
            try:
                initial_state = int(vals[0])
            except:
                error(f"Initital state not an integer: '{vals[0]}'")
        
        if len(vals) < 3:
            error(f"State {state_id} was not in correct format: '{line}'")
        
        state_id += 1
        try:
            s0 = int(vals[0])
            s1 = int(vals[1])
            p  = int(vals[2])
            probs.append(p)
            states.append((s0, s1))
        except:
            error(f"Couldn't parse integers for state {state_id}")
    return FSM(states, probs, initial_state)

# Prints the FSM to a digrpah file
# TODO: Use the python graphiz library to generate the image directly
# See: https://en.wikipedia.org/wiki/DOT_(graph_description_language)
def write_to_digraph(fsm: FSM, filename: str):
    name = filename.split(".")[0]
    # find self referential states
    self_ref = []
    for curr, (s0, s1) in enumerate(fsm.state_transitions):
        if curr == s0 or curr == s1:
            self_ref.append(str(curr))
    file = open(filename, "w")
    file.writelines([
        f"digraph {name} {{\n",
        "\tfontname=\"Helvetica,Arial,sans-serif\"\n",
        "\tnode [fontname=\"Helvetica,Arial,sans-serif\"]\n",
        "\tedge [fontname=\"Helvetica,Arial,sans-serif\"]\n",
        "\trankdir=LR;\n",
        f"\tnode [shape = doublecircle, color = cyan]; {fsm.initial_state};\n"
        "\tnode [shape = doublecircle, color = magenta];\n"
    ])
    # self referential states are doublecircle-ed
    file.write(f"\t{' '.join(self_ref)};\n")
    file.write("\tnode [shape = circle, color = black];\n")
    for curr, (s0, s1) in enumerate(fsm.state_transitions):
        file.write(f"\t{curr: >4} -> {s0: >4} [label=\"0\", color=darkorange];\n")
        file.write(f"\t{curr: >4} -> {s1: >4} [label=\"1\", color=green];\n")
    file.write("}\n")
    file.close()
    print(f"To make an svg use: dot {filename} -Tsvg > graph.svg")

def info(fsm: FSM):
    # get min/max state
    # get min/max probs
    # get probability of reaching states * prob -> expected entropy of source
    pass

def cmp(fsm_a: FSM, fsm_b: FSM):
    # try compare fsms
    # print unreachable states
    # dfs
    pass

def trim(fsm: FSM) -> FSM:
    pass

def unreachable(fsm: FSM):
    pass

def minimize(fsm: FSM) -> FSM:
    pass

def run(fsm: FSM, filename: str):
    pass

def run_strip(fsm: FSM, filename: str) -> FSM:
    pass

def conv(fsm: FSM, fmt: str) -> FSM:
    pass


args = sys.argv
if len(args) < 2:
    print("Incorrect usage")
    # TODO: Print usage
    sys.exit(1)

command = args[1]
if command == "print":
    # TODO: Require arg count to be some
    # TODO: Try/except file opening
    fsm_file = args[2]
    digraph_file = args[3]
    fsm = read_from_file(fsm_file)
    write_to_digraph(fsm, digraph_file)

