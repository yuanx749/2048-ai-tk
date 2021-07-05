import math
from heapq import heappush

from Grid import DIRECTIONS, Grid
from Minimax import Minimax


class PlayerAI(Minimax):
    def __init__(self, time_limit=0.1):
        super().__init__(time_limit)
        self.verbose = False

    def terminal_test(self, state, depth):
        grid = Grid(grid=state)
        if depth == 0 or not grid.can_move():
            return True

    def heuristic(self, state):
        grid = Grid(grid=state)
        weights = [10, 1, 1, 1, -1, 10, 1]
        matrix = self.get_log_matrix(state)
        available_number_of_cells = len(grid.get_available_cells())
        average_tile_number = (
            sum(sum(row) for row in matrix)
            / (grid.height*grid.width - available_number_of_cells))
        tiles = [
            matrix[i][j] for i in range(grid.height)
            for j in range(grid.width) if matrix[i][j] != 0]
        median_tile_number = sorted(tiles)[len(tiles) // 2]
        score = (
            weights[0] * available_number_of_cells
            + weights[1] * average_tile_number
            + weights[2] * median_tile_number
            + weights[3] * math.log(grid.get_max_tile(), 2)
            + weights[4] * self.diff_between_adj_tiles(matrix)
            + weights[5] * self.potential_merging(matrix)
            + weights[6] * self.ordering(matrix))
        return score

    @staticmethod
    def get_log_matrix(state):
        return tuple(tuple(
            math.log(x, 2) if x != 0 else 0 for x in state[i])
            for i in range(len(state)))

    @staticmethod
    def diff_between_adj_tiles(matrix):
        return (
            sum(sum(abs(matrix[i][j] - matrix[i][j + 1])
                for j in range(len(matrix[0]) - 1))
                for i in range(len(matrix)))
            + sum(sum(abs(matrix[i][j] - matrix[i + 1][j])
                  for i in range(len(matrix) - 1))
                  for j in range(len(matrix[0]))))

    @staticmethod
    def potential_merging(matrix):
        return (
            sum(sum(1 if matrix[i][j] != 0
                and matrix[i][j] == matrix[i][j + 1]
                else 0 for j in range(len(matrix[0]) - 1))
                for i in range(len(matrix)))
            + sum(sum(1 if matrix[i][j] != 0
                  and matrix[i][j] == matrix[i + 1][j]
                  else 0 for i in range(len(matrix) - 1))
                  for j in range(len(matrix[0]))))

    @staticmethod
    def ordering(matrix):
        score = 0
        for i in range(len(matrix)):
            if (all(matrix[i][j] >= matrix[i][j + 1]
                    for j in range(len(matrix[i]) - 1)) or
                all(matrix[i][j] <= matrix[i][j + 1]
                    for j in range(len(matrix[i]) - 1))):
                score += max(matrix[i])
            else:
                score -= max(matrix[i])
        for j in range(len(matrix[0])):
            if (all(matrix[i][j] >= matrix[i + 1][j]
                    for i in range(len(matrix) - 1)) or
                all(matrix[i][j] <= matrix[i + 1][j]
                    for i in range(len(matrix) - 1))):
                score += max(matrix[i][j] for i in range(len(matrix)))
            else:
                score -= max(matrix[i][j] for i in range(len(matrix)))
        return score

    def children_min(self, state):
        grid = Grid(grid=state)
        cells = grid.get_available_cells()
        children = []
        for cell in cells:
            for tile_value in [2, 4]:
                child = grid.clone()
                child.set_tile(cell[0], cell[1], tile_value)
                if self.order:
                    heappush(
                        children, (self.evaluate(child.state), child.state))
                else:
                    children.append(child.state)
                self.timeout()
        return children

    def children_max(self, state):
        grid = Grid(grid=state)
        children = []
        for direction in DIRECTIONS:
            child = grid.clone()
            if child.move(direction):
                if self.order:
                    heappush(
                        children, (-self.evaluate(child.state), child.state))
                else:
                    children.append(child.state)
            self.timeout()
        return children

    def get_move_to_child(self, state, child):
        for direction in DIRECTIONS:
            grid = Grid(grid=state)
            grid.move(direction)
            if grid.state == child:
                if self.verbose:
                    matrix = self.get_log_matrix(child)
                    print(
                        self.depth - 1,
                        self.diff_between_adj_tiles(matrix),
                        self.potential_merging(matrix),
                        self.ordering(matrix))
                return direction
