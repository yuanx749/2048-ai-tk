from Grid import DIRECTIONS, Grid
from heapq import heappush, heappop
import time
import math


class PlayerAI:
    def __init__(self, time_limit=0.1, order=True):
        self.time_limit = time_limit
        self.time_start = time.time()
        self.order = order
        self.value = {}

    def set_time_limit(self, time_limit):
        self.time_limit = time_limit

    def timeout(self):
        assert time.time() - self.time_start <= self.time_limit

    def terminal_test(self, grid, depth):
        if depth == 0 or not grid.can_move():
            return True

    def evaluate(self, grid):
        grid_tuple = grid.to_tuple()
        if grid_tuple not in self.value:
            weights = [10, 1, 1, 1, -1, 10, 1]
            matrix = self.get_log_matrix(grid)
            available_number_of_cells = len(grid.get_available_cells())
            average_tile_number = (
                sum(sum(row) for row in matrix)
                / (grid.height*grid.width - available_number_of_cells))
            tiles = [
                matrix[i][j] for i in range(grid.height)
                for j in range(grid.width) if matrix[i][j] != 0]
            median_tile_number = sorted(tiles)[len(tiles) // 2]
            self.value[grid_tuple] = (
                weights[0] * available_number_of_cells
                + weights[1] * average_tile_number
                + weights[2] * median_tile_number
                + weights[3] * math.log(grid.get_max_tile(), 2)
                + weights[4] * self.diff_between_adj_tiles(matrix)
                + weights[5] * self.potential_merging(matrix)
                + weights[6] * self.ordering(matrix))
        return self.value[grid_tuple]

    def get_log_matrix(self, grid):
        return tuple(tuple(
            math.log(x, 2) if x != 0 else 0 for x in grid.grid[i])
            for i in range(grid.height))

    def diff_between_adj_tiles(self, matrix):
        return (
            sum(sum(abs(matrix[i][j] - matrix[i][j + 1])
                for j in range(len(matrix[0]) - 1))
                for i in range(len(matrix)))
            + sum(sum(abs(matrix[i][j] - matrix[i + 1][j])
                  for i in range(len(matrix) - 1))
                  for j in range(len(matrix[0]))))

    def potential_merging(self, matrix):
        return (
            sum(sum(1 if matrix[i][j] != 0
                and matrix[i][j] == matrix[i][j + 1]
                else 0 for j in range(len(matrix[0]) - 1))
                for i in range(len(matrix)))
            + sum(sum(1 if matrix[i][j] != 0
                  and matrix[i][j] == matrix[i + 1][j]
                  else 0 for i in range(len(matrix) - 1))
                  for j in range(len(matrix[0]))))

    def ordering(self, matrix):
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

    def children_min(self, grid):
        cells = grid.get_available_cells()
        children = []
        for cell in cells:
            for tile_value in [2, 4]:
                child = grid.clone()
                child.set_tile(cell[0], cell[1], tile_value)
                if self.order:
                    heappush(children, (self.evaluate(child), child.grid))
                else:
                    children.append(child)
                self.timeout()
        return children

    def minimize(self, grid, alpha, beta, depth):
        self.timeout()
        if self.terminal_test(grid, depth):
            return None, self.evaluate(grid)
        min_child, min_utility = None, float('inf')
        children = self.children_min(grid)
        while len(children) > 0:
            if self.order:
                child_grid = heappop(children)[1]
                child = Grid(grid=child_grid)
            else:
                child = children.pop()
            _, utility = self.maximize(child, alpha, beta, depth - 1)
            if utility < min_utility:
                min_child, min_utility = child, utility
            if min_utility <= alpha:
                break
            if min_utility < beta:
                beta = min_utility
        return min_child, min_utility

    def children_max(self, grid):
        children = []
        for direction in DIRECTIONS:
            child = grid.clone()
            if child.move(direction):
                if self.order:
                    heappush(children, (-self.evaluate(child), child.grid))
                else:
                    children.append(child)
            self.timeout()
        return children

    def maximize(self, grid, alpha, beta, depth):
        self.timeout()
        if self.terminal_test(grid, depth):
            return None, self.evaluate(grid)
        max_child, max_utility = None, float('-inf')
        children = self.children_max(grid)
        while len(children) > 0:
            if self.order:
                child_grid = heappop(children)[1]
                child = Grid(grid=child_grid)
            else:
                child = children.pop()
            _, utility = self.minimize(child, alpha, beta, depth - 1)
            if utility > max_utility:
                max_child, max_utility = child, utility
            if max_utility >= beta:
                break
            if max_utility > alpha:
                alpha = max_utility
        return max_child, max_utility

    def get_move(self, grid):
        self.time_start = time.time()
        child = None
        depth = 0
        while True:
            try:
                depth += 1
                child, _ = self.maximize(
                    grid, float('-inf'), float('inf'), depth)
            except AssertionError:
                break
        if child is None:
            return None
        for direction in DIRECTIONS:
            grid_copy = grid.clone()
            grid_copy.move(direction)
            if grid_copy.grid == child.grid:
                # matrix = self.get_log_matrix(child)
                # print(
                #     depth - 1,
                #     self.diff_between_adj_tiles(matrix),
                #     self.potential_merging(matrix),
                #     self.ordering(matrix))
                return direction
