from src.helpers.turing_machine import TuringMachineSimulator, DIR_R, DIR_L, DIR_S, BLANK


# ==========================================
# PROGRAM 1: Nondeterministic TM [cite: 137]
# ==========================================
class NTM_Tracer(TuringMachineSimulator):
    def run(self, input_string, max_depth):
        """
        Performs a Breadth-First Search (BFS) trace of the NTM.
        Ref: Section 4.1 "Trees as List of Lists" [cite: 146]
        """
        print(f"Tracing NTM: {self.machine_name} on input '{input_string}'")

        # Initial Configuration: ["", start_state, input_string]
        # Note: Represent configuration as triples (left, state, right) [cite: 156]
        right = input_string if input_string else BLANK
        initial_config = ["", self.start_state, right, None, None]

        # The tree is a list of lists of configurations
        tree = [[initial_config]]
        self.tree = tree # store so print_trace_path can see it

        depth = 0
        accepted = False
        rejected = False
        accept_node = None
        total_transitions = 0
        expanded_configs = 0
        generated_children = 0

        while depth < max_depth and not accepted:
            current_level = tree[-1]
            next_level = []
            all_rejected = True

            # TODO: STUDENT IMPLEMENTATION NEEDED
            # 1. Iterate through every config in current_level.
            # 2. Check if config is Accept (Stop and print success) [cite: 179]
            # 3. Check if config is Reject (Stop this branch only) [cite: 181]
            # 4. If not Accept/Reject, find valid transitions in self.transitions.
            # 5. If no explicit transition exists, treat as implicit Reject.
            # 6. Generate children configurations and append to next_level[cite: 148].

            # loop through every configuration
            for idx, config in enumerate(current_level):
                left, state, right = config[0], config[1], config[2]

                # check for accept
                if state == self.accept_state:
                    accepted = True
                    accept_node = (depth, idx)
                    break

                # if rejected, only skip this iteration
                if state == self.reject_state:
                    continue

                expanded_configs += 1

                all_rejected = False # there's at least one non-reject state

                # read next symbol, if there's nothing left it's blank
                if right:
                    read_symbol = right[0]
                    rest_right = right[1:]
                else:
                    read_symbol = BLANK
                    rest_right = ""

                # find all nondeterministic transitions for state, symbol
                transitions = self.get_transitions(state, (read_symbol,))

                # no valid transitions, so we move to reject
                if not transitions:
                    total_transitions += 1
                    child = [left, self.reject_state, right, depth, idx]
                    next_level.append(child)
                    generated_children += 1
                    continue

                # for every nondeterministic transition, make a child configuration with the parent's id
                for t in transitions:
                    next_state = t["next"]
                    write_symbol = t["write"][0]
                    direction = t["move"][0]

                    total_transitions += 1

                    if direction == DIR_R:
                        new_left = left + write_symbol

                        if rest_right:
                            new_right = rest_right
                        else:
                            new_right = BLANK
                    elif direction == DIR_L:
                        w_prime = write_symbol + rest_right
                        if left:
                            u = left[:-1]
                            c = left[-1]
                            new_left = u
                            new_right = c + w_prime
                        else:
                            new_left = ""
                            new_right = BLANK + w_prime
                    elif direction == DIR_S:
                        new_left = left
                        new_right = write_symbol + rest_right

                    else:
                        new_left = left
                        new_right = write_symbol + rest_right
                    # store parent idx for reconstruction later
                    child = [new_left, next_state, new_right, depth, idx]
                    next_level.append(child)
                    generated_children += 1

            if accepted:
                break

            # if there's no more configuration to look at -> reject
            if not next_level:
                rejected = True
                break


            tree.append(next_level)
            depth += 1

        tree_depth = depth

        if expanded_configs > 0:
            degree = generated_children / expanded_configs
        else:
            degree = 0.0

        # print final output
        print(f"Machine name: {self.machine_name}")
        print(f"Initial String: {input_string}")
        print(f"Tree Depth: {tree_depth}")
        print(f"Total transitions simulated: {total_transitions}")
        print(f"Degree of nondeterminism: {degree:.2f}")

        # follow formatting labeled in project document
        if accepted and accept_node is not None:
            print(f"String accepted in {accept_node[0]} transitions.")
            self.print_trace_path(accept_node)
        elif rejected:
            print(f"String rejected in {tree_depth} transitions.")
        elif depth >= max_depth:
            print(f"Execution stopped after {max_depth} steps.")# [cite: 259]

    def print_trace_path(self, final_node):
        """
        Backtrack and print the path from root to the accepting node.
        Ref: Section 4.2 [cite: 165]
        """
        # we want to start from the accepting final configuration
        level, index = final_node
        path = []


        while level is not None and index is not None:
            config = self.tree[level][index] # get config
            path.append(config)
            parent_level = config[3] # get the parents info to backtrack
            parent_index = config[4]
            level, index = parent_level, parent_index

        path.reverse() # reverse because we went from bottom->top


        for config in path:
            left, state, right = config[0], config[1], config[2]
            # if right is not empty, the head is the first symbol of 'right'
            if right:
                head_char = right[0]
                rest_right = right[1:]
            else:
                head_char = BLANK
                rest_right = ""

            # follow exact formatting
            print(f"{left}, {state}, {head_char}, {rest_right}")

