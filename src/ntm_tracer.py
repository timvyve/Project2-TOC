from src.helpers.turing_machine import TuringMachineSimulator, DIR_R


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
        right = input_string if input_string  else BLANK
        initial_config = ["", self.start_state, right, None, None]

        # The tree is a list of lists of configurations
        tree = [[initial_config]]
        self.tree = tree # store so print_trace_path can see it

        depth = 0
        accepted = False
        rejected = False
        accept_node = None
        total_transitions = 0

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

            for idx, config in enumerate(current_level):
                left, state, right = config[0], config[1], config[2]

                if state = self.accept_state:
                    accepted = True
                    accept_node = (depth, idx)
                    break

                if state == self.reject_state:
                    continue

                all_rejected = False # there's at least one non-reject state

                if right:
                    read_symbol = right[0]
                    rest_right = right[1:]
                else:
                    read_symbol = BLANK
                    rest_right = ""

                transitions = self.get_transitions(state, (read_symbol,))

                if not transitions:
                    total_transitions += 1
                    child = [left, self.reject_state, right, depth, idx]
                    next_level.append(child)
                    continue

                for t in transitions:
                    next_state = t["next"]
                    write_symbol = t["write"][0]
                    direction = t["direction"][0]

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

                    child = [new_left, next_state, new_right, depth, idx]
                    next_level.append(child)


            # Placeholder for logic:
            if not next_level and all_rejected:
                rejected = True
                break

            if accepted:
                break

            tree.append(next_level)
            depth += 1

        tree_depth = depth

        print(f"Machine name: {self.machine_name}")
        print(f"Initial String: {input_string}")
        print(f"Tree Depth: {tree_depth}")
        print(f"Total transitions simulated: {total_transitions}")

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
        level, index = final_node
        path = []

        while level is not None and index is not None:
            config = self.tree[level][index]
            path.append(config)
            parent_level = config[3]
            parent_index = config[4]
            level, index = parent_level, parent_index

        path.reverse()

        for config in path:
            left, state, right = config[0], config[1], config[2]

            if right:
                head_char = right[0]
                rest_right = right[1:]
            else:
                head_char = BLANK
                rest_right = ""

            print(f"{left, {state}, {head_char}, {rest_right}}")

