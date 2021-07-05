import time
from abc import ABC, abstractmethod
from heapq import heappop


class Minimax(ABC):
    """
    General minimax algorithm.
    Node are represented by hashable states.
    """
    def __init__(self, time_limit):
        self.time_limit = time_limit
        self.time_start = time.time()
        self.order = True
        self.cache = True
        self.value = {}
        self.depth = 0

    def set_time_limit(self, time_limit):
        self.time_limit = time_limit

    def timeout(self):
        """
        Raises AssertionError if time out.
        """
        assert time.time() - self.time_start <= self.time_limit

    @abstractmethod
    def terminal_test(self, state, depth):
        pass

    @abstractmethod
    def heuristic(self, state):
        pass

    def evaluate(self, state):
        """
        Returns the evaluation score.
        """
        if self.cache:
            if state not in self.value:
                self.value[state] = self.heuristic(state)
            score = self.value[state]
        else:
            score = self.heuristic(state)
        return score

    @abstractmethod
    def children_min(self, state):
        """
        Returns the list or heap of children nodes of min node.
        """
        pass

    @abstractmethod
    def children_max(self, state):
        """
        Returns the list or heap of children nodes of max node.
        """
        pass

    def pop_children(self, children):
        if self.order:
            state = heappop(children)[1]
        else:
            state = children.pop()
        return state

    def minimize(self, state, alpha, beta, depth):
        self.timeout()
        if self.terminal_test(state, depth):
            return None, self.evaluate(state)
        min_child, min_utility = None, float('inf')
        children = self.children_min(state)
        while len(children) > 0:
            child = self.pop_children(children)
            _, utility = self.maximize(child, alpha, beta, depth - 1)
            if utility < min_utility:
                min_child, min_utility = child, utility
            if min_utility <= alpha:
                break
            if min_utility < beta:
                beta = min_utility
        return min_child, min_utility

    def maximize(self, state, alpha, beta, depth):
        self.timeout()
        if self.terminal_test(state, depth):
            return None, self.evaluate(state)
        max_child, max_utility = None, float('-inf')
        children = self.children_max(state)
        while len(children) > 0:
            child = self.pop_children(children)
            _, utility = self.minimize(child, alpha, beta, depth - 1)
            if utility > max_utility:
                max_child, max_utility = child, utility
            if max_utility >= beta:
                break
            if max_utility > alpha:
                alpha = max_utility
        return max_child, max_utility

    @abstractmethod
    def get_move_to_child(self, state, child):
        """
        Returns the move from state to child state.
        """
        pass

    def get_move(self, state):
        """
        Returns the best move or None by iterative deepening.
        """
        self.time_start = time.time()
        child = None
        depth = 0
        while True:
            try:
                depth += 1
                child, _ = self.maximize(
                    state, float('-inf'), float('inf'), depth)
            except AssertionError:
                break
        if child is None:
            return None
        self.depth = depth
        move = self.get_move_to_child(state, child)
        return move
