from random import randint


class Field:

    def __init__(self, x_size: int, y_size: int, mines: int):
        self.size = (x_size, y_size)
        self.bombs = self.get_bombs(mines, x_size, y_size)
        self.field = [[0 for i in range(x_size)] for _ in range(y_size)]
        self.fill_field_list()

    @staticmethod
    def get_bombs(n: int, x_size: int, y_size: int):
        bombs = set()
        while len(bombs) < n:
            bombs.add((randint(0, x_size - 1), randint(0, y_size - 1)))
        return bombs

    @staticmethod
    def bomb_mapper(x: int, y: int, field_size: tuple, bombs: set):
        mapper = []
        for i in range(x - 1, x + 2):
            for j in range(y - 1, y + 2):
                if not (i == x and j == y) and i > -1 and j > -1 \
                        and i < field_size[0] and j < field_size[1] \
                        and (i, j) not in bombs:
                    mapper.append((i, j))
        return mapper

    def fill_field_list(self):
        for i, j in self.bombs:
            self.field[i][j] = 9
            for k, m in self.bomb_mapper(i, j, self.size, self.bombs):
                self.field[k][m] += 1

    def __repr__(self):
        return '\n'.join([repr(x) for x in self.field])


if __name__ == '__main__':
    game = Field(10, 10, 10)
    print(game)
