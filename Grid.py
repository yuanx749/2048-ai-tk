import random

DIRECTIONS = (UP, DOWN, LEFT, RIGHT) = range(4)
OFFSETS = ((-1, 0), (1, 0), (0, -1), (0, 1))


class Grid:
    def __init__(self, height=4, width=4, grid=None):
        if grid is None:
            self.height = height
            self.width = width
            self.grid = [[0] * self.width for _ in range(self.height)]
        else:
            self.height = len(grid)
            self.width = len(grid[0])
            self.grid = [
                [grid[row][col] for col in range(self.width)]
                for row in range(self.height)]

    def __str__(self):
        return('\n'.join(
            [''.join([f'{cell:6}' for cell in row]) for row in self.grid]))

    def to_tuple(self):
        return tuple(tuple(row) for row in self.grid)

    def clone(self):
        return Grid(grid=self.grid)

    def get_tile(self, row, col):
        return self.grid[row][col]

    def set_tile(self, row, col, value):
        self.grid[row][col] = value

    def get_available_cells(self):
        cells = []
        for row in range(self.height):
            for col in range(self.width):
                if self.grid[row][col] == 0:
                    cells.append((row, col))
        return cells

    def get_max_tile(self):
        max_tile = 0
        for row in range(self.height):
            for col in range(self.width):
                max_tile = max(max_tile, self.grid[row][col])
        return max_tile

    def merge(self, line):
        result = []
        merge_flag = False
        for tile in line:
            if tile != 0:
                if result == [] or merge_flag or tile != result[-1]:
                    result.append(tile)
                    merge_flag = False
                else:
                    result[-1] += tile
                    merge_flag = True
        result.extend([0] * (len(line) - len(result)))
        return result

    def move(self, direction):
        if direction == UP:
            index_lists = [
                [(row, col) for row in range(self.height)]
                for col in range(self.width)]
        elif direction == DOWN:
            index_lists = [
                [(row, col) for row in range(self.height - 1, -1, -1)]
                for col in range(self.width)]
        elif direction == LEFT:
            index_lists = [
                [(row, col) for col in range(self.width)]
                for row in range(self.height)]
        elif direction == RIGHT:
            index_lists = [
                [(row, col) for col in range(self.width - 1, -1, -1)]
                for row in range(self.height)]
        change = False
        for index_list in index_lists:
            before = [self.grid[row][col] for (row, col) in index_list]
            after = self.merge(before)
            if after != before:
                change = True
                for (row, col), value in zip(index_list, after):
                    self.set_tile(row, col, value)
        return change

    def insert_random_tile(self):
        if random.random() < 0.9:
            tile_value = 2
        else:
            tile_value = 4
        cells = self.get_available_cells()
        if cells != []:
            row, col = random.choice(cells)
            self.set_tile(row, col, tile_value)

    def cross_bound(self, row, col):
        return row < 0 or row >= self.height or col < 0 or col >= self.width

    def can_move(self, dirs=DIRECTIONS):
        for row in range(self.height):
            for col in range(self.width):
                if self.grid[row][col] != 0:
                    for d in dirs:
                        row_adj = row + OFFSETS[d][0]
                        col_adj = col + OFFSETS[d][1]
                        if not self.cross_bound(row_adj, col_adj):
                            adj_cell_value = self.grid[row_adj][col_adj]
                            if (adj_cell_value == self.grid[row][col]
                                    or adj_cell_value == 0):
                                return True
                else:
                    return True
        return False
