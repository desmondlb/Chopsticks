from copy import deepcopy
import random
import time


class GameLogic:
    # state has [cpu state, player state, turn] turn 0 for cpu turn 1 for player

    def player_turn(self, states, num_fingers, pos):
        states[pos] = (states[pos] + num_fingers) % 5
        return states, 0  # return new states and turn flag value as 0 (for cpus turn)

    def player_turn_div(self, states, num_fingers_l, num_fingers_r):
        states[2] = num_fingers_l
        states[3] = num_fingers_r
        return states, 0  # return new states and turn flag value as 0 (for cpus turn)

    def validate(self, states, num_fingers, pos, turn_flag):
        if states[pos] == 0:
            return False
        elif num_fingers == 0:
            return False
        elif turn_flag:  # indicates that it is players turn ( check respective positions)
            if num_fingers in states[2:]:  # check if num_fingers exists on players side
                if pos in [2, 3]:  # if player attacks self
                    return False
                else:
                    return True
            else:
                return False

        elif not turn_flag:  # indicates that it is cpus turn ( check respective positions)
            if num_fingers in states[:2]:  # check if num_fingers exists on cpus side
                if pos in [0, 1]:  # if cpu attacks self
                    return False
                else:
                    return True
            else:
                return False

    def div_validate(self, states, num_fingers_l, num_fingers_r, turn_flag):
        if turn_flag:  # indicates that players turn
            num_pll_states = states[2]
            num_plr_states = states[3]
            if (num_pll_states + num_plr_states) == (
                    num_fingers_l + num_fingers_r):  # Total sum of new player states and old player states should be same
                if num_fingers_r in [num_plr_states, num_pll_states]:
                    return False
                else:
                    return True  # div is valid
            else:
                return False  # div is invalid

        if not turn_flag:  # indicates that cpus turn
            num_cll_states = states[0]
            num_clr_states = states[1]
            if (num_cll_states + num_clr_states) == (
                    num_fingers_l + num_fingers_r):  # Total sum of new cpu states and old cpu states should be same
                if num_fingers_r in [num_clr_states, num_cll_states]:
                    return False
                else:
                    return True  # div is valid
            else:
                return False  # div is invalid

    def is_leaf(self, states, depth, height):
        if depth == height:
            return True
        if (states[0] == 0 and states[1] == 0) or (states[2] == 0 and states[3] == 0):
            return True
        else:
            return False

    def value(self, states, depth):
        if states[2] == 0 and states[3] == 0:
            return 5 - depth + 10
        else:
            if states[0] == 0 and states[1] == 0:
                return -1 * (5 - depth + 10)

            elif states[2] == 0 or states[3] == 0:
                return 10 - depth

            elif states[0] == 0 or states[1] == 0:
                return -1 * (10 - depth)

            else:
                return -2

    def do_if_valid(self, move, states, max_turn):
        new_state = deepcopy(states)
        if max_turn:
            if move == 'div':
                total = states[0] + states[1]
                num_l = int(total / 2)
                num_r = total - num_l
                if self.div_validate(states, num_l, num_r, 0):
                    new_state[0] = num_l
                    new_state[1] = num_r
                    return new_state

            elif move == 'l_oppl':
                if self.validate(states, states[0], 2, 0):
                    new_state[2] = (states[2] + states[0]) % 5
                    return new_state

            elif move == 'l_oppr':
                if self.validate(states, states[0], 3, 0):
                    new_state[3] = (states[3] + states[0]) % 5
                    return new_state

            elif move == 'r_oppl':
                if self.validate(states, states[1], 2, 0):
                    new_state[2] = (states[2] + states[1]) % 5
                    return new_state

            elif move == 'r_oppr':
                if self.validate(states, states[1], 3, 0):
                    new_state[3] = (states[3] + states[1]) % 5
                    return new_state
        else:
            if move == 'div':
                total = states[2] + states[3]
                num_l = int(total / 2)
                num_r = total - num_l
                if self.div_validate(states, num_l, num_r, 1):
                    new_state[2] = num_l
                    new_state[3] = num_r
                    return new_state

            elif move == 'l_oppl':
                if self.validate(states, states[2], 0, 1):
                    new_state[0] = (states[0] + states[2]) % 5
                    return new_state

            elif move == 'l_oppr':
                if self.validate(states, states[2], 1, 1):
                    new_state[1] = (states[1] + states[2]) % 5
                    return new_state

            elif move == 'r_oppl':
                if self.validate(states, states[3], 0, 1):
                    new_state[0] = (states[0] + states[3]) % 5
                    return new_state

            elif move == 'r_oppr':
                if self.validate(states, states[3], 1, 1):
                    new_state[1] = (states[1] + states[3]) % 5
                    return new_state

    def minmax(self, states, current_depth, max_turn, target_depth):
        if self.is_leaf(states, current_depth, target_depth):
            return states
        else:
            child_nodes = []
            moves = ['div', 'l_oppl', 'l_oppr', 'r_oppl', 'r_oppr']
            random.shuffle(moves)
            for move in moves:
                child_nodes.append(self.do_if_valid(move, states, max_turn))
            child_nodes = list(filter(None, child_nodes))
            child_nodes_values = [
                self.value(self.minmax(s, current_depth + 1, not max_turn, target_depth), current_depth) for s
                in child_nodes]
            if max_turn:
                return child_nodes[child_nodes_values.index(max(child_nodes_values))]
            else:
                return child_nodes[child_nodes_values.index(min(child_nodes_values))]

    def cpu_turn(self, states):
        time.sleep(3)
        new_state = self.minmax(states, 0, True, 4)
        return new_state, 1
