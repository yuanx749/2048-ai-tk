import time
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from functools import wraps
from heapq import heappop
from typing import Any, Callable, List, Tuple, Union


@dataclass(order=True)
class PrioritizedItem:
    priority: float
    state: Any = field(compare=False)


class Minimax(ABC):
    """General minimax algorithm with alpha-beta pruning.

    Attributes:
        time_limit: Time limit of each move.
        order: If True, will use heap to order nodes.
        cache: If True, will cache the evaluation score and children.
        depth: Depth of iterative deepening search.
    """
    def __init__(self, time_limit, order=True, cache=True):
        self.time_limit = time_limit
        self.time_start = time.time()
        self.order = order
        self.cache = cache
        self.depth = 0

    def set_time_limit(self, time_limit):
        """Sets time limit."""
        self.time_limit = time_limit

    def timeout(self):
        """Raises `AssertionError` if time out."""
        assert time.time() - self.time_start <= self.time_limit

    @abstractmethod
    def terminal_test(self, state, depth):
        """Terminates if depth is zero or a terminal node is reached."""

    @abstractmethod
    def hashkey(self, state):
        """Returns a hasable key of the state to be used in function cache."""

    # pylint: disable=no-self-argument
    def memoize(func: Callable):
        """Returns a decorator that stores the value `func` returns regarding
        its parameter `state`.
        """
        func.cache = {}

        @wraps(func)
        def wrapper(self, state):
            # pylint: disable=not-callable
            if self.cache:
                key = self.hashkey(state)
                if key not in func.cache:
                    func.cache[key] = func(self, state)
                value = func.cache[key]
            else:
                value = func(self, state)
            return value
        return wrapper

    @abstractmethod
    def _evaluate(self, state):
        pass

    @memoize
    def evaluate(self, state):
        """Returns the evaluation score.
        Calls methods implemented in the subclass.
        """
        return self._evaluate(state)

    @abstractmethod
    def _children_min(self, state):
        pass

    @memoize
    def children_min(self, state) -> Union[tuple, Tuple[PrioritizedItem, ...]]:
        """Returns the tuple or heap of children nodes of min node.
        Calls methods implemented in the subclass.
        """
        return self._children_min(state)

    @abstractmethod
    def _children_max(self, state):
        pass

    @memoize
    def children_max(self, state) -> Union[tuple, Tuple[PrioritizedItem, ...]]:
        """Returns the tuple or heap of children nodes of max node.
        Calls methods implemented in the subclass.
        """
        return self._children_max(state)

    def pop_children(self, children: Union[list, List[PrioritizedItem]]):
        """Pops a child from the children list"""
        if self.order:
            state = heappop(children).state
        else:
            state = children.pop()
        return state

    def minimize(self, state, alpha, beta, depth):
        """Returns the best child and the heuristic value for
        minimizing player.
        """
        self.timeout()
        if self.terminal_test(state, depth):
            return None, self.evaluate(state)
        min_child, min_utility = None, float('inf')
        children = list(self.children_min(state))
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
        """Returns the best child and the heuristic value for
        maximizing player.
        """
        self.timeout()
        if self.terminal_test(state, depth):
            return None, self.evaluate(state)
        max_child, max_utility = None, float('-inf')
        children = list(self.children_max(state))
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
        """Returns the move from state to child state."""

    def get_move(self, state):
        """Returns the best move or None by iterative deepening."""
        self.time_start = time.time()
        child = None
        depth = 0
        if self.cache:
            # pylint: disable=no-member
            self.evaluate.cache.clear()
            self.children_min.cache.clear()
            self.children_max.cache.clear()
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
