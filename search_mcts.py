"""Pure Monte Carlo Tree Search."""

import random
import math, numpy as np
from position import *
from collections import defaultdict


class Node:
    is_root = False
    def __init__(self, state, parent=None, parent_action=None, is_root=False):
        self.state = state
        self.parent = parent
        self.parent_action = parent_action
        self.children = []
        self._number_of_visits = 0
        self._results = defaultdict(int)
        self._results[1] = 0
        self._results[-1] = 0
        self._untried_actions = None
        self._untried_actions = self.untried_actions()
        self.is_root = is_root
        return

    def untried_actions(self):
        self._untried_actions = MoveGen(self.state).legal_moves()
        return self._untried_actions

    def q(self):
        wins = self._results[1]
        loses = self._results[-1]
        return wins - loses

    def n(self):
        return self._number_of_visits

    def expand(self):
        action = self._untried_actions.pop()
        next_state = self.state.make_move(action)
        child_node = Node(
            next_state, parent=self, parent_action=action)

        self.children.append(child_node)
        return child_node

    def is_terminal_node(self):
        return self.state.is_game_over()[0]

    def rollout(self):
        current_rollout_state = self.state

        while not current_rollout_state.is_game_over()[0]:
            possible_moves = MoveGen(current_rollout_state).legal_moves()

            action = self.rollout_policy(possible_moves)
            current_rollout_state = current_rollout_state.make_move(action)
        return current_rollout_state.get_result()

    def backpropagate(self, result):
        self._number_of_visits += 1
        self._results[result] += 1
        if self.parent:
            self.parent.backpropagate(result)

    def is_fully_expanded(self):
        return len(self._untried_actions) == 0

    def best_child(self, c_param=0.1):
        choices_weights = [(c.q() / c.n()) + c_param * np.sqrt((2 * np.log(self.n()) / c.n())) for c in self.children]
        return self.children[np.argmax(choices_weights)]

    def rollout_policy(self, possible_moves):
        return possible_moves[np.random.randint(len(possible_moves))]

    def _tree_policy(self):

        current_node = self
        while not current_node.is_terminal_node():

            if not current_node.is_fully_expanded():
                return current_node.expand()
            else:
                current_node = current_node.best_child()
        return current_node

    def best_action(self):
        simulation_no = 100000
        update_freq = max(simulation_no // 100, 256)

        for i in range(simulation_no):
            v = self._tree_policy()
            reward = v.rollout()
            v.backpropagate(reward)

            # periodically print the best move
            if self.is_root and i % update_freq == 0:
                best_move = self.best_child().parent_action
                print(f"info nodes {i} score n {self.n()} pv {best_move}")

        return self.best_child()


def search(pos: Position):
    root = Node(pos, is_root=True)
    best_node = root.best_action()
    best_move = best_node.parent_action
    best_value = best_node.q()
    print(best_move, best_value)
    return best_move, best_value

