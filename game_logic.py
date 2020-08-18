class GameLogic:
    # state has [cpu state, player state, turn] turn 0 for cpu turn 1 for player

    def player_turn(self, states, num_fingers, pos):
        states[pos] = (states[pos]+num_fingers)%5
        return states, 0  # return new states and turn flag value as 0 (for cpus turn)

    def cpu_turn(self, states):
        return states, 1
        # maximize cost?
        # win prob for the next 3 moves
        # win prob for defensive and off
        # win prob of off if off>def
        #
    def player_turn_div(self, states, num_fingers_l, num_fingers_r):
        states[2] = num_fingers_l
        states[3] = num_fingers_r
        return states, 0 # return new states and turn flag value as 0 (for cpus turn)

    def validate(self, states, num_fingers, pos, turn_flag):
        if turn_flag: #indicates that it is players turn ( check respective positions)
            if num_fingers in states[2:]: #check if numfingers exists on players side
                if states[pos]==num_fingers and pos in [2,3]: #return invalid if player puts the number in same position
                    return False
                else:
                    return True
            else:
                return False

        if not turn_flag:  # indicates that it is cpus turn ( check respective positions)
            if num_fingers in states[:1]:  # check if numfingers exists on cpus side
                if states[pos] == num_fingers and pos in [0,1]:  # return invalid if cpu puts the number in same position
                    return False
                else:
                    return True
            else:
                return False



    def div_validate(self, states, num_fingers_l, num_fingers_r, turn_flag):
        if turn_flag: #indicates that players turn
            num_pll_states = states[2]
            num_plr_states = states[3]
            if (num_pll_states + num_plr_states) == (num_fingers_l + num_fingers_r): #Total sum of new player states and old player states should be same
                return True #div is valid
            else:
                return False #div is invalid

        if not turn_flag: #indicates that cpus turn
            num_cll_states = states[0]
            num_clr_states = states[1]
            if (num_cll_states + num_clr_states) == (num_fingers_l + num_fingers_r): #Total sum of new cpu states and old cpu states should be same
                return True #div is valid
            else:
                return False #div is invalid



